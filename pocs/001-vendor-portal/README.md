# Vendor Portal POC

**Proof of Concept:** Structured quote capture system to eliminate manual data re-entry for Strategic Sourcing Team.

---

## 🎯 What This Is

A working POC that demonstrates:
- Customer interface (module ranking + shortlist)
- SST Admin dashboard (RFQ management)
- Vendor portal (structured quote submission)
- Email notifications (Gmail SMTP)
- Mock Retool API integration

**Goal:** Show SST how structured data capture solves manual re-entry pain points.

---

## 🚀 Quick Start

### Option 1: Easy Way (Recommended)

**Just run the startup script:**

```bash
cd pocs/001-vendor-portal
./run.sh
```

That's it! The script will:
- Activate the Python virtual environment
- Check if database exists (create/seed if needed)
- Start the FastAPI server on http://localhost:8000

**Then open your browser:** http://localhost:8000

**To stop the server:** Press `Ctrl+C`

---

### Option 2: Manual Setup

If you prefer to run commands manually:

**1. Install Dependencies**

```bash
# From project root (vibe-coding/)
source venv/bin/activate
cd pocs/001-vendor-portal
pip install -r requirements.txt
```

**2. Seed Database**

```bash
python database.py
```

This creates `vendor_portal.db` with:
- 200 realistic solar modules (500W-800W)
- 10 fake vendors
- 1 sample project with 3 shortlisted modules
- 3 pending RFQs

**3. Configure Email (Optional)**

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your Gmail credentials:

```
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-digit-app-password
BASE_URL=http://localhost:8000
DEBUG=True
```

**Note:** If you don't configure email, the system will print emails to console instead of sending them.

**4. Run the App**

```bash
python -m uvicorn app:app --reload
```

Visit: **http://localhost:8000**

**To stop the server:** Press `Ctrl+C`

---

## 📋 Features Implemented

### ✅ Customer Interface
- **Module Ranking Table** (`/`) - Browse 200+ solar modules
- **Shortlist Selection** - Select up to 3 modules
- **Module Details Page** (`/customer/module-details`) - Review shortlist + submit RFQ

### ✅ SST Admin Dashboard
- **Dashboard** (`/admin/dashboard`) - View all RFQs and statuses
- **Send Bid** - Email vendors with portal link
- **Quote Comparison** (`/admin/quotes`) - Compare vendor responses
- **Mock Retool API** - Show structured JSON data

### ✅ Vendor Portal
- **Unique Token Access** (`/vendor/<token>`) - Secure vendor-specific link
- **RFQ Details** - See project + module requirements
- **Quote Submission** - Form with price, delivery, payment terms
- **Actions:** Confirm | Decline | Counter-offer
- **Confirmation Page** - Thank you + next steps

### ✅ Email Service
- Gmail SMTP integration
- Professional HTML email template
- Fallback to console printing (if no Gmail configured)

---

## 🗂️ Database Schema

**6 Tables:**
1. `projects` - Solar projects
2. `modules` - Solar module catalog (200 items)
3. `project_shortlist` - Customer selections (max 3)
4. `vendors` - Vendor companies (10 items)
5. `rfqs` - Request for quotes (with unique tokens)
6. `quotes` - Vendor responses

---

## 🧪 Testing the Workflow

### End-to-End Demo:

1. **Customer Flow:**
   - Go to http://localhost:8000
   - Browse modules, add 3 to shortlist
   - Click "Continue to Module Details"
   - Click "Submit RFQ"

2. **Admin Flow:**
   - Go to http://localhost:8000/admin/dashboard
   - See pending RFQs
   - Click "Send Bid" for a vendor
   - Email sent (or printed to console)

3. **Vendor Flow:**
   - Copy vendor portal link from email/console
   - Open link in browser
   - Fill out quote form
   - Submit quote

4. **View Results:**
   - Go to http://localhost:8000/admin/quotes
   - See vendor quotes side-by-side
   - View mock Retool API JSON payload

---

## ✅ POC Status: Core Features Complete!

All core features and templates are now complete. The POC is ready for end-to-end testing.

### ✅ Completed Templates:
- ✅ `customer_ranking.html` - Module ranking table with shortlist
- ✅ `customer_module_details.html` - Shortlist review page
- ✅ `sst_admin_dashboard.html` - Admin dashboard with RFQ management
- ✅ `admin_quotes.html` - Quote comparison with Retool API JSON
- ✅ `vendor_portal.html` - Vendor quote submission form
- ✅ `vendor_confirmation.html` - Thank you confirmation page

### 🎯 Optional Enhancements (Time Permitting):
- Client-side form validation
- Modal dialogs
- Table sorting/filtering
- Loading states
- Better mobile experience

---

## 🎯 Success Criteria

For Tuesday Demo:
- [x] Database seeded with realistic data
- [x] FastAPI backend with all routes
- [x] Email service working
- [x] All templates completed ✨
- [ ] End-to-end workflow tested
- [ ] Demo script prepared

---

## 🚧 Known Limitations (POC)

- No real authentication (demo only)
- SQLite (not production-ready)
- Gmail SMTP (should use SendGrid in production)
- Limited error handling
- Basic form validation
- Mock Retool integration (not real API)
- No mobile optimization

---

## 🔄 Next Steps

1. ✅ ~~Complete remaining templates~~ (DONE!)
2. **Test end-to-end workflow** (Customer → Admin → Vendor → Admin)
3. **Optional: Add basic form validation/UX polish**
4. **Prepare demo script with talking points**
5. **Demo to SST on Tuesday**

---

## 📞 Support

Built with vibe-coding workflow 🚀
