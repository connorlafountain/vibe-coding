# POC Vendor Portal Implementation Plan

**Overall Progress:** `0%`

**Deadline:** Tuesday (5 days)

---

## TLDR

Build proof-of-concept vendor portal with three interfaces (Customer, SST Admin, Vendor) using Python/FastAPI + SQLite + Tailwind CSS. Demonstrates structured quote capture to eliminate manual data entry. Gmail for email sending (POC), token-based vendor auth, simple UI. Delivers end-to-end demo-able workflow by Tuesday.

---

## Critical Decisions

**Decision 1: Gmail SMTP for POC, SendGrid for production**
- Rationale: Gmail is faster to set up for demo, but SendGrid is more reliable for production use
- Action: Use smtplib with Gmail app password, document SendGrid migration path

**Decision 2: Token-based vendor authentication (no login)**
- Rationale: Simplifies POC, unique URL per vendor is secure enough for demo
- Action: Generate UUID tokens, 7-day expiry, include in email link

**Decision 3: No admin authentication for demo**
- Rationale: Demo complexity reduction, focus on core workflow
- Action: Admin dashboard accessible without login, add auth in production notes

**Decision 4: Fake but realistic module data (500W-800W)**
- Rationale: Makes demo believable without real data research
- Action: Generate 200 modules with realistic names (SunPower, JinkoSolar, etc.)

**Decision 5: Simple UI with Tailwind CDN**
- Rationale: Faster development, iterate on design later based on SST feedback
- Action: Use Tailwind via CDN, focus on functionality over aesthetics

**Decision 6: Self-contained POC structure**
- Rationale: Easy to archive, handoff to dev team, or iterate on
- Action: Everything in `pocs/001-vendor-portal/` directory

---

## Tasks

### Phase 1: Project Setup & Foundation

- [ ] 🟥 **Create POC directory structure**
  - [ ] 🟥 Create `pocs/001-vendor-portal/` folder
  - [ ] 🟥 Create subdirectories (templates/, static/, mock_data/)
  - [ ] 🟥 Initialize Git in POC directory

- [ ] 🟥 **Set up Python environment**
  - [ ] 🟥 Create requirements.txt (FastAPI, Uvicorn, SQLAlchemy, Jinja2, etc.)
  - [ ] 🟥 Activate venv and install dependencies
  - [ ] 🟥 Test FastAPI "Hello World"

- [ ] 🟥 **Database schema & mock data**
  - [ ] 🟥 Create database.py with SQLAlchemy models
  - [ ] 🟥 Generate 200 fake modules (500W-800W, realistic names)
  - [ ] 🟥 Generate 10 fake vendors (funny/cool names)
  - [ ] 🟥 Create sample project with 3 shortlisted modules
  - [ ] 🟥 Initialize SQLite database with seed data

### Phase 2: Backend Core (FastAPI Routes)

- [ ] 🟥 **Customer interface routes**
  - [ ] 🟥 GET `/customer/ranking` - Display module ranking table
  - [ ] 🟥 POST `/customer/shortlist` - Add module to shortlist
  - [ ] 🟥 GET `/customer/module-details` - Show shortlisted modules
  - [ ] 🟥 POST `/customer/submit-rfq` - Create RFQ, trigger SST notification

- [ ] 🟥 **SST Admin interface routes**
  - [ ] 🟥 GET `/admin/dashboard` - Show all RFQs with status
  - [ ] 🟥 GET `/admin/rfq/<id>` - RFQ detail view
  - [ ] 🟥 POST `/admin/send-bid/<rfq_id>` - Generate token, send email to vendor
  - [ ] 🟥 GET `/admin/quotes` - Quote comparison view across vendors

- [ ] 🟥 **Vendor portal routes**
  - [ ] 🟥 GET `/vendor/<token>` - Vendor portal (validate token, show RFQ)
  - [ ] 🟥 POST `/vendor/<token>/submit` - Submit quote, update status
  - [ ] 🟥 GET `/vendor/<token>/confirmation` - Thank you page

- [ ] 🟥 **API routes (mock Retool)**
  - [ ] 🟥 GET `/api/quotes/<rfq_id>` - Return quotes as JSON
  - [ ] 🟥 Display mock Retool API payload in admin view

### Phase 3: Email Service

- [ ] 🟥 **Gmail SMTP setup**
  - [ ] 🟥 Create email_service.py
  - [ ] 🟥 Configure Gmail app password (user provides)
  - [ ] 🟥 Test email sending to clafountain@anzarenewables.com

- [ ] 🟥 **Email templates**
  - [ ] 🟥 RFQ notification email (to vendor with portal link)
  - [ ] 🟥 Professional HTML email template
  - [ ] 🟥 Include project details, vendor token link
  - [ ] 🟥 7-day expiry notice

### Phase 4: Frontend Templates (Customer Interface)

- [ ] 🟥 **Base template (shared layout)**
  - [ ] 🟥 Create base.html with Tailwind CDN
  - [ ] 🟥 Header, footer, navigation
  - [ ] 🟥 Mobile-responsive layout

- [ ] 🟥 **Customer ranking table**
  - [ ] 🟥 Create customer_ranking.html
  - [ ] 🟥 Display 200 modules in sortable table
  - [ ] 🟥 Checkbox to select modules for shortlist
  - [ ] 🟥 "Add to Shortlist" button
  - [ ] 🟥 Show shortlist count (3 max)

- [ ] 🟥 **Module details page**
  - [ ] 🟥 Create customer_module_details.html
  - [ ] 🟥 Display shortlisted modules (3)
  - [ ] 🟥 Show mock payment terms, contract info
  - [ ] 🟥 "Submit RFQ" button
  - [ ] 🟥 Confirmation modal with process explanation

### Phase 5: Frontend Templates (SST Admin Interface)

- [ ] 🟥 **Admin dashboard**
  - [ ] 🟥 Create sst_admin_dashboard.html
  - [ ] 🟥 Status overview (New, Sent, Received, Requires Review)
  - [ ] 🟥 RFQ list table with filters
  - [ ] 🟥 Vendor POC info display
  - [ ] 🟥 "Send Bid" button for each RFQ

- [ ] 🟥 **Quote comparison view**
  - [ ] 🟥 Create admin_quotes.html
  - [ ] 🟥 Side-by-side vendor quote comparison
  - [ ] 🟥 Highlight best price, delivery date
  - [ ] 🟥 Export to CSV button (download quotes)
  - [ ] 🟥 Show mock Retool API JSON payload

### Phase 6: Frontend Templates (Vendor Portal)

- [ ] 🟥 **Vendor portal landing page**
  - [ ] 🟥 Create vendor_portal.html
  - [ ] 🟥 Display RFQ details (project name, modules)
  - [ ] 🟥 Pre-populate module specs
  - [ ] 🟥 Quote submission form (price, delivery, availability, quantity, payment terms)

- [ ] 🟥 **Form actions & validation**
  - [ ] 🟥 Radio buttons: Confirm | Decline | Counter-offer
  - [ ] 🟥 Client-side validation (required fields)
  - [ ] 🟥 "Counter-offer" enables field modification
  - [ ] 🟥 Submit button with loading state

- [ ] 🟥 **Confirmation page**
  - [ ] 🟥 Thank you message
  - [ ] 🟥 "Your quote has been submitted" confirmation
  - [ ] 🟥 Next steps explanation

### Phase 7: Frontend JavaScript & Interactivity

- [ ] 🟥 **Customer interface JS**
  - [ ] 🟥 Module selection (checkbox logic, 3 max)
  - [ ] 🟥 Shortlist counter
  - [ ] 🟥 Confirmation modal on RFQ submit
  - [ ] 🟥 Form submission with Fetch API

- [ ] 🟥 **Admin interface JS**
  - [ ] 🟥 Status filtering (dropdown)
  - [ ] 🟥 "Send Bid" button with confirmation
  - [ ] 🟥 Quote comparison table sorting
  - [ ] 🟥 CSV export functionality

- [ ] 🟥 **Vendor portal JS**
  - [ ] 🟥 Form validation
  - [ ] 🟥 Enable/disable fields based on action (Confirm/Decline/Counter)
  - [ ] 🟥 Submit with loading spinner
  - [ ] 🟥 Error handling & display

### Phase 8: Styling & UI Polish

- [ ] 🟥 **Tailwind components**
  - [ ] 🟥 Buttons (primary, secondary, danger)
  - [ ] 🟥 Forms (inputs, selects, textareas)
  - [ ] 🟥 Tables (sortable, responsive)
  - [ ] 🟥 Modals (confirmation, alerts)
  - [ ] 🟥 Cards (RFQ cards, quote cards)

- [ ] 🟥 **Responsive design**
  - [ ] 🟥 Mobile-friendly tables (scrollable)
  - [ ] 🟥 Tablet layout adjustments
  - [ ] 🟥 Desktop optimized

- [ ] 🟥 **Visual feedback**
  - [ ] 🟥 Loading spinners
  - [ ] 🟥 Success/error messages
  - [ ] 🟥 Status badges (color-coded)
  - [ ] 🟥 Green highlight for accepted quotes

### Phase 9: Testing & Demo Preparation

- [ ] 🟥 **End-to-end workflow test**
  - [ ] 🟥 Customer: Select modules → Submit RFQ
  - [ ] 🟥 Admin: Review RFQ → Send to vendor
  - [ ] 🟥 Email: Receive email with portal link
  - [ ] 🟥 Vendor: Click link → Submit quote
  - [ ] 🟥 Admin: View quote → See Retool JSON

- [ ] 🟥 **Edge case testing**
  - [ ] 🟥 Expired token (7+ days old)
  - [ ] 🟥 Invalid token
  - [ ] 🟥 Decline quote workflow
  - [ ] 🟥 Counter-offer workflow

- [ ] 🟥 **Demo script preparation**
  - [ ] 🟥 Create step-by-step demo script
  - [ ] 🟥 Prepare talking points for SST
  - [ ] 🟥 Screenshot key screens
  - [ ] 🟥 Record backup video (if demo fails)

### Phase 10: Documentation & Handoff

- [ ] 🟥 **POC README**
  - [ ] 🟥 Project overview
  - [ ] 🟥 How to run locally
  - [ ] 🟥 Tech stack explanation
  - [ ] 🟥 Database schema diagram
  - [ ] 🟥 API routes documentation

- [ ] 🟥 **Production migration notes**
  - [ ] 🟥 SendGrid setup instructions
  - [ ] 🟥 Authentication requirements
  - [ ] 🟥 Database migration to PostgreSQL
  - [ ] 🟥 Deployment considerations
  - [ ] 🟥 Security hardening checklist

- [ ] 🟥 **Developer handoff package**
  - [ ] 🟥 Code comments & docstrings
  - [ ] 🟥 Architecture diagram
  - [ ] 🟥 Future feature suggestions
  - [ ] 🟥 Known limitations & technical debt

---

## Implementation Order (Recommended)

**Day 1 (Today):**
- Phase 1: Project setup
- Phase 2: Backend routes (skeleton)
- Phase 3: Email service setup

**Day 2 (Friday):**
- Phase 4: Customer interface templates
- Phase 5: SST Admin interface templates
- Phase 6: Vendor portal templates

**Day 3 (Saturday):**
- Phase 7: Frontend JavaScript
- Phase 8: Styling & UI polish (basic)

**Day 4 (Sunday):**
- Phase 9: Testing & bug fixes
- Refinements based on testing

**Day 5 (Monday):**
- Phase 10: Documentation
- Demo script preparation
- Final polish

**Day 6 (Tuesday):**
- Demo to SST
- Iterate based on feedback

---

## Technical Specifications

### **File Structure:**
```
pocs/001-vendor-portal/
├── README.md
├── app.py                    # FastAPI main app
├── database.py               # SQLAlchemy models + seed data
├── email_service.py          # Gmail SMTP service
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (Gmail creds)
├── .gitignore                # Ignore .env, *.db
├── vendor_portal.db          # SQLite database (generated)
│
├── templates/
│   ├── base.html                     # Shared layout
│   ├── customer_ranking.html         # Customer: module ranking
│   ├── customer_module_details.html  # Customer: shortlist + RFQ
│   ├── sst_admin_dashboard.html      # Admin: dashboard
│   ├── admin_quotes.html             # Admin: quote comparison
│   ├── vendor_portal.html            # Vendor: quote submission
│   └── vendor_confirmation.html      # Vendor: thank you
│
├── static/
│   ├── css/
│   │   └── custom.css                # Additional custom styles
│   └── js/
│       ├── customer.js               # Customer interface JS
│       ├── admin.js                  # Admin interface JS
│       └── vendor.js                 # Vendor portal JS
│
└── mock_data/
    ├── modules.json          # 200 fake modules
    ├── vendors.json          # 10 fake vendors
    └── seed_database.py      # Script to populate DB
```

### **Dependencies (requirements.txt):**
```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.36
jinja2==3.1.4
pydantic==2.9.2
python-multipart==0.0.12
python-dotenv==1.0.1
```

### **Environment Variables (.env):**
```
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
BASE_URL=http://localhost:8000
```

---

## Mock Data Examples

### **Fake Module (realistic):**
```json
{
  "id": 1,
  "name": "JinkoSolar Tiger Neo 580W",
  "manufacturer": "JinkoSolar",
  "wattage": 580,
  "technology": "Monocrystalline PERC",
  "efficiency": 21.8,
  "dimensions": "2278 x 1134 x 30 mm",
  "price_per_watt": 0.25
}
```

### **Fake Vendor (funny/cool names):**
```json
{
  "id": 1,
  "name": "SolarCo Distributors",
  "contact_name": "Jane Smith",
  "email": "jane@solarco.example",
  "phone": "+1-555-0123"
}
```

**More vendor names:**
- PanelSupply Inc.
- SunHarvest Solutions
- Megawatt Merchants
- GigaWatt Traders
- ElectroSun Wholesale
- BrightPanel Co.
- WattWorks Distribution
- SolarStack Suppliers
- PowerGrid Distributors
- SunChase Logistics

---

## Success Metrics

**For Demo:**
- ✅ Complete end-to-end workflow (Customer → Admin → Vendor → Admin)
- ✅ Real email sent and received
- ✅ Structured data captured
- ✅ Mock Retool API payload displayed
- ✅ Professional UI (not hacky)
- ✅ No critical bugs during demo
- ✅ SST says "yes, build this"

**Performance:**
- All pages load < 1 second
- Email delivery < 30 seconds
- Database queries < 100ms

---

## Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Email spam filter | Medium | High | Test thoroughly, use professional template, send from real Gmail |
| Gmail app password setup complexity | Low | Medium | Provide clear instructions, test early |
| Timeline pressure (5 days) | High | High | Focus on core features, skip polish, work efficiently |
| Demo bugs | Medium | High | Thorough testing on Day 4, backup video recording |
| SST feedback requires major changes | Low | Medium | Build flexibly, document easy pivot points |

---

## Notes

- **Self-contained:** Everything in `pocs/001-vendor-portal/` for easy archiving
- **Demo-focused:** Prioritize working features over perfect code
- **Iterative:** Get feedback from SST, refine before handing off to devs
- **Documentation:** Clear README + migration notes for production
- **Learning:** This POC validates approach, not a production system

---

## Next Steps After Planning

1. **Phase 4: Execute** - Build the POC following this plan
2. **Update progress** - Mark tasks complete (🟥→🟨→🟩) as we work
3. **Track completion %** - Update overall progress at top
4. **Demo Tuesday** - Show SST the working system
5. **Iterate** - Refine based on feedback
6. **Handoff** - Package for Anza developers
