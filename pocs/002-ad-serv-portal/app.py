"""
Advisory Services Portal POC - FastAPI Application
"""
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_session, Customer, Project, Milestone, TestResult
from plot_generator import generate_plots_from_file, UPLOAD_DIR
import json
import shutil
from pathlib import Path

app = FastAPI(title="Advisory Services Portal POC")

# Templates and Static Files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add custom Jinja2 filter for JSON parsing
templates.env.filters['from_json'] = json.loads


# Helper function to get database session
def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


# Helper function to calculate project progress
def calculate_progress(milestones):
    """Calculate percentage of milestones completed"""
    if not milestones:
        return 0
    completed = sum(1 for m in milestones if m.status == "complete")
    return int((completed / len(milestones)) * 100)


# ===== CUSTOMER PORTAL ROUTES =====

@app.get("/customer/{portal_token}", response_class=HTMLResponse)
async def customer_portal(portal_token: str, request: Request):
    """Customer portal - view all their projects"""
    db = next(get_db())
    customer = db.query(Customer).filter_by(portal_token=portal_token).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Invalid portal link")

    # Get all projects for this customer with milestone counts
    projects_with_progress = []
    for project in customer.projects:
        progress = calculate_progress(project.milestones)
        projects_with_progress.append({
            "project": project,
            "progress": progress,
            "total_milestones": len(project.milestones),
            "completed_milestones": sum(1 for m in project.milestones if m.status == "complete")
        })

    return templates.TemplateResponse(
        "customer_portal.html",
        {
            "request": request,
            "customer": customer,
            "portal_token": portal_token,
            "projects_data": projects_with_progress
        }
    )


@app.get("/customer/{portal_token}/project/{project_id}", response_class=HTMLResponse)
async def project_detail(portal_token: str, project_id: int, request: Request):
    """Project detail - view milestones and status"""
    db = next(get_db())
    customer = db.query(Customer).filter_by(portal_token=portal_token).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Invalid portal link")

    project = db.query(Project).filter_by(id=project_id, customer_id=customer.id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Calculate progress
    progress = calculate_progress(project.milestones)

    # Sort milestones by order
    sorted_milestones = sorted(project.milestones, key=lambda m: m.order)

    # Group milestones by category
    milestones_by_category = {}
    for milestone in sorted_milestones:
        category = milestone.category or "other"
        if category not in milestones_by_category:
            milestones_by_category[category] = []
        milestones_by_category[category].append(milestone)

    # Get test results for this project
    test_results = db.query(TestResult).filter_by(project_id=project.id).order_by(TestResult.uploaded_at.desc()).all()

    return templates.TemplateResponse(
        "project_detail.html",
        {
            "request": request,
            "customer": customer,
            "portal_token": portal_token,
            "project": project,
            "milestones": sorted_milestones,
            "milestones_by_category": milestones_by_category,
            "progress": progress,
            "test_results": test_results
        }
    )


@app.post("/customer/{portal_token}/project/{project_id}/upload")
async def upload_test_data(
    portal_token: str,
    project_id: int,
    file: UploadFile = File(...)
):
    """Upload IHI test data and generate plots"""
    db = next(get_db())
    customer = db.query(Customer).filter_by(portal_token=portal_token).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Invalid portal link")

    project = db.query(Project).filter_by(id=project_id, customer_id=customer.id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are supported")

    # Save uploaded file
    upload_path = UPLOAD_DIR / f"project_{project_id}_{file.filename}"
    with upload_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Generate plots
    try:
        result = generate_plots_from_file(str(upload_path), project_id)

        # Save test result to database
        # plot_paths now stores the plot data (list of {'title': ..., 'html': ...} dicts)
        test_result = TestResult(
            project_id=project_id,
            filename=file.filename,
            file_path=str(upload_path),
            test_type=result["test_type"],
            plot_paths=json.dumps(result["plots"])  # Store plot HTML data as JSON
        )
        db.add(test_result)
        db.commit()

        print(f"✅ Generated {len(result['plots'])} interactive plots for project {project_id}")

    except Exception as e:
        print(f"❌ Error generating plots: {e}")
        import traceback
        traceback.print_exc()
        # Still redirect back, but plots won't show
        pass

    return RedirectResponse(
        url=f"/customer/{portal_token}/project/{project_id}",
        status_code=303
    )


# ===== ADMIN/INTERNAL ROUTES =====

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Internal admin dashboard - view all customers and projects"""
    db = next(get_db())

    # Get all customers with their projects
    customers = db.query(Customer).all()

    # Get all projects with progress
    all_projects = db.query(Project).all()
    projects_with_progress = []
    for project in all_projects:
        progress = calculate_progress(project.milestones)
        projects_with_progress.append({
            "project": project,
            "progress": progress,
            "customer": project.customer
        })

    # Sort by status priority: blocked > in_progress > testing > planning > complete
    status_order = {"blocked": 0, "in_progress": 1, "testing": 2, "planning": 3, "complete": 4}
    projects_with_progress.sort(key=lambda x: (
        status_order.get(x["project"].status, 5),
        x["project"].created_at
    ))

    # Count projects by status
    status_counts = {}
    for project in all_projects:
        status = project.status
        status_counts[status] = status_counts.get(status, 0) + 1

    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "customers": customers,
            "projects_data": projects_with_progress,
            "status_counts": status_counts,
            "total_projects": len(all_projects)
        }
    )


# ===== HOME REDIRECT =====

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - redirect to admin dashboard for POC"""
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
