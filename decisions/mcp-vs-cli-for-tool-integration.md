---
title: "Decision: MCP vs CLI for Tool Integration"
type: decision
domain: tools-and-platforms
layer: 6
status: synthesized
confidence: high
maturity: growing
derived_from:
  - "Synthesis: Claude Code Harness Engineering"
  - "Synthesis: Claude Code Accuracy Tips"
  - "MCP Integration Architecture"
  - "Claude Code"
reversibility: easy
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
  - id: src-claude-code-accuracy-tips
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=D5bRTv6GhXk"
    title: "Claude Code Works Better When You Do This"
  - id: src-playwright-cli-vs-mcp
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=nN5R9DFYsXY"
    title: "Claude Code + Playwright CLI: Automate QA with Less Tokens"
tags: [mcp, cli, skills, tool-integration, token-efficiency, claude-code, integration-pattern, context-management]
---

# Decision: MCP vs CLI for Tool Integration

## Summary

When integrating tools into LLM-powered workflows, CLI+Skills is the default preferred approach for operational tasks because it loads tool instructions contextually rather than exhausting the context window at startup. MCP servers are preferred for external service integration and tool discovery scenarios where persistent availability across any conversation is needed. The two approaches are complementary and the choice depends on the integration scenario, not a global winner.

## Decision

**Default to CLI+Skills for operational tool integration. Use MCP servers for external service bridges and tool discovery.**

Concretely, this means:
- Wiki pipeline operations (ingest, validate, lint, export, gaps) → CLI tools invoked via Bash, guided by skills loaded on demand
- External services without native CLI (databases, proprietary APIs, third-party SaaS) → MCP servers
- Tools that must be discoverable and callable from any Claude Code conversation without user scaffolding → MCP servers
- Research workflow tasks with defined sequences → CLI + skills (e.g., `python3 -m tools.pipeline run`)

## Alternatives

### Alternative 1: MCP-First (All tools as MCP servers)

Expose every tool as an MCP server. Single integration pattern, consistent JSON-RPC interface, tools always available without explicit loading. **Rejected as the default** because MCP loads all tool schemas into the context window at conversation startup regardless of whether the tools are used. A wiki MCP with 13 tools adds schema overhead to every message in every conversation, even those unrelated to wiki operations. The Playwright CLI vs MCP comparison in the accuracy tips source confirms: CLI was cheaper and more accurate. Google Trends data cited in the same source shows CLI overtaking MCP in adoption.

### Alternative 2: Skills-Only (No MCP, no CLI direct invocation)

Teach Claude via SKILL.md files only, with all tool operations embedded as natural language instructions. No subprocess invocations, no MCP servers. **Rejected** because this ties executable capability to Claude's interpretation of instructions at runtime. Harness engineering explicitly distinguishes between prompt-based guidance and runtime enforcement — hooks and CLI tools operate at execution time independent of whether Claude follows instructions correctly. Pure skills cannot block dangerous operations (sudo, force-push, .env writes); only executable hooks can.

### Alternative 3: CLI+Skills for Everything (No MCP at all)

Never deploy MCP servers, always use CLI tools and skills. **Rejected** because MCP has genuine advantages for external service integration: it provides a stable API contract, handles authentication and session management, and makes tools discoverable across any Claude Code conversation without per-session setup. For the planned NotebookLM and Obsidian integrations, MCP is the appropriate pattern since these are not filesystem-accessible services.

## Rationale

Multiple independent sources converge on CLI+Skills as more token-efficient than MCP for operational tooling. The core mechanism is timing of context loading:

**Context loading dynamics**: MCP servers register all their tool schemas at conversation startup. With 13 wiki tools, each exposing a JSON schema with descriptions, parameters, and examples, this represents hundreds of tokens added to every single message. Skills load only when invoked — a user session that never touches wiki operations incurs zero overhead. This is the mechanism behind the accuracy difference: more available context space means less context pressure, fewer hallucinations, and lower cost per task.

**Playwright CLI vs. MCP side-by-side demonstration (src-playwright-cli-vs-mcp):** A dedicated comparison video provides the clearest mechanical proof. Playwright MCP dumps the complete accessibility tree of the current page into Claude's context window after every single navigation step or browser action — every click, every form submit, every page load triggers a full accessibility tree injection. Playwright CLI saves page state to a YAML file on disk; Claude reads the file only when it needs to locate a specific element, and skips the read entirely when it already knows what to do. In a 10-step QA test, MCP injects 10 full accessibility trees (each containing hundreds of tokens of element data). CLI loads 2-3 targeted YAML snapshots on demand. This is the mechanistic basis for the 12x cost differential referenced in the accuracy tips source. Importantly, Microsoft (Playwright's creator) now officially recommends CLI over MCP for AI agent use, and the CLI has 3x more features than the MCP version — eliminating any residual capability argument for MCP on this tool.

**When MCP still wins: unknown pages and aggregated operations**: The Playwright comparison reveals a specific use case where MCP retains an advantage — when Claude needs to test or explore a page it has never seen before, MCP's forced full-page visibility ensures nothing is missed (unexpected errors, dynamic state changes, edge cases). The CLI's lazy-loading means Claude may miss errors that appear in the full page if it does not know to look for them. This informs a refined heuristic: use CLI for structured, known-workflow automation (regression tests, form filling, known-flow verification), and use MCP for exploratory testing or pages with high uncertainty. More broadly, MCP is appropriate for aggregated or grouped operations where full visibility at every step has genuine value — not mindlessly added to every agent config by default.

**Quantified degradation curve** (from src-claude-code-accuracy-tips): Accuracy is high at 20% context usage, drops significantly at 40%, becomes unreliable at 60%+, and produces bugs/hallucinations at 80%. MCP schema overhead shifts the starting point upward before any real work begins. CLI starts at zero.

**Harness engineering principle**: The harness engineering synthesis explicitly states "CLI over MCP is emerging consensus — multiple sources now converge on CLI+Skills being more token-efficient and accurate than MCP for tool integration." This aligns with the emerging community consensus from practitioners building at scale (the accuracy tips source is from a former Amazon/Microsoft senior engineer building an entire startup with Claude Code).

**MCP's genuine value proposition**: MCP shines when tools need to be available across any conversation without user scaffolding, or when integrating services that do not expose a CLI. The wiki's planned NotebookLM MCP server is the right use of the pattern — notebooklm-py does offer a CLI, but an MCP wrapper gives any conversation access to query notebooks without per-session skill loading. Similarly, the planned Obsidian MCP exposes vault management to agents that have no filesystem path to the Windows-side vault. The principle: MCP should be used deliberately for aggregated access or services requiring persistent availability, not added reflexively to every agent config.

**Practical split for this system**: The wiki pipeline tools already exist as CLI Python modules (`python3 -m tools.pipeline`, `python3 -m tools.validate`, etc.). The MCP server wrapping them (already prototyped) is appropriate for discoverability and cross-conversation access, but for routine operation within a dedicated wiki conversation, invoking CLI directly via Bash is lower-overhead and produces higher accuracy per the measured degradation curve.

## Reversibility

**Easy to reverse.** The CLI tools and MCP server are parallel interfaces to the same underlying Python modules — switching between them requires updating how tools are invoked, not rewriting tool logic. If MCP-first proves better in practice (e.g., as context windows grow to 1M+, schema overhead becomes negligible), the migration path is: update CLAUDE.md to reference MCP tools instead of Bash commands, and remove skill loading steps from the ingestion workflow. No data migration, no schema changes, no infrastructure teardown. The wiki's own MCP server (`.mcp.json`, `tools/mcp_server.py`) already exists and can be promoted to primary at any time.

The one nuance: if CLI skills accumulate significant institutional knowledge that diverges from MCP tool descriptions, keeping them in sync becomes overhead. Document both surfaces together to avoid drift.

## Dependencies

**Downstream effects of this decision:**

- **CLAUDE.md conventions**: Instructions for operating the wiki direct Claude to use `python3 -m tools.pipeline` commands rather than MCP tool calls for routine operations. If reversed, CLAUDE.md must be updated.
- **Wiki MCP server scope**: The existing MCP server (`tools/mcp_server.py`, 13 tools) is positioned as a convenience layer for cross-conversation access, not the primary operational interface. Its schema design should remain thin (no bloated parameter descriptions) to minimize context overhead if ever used as primary.
- **Skill design**: Skills like the wiki-agent skill should continue to reference CLI commands as the operational primitives. Skills that wrap MCP tool calls are valid only for external service integrations (NotebookLM, Obsidian).
- **Agent team patterns**: When subagents execute wiki operations in parallel, CLI invocation is preferable to MCP because each subagent gets a fresh context window. Routing subagent work through MCP adds schema overhead to each fresh context unnecessarily.
- **Context7 integration**: Context7 is available as both MCP server and CLI+Skills. Per this decision, prefer the skill form unless cross-conversation discoverability is required.
- **Future 1M context window**: As context windows expand, the token overhead argument weakens. This decision should be revisited when 1M context becomes standard — at that point, MCP-first may become the correct default due to consistency and discoverability advantages.

## Relationships

- DERIVED FROM: Synthesis: Claude Code Harness Engineering
- DERIVED FROM: Synthesis: Claude Code Accuracy Tips
- DERIVED FROM: Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens
- DERIVED FROM: MCP Integration Architecture
- DERIVED FROM: Claude Code
- RELATES TO: Claude Code Skills
- RELATES TO: Claude Code Context Management
- RELATES TO: Wiki Ingestion Pipeline
- FEEDS INTO: Research Pipeline Orchestration

## Backlinks

[[Synthesis: Claude Code Harness Engineering]]
[[Synthesis: Claude Code Accuracy Tips]]
[[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]]
[[MCP Integration Architecture]]
[[Claude Code]]
[[Claude Code Skills]]
[[Claude Code Context Management]]
[[Wiki Ingestion Pipeline]]
[[Research Pipeline Orchestration]]
