# POC Development Command

**Purpose:** Fast, iterative POC development with minimal overhead. Build → Test → Refine.

**When to use:**
- Rapid experimentation needed
- Validating an idea or approach
- Demo/presentation deadline approaching
- Testing feasibility before full build
- Time-boxed exploration (hours/days, not weeks)

**When NOT to use:**
- Production-ready features
- Well-defined requirements (use /vibe-code instead)
- Long-term projects requiring extensive documentation

---

## Phase 1: Quick Capture (2 minutes)

Ask the user these essential questions ONLY:

1. **What problem are you solving?** (1-2 sentences max)
2. **Who is this POC for?** (Demo audience, stakeholders, yourself?)
3. **What's the deadline/timeline?** (Hours? Days? Week?)
4. **What would "success" look like?** (What needs to work to validate the idea?)
5. **Any existing code/data to reference?** (APIs, databases, repos?)

**Output:** Create a simple `pocs/XXX-[name]/README.md` with:
- Problem statement
- Success criteria (3-5 bullet points max)
- Timeline
- Out of scope (what you're NOT building)

---

## Phase 2: Rapid Planning (5 minutes)

**Don't overthink it.** Create a simple mental model:

1. **What's the minimum viable demo?** (Core flow only)
2. **What can you fake/mock?** (Real data? Real auth? Real deployment?)
3. **What tech stack gets you there fastest?** (Use what you know)
4. **What's the riskiest part?** (Build that first)

**Output:** Mental checklist or quick bulleted list in README (NOT a formal plan.md)

Example:
```markdown
## Quick Plan
- [ ] Database schema (mock data OK)
- [ ] Core workflow (happy path only)
- [ ] Basic UI (ugly is fine)
- [ ] One working demo scenario
```

---

## Phase 3: Build Fast (80% of time)

**Principles:**
- ✅ Build the happy path first
- ✅ Hardcode values if it saves time
- ✅ Skip error handling (unless critical)
- ✅ Mock external APIs
- ✅ Copy-paste liberally
- ✅ Ugly code is fine
- ❌ Don't build auth (unless that's the POC)
- ❌ Don't write tests (unless that's the POC)
- ❌ Don't optimize
- ❌ Don't refactor

**Iteration Loop:**
1. Build smallest working piece
2. Show user / test immediately
3. Get feedback
4. Adjust and repeat

**Self-contained structure:**
```
pocs/001-[name]/
  ├── README.md         # What it does, how to run it
  ├── requirements.txt  # If applicable
  ├── run.sh           # One-command startup
  └── [code files]
```

---

## Phase 4: Quick Demo Prep (10% of time)

**Before showing to others:**
- [ ] Add a "Quick Start" section to README
- [ ] Test the run.sh / startup process
- [ ] Prepare 1-2 sentences explaining what it does
- [ ] Screenshot the working state (optional)
- [ ] Note what's NOT implemented (set expectations)

**Don't:**
- Write extensive documentation
- Create formal presentations
- Deploy to production environments
- Refactor working code

---

## Phase 5: Iterate or Graduate

**After showing the POC, you have 3 options:**

### Option A: Iterate
- Feedback says "close but needs X"
- Add quick improvements
- Re-demo

### Option B: Graduate to Full Project
- POC validated the approach
- Time to build it properly
- Use `/vibe-code` for full workflow
- Archive POC for reference

### Option C: Archive
- POC proved idea won't work
- Lessons learned documented in README
- Move POC to `pocs/archive/`
- Start fresh with new approach

---

## Key Differences from /vibe-code

| Aspect | POC | Vibe-Code |
|--------|-----|-----------|
| **Planning** | 5 min, informal | 30+ min, detailed plan.md |
| **Documentation** | README only | Full docs, CHANGELOG |
| **Testing** | Manual only | Test strategy required |
| **Code Quality** | Quick & dirty OK | Clean, maintainable |
| **Review** | Show stakeholders | Self-review + peer review |
| **Timeline** | Hours to days | Days to weeks |
| **Goal** | Prove feasibility | Ship production code |

---

## Example POC Session

**User:** "I want to test if we can scrape competitor pricing daily"

**You (Capture):**
- Problem: Manual price checks taking too long
- Success: Script runs daily, emails price changes
- Timeline: Need demo by Friday (3 days)
- Out of scope: UI, authentication, production deployment

**You (Plan):**
```
Quick Plan:
- [ ] Find Python scraping library (BeautifulSoup)
- [ ] Scrape 3 competitor sites (hardcoded URLs)
- [ ] Store in CSV (no database)
- [ ] Email via Gmail SMTP (test email only)
- [ ] Cron job for scheduling (document, don't automate for POC)
```

**You (Build):**
- Day 1: Scraping script for 1 site, prints to console
- Day 2: Add 2 more sites, write to CSV, basic email
- Day 3: Polish output format, test end-to-end

**You (Demo):**
- Show CSV with prices
- Show email received
- Explain: "In production, this would run via cron and handle errors"

**Outcome:** Stakeholder approves → Graduate to /vibe-code for production version

---

## Tips for Effective POCs

1. **Timebox ruthlessly** - If something takes >2 hours, mock it
2. **Communicate constraints** - "This POC doesn't handle X because Y"
3. **Show early and often** - Don't wait for perfection
4. **Document decisions** - Why you chose approach A over B (in README)
5. **Embrace throwaway code** - POCs are meant to be rewritten
6. **Focus on the "magic moment"** - What's the one thing that proves this works?

---

## Ready to Start Your POC?

**Let's go!** I'll ask you the 5 quick questions from Phase 1, then we'll build fast.

What problem are you trying to solve with this POC?
