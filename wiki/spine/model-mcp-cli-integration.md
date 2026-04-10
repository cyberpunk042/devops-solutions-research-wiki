---
title: "Model: MCP and CLI Integration"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [mcp, cli, integration, model, token-efficiency, tool-integration, playwright, sandbox, spine, context-management]
---

# Model: MCP and CLI Integration

## Summary

The MCP and CLI Integration model resolves one of the most consequential architectural decisions in LLM agent design: how to expose external tools to an agent without degrading its context window. MCP servers are powerful but always-on — they load all registered tool schemas at session startup, consuming context budget before any task-relevant token is written. CLI tools paired with skills load on demand, injecting targeted instructions only when the relevant capability is needed. Empirically, this produces a 12x token cost differential in favor of CLI for operational tooling. A third approach — the context-mode sandbox — isolates heavy operations entirely in a subagent with a clean context window, achieving 98% context saving for tasks like full codebase analysis.

## Key Insights

- **MCP's always-available property has a per-turn cost**: Every MCP server with 6-8 tools adds schema overhead to every message in the session — not just when those tools are invoked. A session with five MCP servers registers that overhead on every turn, steadily advancing the context fill rate toward the degradation thresholds (40% = significant degradation; 60% = unreliable; 80% = bugs and hallucinations).

- **CLI+Skills defers all schema loading**: Skill files (SKILL.md) exist on disk and enter the context window only when invoked via slash command or agent decision. Between invocations, they consume zero context budget. This makes CLI+Skills strictly superior to MCP for tools used only in specific workflows.

- **The 12x differential is measured, not estimated**: In a 10-step Playwright QA test, the MCP approach dumped the full accessibility tree into context after every navigation step (10 full dumps). The CLI approach wrote page data to a YAML file and loaded targeted snapshots only when Claude needed a specific element (2-3 selective reads). The measured token cost difference was 12x in favor of CLI. See [[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]] for full methodology.

- **The context-mode sandbox handles the extreme case**: For operations requiring full codebase analysis or processing large document sets, even CLI+Skills may consume too much context. The harness engineering pattern (context-mode) runs the heavy operation as an isolated subagent with a clean context window, then returns only the result to the parent session. The parent session receives a compact result; the subagent absorbs the full token cost in isolation. Measured saving: 98%.

- **MCP genuinely wins for external service bridges**: Tools that need to be discoverable across any conversation — without the user explicitly invoking a skill — benefit from MCP's always-available property. OAuth service integrations, cross-session tool registries, and interactive workflows requiring rapid tool-call iteration are where MCP's overhead is a worthwhile trade.

- **The decision is resolved in this ecosystem**: CLI+Skills is the default for all wiki operations, pipeline tooling, and project-internal workflows. MCP is used for external service bridges (the research wiki's 15-tool MCP server exposes the wiki to any Claude Code conversation) and cross-conversation discoverability scenarios. See [[Decision: MCP vs CLI for Tool Integration]] for full alternatives analysis.

## Deep Analysis

### The Two Integration Strategies

**MCP — Eager Load**

MCP (Model Context Protocol) servers register tool schemas with Claude Code at session startup. The client discovers all registered servers, fetches their tool schemas, and includes those schemas in the context window for the session's duration. The model can invoke any registered tool at any point without further setup.

The cost: schema tokens for all tools enter the context window permanently, regardless of whether those tools are called during the session. A Claude Code session with three MCP servers each defining 5 tools might consume several thousand tokens of overhead before any user message is processed. Across a 200-turn session, those tokens represent budget unavailable for task content.

**CLI+Skills — Deferred Load**

Skills are instruction files (typically `skills/<name>.md`) that describe how to invoke a CLI tool, what parameters it accepts, and how to interpret its output. These files sit on disk between invocations. When a user types `/playwright` or an agent decides the skill is relevant, the skill's content loads into the context window at that moment and stays until the conversation ends or explicitly cleared.

Between invocations: zero overhead. The skill exists on disk, not in context. For tools used occasionally across a long session, this model can preserve thousands of tokens that MCP would have consumed at startup.

### The Third Strategy: Context-Mode Sandbox

The harness engineering model (documented in [[Harness Engineering]]) adds a third integration strategy for the highest-token-cost operations: isolation in a subagent.

Rather than loading a heavy tool into the current session's context, the pattern spawns a fresh Claude Code subprocess (`context: fork` / `--context` flag) with a clean context window. The subagent receives only the task description and necessary context — no session history, no accumulated conversation. It runs the full operation (code analysis, document synthesis, test generation) in its isolated window and writes the result to disk. The parent session reads only the compact output file.

**Why this matters**: a fresh Claude Code session starts with roughly 190,000 tokens of usable context. A main session that has run for 50 turns may have already consumed 40-60% of that. The same codebase analysis that would push the main session past the 80% degradation threshold runs cleanly in the subagent at minimal context fill. The parent session gains the result without bearing the cost.

Measured saving on full codebase analysis tasks: 98% fewer tokens in the parent session.

### Context Fill and the Degradation Curve

The degradation thresholds documented in [[Synthesis: Claude Code Accuracy Tips]] establish why context budget management is not a minor optimization:

- **40% context fill**: significant accuracy degradation begins
- **60% context fill**: outputs become unreliable; model starts losing track of earlier context
- **80% context fill**: active bugs and hallucinations; the model drops constraints and misremembers code

MCP schema noise is explicitly documented as a failure mode at 60%+ fill: the model follows tool schemas from servers that are not relevant to the current task because they are always visible. CLI+Skills eliminates this failure mode for any tool not currently in use.

### The Ecosystem Integration Bindings

The resolved integration pattern for this ecosystem (see [[Decision: MCP vs CLI for Tool Integration]]):

**CLI+Skills**:
- Wiki pipeline operations (pipeline.py, manifest, lint, validate, export)
- Playwright QA automation
- NotebookLM queries (via notebooklm-py skill)
- Context7 documentation fetching
- All project-internal operational tooling

**MCP**:
- Research wiki MCP server (15 tools: wiki_status, wiki_search, wiki_read_page, wiki_post, etc.) — exposes wiki to any Claude Code conversation without pre-configuration
- AICP inference routing bridge
- External service integrations requiring cross-session availability

**Context-Mode Sandbox**:
- Full codebase analysis
- Large document set processing
- Any single operation estimated to consume >30% of the current session's remaining context

### The [[Context-Aware Tool Loading]] Pattern

The [[Context-Aware Tool Loading]] pattern generalizes the MCP vs CLI decision to any information that might enter an agent's context window. It describes three loader types:

1. **Eager** (MCP): always loaded, always available, always consuming budget
2. **Deferred** (Skills, CLI): on-disk until invoked, zero overhead until needed
3. **External** (NotebookLM, Context7): lives entirely outside the context window; agent queries it on demand, receives targeted answers rather than full document dumps

The pattern applies uniformly to browser automation tools (MCP vs CLI), documentation systems (pre-loaded docs vs Context7 on-demand queries), knowledge bases (inline wiki context vs LightRAG graph queries), and skill libraries (always-loaded vs SKILL.md deferred invocation).

### The Decision Framework

When choosing between MCP and CLI for a new tool integration, apply this sequence:

**Step 1 — Identify the usage pattern**
- Tool is used in every session, regardless of task → MCP is a candidate
- Tool is used in specific workflows only → CLI+Skills preferred
- Tool requires authentication state preserved across sessions → MCP
- Tool is invoked 0-3 times per session on average → CLI+Skills

**Step 2 — Assess the schema cost**
- How many tools does this server expose? Each tool schema adds tokens.
- How many other MCP servers are already registered? Each multiplies the per-turn overhead.
- Does schema overhead measurably affect the budget for this session type? Long analytical sessions are more sensitive than short task sessions.

**Step 3 — Evaluate the discoverability need**
- Does the agent need to discover and invoke this tool without explicit user instruction? MCP's always-available property is the mechanism for autonomous discovery.
- Can the user or an explicit agent step invoke the skill at the right time? CLI+Skills handles this without discoverability overhead.

**Step 4 — Consider the sandwich case**
- If the operation is expected to be very heavy (large codebase, many files, complex synthesis), is a context-mode sandbox more appropriate than either MCP or CLI in the main session?

**Defaults in the absence of specific requirements**: CLI+Skills for project-internal tools; MCP for external services that need cross-session availability; context-mode sandbox for operations estimated to consume >30% of the remaining session context.

### The Playwright Case Study in Full

The Playwright comparison is the clearest empirical validation of the MCP vs CLI decision. Both approaches accomplish the same task: automated QA testing of a web application across 10 navigation steps.

**MCP approach**: After every navigation, Playwright MCP dumps the full accessibility tree for the current page into the context window. This is always-on data injection — the model has full page data available at all times, enabling it to interact without explicit read steps.

**CLI approach**: Playwright CLI writes the accessibility tree to a YAML file on disk after navigation. Claude reads the file only when it needs to locate a specific element — typically 2-3 reads per 10-step test rather than 10 automatic injections.

Token cost differential across the 10-step test: 12x fewer tokens with CLI. Accuracy was equivalent or better with CLI — the model was not operating in a degraded context state when it needed to reason about UI elements.

The counter-case: [[Synthesis: Playwright MCP for Visual Development Testing]] documents when MCP wins for Playwright. In interactive visual development workflows (designer iterating rapidly on component appearance), MCP's always-available property makes tight feedback loops faster than the read-file-on-demand model. The 12x cost differential is the correct default for QA automation; MCP is the correct choice for interactive visual iteration.

### MCP Server Design Principles (When MCP Is the Right Choice)

When MCP is the correct integration choice, server design matters for minimizing the schema overhead that makes MCP expensive:

**Minimize tool count**: each tool in an MCP server adds schema tokens on every turn. A server with 15 tools (like the research wiki's MCP server) carries more overhead than a server with 5. When designing an MCP server, expose only the tools that legitimately need to be always-discoverable. Tools that are only used in specific workflows should be CLI skills even if other tools in the same domain are MCP.

**Prefer narrow tool signatures**: tools with many optional parameters produce larger schema definitions. A tool that does one thing with two parameters contributes less overhead than a tool that does five things with eight optional parameters. Composition (calling two tools sequentially) is preferable to adding parameters that make one tool do more.

**Name tools semantically for autonomous invocation**: MCP's advantage over CLI is that the model can discover and invoke tools without explicit user direction. Tool names like `wiki_search`, `wiki_post`, `wiki_status` — the naming convention in the research wiki's MCP server — are self-describing enough that an agent reasoning about its task can recognize when the tool is relevant. Opaque names (`do_operation_7`) defeat the discoverability advantage.

**Document preconditions in tool descriptions**: when the model autonomously invokes an MCP tool, it has only the tool schema and description to guide it. Preconditions that are obvious in a CLI invocation context (where a human is typing the command) are not obvious to an autonomous agent. Put preconditions, side effects, and expected output format explicitly in the tool description — they are part of the schema overhead cost, but they prevent miscalls that are more expensive.

The research wiki's 15-tool MCP server follows these principles: tool names are `wiki_<verb>` format (semantically clear), each tool has a single primary function, and descriptions include what the tool returns so the agent can decide whether the result will be useful before invoking.

## Open Questions

- At what MCP server count does the schema overhead actually exceed a measurable accuracy threshold (not just theoretical)? The 12x figure is task-specific; general benchmarks across task types would strengthen the decision framework.
- Does the `context: fork` sandbox pattern compose with MCP servers? Can a subagent inherit parent MCP registrations, or does it start with a clean server list?
- As MCP servers gain selective tool exposure (exposing only tools relevant to a conversation), does the eager-load cost reduce enough to shift the default recommendation?

## Relationships

- BUILDS ON: [[CLI Tools Beat MCP for Token Efficiency]]
- BUILDS ON: [[Context-Aware Tool Loading]]
- BUILDS ON: [[Decision: MCP vs CLI for Tool Integration]]
- RELATES TO: [[Model: Skills, Commands, and Hooks]]
- RELATES TO: [[Model: Claude Code]]
- RELATES TO: [[Harness Engineering]]
- RELATES TO: [[Model: Ecosystem Architecture]]
- FEEDS INTO: [[Decision: MCP vs CLI for Tool Integration]]

## Backlinks

[[CLI Tools Beat MCP for Token Efficiency]]
[[Context-Aware Tool Loading]]
[[Decision: MCP vs CLI for Tool Integration]]
[[[[Model: Skills]]
[[Commands]]
[[and Hooks]]]]
[[Model: Claude Code]]
[[Harness Engineering]]
[[Model: Ecosystem Architecture]]
[[Model: Design.md and IaC]]
[[Model: Skills, Commands, and Hooks]]
