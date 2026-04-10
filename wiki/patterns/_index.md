# Patterns

Recurring structures validated across 2+ independent systems. Each pattern has concrete instances.

## Cross-Domain Patterns

| Pattern | Instances | Underlying Constraint |
|---------|-----------|----------------------|
| [[Plan Execute Review Cycle]] | OpenFleet, Harness Engineering, wiki pipeline, superpowers | Bounded context + compound error cost |
| [[Context-Aware Tool Loading]] | Skills vs MCP, Playwright CLI vs MCP, NotebookLM | Context window fills → accuracy degrades |
| [[Progressive Distillation]] | Zettelkasten, PARA, wiki maturity, page sections | Signal degrades without explicit distillation |
| [[Deterministic Shell, LLM Core]] | OpenFleet orchestrator, harness rules, wiki post-chain | LLM reasoning is probabilistic |
| [[Gateway-Centric Routing]] | OpenArms gateway, OpenClaw, wiki MCP, OpenFleet orchestrator | N deployments drift without central control |
| [[Scaffold → Foundation → Infrastructure → Features]] | Research Wiki, OpenFleet, AICP, Front-Middleware-Backend | Build lifecycle repeats at every scale |

## Skills Integration Patterns

| Pattern | What It Maps |
|---------|-------------|
| [[Skills + Claude Code]] | How skills extend the Claude Code agent |
| [[Skills + CLI]] | CLI tools paired with SKILL.md files |
| [[Skills + MCP]] | MCP servers as skill infrastructure |
| [[Skills + NotebookLM]] | NotebookLM automation via skills |
| [[Skills + Obsidian]] | Obsidian vault management via skills |

See also: [[Cross-Domain Patterns]] for the meta-analysis of why these 6 patterns recur.

## Pages

- [Context-Aware Tool Loading](context-aware-tool-loading.md) — Only load tool schemas, documentation, or external data into the context window when the agent actually needs them — ...
- [Deterministic Shell, LLM Core](deterministic-shell-llm-core.md) — Deterministic Shell, LLM Core is the architectural pattern of wrapping LLM inference inside a deterministic orchestra...
- [Gateway-Centric Routing](gateway-centric-routing.md) — Gateway-Centric Routing is the architectural pattern of channeling all traffic — messages, tasks, tool calls, or agen...
- [Plan Execute Review Cycle](plan-execute-review-cycle.md) — The Plan→Execute→Review cycle is a recurring structural pattern observed independently across AI agent orchestration ...
- [Progressive Distillation](progressive-distillation.md) — Progressive Distillation is the pattern of processing raw material through successive layers of increasing density an...
- [Scaffold → Foundation → Infrastructure → Features](scaffold-foundation-infrastructure-features.md) — Scaffold → Foundation → Infrastructure → Features (SFIF) is the universal 4-stage build lifecycle that repeats at eve...
- [Pattern: Skills + Claude-Code](skills-claude-code.md) — <!-- 2-3 sentences: what recurs and why it matters -->
- [Pattern: Skills + Cli](skills-cli.md) — <!-- 2-3 sentences: what recurs and why it matters -->
- [Pattern: Skills + Mcp](skills-mcp.md) — <!-- 2-3 sentences: what recurs and why it matters -->
- [Pattern: Skills + Notebooklm](skills-notebooklm.md) — <!-- 2-3 sentences: what recurs and why it matters -->
- [Pattern: Skills + Obsidian](skills-obsidian.md) — <!-- 2-3 sentences: what recurs and why it matters -->

## Tags

`orchestration`, `openfleet`, `mcp`, `agent-architecture`, `deterministic`, `guardrails`, `cross-domain`, `context-management`, `token-efficiency`, `deferred-loading`, `skills`, `cli`, `tool-design`, `accuracy`, `notebooklm`, `playwright`, `context7`, `llm-core`, `shell-pattern`, `harness`
