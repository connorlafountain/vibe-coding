# POC: Vendor Portal for Structured Quote Submission

**Type:** Feature / POC
**Priority:** High
**Effort:** Large
**Status:** To Do
**Deadline:** Tuesday (5 days)

---

## TL;DR

Build proof-of-concept vendor portal that captures structured quote data, eliminating manual re-entry burden for SST (Strategic Sourcing Team). Demonstrates end-to-end workflow: Customer shortlists modules → SST sends RFQs → Vendors submit structured quotes via portal → Data auto-populates into Retool API.

**Goal:** Show SST a working demo to validate approach before handing off to Anza developers.

---

## Current State (The Problem)

**Top 3 pain points from SST feedback:**
1. Module-level quote data manually re-entered into Retool (avg priority: 3)
2. Project-based quote data requires extensive manual entry (avg priority: 3.5)
3. Holistic quote data manually extracted from emails (avg priority: 5.5)

**Root cause:** Supplier quotes arrive unstructured (email, PDF, text) forcing manual data entry into multiple systems (Retool, spreadsheets).

**Current workflow:**
1. Customer creates module shortlist
2. SST manually emails vendors
3. Vendors respond via unstructured email
4. SST manually copies data into Retool + spreadsheets
5. Data is fragmented, error-prone, time-consuming

---

## Desired Outcome (The Solution)

**POC Vendor Portal** that captures structured data at the source.

**New workflow:**
1. Customer selects modules from ranking table → shortlists 3 modules
2. Customer submits RFQ from module details page
3. SST reviews in admin dashboard → clicks "Send Bid" button
4. Vendor receives email with link to portal
5. Vendor logs in, sees RFQ details, submits structured quote
6. Data auto-populates into mock Retool API
7. SST sees comparison view of quotes
8. Customer sees green highlight on accepted modules

**Key improvement:** Structured data capture eliminates manual re-entry (solves all 3 pain points).

---

## Scope: Three Interfaces

### **1. Customer Interface**
- **Ranking table page** - View ~200 modules, select 3 to shortlist
- **Module details page** - Shows shortlisted modules + payment terms/contract info
- **Submit RFQ button** - Triggers RFQ creation
- **Confirmation modal** - "Thank you, you'll be notified when quotes are reviewed. Accepted bids will show with green highlight."

### **2. SST Admin Dashboard**
- **Bid status overview** - Track all RFQs (New, Submitted, Ask Received, Requires Review)
- **Vendor POC info** - See who will receive email
- **"Send Bid" button** - Initiates email to vendor with portal link
- **Quote comparison view** - See all vendor responses side-by-side
- **Detailed info** - All relevant data for decision-making

### **3. Vendor Portal**
- **Email link** - Vendor clicks, lands on RFQ page
- **RFQ details view** - Project name, shortlisted modules (already populated)
- **Quote submission form** - Fields:
  - Module (pre-populated, can modify)
  - Price
  - Delivery date
  - Availability
  - Target quantity
  - Payment terms/schedule
- **Actions:** Confirm | Decline | Counter-offer (modify any field)
- **Submit** - Sends structured data to system
- **Confirmation** - "Thank you, your quote has been submitted"

---

## Data Fields to Capture

**From Customer shortlist:**
- Project name
- 3 modules (from ranking table of ~200 modules)

**From Vendor quote:**
- Module (can be modified)
- Price
- Delivery date
- Availability
- Target quantity
- Payment terms/schedule

**Mock Retool API payload (JSON):**
```json
{
  "project_id": "proj_123",
  "vendor_id": "vendor_456",
  "quote_date": "2026-02-06",
  "modules": [
    {
      "module_id": "mod_789",
      "module_name": "SolarPanel XYZ-500W",
      "price": 0.28,
      "delivery_date": "2026-04-15",
      "availability": "In Stock",
      "target_quantity": 1000,
      "payment_terms": "30% deposit, 70% on delivery"
    }
  ]
}
```

---

## Technical Requirements

### **Tech Stack**
- **Backend:** Python + FastAPI
- **Frontend:** HTML + Tailwind CSS + Vanilla JS
- **Database:** SQLite (local, no setup)
- **Email:** Real email sending to clafountain@anzarenewables.com
- **Structure:** Self-contained in `pocs/001-vendor-portal/`

### **Mock Data Needed**
- 200 fake modules (for ranking table)
- 10 fake vendors with cool/funny names (SolarCo, PanelSupply, etc.)
- 1 sample project
- Mock Retool API responses

### **Integrations (Mocked)**
- Retool API (show JSON payload that would be sent)
- Email sending (real, to test email)

---

## User Flow Diagrams

### **Customer Flow:**
```
Ranking Table (200 modules)
  → Select 3 modules to shortlist
  → Module Details Page (payment terms, contracts)
  → Click "Submit RFQ"
  → Confirmation Modal
  → Wait for notification
  → See green highlight on accepted modules
```

### **SST Admin Flow:**
```
Admin Dashboard (see all RFQs)
  → Review new RFQ
  → Click "Send Bid" button
  → Email sent to vendor
  → Wait for vendor response
  → See quote in comparison view
  → Review and accept/reject
```

### **Vendor Flow:**
```
Receive email
  → Click portal link
  → See RFQ details (pre-populated)
  → Fill quote form (price, delivery, terms)
  → Choose: Confirm | Decline | Counter-offer
  → Submit
  → See confirmation
```

---

## Success Criteria

### **For Demo (Tuesday):**
- ✅ End-to-end workflow works locally
- ✅ Customer can shortlist modules and submit RFQ
- ✅ SST admin can send bid to vendor
- ✅ Real email sent to clafountain@anzarenewables.com
- ✅ Vendor can submit structured quote via portal
- ✅ Mock Retool API payload displayed (showing structured data)
- ✅ SST admin can see comparison view
- ✅ Professional UI (looks real, not hacky)

### **What SST Needs to See:**
- "This solves our manual data entry problem"
- "Vendors will actually use this"
- "Data is structured and ready for Retool"
- "We can scale this to 100+ vendors"

---

## Out of Scope (Not in POC)

- ❌ Real authentication (just demo login)
- ❌ Actual Retool integration (mock it)
- ❌ Real vendor user management
- ❌ Payment processing
- ❌ Mobile optimization
- ❌ Production deployment
- ❌ Full ranking table (just mock ~10 modules visible)
- ❌ Historical quote tracking
- ❌ Advanced filtering/search

---

## File Structure

```
pocs/001-vendor-portal/
├── README.md                 # POC documentation
├── app.py                    # FastAPI backend
├── database.py               # SQLite setup + mock data
├── email_service.py          # Email sending logic
├── requirements.txt          # Python dependencies
├── templates/
│   ├── customer_ranking.html      # Customer: ranking table
│   ├── customer_module_details.html  # Customer: module details
│   ├── sst_admin_dashboard.html   # SST: admin dashboard
│   ├── vendor_portal.html         # Vendor: quote submission
│   └── base.html                  # Shared layout
├── static/
│   ├── css/
│   │   └── styles.css             # Custom styles
│   └── js/
│       └── app.js                 # Frontend interactions
└── mock_data/
    ├── modules.json               # 200 fake modules
    ├── vendors.json               # 10 fake vendors
    └── projects.json              # Sample project
```

---

## Risks & Considerations

**Technical:**
- Email deliverability (spam filters?)
- SQLite sufficient for demo (yes, for POC)
- FastAPI learning curve (minimal, good docs)

**UX:**
- Vendor adoption (will they use portal vs email?)
- SST workflow disruption (changes their process)
- Customer confusion (new UI to learn)

**Timeline:**
- 5 days to build (achievable but tight)
- Need to prioritize MVP features
- Can't be perfect, needs to be functional

---

## Notes

- This POC proves the **concept**, not a production system
- Focus on **demo-ability** over robustness
- SST will provide feedback, then hand off to Anza devs
- Self-contained folder structure allows easy archiving/handoff
- Real email sending makes demo more impressive

---

## Next Steps (After This Issue)

1. **Phase 2: Explore** - Analyze tech stack, understand FastAPI + email setup
2. **Phase 3: Create Plan** - Break down into phases, estimate effort
3. **Phase 4: Execute** - Build the POC
4. **Phase 5: Test** - Demo to SST
5. **Phase 6: Iterate** - Refine based on feedback
6. **Phase 7: Handoff** - Document for Anza developers
