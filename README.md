# Vibe-Coding

> Process-driven development with AI. Think → Plan → Build → Verify → Ship.

A systematic workflow for building software with Claude and Codex that prioritizes thoughtful development over quick hacks. This is an experimental rapid-experimentation space - if successful, it becomes a reusable process for future projects.

---

## What is Vibe-Coding?

**Vibe-coding** is a development methodology that uses structured phases with built-in quality gates to ship better code faster. Instead of jumping straight to implementation, you explore the problem, plan the solution, execute with confidence, and review thoroughly.

**Core philosophy:** Process over output. Multiple quality gates catch issues early. Documented decisions prevent forgotten context. AI assistants (Claude for strategy, Codex for patterns) complement each other.

**Current status:** Solo experimental project. If this process proves valuable, it scales to team collaboration.

---

## Getting Started

### Prerequisites

Before diving in, you'll need:

- **[Claude Code](https://docs.anthropic.com/claude/docs/claude-code)** - VSCode extension or CLI for Claude integration
- **Codex Access** - Via [GitHub Copilot](https://github.com/features/copilot) or [OpenAI API](https://platform.openai.com/)
- **Git/GitHub** - For version control
- **Basic markdown knowledge** - Workflows use markdown for documentation

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/vibe-coding.git
   cd vibe-coding
   ```

2. Open in your editor (VSCode recommended)

3. Read [WORKFLOW.md](WORKFLOW.md) to understand available commands

4. You're ready to vibe-code!

---

## How to Use

### Quick Start

**First time?** Start simple:

1. **Try `/create-issue`** - Practice capturing an idea fast
   ```
   Use create-issue workflow - add a .gitignore rule for .DS_Store
   ```

2. **Try `/vibe-code`** on something small - Run the full workflow
   ```
   Use the vibe-code workflow to add a CHANGELOG.md file
   ```

3. **Read [WORKFLOW.md](WORKFLOW.md)** - Comprehensive guide to all commands

### Example Session

```
You: Use the vibe-code workflow to add user authentication

Claude: Starting vibe-code workflow...

[Phase 1: Capture]
Let me ask a few questions about authentication:
1. What auth method? (JWT, sessions, OAuth)
2. Where should login UI live?
...

[Then proceeds through: Explore → Plan → Execute → Review → Ship]
```

---

## Commands Overview

These workflows guide development phases:

| Command | Purpose |
|---------|---------|
| **vibe-code** | Full workflow orchestrator - use for any non-trivial feature |
| **create-issue** | Fast issue capture while mid-flow |
| **explore** | Deep problem analysis before planning |
| **create-plan** | Design solution with progress tracking |
| **execute** | Build according to plan |
| **test-strategy** | Determine what needs testing (pragmatic, not exhaustive) |
| **review** | Self-review against production checklist |
| **peer-review** | Get Codex feedback, critically evaluate findings |
| **document** | Update docs to match actual code |
| **cto-project** | Strategic CTO mode for architecture decisions |
| **learning-opportunity** | Deep dive learning mode (3 complexity levels) |

**See [WORKFLOW.md](WORKFLOW.md) for detailed documentation of each command.**

---

## Project Structure

```
vibe-coding/
├── commands/           # Workflow command definitions
│   ├── vibe-code.md   # Full workflow orchestrator
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
│   └── *.md
│
├── plans/             # Implementation plans (created by create-plan)
│   └── *.md
│
├── CLAUDE.md          # AI behavior instructions (auto-loaded by Claude)
├── WORKFLOW.md        # Comprehensive workflow documentation
├── README.md          # You are here
└── .vscode/           # VSCode settings (Claude CLI path, etc.)
```

---

## What's Inside

**[WORKFLOW.md](WORKFLOW.md)** - Your comprehensive guide (650 lines)
- Philosophy and principles
- Detailed guide for each command
- Real workflow examples
- Decision trees and best practices
- Claude + Codex collaboration strategy

**[CLAUDE.md](CLAUDE.md)** - Instructions for Claude
- Project-specific AI behavior
- Development principles
- Automatically loaded in every conversation

**[commands/](commands/)** - Individual workflow definitions
- Each command is a markdown template
- Defines AI behavior for that phase
- Customizable to your preferences

**issues/** and **plans/** - Created by workflows
- `issues/` - Captured requirements and bugs
- `plans/` - Implementation plans with progress tracking

---

## Key Concepts

**The Workflow Phases:**
1. **Capture** - Document the idea/requirement
2. **Explore** - Deeply understand the problem (no implementation yet!)
3. **Plan** - Design the solution with clear steps
4. **Execute** - Build it according to plan
5. **Test** - Determine pragmatic testing strategy
6. **Review** - Self-review against checklist
7. **Peer Review** - Get Codex's perspective, verify findings
8. **Document** - Update docs to match reality

**Quality Gates:**
- Multiple review passes catch issues early
- Exploration prevents false starts
- Planning forces architectural thinking
- Testing focuses on critical paths

**Claude + Codex Collaboration:**
- **Claude** → Strategic thinking, architecture, critical evaluation
- **Codex** → Code patterns, bug spotting, fresh perspective
- Together → Higher quality output

---

## Next Steps

**Ready to try?**

1. Start with something simple: `Use create-issue workflow - [your idea]`
2. Run a full workflow: `Use the vibe-code workflow to [small feature]`
3. Deep dive: Read [WORKFLOW.md](WORKFLOW.md) for comprehensive guide

**Questions?** The workflow documentation has examples, decision trees, and best practices.

---

*Built with Claude + Codex. Process over output.*
