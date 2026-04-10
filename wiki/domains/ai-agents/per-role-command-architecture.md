---
title: "Per-Role Command Architecture"
type: concept
domain: ai-agents
status: synthesized
confidence: medium
created: 2026-04-09
updated: 2026-04-10
layer: 2
maturity: growing
sources:
  - id: src-claude-slash-commands
    type: github-repo
    url: https://github.com/artemgetmann/claude-slash-commands
    file: raw/articles/artemgetmannclaude-slash-commands.md
    title: "Claude Code Slash Commands (artemgetmann)"
    ingested: 2026-04-09
  - id: src-plannotator
    type: github-repo
    url: https://github.com/backnotprop/plannotator
    file: raw/articles/backnotpropplannotator.md
    title: "Plannotator — Interactive Plan & Code Review for AI Agents"
    ingested: 2026-04-09
tags: [slash-commands, per-role, commands, workflow, developer-experience, methodology, skills, hooks, plannotator, automation, execution-modes, ecosystem-sharing]
---

# Per-Role Command Architecture

## Summary

Per-role command architecture is the design principle that different practitioner roles — developer, researcher, PM, operator — need different Claude Code slash-command sets, rather than a single flat list of commands available to everyone. The two-scope install model (personal `~/.claude/commands/` and project `.claude/commands/`) provides the mechanical basis, but the full vision extends to role-specific command libraries, commands that invoke full skills, commands that create hook workflows (the Plannotator pattern), and commands scoped to execution modes (autonomous, semi-autonomous, document-only). The current wiki has 6 commands (/continue, /evolve, /ingest, /review, /gaps, /status) — all researcher-oriented. Formalizing the per-role model would make command proliferation manageable, enable ecosystem sharing, and connect commands structurally to the methodology layers.

## Key Insights

> [!tip] Commands are lightweight triggers; skills are full context
> A `/command` is a markdown file with a prompt. A skill is a full instruction set with prerequisites, scripts, and behavioral guidance. The correct composition: commands invoke skills (`/ingest` triggers the `ingest` skill). This keeps commands minimal and reusable while skills carry the operational knowledge.

> [!abstract] Two installation scopes, one design decision
>
> | Scope | Location | What Goes There |
> |-------|----------|----------------|
> | **Personal** | `~/.claude/commands/` | Role-generic utilities, power-user shortcuts (follow user across projects) |
> | **Project** | `.claude/commands/` | Role-specific workflows, team-shared, version-controlled |

> [!warning] The Plannotator pattern: commands + hooks = structural enforcement
> `/plannotator-annotate` is a command that *activates* a hook-intercepted workflow. The command sets up context; the hook provides the structural pause. Without hooks, the command can only *ask* Claude to pause — which it may or may not do. With hooks, the pause is guaranteed. This generalizes to any command requiring a human approval gate.

**Role segmentation reduces cognitive noise.** A developer doesn't need `/evolve`. A PM doesn't need `/ingest`. Per-role scoping turns the command palette from a discovery problem into a workflow guide. Scoped by (1) install scope, (2) role, (3) execution mode — each user sees 6-8 relevant commands.

**Execution modes map to command sets.** Autonomous: `/status`, `/continue`. Semi-autonomous: `/review`, `/evolve`, `/gaps`. Document-only: `/ingest`, `/scaffold`. Mode switching is partially accomplished by which commands are available.

## Deep Analysis

### Current State: The Wiki's 6 Commands

The research wiki has 6 slash commands in `.claude/commands/`:

| Command | Role | Mode | Invokes Skill |
|---|---|---|---|
| `/continue` | All | Autonomous | `continue` skill |
| `/status` | All | Autonomous | Status chain |
| `/ingest` | Researcher | Semi-autonomous | `ingest` skill |
| `/evolve` | Researcher | Semi-autonomous | `evolve` skill |
| `/gaps` | Researcher | Semi-autonomous | `gaps` chain |
| `/review` | Researcher | Semi-autonomous | `review` skill |

All 6 are researcher-oriented. The wiki has no developer commands (no `/implement`, `/test`, `/commit`) and no PM commands (no `/backlog`, `/sprint`, `/retrospective`). This is appropriate for the current single-role use case but would not scale to the full ecosystem (openfleet, AICP, DSPD, devops-control-plane) where multiple practitioner types interact with shared tooling.

### Role Taxonomy and Command Mapping

A formalized per-role command architecture across the ecosystem would look like:

**Generic (all roles, personal scope `~/.claude/commands/`):**
- `/continue` — Resume mission regardless of role
- `/status` — Show current state
- `/help` — Surface available role-specific commands

**Developer role (project scope):**
- `/implement <feature>` — Enter semi-autonomous implementation mode
- `/test` — Run test suite, report failures with context
- `/commit` — Stage, validate, and commit with conventional message
- `/review-pr <number>` — Pull Plannotator-style code review for a PR
- `/debug` — Systematic debugging mode (superpowers pattern)

**Researcher role (project scope — wiki):**
- `/ingest <url>` — Full ingestion pipeline
- `/evolve` — Score and evolve knowledge
- `/gaps` — Gap analysis with action queue
- `/review` — Weekly health check

**PM/Lead role (project scope):**
- `/backlog` — Show and prioritize open work
- `/sprint` — Plan sprint from backlog
- `/retrospective` — Run retrospective with data
- `/handoff` — Generate handoff documentation

**Operator role (project scope):**
- `/deploy <env>` — Execute deployment with pre-flight checks
- `/rollback` — Rollback with verification
- `/incident` — Incident response mode

### Commands as Hook Workflow Triggers: The Plannotator Pattern

The most sophisticated command design pattern is the command-as-hook-trigger. Plannotator operationalizes this:

```
User invokes: /plannotator-annotate
→ Command sends prompt with annotation context to Claude
→ Claude begins planning a response
→ PreToolUse hook fires (or custom plan-mode hook)
→ Hook opens browser UI, pauses agent loop
→ User annotates the plan
→ Structured feedback returned to agent
→ Agent continues with revision instructions
```

This pattern generalizes to any command requiring a human approval gate:
- `/review` could pause at key decisions and surface them for human input before continuing
- `/evolve` could intercept the promotion decision (seed → growing → mature) with a structured approval UI
- A `/propose-architecture` command could show architecture diagrams before writing any code

The critical insight is that the command is *not* doing the interception — the hook is. The command sets up the context; the hook provides the structural enforcement. Without hooks, the command can only *ask* Claude to pause — which it may or may not do. With hooks, the pause is guaranteed.

### Connecting to Execution Modes

The methodology defines three execution modes:
- **Autonomous**: No human in the loop. Agent runs to completion.
- **Semi-autonomous**: Human checkpoints at phase boundaries.
- **Document-only**: Human reviews and approves every significant action.

Per-role commands should surface mode-appropriate interaction patterns:

| Mode | Commands Surfaced | Hook Behavior |
|---|---|---|
| Autonomous | `/continue`, `/status` | Stop hook validates completion criteria |
| Semi-autonomous | `/review`, `/evolve`, `/gaps` | Plannotator-style hooks at phase gates |
| Document-only | `/ingest`, `/scaffold` | PreToolUse blocks writes pending explicit approval |

A future enhancement: commands could set a session mode variable read by hooks. `/document-mode` activates PreToolUse blocks on write operations; `/autonomous-mode` deactivates approval gates. The mode switch is a command that reconfigures hooks — not a prompting change.

### Ecosystem Sharing: The Distribution Problem

The current community pattern for sharing commands is manual (copy files to `~/.claude/commands/` or `.claude/commands/`). There is no package manager, no versioning, no lockfile. The artemgetmann slash-commands repo addresses this with a GitHub-hosted collection, but discovery is still manual.

A per-role architecture suggests the natural distribution unit: role packages. A "researcher package" installs a set of commands + skills + hook configurations appropriate for research workflows. Installation via a bootstrap command (`/add-command` installs this meta-pattern from artemgetmann). Ecosystem sharing across openfleet, AICP, DSPD would use a shared `~/.claude/commands/shared/` directory with a manifest, pulling updates from a shared commands repo.

The wiki's own `/add-command` equivalent would be `python3 -m tools.pipeline scaffold command <name>` — scaffolding a command template with the correct frontmatter and skill-invocation pattern pre-filled.

### The Frontmatter Contract

Command frontmatter drives configuration:
```yaml
---
description: "Ingest a URL into the wiki"
argument-hint: "<url>"
allowed-tools: Bash, Read, Write
---
```

- `description`: Appears in `/help` listing — should be written for role clarity ("Researcher: ingest source URL") not implementation detail
- `argument-hint`: Surfaces expected argument in command palette
- `allowed-tools`: Capability declaration — minimum permissions for the command to function. Commands with broad `allowed-tools` should be scrutinized; narrow scoping is safer and more transparent

A per-role extension to frontmatter that doesn't exist yet: `roles: [researcher, pm]` — metadata for filtering command palette by active role context. This would require Claude Code platform support but the design principle is clear.

## Open Questions

- How does command name collision resolve when personal and project scopes define the same command? Does project-scope override, or does personal-scope take precedence? The artemgetmann source does not document this behavior.
- Is there a mechanism for commands to declare dependencies on other commands or skills? A `/review` command that requires the `evolve` skill to be installed has an implicit dependency — currently undeclared.
- How should commands be versioned when distributed as part of a role package? If `/ingest` is updated to invoke a newer skill API, old installations break silently. A semver contract for command packages would solve this but does not currently exist.
- Can a command read the current session mode (autonomous/semi-autonomous/document-only) to alter its behavior at runtime? Or does each mode require a separate command variant?
- What is the right granularity for a "role"? Developer/Researcher/PM is obvious. But within Developer: frontend vs. backend vs. infrastructure each need different commands. Should roles be hierarchical (role → sub-role) or flat with tags?
- How to share commands across the 4-project ecosystem without duplicating files? A symlink approach, a shared submodule, or a `~/.claude/commands/ecosystem/` install target populated by a single script?

## Relationships

- BUILDS ON: [[Claude Code Skills]]
- BUILDS ON: Claude Code Slash Commands (artemgetmann)
- EXTENDS: [[Harness Engineering]]
- IMPLEMENTS: [[Hooks Lifecycle Architecture]]
- RELATES TO: [[Plannotator — Interactive Plan & Code Review for AI Agents]]
- RELATES TO: [[Claude Code Best Practices]]
- RELATES TO: [[Task Lifecycle Stage-Gating]]
- FEEDS INTO: [[Skills Architecture Is the Dominant LLM Extension Pattern]]
- FEEDS INTO: [[Wiki Ingestion Pipeline]]

## Backlinks

[[Claude Code Skills]]
[[Claude Code Slash Commands (artemgetmann)]]
[[Harness Engineering]]
[[Hooks Lifecycle Architecture]]
[[Plannotator — Interactive Plan & Code Review for AI Agents]]
[[Claude Code Best Practices]]
[[Task Lifecycle Stage-Gating]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Wiki Ingestion Pipeline]]
[[Model: Skills, Commands, and Hooks]]
