---
title: "Model: Skills, Commands, and Hooks"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
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

The AI agent extension ecosystem is a four-level hierarchy: CLAUDE.md (always loaded, static instructions) at the base, Skills (on-demand, dynamic instruction sets) as the primary extension mechanism, Hooks (lifecycle event handlers, structural enforcement) as the control plane, and Commands (lightweight slash-command triggers) as the user-facing entry point. These levels are not independent features — they compose into a coordinated system where commands invoke skills, hooks enforce invariants that skills alone cannot guarantee, and configuration files (CLAUDE.md, DESIGN.md, AGENTS.md) provide the static context that governs everything. The central design principle is context-aware loading: static context enters at startup, dynamic context enters on invocation, and the cost difference between eager and deferred loading is up to 12x.

## Key Insights

- **Four levels, not three**: The extension system is commonly described as "skills + commands + hooks" but the actual hierarchy has four tiers. CLAUDE.md is the zeroth level — always loaded, never optional, defining project identity and behavioral constraints before any extension fires. Skills, commands, and hooks build on top of this static foundation.

- **Loading cost is the governing constraint**: Every token loaded at session start occupies context budget permanently. CLAUDE.md loads once and stays. Skills load on invocation and can fork into isolated subagents. Hooks fire at execution boundaries with near-zero context cost. Commands are effectively free — a few lines of prompt text. This cost gradient determines correct placement: put stable, universal rules in CLAUDE.md; put domain-specific operational knowledge in skills; put enforcement in hooks; put workflow entry points in commands.

- **Hooks close the compliance gap**: Instruction files (CLAUDE.md, skills) achieve roughly 60% compliance under context pressure — the model may ignore instructions when the context window fills. Hooks achieve approximately 98% compliance because they operate at the infrastructure level: a PreToolUse hook that blocks a write operation cannot be overridden by reasoning. This is the fundamental reason hooks exist alongside skills — they enforce what skills can only request.

- **The Plannotator pattern generalizes**: A command triggers a workflow; a hook intercepts and enforces structural gates within that workflow. This command+hook composition is the correct architecture for any interactive approval workflow — code review, plan annotation, maturity promotion, architecture sign-off.

- **Skill specification determines portability**: The agentskills.io SKILL.md format, adopted by kepano's official Obsidian skills, created a de facto standard. A skill conforming to this spec works across Claude Code, Codex CLI, OpenCode, Cursor, and any system-prompt-configurable agent. Format choice is a one-time decision with compounding distribution gains.

## Deep Analysis

### Level 0: The Configuration File Ecosystem

Five markdown files at the project root form the static context layer. Each has a distinct purpose, and together they give the agent complete project awareness without any runtime invocation.

| File | Purpose | Loaded When | Who Reads It |
|---|---|---|---|
| CLAUDE.md | Project instructions, behavioral constraints, tooling commands | Session start (always) | Every Claude Code session |
| DESIGN.md | Visual design system — colors, typography, spacing, component patterns | Session start (always) | UI generation tasks |
| AGENTS.md | Multi-agent topology — which agents exist, their roles, handoff rules | Session start (always) | Multi-agent orchestration |
| SOUL.md | Personality, tone, communication style | Session start (always) | All response generation |
| .claude/settings.json | Hooks, permissions, MCP servers, allowed/denied tools | Session start (always) | Claude Code runtime |

CLAUDE.md is the most critical: it is the project brain, loaded into every conversation. It defines domain, conventions, quality gates, and workflow — the equivalent of an operating system's kernel configuration. See [[Claude Code Best Practices]] for structure guidance.

DESIGN.md extends this into the visual domain. A 312-line DESIGN.md like Anthropic's own specification captures an entire design system as machine-readable constraints: semantic color names with hex values and rationale, a 16-role typography hierarchy, component styles with exact CSS, and a Do's/Don'ts section that prevents regression to visual defaults. See [[Design.md Pattern]] for the full analysis.

AGENTS.md and SOUL.md are newer conventions. AGENTS.md defines the multi-agent topology for projects using subagents or fleet architectures. SOUL.md captures personality and communication style as a separate concern from behavioral instructions.

The key property of Level 0: everything here loads at session start and persists for the entire conversation. This is why CLAUDE.md must be concise — every unnecessary line occupies context for the full session.

### Level 1: Skills — On-Demand Dynamic Context

Skills are markdown instruction sets that teach the agent how to perform specific tasks. They are the primary extension mechanism for Claude Code. See [[Claude Code Skills]] for the detailed concept page.

**The SKILL.md format**: A skill is a folder, not a single file. The canonical structure from Anthropic's Thariq and the agentskills.io specification:

```
my-skill/
  SKILL.md          — Trigger description (written for the model, not humans),
                       prerequisites, setup, operational instructions
  references/       — Domain knowledge, schemas, API docs
  scripts/          — Executable scripts the skill can invoke
  examples/         — Example inputs/outputs for few-shot guidance
```

The `description` field in SKILL.md frontmatter is a trigger condition — "when should I fire?" — evaluated by the model to decide whether to load the skill for a given task. Anti-triggers ("do NOT fire when...") prevent false activation. The Gotchas section documents known failure points. See [[Skill Specification Is the Key to Ecosystem Interoperability]] for the standardization story.

**Context forking for isolation**: Skills can declare `context: fork` to execute in an isolated subagent. The main conversation sees only the final result, not intermediate tool calls. This prevents a complex skill execution (e.g., a 40-step ingestion pipeline) from filling the main context window with operational noise. The fork boundary is the mechanism that makes skills composable without mutual interference.

**Two-phase operation**: When Claude loads a skill, it first performs setup (install dependencies, authenticate services) and then enters the operational phase. The NotebookLM skill exemplifies this: phase 1 installs `notebooklm-py` and authenticates with Google; phase 2 provides query, upload, and podcast generation capabilities. Setup runs once; operations repeat.

**Skills compose with hooks**: A skill can declare on-demand hooks that activate only when the skill is loaded. This means a skill does not just provide instructions — it can also install enforcement infrastructure that exists only for the duration of the skill's execution.

### Level 2: Hooks — The 26-Event Control Plane

Hooks are the structural enforcement layer. They fire at lifecycle boundaries in the agent execution loop and can block, modify, inject context, or trigger side effects. See [[Hooks Lifecycle Architecture]] for the complete reference.

**26 events across 7 categories**:

| Category | Events | Control Surface |
|---|---|---|
| Session | SessionStart, SessionEnd, InstructionsLoaded, ConfigChange, CwdChanged | Context restoration, environment setup |
| Tool | PreToolUse, PostToolUse, PostToolUseFailure | Block operations, modify inputs, validate outputs |
| Permission | PermissionRequest, PermissionDenied | Custom permission logic |
| Subagent | SubagentStart, SubagentStop | Inject subagent context, aggregate results |
| Task | TaskCreated, TaskCompleted | Readiness validation, downstream triggers |
| System | Notification, FileChanged, WorktreeCreate, WorktreeRemove, Elicitation, ElicitationResult, UserPromptSubmit | Environment reactions, input preprocessing |
| Compaction | PreCompact, PostCompact | State snapshot and restoration |

Plus meta-control: **Stop** (prevent premature completion) and **TeammateIdle** (prevent idle waste).

**The blocking pattern**: PreToolUse is the highest-leverage hook. Its four decision gradations — `block` (hard deny), `allow` (skip permission checks), `ask` (escalate to user), `defer` (pass to next hook) — plus `updatedInput` (modify the tool call in-flight) make it qualitatively more powerful than binary pass/fail. A PreToolUse hook can enforce "no implementation writes during documentation stage" at the infrastructure level, making the constraint impossible to violate rather than merely discouraged.

**The reverse hook axis**: Stop and TeammateIdle invert the PreToolUse pattern. PreToolUse gates initiation — it fires before an action and can prevent it. Stop fires when the agent finishes responding and can force continuation. Together they bracket the task execution window from both ends: PreToolUse prevents forbidden initiation, Stop prevents premature completion.

**Four handler types** with different cost/capability tradeoffs: `command` (shell script, fastest, full OS access), `http` (remote endpoint, network latency), `prompt` (single-turn LLM evaluation, lightweight AI reasoning), `agent` (full subagent with tool access, highest power and cost).

**Scope hierarchy**: user settings → project settings → local settings → plugins → policies. Lower scopes add but cannot remove higher-scope hooks. Policy-scope hooks are organization-enforced and unoverridable — the correct substrate for cross-project safety invariants.

### Level 3: Commands — Lightweight User Triggers

Commands are slash-command entry points: markdown files in `.claude/commands/` (project scope) or `~/.claude/commands/` (personal scope) containing prompt text that gets injected when the user types `/command-name`. See [[Per-Role Command Architecture]] for the full design.

**Commands invoke skills, not replace them**: The correct relationship is `/ingest` triggers the `ingest` skill rather than duplicating its logic. Commands are thin triggers; skills carry the operational knowledge. This keeps commands minimal, reusable, and cheap — a few lines of prompt text versus a full skill folder.

**Per-role segmentation**: Different practitioner roles need different command palettes:

| Role | Example Commands | Scope |
|---|---|---|
| Generic (all roles) | `/continue`, `/status`, `/help` | Personal (`~/.claude/commands/`) |
| Developer | `/implement`, `/test`, `/commit`, `/debug` | Project (`.claude/commands/`) |
| Researcher | `/ingest`, `/evolve`, `/gaps`, `/review` | Project |
| PM/Lead | `/backlog`, `/sprint`, `/retrospective`, `/handoff` | Project |
| Operator | `/deploy`, `/rollback`, `/incident` | Project |

Role segmentation reduces cognitive noise: a developer does not see `/evolve`; a researcher does not see `/deploy`. The command palette becomes a role-appropriate workflow guide rather than a discovery problem.

**Execution modes map to command sets**: Autonomous mode surfaces `/continue` and `/status`. Semi-autonomous surfaces `/review`, `/evolve`, `/gaps`. Document-only surfaces `/ingest`, `/scaffold`. A future enhancement: a command like `/document-mode` could set a session variable that reconfigures hooks — making the mode switch a structural change, not a prompting change.

### The Context-Aware Loading Principle

The organizing principle across all four levels is [[Context-Aware Tool Loading]]: load information into the context window only when the agent needs it, never eagerly.

**Level 0** (CLAUDE.md, DESIGN.md) is the exception — static context loaded at startup because it governs every interaction. This is why these files must be concise: they pay their context cost for the entire session.

**Level 1** (Skills) loads on invocation. A skill folder with references, scripts, and examples enters context only when the model decides the skill is relevant to the current task, or when the user invokes it via a command. Context forking further isolates the cost.

**Level 2** (Hooks) has near-zero context cost. Hooks execute at boundaries and inject only `additionalContext` strings when needed. They do not occupy persistent context.

**Level 3** (Commands) is effectively free — a few lines of prompt text that trigger the real work in skills and hooks.

The measured cost difference: MCP servers that eagerly load all tool schemas at session start consume up to 12x more tokens than skills that load equivalent capabilities on demand. This is not a micro-optimization — it determines whether an agent session remains accurate (context at 20%) or degrades into hallucination (context at 60%+).

### The Plannotator Pattern: Command + Hook Composition

The most sophisticated composition pattern is the command-as-hook-trigger. [[Plannotator — Interactive Plan & Code Review for AI Agents]] operationalizes this:

1. User invokes `/plannotator-annotate` (command)
2. Command sends prompt with annotation context to Claude
3. Claude begins planning a response
4. PreToolUse hook fires, opens browser UI, pauses agent loop
5. User annotates the plan in the UI
6. Structured feedback returns to agent
7. Agent continues with revision instructions

The critical insight: the command is not doing the interception — the hook is. The command sets up context; the hook provides structural enforcement. Without hooks, the command can only *ask* Claude to pause — which it may or may not do under context pressure. With hooks, the pause is guaranteed.

This pattern generalizes to any workflow requiring a human approval gate: code review, maturity promotion (`seed → growing → mature`), architecture proposals, deployment sign-off. The command is the user-facing affordance; the hook is the infrastructure guarantee.

### How the System Composes

The four levels are not a menu of independent features — they are a designed system where each level depends on the others:

```
Commands (user trigger)
  └─→ invoke Skills (operational knowledge)
        └─→ which declare on-demand Hooks (structural enforcement)
              └─→ all governed by CLAUDE.md (static context)
```

A concrete example from this wiki: the `/evolve` command triggers the `evolve` skill, which scores candidates, scaffolds pages, and promotes maturity. A PreToolUse hook could enforce "no promotion to `mature` without 3+ relationship links" — a quality gate that the skill describes but only the hook guarantees. CLAUDE.md defines the page schema and quality standards that both the skill and hook reference.

Another example: a developer's `/implement` command triggers an implementation skill. A Stop hook prevents completion until tests pass. PreToolUse hooks block writes to `docs/` during implementation stage. DESIGN.md constrains the visual output. AGENTS.md routes subtasks to specialist subagents. Every level participates.

## Open Questions

- Can skills dynamically register and unregister hooks at runtime, or must on-demand hooks be declared statically in the skill folder? Dynamic registration would enable skills that adapt their enforcement profile based on task state.
- What is the practical limit on hook chain depth when using `defer` decisions? A 5-hook composition chain with 100ms per handler adds 500ms latency per tool call.
- Is there a convergence path between the SKILL.md spec (agentskills.io) and the MCP tool registration protocol? Both describe agent capabilities, but in incompatible formats.
- How should the configuration file ecosystem handle conflicts between CLAUDE.md behavioral constraints and DESIGN.md visual constraints when generating UI?
- Can command selection be automated based on detected role context, or must role segmentation always be manual installation of command sets?

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
- FEEDS INTO: [[Model Guide: Claude Code]]
- FEEDS INTO: [[Model Guide: MCP + CLI Integration]]
- FEEDS INTO: [[Model Guide: Methodology]]

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
[[Model Guide: Claude Code]]
[[Model Guide: MCP + CLI Integration]]
[[Model Guide: Methodology]]
