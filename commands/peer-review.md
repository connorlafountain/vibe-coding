# Peer Review (Claude + Codex)

Get a second opinion from Codex. Use different AI strengths: Claude (architecture, strategic thinking) + Codex (code patterns, common pitfalls).

## Phase 1: Prepare Review Request

**Claude's job:** Create a review request for Codex with necessary context.

### Generate this output:

```
=== CODEX REVIEW REQUEST ===

Hi Codex! Please review the following code implementation.

**What was built:**
[Brief description of the feature/changes]

**Files changed:**
[List of modified files with key changes]

**Code to review:**
[Include relevant code snippets - keep focused, not entire files]

**What to look for:**
- Common bugs or anti-patterns
- Performance issues
- Security concerns
- Edge cases we might have missed
- Better approaches or patterns

Please provide specific, actionable feedback with file names and line numbers where relevant.
===========================
```

**User:** Copy this review request to Codex (GitHub Copilot, OpenAI Playground, etc.) and paste Codex's response back here.

---

## Phase 2: Critical Evaluation

**Once you receive Codex's feedback, paste it below:**

---

[PASTE CODEX FEEDBACK HERE]

---

## Phase 3: Verification & Action Plan

**Claude's job:** Critically evaluate each finding from Codex.

Important context:
- **Codex has less context** on this project's history and decisions
- **You are the technical lead** - don't accept findings at face value
- Your job is to verify each finding against actual code

For EACH finding:

1. **Verify it exists** - Check the actual code. Is this issue real?
2. **If it doesn't exist** - Explain why (maybe already handled, or Codex misunderstood)
3. **If it does exist** - Assess severity and priority

### Output Format:

**✅ Valid Findings (Confirmed Issues)**
- **[Severity]** [File:line] - [Issue]
  - Codex concern: [What they said]
  - Verification: [Confirmed - here's why it's a real issue]
  - Fix priority: [Critical/High/Medium/Low]
  - Action: [What we'll do about it]

**❌ Invalid Findings (Not Applicable)**
- [File:line] - [Codex concern]
  - Why it's not an issue: [Clear explanation]
  - What Codex missed: [Context they didn't have]

**📊 Summary**
- Valid findings: X
- Invalid findings: X
- Critical issues to fix: X
- High priority: X
- Medium priority: X

**🎯 Action Plan**
1. [Fix for critical issue 1]
2. [Fix for critical issue 2]
3. [Fix for high priority issue 1]

---

## Automation Ideas (Future)

When we're ready to automate this:
- Auto-generate review request from git diff
- API integration with Codex (if available)
- Auto-verification of common patterns
- One-command review workflow