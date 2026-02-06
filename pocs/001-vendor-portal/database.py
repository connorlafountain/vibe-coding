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

    rfqs = relationship("RFQ", back_populates="vendor")


class RFQ(Base):
    __tablename__ = 'rfqs'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    token = Column(String, unique=True, nullable=False)
    status = Column(String, default='pending')  # pending, sent, viewed, submitted, declined
    sent_at = Column(DateTime)
    expires_at = Column(DateTime)

    project = relationship("Project", back_populates="rfqs")
    vendor = relationship("Vendor", back_populates="rfqs")
    quotes = relationship("Quote", back_populates="rfq")


class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    rfq_id = Column(Integer, ForeignKey('rfqs.id'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    price = Column(Float, nullable=False)
    delivery_date = Column(String, nullable=False)
    availability = Column(String, nullable=False)
    target_quantity = Column(Integer, nullable=False)
    payment_terms = Column(Text, nullable=False)
    action = Column(String, nullable=False)  # confirm, decline, counter
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

    # Create 10 fake vendors with funny/cool names
    vendors_data = [
        ("SolarCo Distributors", "Jane Smith", "jane@solarco.example", "+1-555-0123"),
        ("PanelSupply Inc.", "Bob Johnson", "bob@panelsupply.example", "+1-555-0456"),
        ("SunHarvest Solutions", "Alice Wong", "alice@sunharvest.example", "+1-555-0789"),
        ("Megawatt Merchants", "Carlos Rodriguez", "carlos@megawatt.example", "+1-555-0111"),
        ("GigaWatt Traders", "Emma Chen", "emma@gigawatt.example", "+1-555-0222"),
        ("ElectroSun Wholesale", "David Kim", "david@electrosun.example", "+1-555-0333"),
        ("BrightPanel Co.", "Sarah Thompson", "sarah@brightpanel.example", "+1-555-0444"),
        ("WattWorks Distribution", "Michael Brown", "michael@wattworks.example", "+1-555-0555"),
        ("SolarStack Suppliers", "Lisa Martinez", "lisa@solarstack.example", "+1-555-0666"),
        ("PowerGrid Distributors", "Tom Anderson", "tom@powergrid.example", "+1-555-0777"),
    ]

    vendors = []
    for name, contact, email, phone in vendors_data:
        vendor = Vendor(name=name, contact_name=contact, email=email, phone=phone)
        vendors.append(vendor)

    session.add_all(vendors)
    session.commit()
    print(f"✓ Created {len(vendors)} vendors")

    # Create a sample project with 3 shortlisted modules
    project = Project(
        name="Arizona Solar Farm 100MW",
        status="draft",
        created_at=datetime.utcnow()
    )
    session.add(project)
    session.commit()
    print(f"✓ Created sample project: {project.name}")

    # Add 3 random modules to shortlist
    shortlisted_modules = random.sample(modules, 3)
    for module in shortlisted_modules:
        shortlist = ProjectShortlist(project_id=project.id, module_id=module.id)
        session.add(shortlist)

    session.commit()
    print(f"✓ Added {len(shortlisted_modules)} modules to project shortlist")

    # Create RFQs for 3 vendors (pending, not sent yet)
    sample_vendors = random.sample(vendors, 3)
    for vendor in sample_vendors:
        rfq = RFQ(
            project_id=project.id,
            vendor_id=vendor.id,
            token=str(uuid.uuid4()),
            status='pending',
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        session.add(rfq)

    session.commit()
    print(f"✓ Created {len(sample_vendors)} RFQs")

    print("\n✅ Database seeded successfully!")
    session.close()


if __name__ == "__main__":
    seed_database()
