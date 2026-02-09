"""
Vendor Portal POC - FastAPI Application
"""
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
from database import get_session, Project, Module, Vendor, RFQ, Quote, ProjectShortlist
from email_service import send_rfq_email

app = FastAPI(title="Vendor Portal POC")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Helper function to get database session
def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


# ===== CUSTOMER INTERFACE ROUTES =====

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page / Customer ranking table"""
    db = next(get_db())
    modules = db.query(Module).order_by(Module.wattage.desc()).limit(50).all()
    project = db.query(Project).first()

    # Get shortlisted module IDs
    shortlisted_ids = []
    if project:
        shortlist = db.query(ProjectShortlist).filter_by(project_id=project.id).all()
        shortlisted_ids = [s.module_id for s in shortlist]

    return templates.TemplateResponse(
        "customer_ranking.html",
        {
            "request": request,
            "modules": modules,
            "shortlisted_ids": shortlisted_ids,
            "project": project
        }
    )


@app.post("/customer/shortlist")
async def add_to_shortlist(module_id: int = Form(...)):
    """Add module to project shortlist"""
    db = next(get_db())
    project = db.query(Project).first()

    if not project:
        # Create project if doesn't exist
        project = Project(name="New Solar Project", status="draft")
        db.add(project)
        db.commit()
        db.refresh(project)

    # Check if already shortlisted
    existing = db.query(ProjectShortlist).filter_by(
        project_id=project.id,
        module_id=module_id
    ).first()

    if not existing:
        # Check shortlist limit (max 3)
        shortlist_count = db.query(ProjectShortlist).filter_by(project_id=project.id).count()
        if shortlist_count >= 3:
            raise HTTPException(status_code=400, detail="Maximum 3 modules can be shortlisted")

        shortlist = ProjectShortlist(project_id=project.id, module_id=module_id)
        db.add(shortlist)
        db.commit()

    return RedirectResponse(url="/", status_code=303)


@app.get("/customer/module-details", response_class=HTMLResponse)
async def module_details(request: Request):
    """Show shortlisted modules and RFQ submission"""
    db = next(get_db())
    project = db.query(Project).first()

    if not project:
        return RedirectResponse(url="/", status_code=303)

    # Get shortlisted modules
    shortlist = db.query(ProjectShortlist).filter_by(project_id=project.id).all()
    modules = [s.module for s in shortlist]

    return templates.TemplateResponse(
        "customer_module_details.html",
        {
            "request": request,
            "project": project,
            "modules": modules
        }
    )


@app.post("/customer/submit-rfq")
async def submit_rfq():
    """Submit RFQ - transitions project to ready for SST review"""
    db = next(get_db())
    project = db.query(Project).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.status = "rfq_submitted"
    db.commit()

    return RedirectResponse(url="/customer/module-details", status_code=303)


# ===== SST ADMIN INTERFACE ROUTES =====

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """SST Admin dashboard - view all projects and RFQs"""
    db = next(get_db())
    projects = db.query(Project).all()

    # Get selected project (default to first)
    selected_project_id = request.query_params.get("project_id")
    if selected_project_id:
        project = db.query(Project).filter_by(id=int(selected_project_id)).first()
    else:
        project = projects[0] if projects else None

    rfqs = []
    shortlisted_modules = []
    if project:
        rfqs = db.query(RFQ).filter_by(project_id=project.id).all()
        shortlist = db.query(ProjectShortlist).filter_by(project_id=project.id).all()
        shortlisted_modules = [s.module for s in shortlist]

    return templates.TemplateResponse(
        "sst_admin_dashboard.html",
        {
            "request": request,
            "projects": projects,
            "project": project,
            "rfqs": rfqs,
            "shortlisted_modules": shortlisted_modules
        }
    )


@app.post("/admin/project/{project_id}/update")
async def update_project(
    project_id: int,
    target_mw: float = Form(...),
    delivery_date: str = Form(...)
):
    """Update project parameters"""
    db = next(get_db())
    project = db.query(Project).filter_by(id=project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.target_mw = target_mw
    project.delivery_date = delivery_date
    db.commit()

    return RedirectResponse(url=f"/admin/dashboard?project_id={project_id}", status_code=303)


@app.post("/admin/module/{module_id}/update")
async def update_module_catalog(
    module_id: int,
    price_per_watt: float = Form(...)
):
    """Update module catalog pricing"""
    db = next(get_db())
    module = db.query(Module).filter_by(id=module_id).first()

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    module.price_per_watt = price_per_watt
    db.commit()

    # Get the project_id from referrer or use default
    # For simplicity, redirect to dashboard
    return RedirectResponse(url="/admin/dashboard", status_code=303)


@app.post("/admin/send-rfqs/{project_id}")
async def send_rfqs(project_id: int):
    """Create and send RFQs for all shortlisted modules"""
    db = next(get_db())
    project = db.query(Project).filter_by(id=project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get shortlisted modules
    shortlist = db.query(ProjectShortlist).filter_by(project_id=project.id).all()

    if not shortlist:
        raise HTTPException(status_code=400, detail="No modules shortlisted")

    # For each shortlisted module, create RFQ and send to manufacturer's vendor
    rfqs_created = 0
    for item in shortlist:
        module = item.module

        # Find vendor that matches this module's manufacturer
        vendor = db.query(Vendor).filter_by(name=module.manufacturer).first()

        if not vendor:
            print(f"⚠️  No vendor found for manufacturer: {module.manufacturer}")
            continue

        # Check if RFQ already exists for this combination
        existing_rfq = db.query(RFQ).filter_by(
            project_id=project.id,
            vendor_id=vendor.id,
            module_id=module.id
        ).first()

        if existing_rfq:
            # RFQ already exists, just resend email if pending
            if existing_rfq.status == 'pending':
                portal_link = f"http://localhost:8000/vendor/{vendor.portal_token}"
                send_rfq_email(
                    to_email=vendor.email,
                    vendor_name=vendor.name,
                    contact_name=vendor.contact_name,
                    project_name=project.name,
                    module_name=module.name,
                    module_wattage=module.wattage,
                    module_manufacturer=module.manufacturer,
                    portal_link=portal_link
                )
                existing_rfq.status = 'sent'
                existing_rfq.sent_at = datetime.utcnow()
            continue

        # Create new RFQ
        rfq = RFQ(
            project_id=project.id,
            vendor_id=vendor.id,
            module_id=module.id,
            token=str(uuid.uuid4()),
            status='pending',
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        db.add(rfq)
        db.commit()
        db.refresh(rfq)

        # Send email with vendor portal link
        portal_link = f"http://localhost:8000/vendor/{vendor.portal_token}"
        success = send_rfq_email(
            to_email=vendor.email,
            vendor_name=vendor.name,
            contact_name=vendor.contact_name,
            project_name=project.name,
            module_name=module.name,
            module_wattage=module.wattage,
            module_manufacturer=module.manufacturer,
            portal_link=portal_link
        )

        if success:
            rfq.status = 'sent'
            rfq.sent_at = datetime.utcnow()
            db.commit()
            rfqs_created += 1

    # Update project status
    project.status = 'rfqs_sent'
    db.commit()

    print(f"✅ Created and sent {rfqs_created} RFQs")
    return RedirectResponse(url=f"/admin/dashboard?project_id={project_id}", status_code=303)


@app.get("/admin/quotes", response_class=HTMLResponse)
async def admin_quotes(request: Request):
    """View quote comparison and mock Retool API"""
    db = next(get_db())
    quotes = db.query(Quote).all()
    rfqs = db.query(RFQ).filter_by(status="submitted").all()

    # Build mock Retool API payload
    retool_data = []
    for quote in quotes:
        retool_data.append({
            "project_id": quote.rfq.project_id,
            "vendor_id": quote.rfq.vendor_id,
            "vendor_name": quote.rfq.vendor.name,
            "quote_date": quote.submitted_at.isoformat(),
            "module_id": quote.module_id,
            "module_name": quote.module.name,
            "price": quote.price,
            "delivery_date": quote.delivery_date,
            "target_quantity": quote.target_quantity,
            "payment_terms": quote.payment_terms,
            "action": quote.action,
            "amendments": quote.amendments if quote.amendments else None
        })

    return templates.TemplateResponse(
        "admin_quotes.html",
        {
            "request": request,
            "quotes": quotes,
            "rfqs": rfqs,
            "retool_data": retool_data
        }
    )


# ===== VENDOR PORTAL ROUTES =====

@app.get("/vendor/{portal_token}", response_class=HTMLResponse)
async def vendor_dashboard(portal_token: str, request: Request):
    """Vendor dashboard - view all open RFQs"""
    db = next(get_db())
    vendor = db.query(Vendor).filter_by(portal_token=portal_token).first()

    if not vendor:
        raise HTTPException(status_code=404, detail="Invalid vendor portal link")

    # Get all RFQs for this vendor
    rfqs = db.query(RFQ).filter_by(vendor_id=vendor.id).all()

    return templates.TemplateResponse(
        "vendor_dashboard.html",
        {
            "request": request,
            "vendor": vendor,
            "rfqs": rfqs
        }
    )


@app.get("/vendor/{portal_token}/rfq/{rfq_id}", response_class=HTMLResponse)
async def vendor_rfq_detail(portal_token: str, rfq_id: int, request: Request):
    """Vendor RFQ detail - view specific RFQ and submit quote"""
    db = next(get_db())
    vendor = db.query(Vendor).filter_by(portal_token=portal_token).first()

    if not vendor:
        raise HTTPException(status_code=404, detail="Invalid vendor portal link")

    rfq = db.query(RFQ).filter_by(id=rfq_id, vendor_id=vendor.id).first()

    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")

    # Check if token expired
    if rfq.expires_at and rfq.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="This RFQ has expired")

    # Mark as viewed
    if rfq.status == "sent":
        rfq.status = "viewed"
        db.commit()

    return templates.TemplateResponse(
        "vendor_portal.html",
        {
            "request": request,
            "rfq": rfq,
            "module": rfq.module,
            "project": rfq.project,
            "vendor": vendor,
            "portal_token": portal_token
        }
    )


@app.post("/vendor/{portal_token}/rfq/{rfq_id}/submit")
async def submit_quote(
    portal_token: str,
    rfq_id: int,
    price: float = Form(...),
    delivery_date: str = Form(...),
    target_quantity: int = Form(...),
    payment_terms: str = Form(...),
    action: str = Form(...),
    amendments: str = Form(default="")
):
    """Vendor submits quote"""
    db = next(get_db())
    vendor = db.query(Vendor).filter_by(portal_token=portal_token).first()

    if not vendor:
        raise HTTPException(status_code=404, detail="Invalid vendor portal link")

    rfq = db.query(RFQ).filter_by(id=rfq_id, vendor_id=vendor.id).first()

    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")

    # Create quote
    quote = Quote(
        rfq_id=rfq.id,
        module_id=rfq.module_id,
        price=price,
        delivery_date=delivery_date,
        target_quantity=target_quantity,
        payment_terms=payment_terms,
        action=action,
        amendments=amendments if amendments else None,
        submitted_at=datetime.utcnow()
    )

    db.add(quote)
    rfq.status = "submitted" if action != "decline" else "declined"
    db.commit()

    return RedirectResponse(url=f"/vendor/{portal_token}/rfq/{rfq_id}/confirmation", status_code=303)


@app.get("/vendor/{portal_token}/rfq/{rfq_id}/confirmation", response_class=HTMLResponse)
async def vendor_confirmation(portal_token: str, rfq_id: int, request: Request):
    """Thank you page after vendor submits quote"""
    db = next(get_db())
    vendor = db.query(Vendor).filter_by(portal_token=portal_token).first()

    if not vendor:
        raise HTTPException(status_code=404, detail="Invalid vendor portal link")

    rfq = db.query(RFQ).filter_by(id=rfq_id, vendor_id=vendor.id).first()

    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")

    return templates.TemplateResponse(
        "vendor_confirmation.html",
        {
            "request": request,
            "rfq": rfq,
            "vendor": vendor,
            "portal_token": portal_token
        }
    )


# ===== API ROUTES (Mock Retool) =====

@app.get("/api/quotes/{rfq_id}")
async def get_quotes_api(rfq_id: int):
    """API endpoint - get quotes for RFQ (mock Retool integration)"""
    db = next(get_db())
    quotes = db.query(Quote).filter_by(rfq_id=rfq_id).all()

    return {
        "rfq_id": rfq_id,
        "quotes": [
            {
                "id": q.id,
                "module_name": q.module.name,
                "vendor_name": q.rfq.vendor.name,
                "price": q.price,
                "delivery_date": q.delivery_date,
                "availability": q.availability,
                "target_quantity": q.target_quantity,
                "payment_terms": q.payment_terms,
                "action": q.action,
                "submitted_at": q.submitted_at.isoformat()
            }
            for q in quotes
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
