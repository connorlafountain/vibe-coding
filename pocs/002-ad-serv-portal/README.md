# Advisory Services Portal POC

**Purpose:** Provide visibility into project status and milestones for Advisory Services customers and internal Anza team.

**Problem Solved:** Currently, Advisory Services customers have no centralized portal to track their battery storage projects. All communication is manual, data visualizations are one-off images, and there's no way to see engineering milestones, testing progress, or documentation in one place.

**This POC demonstrates:** A customer portal where clients can log in to see their projects, track milestone progress with visual timelines, and view project status at a glance.

---

## What It Does

✅ **Customer Portal** - Clients see all their projects with status, location, capacity, and progress
✅ **Project Detail View** - Visual milestone timeline with completion tracking
✅ **Visual Status System** - Color-coded badges for project and milestone status
✅ **Progress Tracking** - Percentage complete based on milestone completion
✅ **Admin Dashboard** - Internal view of all customers and projects across the portfolio
✅ **Mock Data** - 3 customers, 6 projects, 42 milestones demonstrating real scenarios

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Portal

```bash
./run.sh
```

This will:
- Initialize the database
- Seed mock data (3 customers, 6 projects)
- Start the web server at `http://localhost:8000`

---

## Portal Access URLs

### Customer Portals (Demo)
- **Acme Solar Inc:** http://localhost:8000/customer/acme-solar-2024
  - 2 projects: Maple Street (complete), Riverside (testing)

- **GreenTech Energy:** http://localhost:8000/customer/greentech-energy-2024
  - 2 projects: Solar Ridge (in progress), Valley View (planning)

- **PowerGrid Solutions:** http://localhost:8000/customer/powergrid-2024
  - 2 projects: Coastal Storage (testing with blocked milestone), Mountain Peak (in progress)

### Internal Access
- **Admin Dashboard:** http://localhost:8000/admin/dashboard
  - View all customers and projects
  - Monitor progress across the portfolio
  - Quick links to customer portals

---

## Features

### Customer Portal View
- **Project List** - All projects with status badges and progress bars
- **Quick Stats** - Total projects, active, completed, planning counts
- **Project Cards** - Location, capacity, expected completion date
- **Progress Tracking** - Visual percentage and milestone counts

### Project Detail View
- **Project Overview** - Name, description, location, capacity, dates
- **Overall Progress** - Large progress bar showing % complete
- **Milestone Timeline** - Visual timeline with:
  - Status indicators (complete, in progress, blocked, not started)
  - Category badges (engineering, testing, procurement, construction)
  - Due dates and completion dates
  - Notes and details
- **Milestones by Category** - Summary view grouped by category

### Admin Dashboard
- **Portfolio Stats** - Total customers, projects, status breakdown
- **All Projects Table** - Sortable view with customer, location, status, progress
- **Customer List** - All customers with project counts and portal links

---

## Project Statuses

| Status | Color | Meaning |
|--------|-------|---------|
| **Planning** | Gray | Project in initial planning phase |
| **In Progress** | Blue | Active development/construction |
| **Testing** | Purple | IHI commissioning or validation testing |
| **Complete** | Green | Project successfully completed |
| **Blocked** | Red | Issue preventing progress |

---

## Milestone Categories

- **Engineering** - Design reviews, site surveys, technical work
- **Testing** - IHI commissioning tests, temperature/humidity validation
- **Procurement** - Equipment ordering and delivery
- **Construction** - Installation and build work

---

## Mock Data Overview

### Customers
1. **Acme Solar Inc** (Boston-focused)
2. **GreenTech Energy** (Texas/Colorado)
3. **PowerGrid Solutions** (California/Utah)

### Projects Showcase Different States
- **Complete:** Maple Street (all milestones done)
- **Testing:** Riverside (commissioning in progress)
- **Testing with Blocker:** Coastal Storage (awaiting HVAC sensors)
- **In Progress:** Solar Ridge (design review underway)
- **In Progress:** Mountain Peak (procurement phase)
- **Planning:** Valley View (not yet started)

---

## Success Criteria Checklist

- [x] Customer can see their projects with status
- [x] Project detail shows milestone timeline
- [x] Visual status indicators work (colors, badges)
- [x] Dates are visible and make sense
- [x] Mock data looks realistic
- [x] Internal admin can see all customer projects
- [x] Progress percentage calculates correctly
- [x] Milestones grouped by category
- [x] Status badges color-coded appropriately
- [x] Responsive design (mobile-friendly)

---

## Out of Scope (Future Enhancements)

These features are **not** in the POC but would be important for production:

1. **File Upload & Plot Generation**
   - Integrate IHI plotting scripts (uploaded to `inputs/`)
   - Upload Excel test files
   - Generate and display plots inline

2. **Document Management**
   - Upload/download project documents
   - Version tracking
   - File categorization

3. **Authentication**
   - Real login system (email/password)
   - Role-based permissions
   - Multi-factor authentication

4. **Notifications**
   - Email alerts when milestones complete
   - Status change notifications
   - Weekly summaries

5. **Real-time Updates**
   - WebSocket integration
   - Live milestone updates

6. **Analytics**
   - Project performance metrics
   - Timeline adherence tracking

---

## Technical Stack

- **Backend:** FastAPI (Python web framework)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** Jinja2 templates + Tailwind CSS (via CDN)
- **Data:** Mock data seeded via `database.py`

---

## File Structure

```
pocs/002-ad-serv-portal/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── run.sh                     # One-command startup
├── database.py                # SQLAlchemy models + seed data
├── app.py                     # FastAPI routes
├── templates/
│   ├── base.html             # Base template with Tailwind
│   ├── home.html             # Portal access links
│   ├── customer_portal.html  # Customer project list
│   ├── project_detail.html   # Milestone timeline view
│   └── admin_dashboard.html  # Internal admin view
├── static/                    # (empty - using Tailwind CDN)
└── inputs/                    # IHI plotting scripts (future phase)
    ├── IHI Commissioning Plot Script/
    └── IHI Temperature and Humidity Plot Script/
```

---

## Development Notes

### Database Schema
- **Customer** - name, contact info, portal_token
- **Project** - name, status, dates, location, capacity
- **Milestone** - name, category, status, dates, notes, order

### Authentication
- Simple portal token authentication (like vendor-portal POC)
- No passwords in POC - just unique URLs per customer
- Production would need real auth

### Data Relationships
- One customer has many projects
- One project has many milestones
- Milestones ordered by `order` field

---

## Testing the POC

1. **Start the server:** `./run.sh`
2. **Visit home page:** http://localhost:8000
3. **Click a customer portal** (e.g., Acme Solar)
4. **View project list** - check progress bars and stats
5. **Click "View Details"** on a project
6. **Verify milestone timeline** - status colors, dates, notes
7. **Visit Admin Dashboard** - see all projects across all customers
8. **Navigate between portals** using links

---

## Next Steps (If Graduating to Full Build)

1. Use `/vibe-code` workflow for production implementation
2. Add real authentication system
3. Integrate IHI plotting scripts for data visualization
4. Build document management system
5. Add email notification system
6. Create customer onboarding flow
7. Deploy to production environment
8. Set up monitoring and analytics

---

## POC Lessons Learned

✅ **Works Well:**
- Simple portal token auth is sufficient for POC
- Visual status system makes progress obvious at a glance
- Mock data demonstrates real-world scenarios effectively
- Admin + customer views solve both internal and external visibility

📝 **For Production:**
- Need real-time updates when milestones change
- File upload/download is critical (not just viewing)
- Email notifications would reduce manual communication overhead
- Analytics on timeline adherence would be valuable

---

**Built with:** POC workflow (rapid iteration, mock data, minimal overhead)
**Next Phase:** Graduate to `/vibe-code` for production-ready implementation
