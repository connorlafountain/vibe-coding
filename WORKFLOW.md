# Vibe-Coding Workflow Documentation

**Process over output. Think → Plan → Build → Verify → Ship.**

This is your complete guide to the vibe-coding workflow - a systematic approach to building software with AI assistance that prioritizes thoughtful development over quick hacks.

---

## 🎯 Philosophy

### Core Principles

1. **Think Before Building** - Exploration and planning save more time than they take
2. **Multiple Quality Gates** - Catch issues early through reviews and testing
3. **Documented Decisions** - Future you (and your team) will thank you
4. **Pragmatic Process** - Skip phases that don't add value
5. **Leverage AI Strengths** - Claude for strategy, Codex for patterns

### The Vibe-Coding Mindset

Traditional coding: Idea → Code → Debug → Ship → Regret

Vibe-coding: Idea → Explore → Plan → Execute → Review → Ship → Confidence

**Why it works:**
- Fewer false starts (exploration identifies issues early)
- Better architecture (planning forces thinking)
- Higher quality (multiple review passes)
- Faster iteration (clear plans are easier to follow)

---

## 🛠️ Available Commands

All commands are in the `commands/` directory. Reference them by using their name (e.g., "use the create-issue workflow").

### Quick Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| **vibe-code** | Full workflow orchestrator | Starting any non-trivial feature |
| **create-issue** | Fast issue capture | Mid-flow, need to document idea |
| **explore** | Deep problem analysis | Before planning complex features |
| **create-plan** | Design solution | After exploration, before coding |
| **execute** | Build the solution | When plan is ready |
| **test-strategy** | Determine testing approach | After implementation |
| **review** | Self-review code | Before peer review |
| **peer-review** | Get Codex feedback | For critical/complex changes |
| **document** | Update docs | After changes are complete |
| **cto-project** | Strategic CTO mode | High-level planning, architecture |
| **learning-opportunity** | Deep learning mode | Want to understand concepts |

---

## 📋 Detailed Command Guide

### 🚀 `/vibe-code` - The Full Workflow

**What it does:** Orchestrates the entire development process from idea to shipped code.

**Phases:**
1. Capture → Document the idea
2. Explore → Understand the problem deeply
3. Plan → Design the solution
4. Execute → Build it
5. Test Strategy → Determine what to test
6. Review → Self-review
7. Peer Review → Get Codex's input
8. Document → Update docs

**When to use:**
- Starting any feature that will touch multiple files
- Complex bug fixes that need investigation
- Anything where "just code it" would be risky

**When NOT to use:**
- Simple typo fixes
- One-line changes
- Trivial updates

**Usage:**
```
Use the vibe-code workflow to [brief description of feature]
```

**Example:**
```
Use the vibe-code workflow to add user authentication
```

**Checkpoints:**
At each phase, you can:
- ✅ Continue to next phase
- ⏭️ Skip phase (if not needed)
- 🔄 Iterate on current phase
- 🛑 Stop here (finish later)

---

### 📝 `/create-issue` - Fast Issue Capture

**What it does:** Quickly captures bugs/features/ideas while you're mid-flow.

**Process:**
1. Asks 2-3 targeted questions
2. Searches codebase for context (if helpful)
3. Creates `issues/[slug].md` with complete information

**When to use:**
- You're working and think of something else that needs doing
- Want to capture an idea before forgetting
- Need to document a bug for later

**Output:** `issues/[slug].md` containing:
- Clear title and TL;DR
- Current state vs expected outcome
- Relevant files
- Type/priority/effort labels

**Usage:**
```
Use create-issue workflow - [brief description]
```

---

### 🔍 `/explore` - Deep Problem Analysis

**What it does:** Acts as CTO to deeply understand a problem before planning.

**Process:**
1. Analyzes existing codebase
2. Identifies dependencies, constraints, edge cases
3. Asks clarifying questions
4. Continues until NO ambiguity remains

**When to use:**
- Before planning complex features
- When requirements are unclear
- When integrating with existing code
- When you're not sure of the best approach

**Output:**
- Complete understanding of problem
- Identified edge cases
- Technical constraints
- Clear requirements (no assumptions)

**Usage:**
```
Use explore workflow - [describe the problem]
```

**Key point:** This is NOT implementation. Just exploration and questions.

---

### 📐 `/create-plan` - Design the Solution

**What it does:** Creates executable implementation plan based on exploration.

**Process:**
1. Reviews exploration findings
2. Designs minimal, focused solution
3. Creates `plans/[slug].md` with:
   - TLDR
   - Critical decisions
   - Phased tasks with progress tracking
   - Overall completion percentage

**When to use:**
- After exploration phase
- Before starting implementation
- When you need a roadmap

**Output:** `plans/[slug].md` with:
```markdown
# Feature Implementation Plan

**Overall Progress:** 0%

## TLDR
[What we're building and why]

## Critical Decisions
- Decision 1: [choice] - [rationale]

## Tasks:
- [ ] 🟥 **Phase 1: Setup**
  - [ ] 🟥 Create files
  - [ ] 🟥 Add dependencies
```

**Usage:**
```
Use create-plan workflow based on our exploration
```

---

### ⚡ `/execute` - Build the Solution

**What it does:** Implements the code according to plan.

**Process:**
1. Follows plan.md step-by-step
2. Writes clean, modular code
3. Updates progress (🟥→🟨→🟩)
4. Tracks completion percentage

**When to use:**
- After plan is created and approved
- When you're ready to actually code

**Output:**
- Implemented code
- Updated plan.md with progress
- Commit-ready changes

**Usage:**
```
Use execute workflow - implement according to plans/[slug].md
```

---

### 🧪 `/test-strategy` - Determine Testing Approach

**What it does:** Analyzes code and creates focused, pragmatic test plan.

**Process:**
1. Reviews implemented code
2. Identifies what NEEDS testing (not everything)
3. Suggests test types (unit/integration/E2E)
4. Provides implementation guidance

**When to use:**
- After implementation
- Before shipping critical features
- When you need testing guidance

**Output:**
- Priority-based test plan (Critical/High/Low)
- Specific test cases
- What we're NOT testing (and why)
- Implementation guide

**Usage:**
```
Use test-strategy workflow for [feature/files]
```

**Key principle:** Pragmatic testing - test what matters, skip what doesn't.

---

### ✅ `/review` - Self-Review Code

**What it does:** Comprehensive code review against production checklist.

**Checks:**
- Logging (no console.log)
- Error handling
- TypeScript quality
- Production readiness
- Performance
- Security
- Architecture patterns

**When to use:**
- After implementation
- Before peer review
- Before committing critical changes

**Output:**
- ✅ What looks good
- ⚠️ Issues found (with severity)
- 📊 Summary of findings

**Usage:**
```
Use review workflow for [files/feature]
```

---

### 👥 `/peer-review` - Get Codex Feedback

**What it does:** Gets second opinion from Codex, then critically evaluates it.

**Process:**
1. **Phase 1:** Claude prepares review request for Codex
2. **Phase 2:** You copy to Codex, paste response back
3. **Phase 3:** Claude verifies each finding

**When to use:**
- Critical features (auth, payments, data handling)
- Complex algorithms
- When you want a fresh perspective
- Before shipping important changes

**Output:**
- Valid findings (confirmed issues)
- Invalid findings (with explanations)
- Prioritized action plan

**Usage:**
```
Use peer-review workflow for [feature]
```

**Key point:** Claude doesn't blindly accept Codex's feedback - verifies each finding.

---

### 📚 `/document` - Update Documentation

**What it does:** Updates docs to match actual code implementation.

**Process:**
1. Reviews recent changes
2. **Reads actual code** (doesn't trust existing docs)
3. Updates CHANGELOG.md
4. Updates affected docs

**When to use:**
- After feature completion
- Before committing
- When docs are stale

**Output:**
- Updated CHANGELOG.md (under "Unreleased")
- Accurate docs matching implementation
- Concise, practical descriptions

**Usage:**
```
Use document workflow - update docs for [feature]
```

**Critical rule:** VERIFY code, don't assume. Docs lie, code doesn't.

---

### 🎩 `/cto-project` - Strategic CTO Mode

**What it does:** Acts as technical CTO for high-level planning and architecture.

**Behavior:**
- Pushes back when needed (not a people pleaser)
- Asks clarifying questions instead of guessing
- High-level plans first, then concrete steps
- Identifies risks and tradeoffs

**When to use:**
- Starting new projects
- Major architectural decisions
- When you need strategic thinking
- Evaluating different approaches

**Usage:**
```
Use cto-project mode - [describe what you want to discuss]
```

**Key point:** CTO mode challenges assumptions to ensure success.

---

### 🎓 `/learning-opportunity` - Deep Learning Mode

**What it does:** Teaches concepts at three increasing complexity levels.

**Structure:**
- **Level 1:** Core concept (what and why)
- **Level 2:** How it works (mechanics and tradeoffs)
- **Level 3:** Deep dive (production implications)

**When to use:**
- Want to understand a pattern/concept deeply
- Encountered something new in codebase
- Need to level up your knowledge

**Tone:** Peer-to-peer (not teacher-student), technical but clear.

**Usage:**
```
Use learning-opportunity mode - explain [concept/pattern]
```

---

## 🤝 Claude + Codex Collaboration

### Why Two AI Models?

Different AI models have different strengths. Use both strategically:

**Claude (Sonnet 4.5)** - Strategic thinking, architecture, reviews
- Deep exploration and analysis
- CTO-level decision making
- Critical evaluation of code
- Architectural planning

**Codex** - Code generation, pattern recognition
- Spotting common bugs
- Recognizing anti-patterns
- Code optimization
- Fresh perspective on implementation

### How They Work Together

1. **Claude explores and plans** - Understands the problem deeply
2. **Claude implements** - Writes the code following the plan
3. **Claude self-reviews** - First quality gate
4. **Codex peer-reviews** - Second opinion, different perspective
5. **Claude evaluates Codex feedback** - Critically verifies findings

**The key:** Claude doesn't blindly accept Codex's feedback. Codex has less context, so Claude verifies each finding against actual code.

---

## 🎯 Workflow Examples

### Example 1: Simple Bug Fix

**Scenario:** Fix a typo in validation logic

**Workflow:**
1. Use `create-issue` to document it
2. Skip explore (obvious fix)
3. Skip create-plan (too simple)
4. Make the fix directly
5. Use `review` to check
6. Skip peer-review (trivial change)
7. Commit

**Total time:** ~5 minutes

---

### Example 2: Medium Feature

**Scenario:** Add export to CSV functionality

**Workflow:**
1. Use `create-issue` to capture requirements
2. Use `explore` to understand data structure and format needs
3. Use `create-plan` to design the implementation
4. Use `execute` to build it
5. Use `test-strategy` to plan tests
6. Use `review` to self-check
7. Skip peer-review (straightforward feature)
8. Use `document` to update CHANGELOG
9. Commit

**Total time:** ~1-2 hours

---

### Example 3: Complex Feature

**Scenario:** Add user authentication system

**Workflow:**
1. Use `vibe-code` full workflow
   - Capture: Document auth requirements
   - Explore: Understand security, session management, existing user system
   - Plan: Design auth flow, token management, middleware
   - Execute: Build auth system
   - Test Strategy: Plan comprehensive tests (security critical!)
   - Review: Self-check for security issues
   - Peer Review: Get Codex to spot security vulnerabilities
   - Document: Update README and CHANGELOG
2. Commit with confidence

**Total time:** ~4-8 hours, but shipped with high quality

---

## 📊 Decision Tree: Which Command to Use?

```
Starting work?
├─ Simple/trivial change? → Just do it + commit
├─ Bug/feature idea mid-flow? → create-issue
├─ Need to understand existing code? → explore
├─ Planning complex feature? → explore → create-plan
├─ Ready to build? → execute
├─ Code written, need tests? → test-strategy
├─ Need to review? → review
├─ Critical feature? → review → peer-review
├─ Docs need updating? → document
├─ Strategic decision? → cto-project
├─ Want to learn concept? → learning-opportunity
└─ Full feature workflow? → vibe-code (orchestrates all)
```

---

## 🎨 Best Practices

### Do's ✅

- **Use exploration for complex features** - Save time by thinking first
- **Keep plans minimal** - Scope creep kills momentum
- **Update progress as you go** - Don't batch updates
- **Skip phases that don't add value** - Process should serve you, not vice versa
- **Review critical code** - Auth, payments, data handling
- **Document decisions** - Future you needs context
- **Use Codex for fresh perspective** - Different eyes catch different issues

### Don'ts ❌

- **Don't skip exploration on complex features** - Leads to false starts
- **Don't assume requirements** - Ask questions until clear
- **Don't blindly accept AI suggestions** - Verify findings
- **Don't test everything** - Focus on critical paths
- **Don't create process for process sake** - Stay pragmatic
- **Don't rush to code** - Planning pays off

---

## 📁 File Structure

Your vibe-coding workspace:

```
project/
├── commands/           # Slash command definitions
│   ├── vibe-code.md
│   ├── create-issue.md
│   ├── explore.md
│   ├── create-plan.md
│   ├── execute.md
│   ├── test-strategy.md
│   ├── review.md
│   ├── peer-review.md
│   ├── document.md
│   ├── cto-project.md
│   └── learning-opportunity.md
│
├── issues/            # Captured issues (created by create-issue)
│   ├── auth-bug.md
│   └── csv-export.md
│
├── plans/             # Implementation plans (created by create-plan)
│   ├── auth-system.md
│   └── csv-export.md
│
├── CLAUDE.md          # Project instructions for Claude (auto-loaded)
├── WORKFLOW.md        # This file - your workflow guide
└── CHANGELOG.md       # Updated by document workflow
```

---

## 🚀 Getting Started

### First Time Setup

1. **Read this file** - Understand the workflow
2. **Review commands/** - Familiarize yourself with each command
3. **Try a simple feature** - Use `vibe-code` for something small
4. **Iterate and adapt** - Adjust workflow to your needs

### Your First Vibe-Code Session

```
You: Use the vibe-code workflow to add a dark mode toggle

Claude: Starting vibe-code workflow...

[Phase 1: Capture]
Let me ask a few questions about the dark mode toggle:
1. Where should the toggle be located?
2. Should preference persist across sessions?
3. ...
```

Just start with "Use the vibe-code workflow to [feature]" and Claude will guide you through each phase!

---

## 💡 Tips for Success

1. **Trust the process** - Exploration feels slow but saves time
2. **Be specific** - "Add dark mode" → "Add dark mode toggle in settings that persists"
3. **Use checkpoints** - Pause between phases to review
4. **Skip what doesn't matter** - Not every change needs peer review
5. **Document as you go** - Easier than reconstructing later
6. **Learn from mistakes** - Update commands when AI makes errors
7. **Stay pragmatic** - Process serves the code, not the other way around

---

## 🔄 Continuous Improvement

This workflow should evolve with your needs:

**When Claude consistently makes mistakes:**
1. Ask what prompted that decision
2. Update relevant command file with better instructions
3. Add to CLAUDE.md if it's project-specific

**When a command isn't working:**
- Adjust the template
- Add clarifying instructions
- Remove what doesn't add value

**The workflow belongs to you.** Modify it, streamline it, make it yours.

---

## 📞 Quick Reference

**Starting work:** `Use the vibe-code workflow to [feature]`

**Mid-flow idea:** `Use create-issue workflow - [idea]`

**Need to understand:** `Use explore workflow - [problem]`

**Ready to build:** `Use execute workflow - implement plans/[file].md`

**Review code:** `Use review workflow for [files]`

**Get Codex input:** `Use peer-review workflow for [feature]`

**Update docs:** `Use document workflow - [what changed]`

**Strategic thinking:** `Use cto-project mode - [discussion]`

**Learn concept:** `Use learning-opportunity mode - explain [topic]`

---

## 🎯 Remember

**Process over output.**

The goal isn't to write code fast. The goal is to write code **right**.

- Think before building
- Plan before coding
- Review before shipping
- Document before forgetting

Vibe-coding is about building software thoughtfully, with AI as your strategic partner.

**Now go build something amazing.** 🚀
