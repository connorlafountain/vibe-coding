"""
Database models and seed data for Vendor Portal POC
"""
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random

Base = declarative_base()

# Database Models

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, default='draft')  # draft, rfq_sent, quotes_received
    created_at = Column(DateTime, default=datetime.utcnow)
    target_mw = Column(Float, nullable=False, default=100.0)  # Project size in MW
    delivery_date = Column(String, nullable=False, default='Q3 2026')  # Expected delivery

    shortlist = relationship("ProjectShortlist", back_populates="project")
    rfqs = relationship("RFQ", back_populates="project")


class Module(Base):
    __tablename__ = 'modules'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    wattage = Column(Integer, nullable=False)
    technology = Column(String, nullable=False)
    efficiency = Column(Float, nullable=False)
    dimensions = Column(String, nullable=False)
    price_per_watt = Column(Float, nullable=False)

    shortlist = relationship("ProjectShortlist", back_populates="module")
    quotes = relationship("Quote", back_populates="module")


class ProjectShortlist(Base):
    __tablename__ = 'project_shortlist'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)

    project = relationship("Project", back_populates="shortlist")
    module = relationship("Module", back_populates="shortlist")


class Vendor(Base):
    __tablename__ = 'vendors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    portal_token = Column(String, unique=True, nullable=False)
    payment_terms = Column(String, nullable=False, default='Net 30')

    rfqs = relationship("RFQ", back_populates="vendor")


class RFQ(Base):
    __tablename__ = 'rfqs'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    token = Column(String, unique=True, nullable=False)
    status = Column(String, default='pending')  # pending, sent, viewed, submitted, declined
    sent_at = Column(DateTime)
    expires_at = Column(DateTime)

    project = relationship("Project", back_populates="rfqs")
    vendor = relationship("Vendor", back_populates="rfqs")
    module = relationship("Module")
    quotes = relationship("Quote", back_populates="rfq")


class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    rfq_id = Column(Integer, ForeignKey('rfqs.id'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    price = Column(Float, nullable=False)
    delivery_date = Column(String, nullable=False)
    target_quantity = Column(Integer, nullable=False)
    payment_terms = Column(Text, nullable=False)
    action = Column(String, nullable=False)  # confirm, amendment, decline
    amendments = Column(Text, nullable=True)  # JSON string of what was changed
    submitted_at = Column(DateTime, default=datetime.utcnow)

    rfq = relationship("RFQ", back_populates="quotes")
    module = relationship("Module", back_populates="quotes")


# Database initialization and seed data

DATABASE_URL = "sqlite:///./vendor_portal.db"

def init_database():
    """Initialize database and create all tables"""
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine

def get_session():
    """Get database session"""
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def seed_database():
    """Populate database with mock data"""
    engine = init_database()
    session = get_session()

    # Check if already seeded
    if session.query(Module).count() > 0:
        print("Database already seeded")
        return

    print("Seeding database...")

    # Create 200 fake modules (realistic solar panel data)
    manufacturers = [
        "JinkoSolar", "Trina Solar", "LONGi Solar", "Canadian Solar",
        "JA Solar", "First Solar", "Hanwha Q CELLS", "REC Group",
        "SunPower", "Risen Energy", "GCL System Integration", "Jinergy"
    ]

    technologies = [
        "Monocrystalline PERC", "Polycrystalline", "Monocrystalline HJT",
        "Thin Film CdTe", "Bifacial PERC", "TOPCon", "IBC"
    ]

    modules = []
    for i in range(200):
        wattage = random.choice(range(500, 805, 5))  # 500W to 800W in 5W increments
        manufacturer = random.choice(manufacturers)
        technology = random.choice(technologies)
        efficiency = round(random.uniform(19.5, 23.5), 1)

        # Realistic dimensions for solar panels
        length = random.choice([2278, 2384, 2465, 2590])
        width = random.choice([1134, 1303, 1422])
        depth = random.choice([30, 35, 40])

        module = Module(
            name=f"{manufacturer} {technology.split()[0]} {wattage}W",
            manufacturer=manufacturer,
            wattage=wattage,
            technology=technology,
            efficiency=efficiency,
            dimensions=f"{length} x {width} x {depth} mm",
            price_per_watt=round(random.uniform(0.22, 0.32), 3)
        )
        modules.append(module)

    session.add_all(modules)
    session.commit()
    print(f"✓ Created {len(modules)} modules")

    # Create vendors that match module manufacturers (1:1 mapping)
    # Each manufacturer is essentially a vendor for their own products
    contact_names = [
        "James Chen", "Maria Rodriguez", "David Kim", "Sarah Johnson",
        "Michael Zhang", "Emma Thompson", "Carlos Martinez", "Lisa Wang",
        "Robert Brown", "Anna Lee", "Thomas Anderson", "Jessica Taylor"
    ]

    # Standard payment terms for each vendor
    payment_terms_options = [
        "Net 30", "Net 45", "50% deposit, 50% on delivery",
        "Net 60", "Letter of Credit", "Net 30, 2% discount if paid in 10 days",
        "Net 45, 1.5% discount if paid in 15 days", "Cash on Delivery",
        "Net 30 from delivery", "50% upfront, 25% on shipment, 25% on delivery",
        "Net 60 from invoice date", "Net 30 with approved credit"
    ]

    vendors = []
    vendor_map = {}  # Map manufacturer -> vendor for easy lookup
    for i, manufacturer in enumerate(manufacturers):
        # Create email-friendly manufacturer name
        email_name = manufacturer.lower().replace(" ", "").replace("qcells", "qcells")
        vendor = Vendor(
            name=manufacturer,
            contact_name=contact_names[i],
            email="clafountain@anzarenewables.com",  # All emails go to Connor for POC
            phone=f"+1-555-{str(i).zfill(4)}",
            portal_token=str(uuid.uuid4()),  # Unique portal access token per vendor
            payment_terms=payment_terms_options[i]  # Each vendor has their standard terms
        )
        vendors.append(vendor)
        vendor_map[manufacturer] = vendor

    session.add_all(vendors)
    session.commit()
    print(f"✓ Created {len(vendors)} manufacturer-based vendors")

    # Create a sample project with 3 shortlisted modules
    project = Project(
        name="Arizona Solar Farm 100MW",
        status="draft",
        created_at=datetime.utcnow(),
        target_mw=100.0,  # 100 MW project
        delivery_date="Q3 2026"  # Expected delivery
    )
    session.add(project)
    session.commit()
    print(f"✓ Created sample project: {project.name}")

    # Don't pre-populate shortlist - let user select their own modules
    # (This makes testing easier)
    session.commit()
    print(f"✓ Project created with empty shortlist (ready for user selection)")

    # Note: RFQs are created when admin clicks "Send RFQs" button
    # Each RFQ is tied to a specific module and sent to that module's manufacturer
    print(f"✓ No RFQs created yet (will be created when admin sends bids)")

    print("\n✅ Database seeded successfully!")
    session.close()


if __name__ == "__main__":
    seed_database()
