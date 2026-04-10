---
title: "Model: Skills, Commands, and Hooks"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-10
sources:
  - id: src-shanraisshan-claude-code-best-practice
    type: documentation
    url: "https://github.com/shanraisshan/claude-code-best-practice"
    title: "shanraisshan/claude-code-best-practice"
  - id: src-claude-code-hooks-reference
    type: documentation
    url: "https://code.claude.com/docs/en/hooks"
    title: "Claude Code Hooks Reference — Full Research"
  - id: src-claude-slash-commands
    type: github-repo
    url: "https://github.com/artemgetmann/claude-slash-commands"
    title: "Claude Code Slash Commands (artemgetmann)"
  - id: src-plannotator
    type: github-repo
    url: "https://github.com/backnotprop/plannotator"
    title: "Plannotator — Interactive Plan & Code Review for AI Agents"
  - id: src-kepano-obsidian-skills
    type: documentation
    url: "https://github.com/kepano/obsidian-skills"
    title: "kepano/obsidian-skills"
  - id: src-awesome-design-md
    type: documentation
    url: "https://github.com/VoltAgent/awesome-design-md"
    title: "VoltAgent/awesome-design-md — 58 Design Systems"
tags: [skills, commands, hooks, model-definition, ai-agent-extension, per-role, plannotator, design-md, context-loading, lifecycle, harness-engineering, spine]
---

# Model: Skills, Commands, and Hooks

## Summary

The AI agent extension ecosystem is a four-level hierarchy: CLAUDE.md (always loaded, static instructions) at the base, Skills (on-demand, dynamic instruction sets) as the primary extension mechanism, Hooks (lifecycle event handlers, structural enforcement) as the control plane, and Commands (lightweight slash-command triggers) as the user-facing entry point. These levels are not independent features — they compose into a coordinated system where commands invoke skills, hooks enforce invariants that skills alone cannot guarantee, and configuration files provide the static context governing everything. ==The central design principle is context-aware loading: static context enters at startup, dynamic context enters on invocation, and the cost difference between eager and deferred loading is up to 12x.==

## Key Insights

- **Four levels, not three.** CLAUDE.md is the zeroth level — always loaded, never optional, defining project identity before any extension fires. Skills, commands, and hooks build on top of this static foundation.

- **Loading cost is the governing constraint.** CLAUDE.md loads once and stays. Skills load on invocation and can fork. Hooks fire at boundaries with near-zero context cost. Commands are effectively free. This cost gradient determines correct placement.

- **Hooks close the compliance gap.** Instruction files achieve ~60% compliance under context pressure. Hooks achieve ~98% because they operate at the infrastructure level. This is the fundamental reason hooks exist alongside skills — they enforce what skills can only request.

- **The Plannotator pattern generalizes.** A command triggers a workflow; a hook intercepts and enforces structural gates within that workflow. This command+hook composition is the correct architecture for any interactive approval workflow.

- **Skill specification determines portability.** The agentskills.io SKILL.md format works across Claude Code, Codex CLI, OpenCode, Cursor, and any system-prompt-configurable agent. Format choice is a one-time decision with compounding distribution gains.

## Deep Analysis

### Level 0: The Configuration File Ecosystem

> [!info] **Five static config files form the foundation**
> | File | Purpose | Loaded when | Who reads it |
> |------|---------|-------------|-------------|
> | **CLAUDE.md** | Project instructions, constraints, commands | Every message | Every session |
> | **DESIGN.md** | Visual design system — colors, typography, components | Every message | UI generation tasks |
> | **AGENTS.md** | Multi-agent topology — roles, handoffs | Every message | Multi-agent orchestration |
> | **SOUL.md** | Personality, tone, communication style | Every message | All response generation |
> | **.claude/settings.json** | Hooks, permissions, MCP servers, tools | Session start | Claude Code runtime |

CLAUDE.md is the most critical — the project brain, loaded into every conversation. It defines domain, conventions, quality gates, and workflow. Keep it under 200 lines. See [[Claude Code Best Practices]].

DESIGN.md extends into the visual domain. A 312-line DESIGN.md like Anthropic's captures an entire design system as machine-readable constraints: semantic color names, typography hierarchy, component styles, Do's/Don'ts as constraint engineering. See [[Design.md Pattern]].

> [!warning] **Level 0 cost**
> Everything here loads at session start and persists the ENTIRE conversation. Every unnecessary line in CLAUDE.md occupies context for the full session. This is why it must be concise — it's the highest-cost configuration surface.

---

### Level 1: Skills — On-Demand Dynamic Context

> [!info] **The primary extension mechanism — zero cost when unused**
> Skills are markdown instruction sets (SKILL.md) organized in folders. They load into context only when triggered by user invocation, slash command, or model recognition.

**The SKILL.md format** — a skill is a folder, not a single file:

```
my-skill/
  SKILL.md          — Trigger description (for the model, not humans),
                       prerequisites, setup, instructions
  references/       — Domain knowledge, schemas, API docs
  scripts/          — Executable scripts the skill invokes
  examples/         — Example inputs/outputs for few-shot guidance
```

> [!tip] **Key architecture patterns**
> - **Progressive disclosure** — SKILL.md at root, deep context in subdirectories read only when needed
> - **Context forking** — `context: fork` runs the skill in an isolated subagent, preventing intermediate tool calls from polluting the main conversation
> - **Two-phase operation** — setup (install deps, authenticate) then use (execute repeatedly)
> - **On-demand hooks** — skills can declare hooks that activate only during skill execution
> - **Composition** — higher-level workflow skills orchestrate lower-level capability skills

> [!example]- **Real instance: this wiki's skill ecosystem**
> 5 skills with distinct roles:
> - **wiki-agent** — ingestion methodology, 3 modes (auto/guided/smart), quality gates, depth verification
> - **evolve** — evolution pipeline: score → scaffold → generate → review maturity
> - **continue** — session resume: run diagnostics, show state, present options
> - **model-builder** — create/review/evolve models with content + styling standards
> - **notebooklm** — mirror wiki to NotebookLM sources
>
> Each is self-contained. A subagent loaded with wiki-agent + CLAUDE.md can ingest sources independently.

> [!abstract] **Why skills are the dominant pattern**
> Skills load on demand at zero baseline cost. MCP loads at startup. Hooks enforce but don't teach. Commands trigger but carry no knowledge. For extending an agent with new CAPABILITIES, skills are the correct default. See [[Skills Architecture Is the Dominant LLM Extension Pattern]].

---

### Level 2: Hooks — The 26-Event Control Plane

> [!info] **Structural enforcement — ~98% compliance via execution-time blocking**
> Hooks fire at lifecycle boundaries and can block, modify, inject context, or trigger side effects. Unlike skills (instructions the model may follow), hooks are enforcement the model cannot bypass.

> [!info] **26 events across 7 categories**
> | Category | Events | Control surface |
> |----------|--------|----------------|
> | **Session** | SessionStart, SessionEnd, InstructionsLoaded, ConfigChange, CwdChanged | Context restoration, environment setup |
> | **Tool** | PreToolUse, PostToolUse, PostToolUseFailure | Block operations, modify inputs, validate outputs |
> | **Permission** | PermissionRequest, PermissionDenied | Custom permission logic |
> | **Subagent** | SubagentStart, SubagentStop | Inject context, aggregate results |
> | **Task** | TaskCreated, TaskCompleted | Readiness validation, downstream triggers |
> | **System** | Notification, FileChanged, WorktreeCreate/Remove, Elicitation, UserPromptSubmit | Environment reactions, input preprocessing |
> | **Compaction** | PreCompact, PostCompact | State snapshot and restoration |
>
> Plus meta-control: **Stop** (prevent premature completion) and **TeammateIdle** (prevent idle waste).

> [!tip] **The three critical hook patterns**
> - **Blocking** — PreToolUse fires before a tool executes. Returns `block` (deny), `allow` (bypass checks), `ask` (escalate), `defer` (pass to next hook). Plus `updatedInput` to modify the call in-flight. Qualitatively more powerful than binary pass/fail.
> - **Reverse hook** — Stop fires when the agent finishes. Returns `block` to force continuation. TeammateIdle prevents idle agents. Together they bracket execution from BOTH ends.
> - **Context injection** — SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, SubagentStart accept `additionalContext` — injecting information without user intervention. The mechanism context-mode uses to restore state after compaction.

> [!info] **Four handler types**
> | Type | Speed | Power | Use for |
> |------|-------|-------|---------|
> | `command` | Fastest | Full OS access | Shell scripts, file checks, git operations |
> | `http` | Network latency | Remote endpoints | External validation services |
> | `prompt` | LLM inference | Lightweight AI reasoning | Nuanced decisions at hook boundaries |
> | `agent` | Slowest, most expensive | Full subagent with tools | Complex multi-step enforcement |

> [!warning] **Scope hierarchy**
> user settings → project settings → local settings → plugins → policies. Lower scopes can add but NOT remove higher-scope hooks. Policy-scope hooks are organization-enforced and unoverridable — the correct substrate for cross-project safety invariants.

---

### Level 3: Commands — Lightweight User Triggers

> [!info] **Slash-invoked prompt templates — effectively free**
> Commands are markdown files in `.claude/commands/` (project) or `~/.claude/commands/` (personal). They inject a prompt when the user types `/command-name`.

**Commands invoke skills, not replace them.** `/ingest` triggers the wiki-agent skill. `/build-model` triggers the model-builder skill. Commands are thin triggers; skills carry knowledge.

> [!info] **Per-role command segmentation**
> | Role | Commands | Scope |
> |------|----------|-------|
> | **Generic** | `/continue`, `/status`, `/help` | Personal |
> | **Developer** | `/implement`, `/test`, `/commit`, `/debug` | Project |
> | **Researcher** | `/ingest`, `/evolve`, `/gaps`, `/review` | Project |
> | **PM/Lead** | `/backlog`, `/sprint`, `/retrospective` | Project |
> | **Operator** | `/deploy`, `/rollback`, `/incident` | Project |
>
> Role segmentation reduces noise: a developer doesn't see `/evolve`; a researcher doesn't see `/deploy`. The command palette becomes a role-appropriate workflow guide.

---

### The Context-Aware Loading Principle

> [!abstract] **The organizing principle across all four levels**
> Load information into the context window only when the agent needs it, never eagerly.

| Level | When it loads | Context cost | Why |
|-------|-------------|-------------|-----|
| 0 — Config files | Session start | Permanent (every message) | Governs every interaction — must be concise |
| 1 — Skills | On invocation | Temporary (until task done) | Capabilities needed only for specific operations |
| 2 — Hooks | At boundaries | Near-zero (fire and return) | Enforcement doesn't need persistent context |
| 3 — Commands | On `/invoke` | One-time injection | Triggers the real work in skills/hooks |

The measured cost difference: MCP servers that eagerly load all tool schemas at session start consume up to 12x more tokens than skills that load equivalent capabilities on demand. See [[CLI Tools Beat MCP for Token Efficiency]].

---

### The Plannotator Pattern: Command + Hook Composition

The most sophisticated composition pattern — a command triggers a workflow, a hook enforces structural gates within it.

> [!example]- **How Plannotator works**
> 1. User invokes `/plannotator-annotate` (command)
> 2. Command sends prompt with annotation context to Claude
> 3. Claude begins planning a response
> 4. **PreToolUse hook** fires, opens browser UI, pauses agent loop
> 5. User annotates the plan in the browser
> 6. Structured feedback returns to agent
> 7. Agent continues with revision instructions
>
> The command sets up context. The hook provides structural enforcement. Without hooks, the command can only *ask* Claude to pause — ~60% compliance. With hooks, the pause is guaranteed.

> [!tip] **This pattern generalizes to any approval workflow**
> Code review, maturity promotion (`seed → growing → mature`), architecture proposals, deployment sign-off. The command is the user-facing affordance. The hook is the infrastructure guarantee. See [[Plannotator — Interactive Plan & Code Review for AI Agents]].

---

### How the System Composes

The four levels are a designed system where each level depends on the others:

```
Commands (user trigger)
  └─→ invoke Skills (operational knowledge)
        └─→ which declare on-demand Hooks (structural enforcement)
              └─→ all governed by CLAUDE.md (static context)
```

> [!example]- **Composition in this wiki**
> `/evolve` command → triggers `evolve` skill → skill scores candidates, scaffolds pages, promotes maturity → a PreToolUse hook could enforce "no promotion to `mature` without 3+ relationship links" → CLAUDE.md defines the page schema and quality standards both skill and hook reference.
>
> Every level participates. Remove any level and the system degrades: no command = user can't trigger the workflow. No skill = no operational knowledge. No hook = quality gates are suggestions. No CLAUDE.md = no schema to validate against.

---

### Key Pages

| Page | Layer | Role in the model |
|------|-------|-------------------|
| [[Claude Code Skills]] | L2 | The L1 extension mechanism — SKILL.md format, progressive disclosure, context forking |
| [[Hooks Lifecycle Architecture]] | L2 | The L2 control plane — 26 events, 7 categories, blocking/reverse/injection patterns |
| [[Per-Role Command Architecture]] | L2 | The L3 user interface — role segmentation, command palettes, execution mode mapping |
| [[Design.md Pattern]] | L2 | Part of L0 config — visual design system as machine-readable constraints |
| [[Claude Code Best Practices]] | L2 | Teaching content — planning discipline, CLAUDE.md structure, skill architecture |
| [[Context-Aware Tool Loading]] | L5 | The organizing pattern — defer loading, never pre-load, measured cost differential |
| [[Skills Architecture Is the Dominant LLM Extension Pattern]] | L4 | Lesson: skills beat MCP, hooks, and commands for capability extension |
| [[CLI Tools Beat MCP for Token Efficiency]] | L4 | Lesson: eager vs deferred loading — the 12x cost differential |
| [[Skill Specification Is the Key to Ecosystem Interoperability]] | L4 | Lesson: format choice compounds into distribution gains |
| [[Plannotator — Interactive Plan & Code Review for AI Agents]] | L2 | The command+hook composition pattern for interactive approval workflows |
| [[Harness Engineering]] | L2 | The governing concept — all four levels as a coordinated control system |
| [[Decision: MCP vs CLI for Tool Integration]] | L6 | When to use MCP (external bridges) vs CLI+Skills (operational tasks) |

---

### Lessons Learned

| Lesson | What was learned |
|--------|-----------------|
| [[Skills Architecture Is the Dominant LLM Extension Pattern]] | Skills load on demand at zero baseline. For extending with capabilities, skills are the correct default. |
| [[CLI Tools Beat MCP for Token Efficiency]] | 12x cost differential. Eager loading (MCP) vs deferred loading (skills). Default to CLI for operational tasks. |
| [[Skill Specification Is the Key to Ecosystem Interoperability]] | agentskills.io format works across 5+ agent platforms. Format choice is a one-time decision with compounding gains. |
| [[The Agent Must Practice What It Documents]] | Skills that teach methodology must also be in CLAUDE.md. Teaching and enforcement must be layered. |
| [[Always Plan Before Executing]] | Planning prevents rework — and the extension system is HOW planning is operationalized (skills carry the planning workflow). |

---

### State of Knowledge

> [!success] **Well-covered (multiple sources, real evidence)**
> - Four-level hierarchy with cost-enforcement trade-offs (CLAUDE.md, Skills, Hooks, Commands)
> - SKILL.md format specification (agentskills.io standard, progressive disclosure, context forking)
> - Hook event taxonomy (26 events, 7 categories, 4 handler types, scope hierarchy)
> - The Plannotator command+hook composition pattern
> - Context-aware loading principle with measured 12x cost differential
> - Per-role command segmentation
> - 5 real skills operating in this wiki

> [!warning] **Thin or unverified**
> - On-demand hooks in skills — documented in best practices but untested in this ecosystem
> - Hook chain latency — what's the practical limit on `defer` composition depth?
> - Dynamic hook registration — can skills register/unregister hooks at runtime?
> - AGENTS.md and SOUL.md — newer conventions, less ecosystem evidence
> - Command automation based on detected role context — currently manual installation
> - Convergence path between SKILL.md and MCP tool registration — incompatible formats, unclear if they should merge

---

### How to Adopt

> [!info] **Setting up the extension system for a new project**
> 1. **CLAUDE.md** — under 200 lines. Project structure, conventions, key commands, quality gates.
> 2. **At least 1 skill** — the primary workflow (ingestion, building, deploying — whatever the project's core loop is). Folder with SKILL.md + subdirectories.
> 3. **1 command per skill** — `/command-name` triggers the skill. Place in `.claude/commands/`.
> 4. **Safety hooks** — minimum: block sudo, force-push, .env writes. Copy R01-R04 from claude-code-harness.
> 5. **(Optional) DESIGN.md** — if the project has a UI. Visual design system as agent-readable constraints.

> [!warning] **INVARIANT — never change these**
> - CLAUDE.md under 200 lines — it loads on EVERY message
> - Skills are folders with SKILL.md, not single files — progressive disclosure requires subdirectories
> - Commands invoke skills, never duplicate their logic — thin triggers, not standalone instructions
> - Hooks enforce at execution time — the ~98% vs ~60% compliance gap is real and structural
> - Context-aware loading — never eagerly load what can be deferred

> [!tip] **PER-PROJECT — always adapt these**
> - Which skills exist (domain-specific — wiki-agent vs frontend-builder vs deployment-manager)
> - Which hooks to enable (safety guardrails are universal; workflow enforcement is project-specific)
> - Which commands to expose (match the project's workflows and team roles)
> - Whether to use DESIGN.md, AGENTS.md, SOUL.md (depends on project type)
> - How deep the skill ecosystem goes (1 skill for simple projects, 5+ for complex ones)

> [!bug]- **What goes wrong if you skip this**
> - **No skills** → every capability re-explained per conversation. No reuse, no consistency, no progressive disclosure.
> - **Skills but no hooks** → ~60% compliance. The agent follows skill instructions most of the time, but under context pressure it forgets or ignores them.
> - **Hooks but no skills** → correct enforcement but no teaching. The agent is blocked from bad actions but doesn't know WHY or what to do instead.
> - **No commands** → skills must be invoked by name or auto-detected. Users don't know what's available. The extension system is invisible.
> - **No CLAUDE.md** → no static foundation. Every session starts from zero. Skills have no conventions to reference.

## Open Questions

> [!question] **Can skills dynamically register hooks at runtime?**
> Static on-demand hooks are declared in the skill folder. Dynamic registration would let skills adapt enforcement based on task state. (Requires: testing hook lifecycle API)

> [!question] **What is the practical limit on hook chain depth?**
> A 5-hook composition chain with 100ms per handler adds 500ms latency per tool call. Where does latency become unacceptable? (Requires: benchmarking with real hook chains)

> [!question] **Is there a convergence path between SKILL.md and MCP tool registration?**
> Both describe agent capabilities in incompatible formats. Should they merge? Or is the distinction (deferred vs eager loading) fundamental? (Requires: analysis of whether MCP tooling could adopt deferred loading)

## Relationships

- BUILDS ON: [[Claude Code Skills]]
- BUILDS ON: [[Hooks Lifecycle Architecture]]
- BUILDS ON: [[Per-Role Command Architecture]]
- BUILDS ON: [[Design.md Pattern]]
- BUILDS ON: [[Context-Aware Tool Loading]]
- BUILDS ON: [[Skill Specification Is the Key to Ecosystem Interoperability]]
- RELATES TO: [[Plannotator — Interactive Plan & Code Review for AI Agents]]
- RELATES TO: [[Harness Engineering]]
- RELATES TO: [[Claude Code Best Practices]]
- RELATES TO: [[Model: Methodology]]
- FEEDS INTO: [[Model: Claude Code]]
- FEEDS INTO: [[Model: MCP and CLI Integration]]

## Backlinks

[[Claude Code Skills]]
[[Hooks Lifecycle Architecture]]
[[Per-Role Command Architecture]]
[[Design.md Pattern]]
[[Context-Aware Tool Loading]]
[[Skill Specification Is the Key to Ecosystem Interoperability]]
[[Plannotator — Interactive Plan & Code Review for AI Agents]]
[[Harness Engineering]]
[[Claude Code Best Practices]]
[[Model: Methodology]]
[[Model: Claude Code]]
[[Model: MCP and CLI Integration]]
[[Model: Ecosystem Architecture]]
