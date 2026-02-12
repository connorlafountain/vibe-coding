"""
Advisory Services Portal POC - Database Models and Seed Data
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid

# Database setup
DATABASE_URL = "sqlite:///./advisory_services.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    """Get database session"""
    return SessionLocal()


# ===== DATABASE MODELS =====

class Customer(Base):
    """Customer/Client company"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_name = Column(String)
    contact_email = Column(String)
    portal_token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    projects = relationship("Project", back_populates="customer", cascade="all, delete-orphan")


class Project(Base):
    """Customer project (battery storage installation)"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # planning, in_progress, testing, complete
    start_date = Column(String)
    expected_completion = Column(String)
    location = Column(String)
    capacity = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="projects")
    milestones = relationship("Milestone", back_populates="project", cascade="all, delete-orphan")
    test_results = relationship("TestResult", back_populates="project", cascade="all, delete-orphan")


class Milestone(Base):
    """Project milestone (engineering, testing, etc.)"""
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    category = Column(String)  # engineering, testing, procurement, construction
    status = Column(String, nullable=False)  # not_started, in_progress, complete, blocked
    due_date = Column(String)
    completion_date = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="milestones")


class TestResult(Base):
    """IHI test data upload and generated plots"""
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    filename = Column(String, nullable=False)  # Original uploaded filename
    file_path = Column(String, nullable=False)  # Path to uploaded Excel file
    test_type = Column(String, nullable=False)  # "commissioning" or "temp_humidity"
    plot_paths = Column(Text)  # JSON array of plot image paths
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="test_results")


# ===== SEED DATA =====

def seed_database():
    """Seed database with mock data"""
    db = get_session()

    # Clear existing data
    db.query(TestResult).delete()
    db.query(Milestone).delete()
    db.query(Project).delete()
    db.query(Customer).delete()
    db.commit()

    print("🌱 Seeding Advisory Services Portal database...")

    # ===== CUSTOMER 1: Acme Solar Inc =====
    customer1 = Customer(
        name="Acme Solar Inc",
        contact_name="Sarah Johnson",
        contact_email="sjohnson@acmesolar.example",
        portal_token="acme-solar-2024"
    )
    db.add(customer1)
    db.commit()
    db.refresh(customer1)

    # Project 1: Maple Street - Complete
    project1 = Project(
        customer_id=customer1.id,
        name="Maple Street Battery Storage",
        status="complete",
        start_date="Q1 2024",
        expected_completion="Q3 2024",
        location="Boston, MA",
        capacity="5 MW / 20 MWh",
        description="Community battery storage system for peak shaving and grid support"
    )
    db.add(project1)
    db.commit()
    db.refresh(project1)

    # Milestones for Maple Street (all complete)
    milestones_p1 = [
        Milestone(project_id=project1.id, name="Site Survey", category="engineering",
                  status="complete", due_date="2024-02-15", completion_date="2024-02-10",
                  notes="Site assessment completed ahead of schedule", order=1),
        Milestone(project_id=project1.id, name="Engineering Design Review", category="engineering",
                  status="complete", due_date="2024-03-01", completion_date="2024-02-28",
                  notes="Design approved with minor revisions", order=2),
        Milestone(project_id=project1.id, name="Equipment Procurement", category="procurement",
                  status="complete", due_date="2024-04-15", completion_date="2024-04-10", order=3),
        Milestone(project_id=project1.id, name="IHI Commissioning Tests", category="testing",
                  status="complete", due_date="2024-06-01", completion_date="2024-05-28",
                  notes="All capacity and ramp rate tests passed", order=4),
        Milestone(project_id=project1.id, name="Temperature & Humidity Validation", category="testing",
                  status="complete", due_date="2024-06-15", completion_date="2024-06-12",
                  notes="Environmental conditions within spec", order=5),
        Milestone(project_id=project1.id, name="Final Acceptance", category="engineering",
                  status="complete", due_date="2024-07-01", completion_date="2024-06-30", order=6),
        Milestone(project_id=project1.id, name="Project Closeout", category="engineering",
                  status="complete", due_date="2024-07-15", completion_date="2024-07-10",
                  notes="Documentation submitted and archived", order=7),
    ]
    for m in milestones_p1:
        db.add(m)

    # Project 2: Riverside - Testing phase
    project2 = Project(
        customer_id=customer1.id,
        name="Riverside Energy Center",
        status="testing",
        start_date="Q2 2024",
        expected_completion="Q4 2024",
        location="Portland, OR",
        capacity="10 MW / 40 MWh",
        description="Large-scale utility battery storage with renewable integration"
    )
    db.add(project2)
    db.commit()
    db.refresh(project2)

    # Milestones for Riverside (mixed progress)
    milestones_p2 = [
        Milestone(project_id=project2.id, name="Site Survey", category="engineering",
                  status="complete", due_date="2024-04-01", completion_date="2024-03-28", order=1),
        Milestone(project_id=project2.id, name="Engineering Design Review", category="engineering",
                  status="complete", due_date="2024-05-01", completion_date="2024-04-30", order=2),
        Milestone(project_id=project2.id, name="Equipment Procurement", category="procurement",
                  status="complete", due_date="2024-06-30", completion_date="2024-06-25", order=3),
        Milestone(project_id=project2.id, name="IHI Commissioning Tests", category="testing",
                  status="in_progress", due_date="2024-08-15", completion_date=None,
                  notes="Capacity tests complete; ramp rate tests in progress", order=4),
        Milestone(project_id=project2.id, name="Temperature & Humidity Validation", category="testing",
                  status="not_started", due_date="2024-09-01", completion_date=None, order=5),
        Milestone(project_id=project2.id, name="Final Acceptance", category="engineering",
                  status="not_started", due_date="2024-10-01", completion_date=None, order=6),
        Milestone(project_id=project2.id, name="Project Closeout", category="engineering",
                  status="not_started", due_date="2024-10-15", completion_date=None, order=7),
    ]
    for m in milestones_p2:
        db.add(m)

    # ===== CUSTOMER 2: GreenTech Energy =====
    customer2 = Customer(
        name="GreenTech Energy",
        contact_name="Michael Chen",
        contact_email="mchen@greentech.example",
        portal_token="greentech-energy-2024"
    )
    db.add(customer2)
    db.commit()
    db.refresh(customer2)

    # Project 3: Solar Ridge - In Progress
    project3 = Project(
        customer_id=customer2.id,
        name="Solar Ridge Storage Facility",
        status="in_progress",
        start_date="Q3 2024",
        expected_completion="Q1 2025",
        location="Austin, TX",
        capacity="15 MW / 60 MWh",
        description="Co-located battery storage with 50 MW solar farm"
    )
    db.add(project3)
    db.commit()
    db.refresh(project3)

    # Milestones for Solar Ridge (early stages)
    milestones_p3 = [
        Milestone(project_id=project3.id, name="Site Survey", category="engineering",
                  status="complete", due_date="2024-06-15", completion_date="2024-06-12", order=1),
        Milestone(project_id=project3.id, name="Engineering Design Review", category="engineering",
                  status="in_progress", due_date="2024-07-30", completion_date=None,
                  notes="Initial design submitted; awaiting utility approval", order=2),
        Milestone(project_id=project3.id, name="Equipment Procurement", category="procurement",
                  status="not_started", due_date="2024-09-15", completion_date=None, order=3),
        Milestone(project_id=project3.id, name="IHI Commissioning Tests", category="testing",
                  status="not_started", due_date="2024-11-30", completion_date=None, order=4),
        Milestone(project_id=project3.id, name="Temperature & Humidity Validation", category="testing",
                  status="not_started", due_date="2024-12-15", completion_date=None, order=5),
        Milestone(project_id=project3.id, name="Final Acceptance", category="engineering",
                  status="not_started", due_date="2025-01-15", completion_date=None, order=6),
        Milestone(project_id=project3.id, name="Project Closeout", category="engineering",
                  status="not_started", due_date="2025-02-01", completion_date=None, order=7),
    ]
    for m in milestones_p3:
        db.add(m)

    # Project 4: Valley View - Planning
    project4 = Project(
        customer_id=customer2.id,
        name="Valley View Microgrid",
        status="planning",
        start_date="Q4 2024",
        expected_completion="Q2 2025",
        location="Denver, CO",
        capacity="8 MW / 32 MWh",
        description="Microgrid battery storage for critical infrastructure resilience"
    )
    db.add(project4)
    db.commit()
    db.refresh(project4)

    # Milestones for Valley View (all not started)
    milestones_p4 = [
        Milestone(project_id=project4.id, name="Site Survey", category="engineering",
                  status="not_started", due_date="2024-09-01", completion_date=None, order=1),
        Milestone(project_id=project4.id, name="Engineering Design Review", category="engineering",
                  status="not_started", due_date="2024-10-15", completion_date=None, order=2),
        Milestone(project_id=project4.id, name="Equipment Procurement", category="procurement",
                  status="not_started", due_date="2024-12-01", completion_date=None, order=3),
        Milestone(project_id=project4.id, name="IHI Commissioning Tests", category="testing",
                  status="not_started", due_date="2025-02-15", completion_date=None, order=4),
        Milestone(project_id=project4.id, name="Temperature & Humidity Validation", category="testing",
                  status="not_started", due_date="2025-03-01", completion_date=None, order=5),
        Milestone(project_id=project4.id, name="Final Acceptance", category="engineering",
                  status="not_started", due_date="2025-04-01", completion_date=None, order=6),
        Milestone(project_id=project4.id, name="Project Closeout", category="engineering",
                  status="not_started", due_date="2025-04-15", completion_date=None, order=7),
    ]
    for m in milestones_p4:
        db.add(m)

    # ===== CUSTOMER 3: PowerGrid Solutions =====
    customer3 = Customer(
        name="PowerGrid Solutions",
        contact_name="Emily Rodriguez",
        contact_email="erodriguez@powergrid.example",
        portal_token="powergrid-2024"
    )
    db.add(customer3)
    db.commit()
    db.refresh(customer3)

    # Project 5: Coastal Storage - Testing (with one blocked milestone)
    project5 = Project(
        customer_id=customer3.id,
        name="Coastal Energy Storage",
        status="testing",
        start_date="Q1 2024",
        expected_completion="Q3 2024",
        location="San Diego, CA",
        capacity="12 MW / 48 MWh",
        description="Coastal battery installation with grid stability services"
    )
    db.add(project5)
    db.commit()
    db.refresh(project5)

    # Milestones for Coastal Storage (one blocked)
    milestones_p5 = [
        Milestone(project_id=project5.id, name="Site Survey", category="engineering",
                  status="complete", due_date="2024-02-15", completion_date="2024-02-10", order=1),
        Milestone(project_id=project5.id, name="Engineering Design Review", category="engineering",
                  status="complete", due_date="2024-03-15", completion_date="2024-03-12", order=2),
        Milestone(project_id=project5.id, name="Equipment Procurement", category="procurement",
                  status="complete", due_date="2024-05-01", completion_date="2024-04-28", order=3),
        Milestone(project_id=project5.id, name="IHI Commissioning Tests", category="testing",
                  status="complete", due_date="2024-06-15", completion_date="2024-06-12", order=4),
        Milestone(project_id=project5.id, name="Temperature & Humidity Validation", category="testing",
                  status="blocked", due_date="2024-07-01", completion_date=None,
                  notes="Awaiting replacement HVAC sensors from vendor", order=5),
        Milestone(project_id=project5.id, name="Final Acceptance", category="engineering",
                  status="not_started", due_date="2024-08-01", completion_date=None, order=6),
        Milestone(project_id=project5.id, name="Project Closeout", category="engineering",
                  status="not_started", due_date="2024-08-15", completion_date=None, order=7),
    ]
    for m in milestones_p5:
        db.add(m)

    # Project 6: Mountain Peak - In Progress
    project6 = Project(
        customer_id=customer3.id,
        name="Mountain Peak Storage",
        status="in_progress",
        start_date="Q2 2024",
        expected_completion="Q4 2024",
        location="Salt Lake City, UT",
        capacity="6 MW / 24 MWh",
        description="High-altitude battery storage for seasonal demand support"
    )
    db.add(project6)
    db.commit()
    db.refresh(project6)

    # Milestones for Mountain Peak
    milestones_p6 = [
        Milestone(project_id=project6.id, name="Site Survey", category="engineering",
                  status="complete", due_date="2024-04-15", completion_date="2024-04-12", order=1),
        Milestone(project_id=project6.id, name="Engineering Design Review", category="engineering",
                  status="complete", due_date="2024-05-30", completion_date="2024-05-25", order=2),
        Milestone(project_id=project6.id, name="Equipment Procurement", category="procurement",
                  status="in_progress", due_date="2024-07-31", completion_date=None,
                  notes="Long-lead items ordered; delivery expected mid-August", order=3),
        Milestone(project_id=project6.id, name="IHI Commissioning Tests", category="testing",
                  status="not_started", due_date="2024-09-30", completion_date=None, order=4),
        Milestone(project_id=project6.id, name="Temperature & Humidity Validation", category="testing",
                  status="not_started", due_date="2024-10-15", completion_date=None, order=5),
        Milestone(project_id=project6.id, name="Final Acceptance", category="engineering",
                  status="not_started", due_date="2024-11-15", completion_date=None, order=6),
        Milestone(project_id=project6.id, name="Project Closeout", category="engineering",
                  status="not_started", due_date="2024-12-01", completion_date=None, order=7),
    ]
    for m in milestones_p6:
        db.add(m)

    db.commit()

    print("✅ Database seeded successfully!")
    print(f"   - {db.query(Customer).count()} customers")
    print(f"   - {db.query(Project).count()} projects")
    print(f"   - {db.query(Milestone).count()} milestones")
    print("\n📊 Portal Access URLs:")
    print("   - Acme Solar: http://localhost:8000/customer/acme-solar-2024")
    print("   - GreenTech Energy: http://localhost:8000/customer/greentech-energy-2024")
    print("   - PowerGrid Solutions: http://localhost:8000/customer/powergrid-2024")
    print("   - Admin Dashboard: http://localhost:8000/admin/dashboard")


if __name__ == "__main__":
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("📋 Database tables created")

    # Seed data
    seed_database()
