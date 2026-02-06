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
    """SST Admin dashboard - view all RFQs"""
    db = next(get_db())
    rfqs = db.query(RFQ).all()
    project = db.query(Project).first()

    return templates.TemplateResponse(
        "sst_admin_dashboard.html",
        {
            "request": request,
            "rfqs": rfqs,
            "project": project
        }
    )


@app.post("/admin/send-bid/{rfq_id}")
async def send_bid(rfq_id: int):
    """Send RFQ email to vendor"""
    db = next(get_db())
    rfq = db.query(RFQ).filter_by(id=rfq_id).first()

    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")

    # Get shortlisted modules for this project
    shortlist = db.query(ProjectShortlist).filter_by(project_id=rfq.project_id).all()
    modules = [s.module for s in shortlist]

    # Send email
    portal_link = f"http://localhost:8000/vendor/{rfq.token}"
    success = send_rfq_email(
        to_email=rfq.vendor.email,
        vendor_name=rfq.vendor.name,
        contact_name=rfq.vendor.contact_name,
        project_name=rfq.project.name,
        modules=modules,
        portal_link=portal_link
    )

    if success:
        rfq.status = "sent"
        rfq.sent_at = datetime.utcnow()
        db.commit()

    return RedirectResponse(url="/admin/dashboard", status_code=303)


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
            "availability": quote.availability,
            "target_quantity": quote.target_quantity,
            "payment_terms": quote.payment_terms,
            "action": quote.action
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

@app.get("/vendor/{token}", response_class=HTMLResponse)
async def vendor_portal(token: str, request: Request):
    """Vendor portal - view RFQ and submit quote"""
    db = next(get_db())
    rfq = db.query(RFQ).filter_by(token=token).first()

    if not rfq:
        raise HTTPException(status_code=404, detail="Invalid or expired token")

    # Check if token expired
    if rfq.expires_at and rfq.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="This RFQ has expired")

    # Mark as viewed
    if rfq.status == "sent":
        rfq.status = "viewed"
        db.commit()

    # Get shortlisted modules
    shortlist = db.query(ProjectShortlist).filter_by(project_id=rfq.project_id).all()
    modules = [s.module for s in shortlist]

    return templates.TemplateResponse(
        "vendor_portal.html",
        {
            "request": request,
            "rfq": rfq,
            "modules": modules,
            "project": rfq.project,
            "vendor": rfq.vendor
        }
    )


@app.post("/vendor/{token}/submit")
async def submit_quote(
    token: str,
    module_id: int = Form(...),
    price: float = Form(...),
    delivery_date: str = Form(...),
    availability: str = Form(...),
    target_quantity: int = Form(...),
    payment_terms: str = Form(...),
    action: str = Form(...)
):
    """Vendor submits quote"""
    db = next(get_db())
    rfq = db.query(RFQ).filter_by(token=token).first()

    if not rfq:
        raise HTTPException(status_code=404, detail="Invalid token")

    # Create quote
    quote = Quote(
        rfq_id=rfq.id,
        module_id=module_id,
        price=price,
        delivery_date=delivery_date,
        availability=availability,
        target_quantity=target_quantity,
        payment_terms=payment_terms,
        action=action,
        submitted_at=datetime.utcnow()
    )

    db.add(quote)
    rfq.status = "submitted" if action != "decline" else "declined"
    db.commit()

    return RedirectResponse(url=f"/vendor/{token}/confirmation", status_code=303)


@app.get("/vendor/{token}/confirmation", response_class=HTMLResponse)
async def vendor_confirmation(token: str, request: Request):
    """Thank you page after vendor submits quote"""
    db = next(get_db())
    rfq = db.query(RFQ).filter_by(token=token).first()

    if not rfq:
        raise HTTPException(status_code=404, detail="Invalid token")

    return templates.TemplateResponse(
        "vendor_confirmation.html",
        {
            "request": request,
            "rfq": rfq,
            "vendor": rfq.vendor
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
