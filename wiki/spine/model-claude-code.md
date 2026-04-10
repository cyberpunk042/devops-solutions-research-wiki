---
title: "Model: Claude Code"
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
    title: "Claude Code Best Practices"
  - id: src-karpathy-claude-code-10x
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=7sInxhTDA7U"
    title: "Andrej Karpathy Just 10x'd Everyone's Claude Code"
  - id: src-token-hacks-claude-code
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=49V-5Ock8LU"
    title: "18 Claude Code Token Hacks in 18 Minutes"
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
  - id: src-claude-code-hooks-reference
    type: documentation
    url: "https://code.claude.com/docs/en/hooks"
    title: "Claude Code Hooks Reference"
tags: [claude-code, model-definition, agent-architecture, skills, hooks, context-management, harness-engineering, mcp, extension-system, spine]
---

# Model: Claude Code

## Summary

Claude Code is Anthropic's CLI coding agent — a tool-use loop that reads, writes, and reasons about codebases from the terminal. This model defines how the agent works as an extensible runtime: the core agent loop, the four-level extension system (CLAUDE.md, Skills, Hooks, Commands), the context management discipline that governs session quality, the MCP vs CLI+Skills decision that shapes tool integration architecture, and the harness engineering concept that coordinates all layers into a governed system. This is the execution engine behind the research wiki's ingestion pipeline, every OpenFleet agent, and the primary human-to-system interface for the entire ecosystem. Understanding this model means knowing how to extend Claude Code correctly, constrain it safely, and keep its context window healthy.

## Key Insights

- **Agent loop, not chatbot**: Claude Code operates as an iterative decide-call-evaluate loop. Each turn, the model selects tools (Read, Write, Edit, Bash, Grep, Glob, WebFetch, Agent, etc.), executes them, evaluates results, and repeats until the task completes or it yields to the user. There is no fixed pipeline — the agent decides the sequence at runtime.

- **Four-level extension system**: CLAUDE.md (static project config, always loaded), Skills (dynamic context loaded on demand via SKILL.md files), Hooks (26 lifecycle events for structural enforcement), Commands (lightweight slash triggers that inject prompts or invoke skills). Each level has a different cost-benefit profile and they compose into a coordinated harness.

- **Context window is the primary constraint**: Context management directly affects output quality. Every architectural decision — lean CLAUDE.md, deferred skill loading, CLI over MCP — traces back to using context efficiently. Degradation at higher utilization is probabilistic, not deterministic — well-managed sessions can work effectively throughout, but careless context loading accelerates problems.

- **CLI+Skills beats MCP for operational tasks**: A 12x cost differential measured on Playwright CLI vs MCP. MCP loads all tool schemas at startup; CLI+Skills loads nothing until invoked. MCP wins for external service bridges and tool discovery across conversations. See [[Decision: MCP vs CLI for Tool Integration]].

- **Harness engineering is the governing concept**: CLAUDE.md + Skills + Hooks + Commands + Subagents form a coordinated control system with runtime enforcement. The 13 guardrail rules (R01-R13) block dangerous operations at execution time — not as suggestions the model may ignore, but as hooks that prevent the operation from completing.

- **Subagent parallelism for context isolation**: The Agent tool spawns workers that share the filesystem but not the conversation context. Each subagent gets a fresh context window, protecting the main conversation from bloat. This is the mechanism for parallel research, independent file modifications, and isolated testing.

## Deep Analysis

### The Agent Architecture

Claude Code's core is a tool-use loop: the model receives a prompt, decides which tools to invoke, executes them, reads the results, and decides again. This loop continues until the task is complete or the model yields control. The key properties:

**Tool dispatch is model-decided.** The agent chooses from available tools each turn. A single response can chain multiple calls (Read a file, Edit it, run Bash to test, Grep to verify). There is no predetermined sequence — the model plans and adapts dynamically based on tool outputs.

**Permission governance gates execution.** Before sensitive tools execute (Write, Bash, etc.), the permission system checks project settings, user settings, and hook decisions. This creates a checkpoint layer between the model's intent and actual execution.

**Subagents provide parallelism without context pollution.** The Agent tool spawns an isolated worker with its own context window. The main conversation delegates a task ("research X and write a summary to /tmp/result.md"), the subagent executes independently, and the main conversation reads the output file. Context stays clean. This is how the research wiki runs parallel ingestion and how OpenFleet coordinates agent teams.

**The loop has no fixed depth.** Claude Code will continue calling tools until it believes the task is done. This makes it powerful for multi-step tasks but means unbounded sessions can exhaust context. The compaction mechanism (/compact) summarizes history to reclaim space, but quality degrades after 3-4 compactions — at which point a fresh session with a transferred summary is the correct move.

### The Extension System

Claude Code exposes four extension levels, each with different loading behavior, enforcement strength, and context cost:

#### Level 1: CLAUDE.md — Static Project Config

CLAUDE.md is loaded on every single message. It defines project conventions, file structure, workflow rules, and pointers to detailed resources. Because it is charged per-message, it must be treated as a hot path:

- Keep under 200 lines. Every line compounds across every message in every session.
- Treat it as an index, not an encyclopedia. Point to files; do not contain them.
- Use `.claude/rules/` to split large instruction sets into files loaded alongside CLAUDE.md.
- Wrap critical rules in `<important if="...">` tags to prevent attention dropout in long files.

The correct mental model: CLAUDE.md is the routing table. It tells the agent where knowledge lives and what conventions to follow. Detailed knowledge belongs in skills, referenced files, or wiki pages.

#### Level 2: Skills — Dynamic Context on Demand

Skills are markdown instruction files (SKILL.md) organized in folders under `.claude/skills/` or `skills/`. They load into context only when triggered — by user invocation, slash command, or model recognition of a relevant task. Properties:

- **Plain markdown, no compilation.** A skill is text that teaches the agent a capability.
- **Two-phase operation.** Setup (install dependencies, authenticate) then use (execute the capability repeatedly).
- **Progressive disclosure via folder structure.** SKILL.md at root, with references/, scripts/, and examples/ subdirectories for deeper context the agent reads only when needed.
- **Context forking.** Skills can specify `context: fork` to run in an isolated subagent, preventing intermediate tool calls from polluting the main conversation.
- **Zero cost when unused.** Unlike CLAUDE.md (always loaded) and MCP (schemas loaded at startup), a skill that is never invoked costs nothing.

This is why skills are the dominant extension pattern. See [[Claude Code Skills]], [[Skills Architecture Is the Dominant LLM Extension Pattern]].

#### Level 3: Hooks — Structural Enforcement

Hooks are the runtime enforcement layer. They fire shell commands, HTTP requests, prompt evaluations, or full subagents at 26 lifecycle events across 7 categories (session, tool, permission, subagent, task, system, compaction). The critical patterns:

**The blocking pattern.** PreToolUse fires before a tool executes. A hook can return `block` to prevent it, `allow` to bypass permission checks, `ask` to escalate to the user, or `defer` to let other hooks decide. This is how the 13 guardrail rules (R01-R13) enforce safety — blocking sudo, force-push, .env writes, and --no-verify at execution time with ~98% compliance, compared to ~60% for instruction-only approaches.

**The reverse-hook pattern.** Stop fires when the agent finishes responding. A hook can block the stop, forcing the agent to continue. TeammateIdle prevents an agent from going idle. These invert the PreToolUse pattern — gating completion instead of initiation — creating bidirectional control.

**Context injection.** SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, and SubagentStart accept `additionalContext` in their response, injecting information into the running conversation without user intervention. This is how session state survives compaction.

**Stage-gate enforcement.** A PreToolUse hook can block all Write/Edit calls to `src/` during a documentation phase, enforcing "no implementation in document stage" at the infrastructure level. This is the bridge between methodology (instructions that may be ignored) and enforcement (hooks that cannot be bypassed).

See [[Hooks Lifecycle Architecture]] for the full 26-event taxonomy.

#### Level 4: Commands — Lightweight Triggers

Commands are slash-invoked prompt templates (e.g., `/commit`, `/review-pr`, `/plan`). They inject a structured prompt into the current context or invoke a skill. Commands are the thinnest layer — they add no persistent overhead and serve as the user-facing interface to skills and workflows.

Commands compose with hooks via the Plannotator pattern: a command initiates a workflow, and a hook enforces its constraints. For example, `/careful` activates a skill that blocks destructive Bash commands via a PreToolUse hook — the command is the trigger, the hook is the enforcement.

See [[Per-Role Command Architecture]] for role-segmented command palettes.

### The Context Management Discipline

Context management is not a technique — it is the primary lever on Claude Code output quality. The degradation curve defines the operating envelope:

**Note on context utilization**: One practitioner (former Amazon/Microsoft engineer) reported observing increased error rates at higher context usage percentages (40%, 60%, 80% thresholds). However, context degradation is PROBABILISTIC, not deterministic — a well-driven session with clean CLAUDE.md, proper skill loading, and good context management can work effectively to very high utilization without issues. The real principle: manage context proactively (lean CLAUDE.md, deferred skill loading, subagent isolation), but don't treat arbitrary thresholds as hard limits. Quality depends on HOW the context is used, not just how MUCH is used.

**What IS verified about context management:**
- Session overhead exists — system prompts, tools, MCP schemas consume tokens before any conversation starts. Each connected MCP server adds to this baseline.
- Subagent isolation gives each worker a fresh context window — this is a structural fact, not an observation.
- Compaction reclaims space but loses detail — this is how the mechanism works, not a quality judgment.
- CLI+Skills loads on demand vs MCP at startup — this is measurable and verified by the Playwright comparison.

**What is NOT verified (presented as fact elsewhere in this wiki but actually one person's observation):**
- The specific degradation thresholds (20%, 40%, 60%, 80%)
- Whether degradation is a step function or gradual
- The "51,000 token" baseline — real measurement from one developer's specific setup, not universal
- The "5-minute prompt cache TTL" — reported by one source, not confirmed by Anthropic
- The "3-4 compactions" degradation claim — one developer's observation from their workflow

These need proper research or marking as unverified. See the source: a single YouTube video from one practitioner, not Anthropic documentation or measured benchmarks.

See [[Claude Code Context Management]] for the full analysis.

### The MCP vs CLI+Skills Decision

This is a resolved architectural decision with clear heuristics. The mechanism is timing of context loading:

**MCP loads all tool schemas at conversation startup.** With 13 wiki tools, hundreds of tokens are added to every message regardless of whether any tool is used. A Playwright MCP dumps the full accessibility tree after every browser action — 10 steps means 10 full tree injections.

**CLI+Skills loads nothing until invoked.** The wiki pipeline as CLI (`python3 -m tools.pipeline`) adds zero overhead to conversations that never touch wiki operations. When invoked, only the relevant skill loads. The Playwright CLI saves state to a YAML file; Claude reads it only when needed and skips it when it already knows what to do. Result: 2-3 targeted reads vs 10 full dumps. This is the mechanism behind the 12x cost differential.

**When MCP wins.** External services without native CLI (databases, proprietary APIs, SaaS). Tool discovery across any conversation without per-session setup. Exploratory testing where full visibility at every step has genuine value. The planned NotebookLM and Obsidian MCP integrations are correct uses of the pattern — they bridge services that are not filesystem-accessible.

**The heuristic.** Default to CLI+Skills for operational tasks. Use MCP for external service bridges and cross-conversation tool discovery. See [[Decision: MCP vs CLI for Tool Integration]] for the full decision record.

The [[Context-Aware Tool Loading]] pattern generalizes this: defer all tool schema loading until actually needed. Never pre-load at session start.

### Harness Engineering

Harness engineering is the concept that ties the extension system together. A harness is CLAUDE.md + Skills + Hooks + Commands + Subagents working as a coordinated control system — not as independent features added ad hoc.

**The enforcement hierarchy:**

| Level | Mechanism | Compliance | Example |
|---|---|---|---|
| Prompt guidance | CLAUDE.md, SKILL.md | ~60% (model may ignore) | "Always run tests before committing" |
| Workflow orchestration | Skills, pipeline chains | ~80% (sequenced but not enforced) | Research-Plan-Execute-Review cycle |
| Runtime guardrails | Hooks (PreToolUse blocking) | ~98% (execution-time enforcement) | Block sudo, force-push, .env writes |
| Deterministic orchestration | External state machine | 100% (no LLM in loop) | OpenFleet 30s brain cycle |

The 13 guardrail rules (R01-R13) from the claude-code-harness project implement level 3: denial rules (block sudo, .git/.env writes, force-push), query rules (flag out-of-scope writes), security rules (prevent --no-verify, direct main pushes), and post-execution checks (warn assertion tampering). These are TypeScript hooks with real enforcement, not prompt suggestions.

**The 5-verb workflow** — Setup, Plan, Work, Review, Release — is the universal pattern that harness engineering codifies. It appears independently in superpowers (brainstorm-plan-execute-verify), OpenFleet (task-dispatch-execute-review-complete), and the research wiki's ingestion pipeline (extract-analyze-synthesize-write-integrate). The convergence across 10+ open-source frameworks confirms this cycle is inherent to effective AI-assisted development. See [[Plan Execute Review Cycle]].

**This ecosystem currently operates at levels 0-2** (prompt guidance + workflow orchestration via skills and pipeline chains). Level 3 (hook-based runtime guardrails) is the natural next step. Level 4 (deterministic orchestration) is already implemented in OpenFleet's brain.

### Key Lessons from This Ecosystem

Four validated lessons emerge from operating Claude Code at scale in this ecosystem:

**1. Always Plan Before Executing** ([[Always Plan Before Executing]]). The planning step is not optional. The biggest source of token waste is not expensive models — it is the agent going down a wrong path and scrapping work. Boris Cherny (Claude Code's creator) recommends: "Do not make any changes until you have 95% confidence in what you need to build." Watch the first few steps, then let it run.

**2. Context Management Is the Primary Lever** ([[Claude Code Context Management]]). A developer who practices context hygiene gets 3-5x more useful work per session than one who does not. Lean CLAUDE.md, manual compaction at 60%, fresh sessions over infinite continuation, disconnecting unused MCPs — these are not optimizations but prerequisites.

**3. Skills Architecture Is the Dominant Pattern** ([[Skills Architecture Is the Dominant LLM Extension Pattern]]). Skills load on demand at zero baseline cost. MCP loads at startup. Hooks enforce constraints but do not teach capabilities. Commands trigger workflows but carry no knowledge. Skills are the correct default for extending Claude Code with new capabilities.

**4. CLI Beats MCP for Token Efficiency** ([[CLI Tools Beat MCP for Token Efficiency]]). The 12x cost differential measured on Playwright is not an outlier — it is the structural consequence of eager loading (MCP) vs deferred loading (CLI+Skills). For any tool that does not need cross-conversation discovery or external service bridging, CLI+Skills is the correct integration pattern.

### Documentation Layers in a Claude Code Project

A Claude Code project has distinct documentation layers that must not be conflated:

| Layer | Where | Purpose | Who reads it |
|-------|-------|---------|-------------|
| **Agent config** | CLAUDE.md, .claude/rules/ | Agent behavior rules, project conventions | Claude Code (every message) |
| **Wiki knowledge** | wiki/ | Synthesized, structured, evolving knowledge | Agent + human (on demand) |
| **Public docs** | docs/, README.md | User-facing documentation, guides | Humans |
| **Code docs** | Inline comments, JSDoc/docstrings, function headers | Code-level documentation | Developers reading source |
| **Smart docs** | README.md files inside src/ subdirectories | Subsystem explanations alongside the code they document | Developers + agent navigating codebase |
| **Specs and plans** | docs/superpowers/ | Execution track artifacts, temporary | Agent during implementation |

An agent MUST NOT:
- Put wiki knowledge in code comments (wrong audience, wrong lifecycle)
- Put code docs in the wiki (too granular, changes with every refactor)
- Conflate public docs with wiki pages (different readers, different update cadence)
- Mix specs with permanent knowledge (specs are ephemeral, wiki is permanent)

### How to Attach the Second Brain to a Claude Code Project

When adding the LLM Wiki model to an existing Claude Code project:

1. **Create the wiki structure** — `raw/`, `wiki/` (with subdirectories), `config/wiki-schema.yaml`, `config/templates/`. This coexists with existing project structure.
2. **Add methodology rules to CLAUDE.md** — stage gates, quality gates, the three operations (ingest, query, lint). See the Agent Methodology section format.
3. **Create initial skills** — at minimum: wiki-agent (ingest/query), evolve (evolution pipeline), continue (session resume).
4. **Start ingesting** — scan the project itself first (`pipeline scan ../project/`), then ingest external sources.
5. **Tolerate existing docs** — don't restructure old documentation. Let it coexist. The wiki adds a NEW layer; it doesn't replace what's there.

For projects with an "old model" (scattered docs, no frontmatter, no schema): the wiki coexists alongside. Over time, valuable knowledge migrates into the wiki. Old docs are never force-deleted — they decay naturally as the wiki becomes the authoritative source.

### OpenArms as a Live Instance

OpenArms demonstrates this model in production:
- **CLAUDE.md = AGENTS.md** (symlinked) — 351 lines covering architecture boundaries, plugin SDK, channel implementation, gateway protocol
- **Progressive disclosure** — each major subsystem has its own AGENTS.md (`src/plugin-sdk/AGENTS.md`, `src/channels/AGENTS.md`, `src/gateway/protocol/AGENTS.md`)
- **wiki/ with backlog** — embedded LLM wiki adapted from this research wiki. Epics, modules, tasks with frontmatter state machines.
- **Skills ecosystem** — 50+ skills bundled, new skills directed to ClawHub marketplace
- **Methodology enforcement** — wiki/config/methodology.yaml + wiki/config/agent-directive.md governing autonomous agent operation
- **`read_when` metadata** — docs self-declare their relevance via frontmatter, enabling agents to know when to load a doc without reading everything

The key insight from OpenArms: the documentation layers WORK when each layer has a clear owner (CLAUDE.md = agent, wiki/ = knowledge, docs/ = humans, src/ = developers) and the agent knows which layer to read for which purpose.

## Open Questions

- What is the optimal number of concurrent subagents before filesystem contention degrades throughput? (Requires: empirical benchmarking with parallel file operations)
- At what point does harness complexity (hooks + skills + commands) become a net negative for productivity? (Requires: empirical data on harness infrastructure overhead vs rework prevention benefit)
- How will Claude Code's extension model evolve as context windows grow to 1M+ tokens — does the degradation curve shift or does it remain proportional?

## Relationships

- BUILDS ON: [[Claude Code]]
- BUILDS ON: [[Claude Code Skills]]
- BUILDS ON: [[Hooks Lifecycle Architecture]]
- BUILDS ON: [[Claude Code Best Practices]]
- BUILDS ON: [[Claude Code Context Management]]
- BUILDS ON: [[Harness Engineering]]
- BUILDS ON: [[Decision: MCP vs CLI for Tool Integration]]
- ENABLES: [[Model: Skills, Commands, and Hooks]]
- ENABLES: [[Model: MCP and CLI Integration]]
- ENABLES: [[Model: LLM Wiki]]
- ENABLES: [[Model: Ecosystem Architecture]]
- RELATES TO: [[Model: Methodology]]
- IMPLEMENTS: [[Plan Execute Review Cycle]]
- IMPLEMENTS: [[Context-Aware Tool Loading]]
- DERIVED FROM: [[Always Plan Before Executing]], [[CLI Tools Beat MCP for Token Efficiency]], [[Skills Architecture Is the Dominant LLM Extension Pattern]]

## Backlinks

[[Claude Code]]
[[Claude Code Skills]]
[[Hooks Lifecycle Architecture]]
[[Claude Code Best Practices]]
[[Claude Code Context Management]]
[[Harness Engineering]]
[[Decision: MCP vs CLI for Tool Integration]]
[[[[Model: Skills]]
[[Commands]]
[[and Hooks]]]]
[[Model: MCP and CLI Integration]]
[[Model: LLM Wiki]]
[[Model: Ecosystem Architecture]]
[[Model: Methodology]]
[[Plan Execute Review Cycle]]
[[Context-Aware Tool Loading]]
[[Always Plan Before Executing]]
[[CLI Tools Beat MCP for Token Efficiency]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Model: Skills, Commands, and Hooks]]
