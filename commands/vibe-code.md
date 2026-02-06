# Vibe-Code: Full Workflow Orchestrator

Run the complete vibe-coding workflow from idea to shipped code. This command orchestrates all phases with built-in quality gates.

## The Process

This workflow runs through these phases:
1. **Capture** → Document the idea/issue
2. **Explore** → Deeply understand the problem
3. **Plan** → Design the solution
4. **Execute** → Build it
5. **Test** → Determine testing strategy
6. **Review** → Self-review the code
7. **Peer Review** → Get Codex's perspective
8. **Document** → Update docs

**You control the flow.** At each phase checkpoint, I'll pause and you can:
- ✅ Continue to next phase
- ⏭️ Skip a phase (if not needed)
- 🔄 Iterate on current phase
- 🛑 Stop here (finish later)

---

## Phase 1: Capture the Issue

**Creating issue document...**

Ask targeted questions to capture:
- What's the feature/bug/improvement
- Current behavior vs desired behavior
- Type (bug/feature/improvement) and priority
- Relevant files/context

**Output:** Create `issues/[slug].md` with:
- Clear title and TL;DR
- Current state vs expected outcome
- Relevant files
- Type/priority/effort labels

📍 **Checkpoint:** Issue documented. Ready to explore?

---

## Phase 2: Exploration

**Deep dive into the problem...**

My job (as CTO):
- Analyze existing codebase thoroughly
- Understand dependencies, structure, constraints
- Identify edge cases and integration points
- Clarify ANY ambiguity before planning

I'll ask questions. We go back-and-forth until:
- All ambiguities are resolved
- I fully understand the architecture
- We agree on the approach

**Output:** Complete understanding of:
- How this integrates with existing code
- Technical constraints and dependencies
- Edge cases to handle
- Clear requirements (no assumptions)

📍 **Checkpoint:** Exploration complete. Ready to plan?

---

## Phase 3: Create Plan

**Designing the solution...**

Based on exploration, I'll create a detailed plan document.

**Output:** Create `plans/[slug].md` with:

```markdown
# Feature Implementation Plan

**Overall Progress:** 0%

## TLDR
[Brief summary of what we're building and why]

## Critical Decisions
- Decision 1: [choice] - [rationale]
- Decision 2: [choice] - [rationale]

## Tasks:

- [ ] 🟥 **Phase 1: [Name]**
  - [ ] 🟥 Subtask 1
  - [ ] 🟥 Subtask 2

- [ ] 🟥 **Phase 2: [Name]**
  - [ ] 🟥 Subtask 1
  - [ ] 🟥 Subtask 2
```

Plan is:
- Minimal and focused (no scope creep)
- Clear, actionable steps
- Progress tracking with emojis (🟥→🟨→🟩)
- Integrates with existing patterns

📍 **Checkpoint:** Plan created. Ready to build?

---

## Phase 4: Execute

**Building the solution...**

Implement according to the plan:
- Follow existing code patterns and conventions
- Write clean, modular, minimal code
- Update plan.md progress as I work (🟥→🟨→🟩)
- Track overall completion percentage

I'll implement each phase sequentially, updating progress in real-time.

**Output:**
- Implemented code
- Updated plan.md with progress
- Clear commit-ready changes

📍 **Checkpoint:** Implementation complete. Ready for testing strategy?

---

## Phase 5: Test Strategy

**Determining what needs testing...**

Analyze what was built and create focused test plan:
- Identify critical paths worth testing
- Suggest appropriate test types (unit/integration/E2E)
- Focus on pragmatic testing (not everything needs tests)
- Provide clear implementation guidance

**Output:** Test plan with:
- Critical/High/Low priority test areas
- Specific test cases for each
- What we're explicitly NOT testing (and why)
- Implementation guide

📍 **Checkpoint:** Test strategy defined. Ready for self-review?

---

## Phase 6: Self-Review

**Reviewing the code...**

Comprehensive review against checklist:
- Logging (proper logger, no console.log)
- Error handling (try-catch, helpful messages)
- TypeScript (no `any`, proper types)
- Production readiness (no TODOs, no debug code)
- Performance (no unnecessary re-renders)
- Security (auth, validation, safe inputs)
- Architecture (follows existing patterns)

**Output:** Structured review with:
- ✅ What looks good
- ⚠️ Issues found (with severity and fixes)
- 📊 Summary of findings

📍 **Checkpoint:** Self-review complete. Ready for peer review?

---

## Phase 7: Peer Review (Codex)

**Getting second opinion from Codex...**

**Step 1:** I'll prepare a review request for Codex
**Step 2:** You copy it to Codex and paste response back
**Step 3:** I'll critically evaluate Codex's findings

For each Codex finding:
- Verify it's a real issue (check actual code)
- Explain if it's not applicable (Codex lacked context)
- Prioritize valid findings
- Create action plan for fixes

**Output:**
- Valid findings (confirmed issues)
- Invalid findings (with explanations)
- Prioritized action plan

📍 **Checkpoint:** Peer review complete. Ready to update docs?

---

## Phase 8: Documentation

**Updating documentation...**

Review changes and update:
- Read actual code (don't trust existing docs)
- Identify what changed
- Update CHANGELOG.md (under "Unreleased")
- Update any affected README or doc files

**Output:**
- Updated CHANGELOG.md
- Accurate documentation matching code
- Concise, practical descriptions

📍 **Checkpoint:** Documentation complete. Ready to commit?

---

## Final Step: Commit

Create a clean commit with:
- All implemented changes
- Updated docs
- Progress tracking files

Commit message will follow convention:
```
type(scope): brief description

Detailed description of what changed and why.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## Usage Tips

**Starting vibe-code:**
Just say: *"/vibe-code [brief description of what you want to build]"*

**During workflow:**
- Each checkpoint lets you pause, skip, or iterate
- You control the pace - take time to review at each phase
- Skip phases that don't apply (e.g., simple changes don't need peer review)

**Flexibility:**
- Not every project needs every phase
- Simple bugs might be: capture → explore → execute → commit
- Complex features should use full workflow

**The goal:** Process over output. Think → Plan → Build → Verify → Ship.

---

## Principles

✅ **Think before building** - Exploration and planning save time
✅ **Multiple quality gates** - Catch issues early
✅ **Documented decisions** - Know why we did what we did
✅ **Pragmatic process** - Skip what doesn't add value
✅ **Ship with confidence** - Reviews + tests + docs = quality

❌ Don't skip exploration for complex features
❌ Don't assume requirements - clarify first
❌ Don't rush to code - planning pays off
❌ Don't skip reviews for critical changes
