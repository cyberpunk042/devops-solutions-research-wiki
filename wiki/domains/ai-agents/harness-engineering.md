---
title: "Harness Engineering"
type: concept
layer: 2
maturity: growing
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    file: raw/articles/building-claude-code-harness-engineering.md
    title: "Building Claude Code with Harness Engineering"
    ingested: 2026-04-08
  - id: src-harness-engineering-github
    type: documentation
    url: "https://github.com/Chachamaru127/claude-code-harness"
    title: "claude-code-harness GitHub"
    ingested: 2026-04-08
  - id: src-claude-code-accuracy-tips
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=D5bRTv6GhXk"
    file: raw/transcripts/claude-code-works-better-when-you-do-this.txt
    title: "Claude Code Works Better When You Do This"
    ingested: 2026-04-08
tags: [harness-engineering, guardrails, plan-work-review, runtime-safety, agent-orchestration, claude-code, spec-driven, typescript]
---

# Harness Engineering

## Summary

Harness engineering is the practice of building structured control systems around LLM coding agents — moving beyond prompt engineering to runtime guardrails, quality validation, and rerunnable verification that keep development on a defined path. Anthropic's Claude Code implements this internally with a streaming agent loop, permission-governed tool dispatch, and context management layer. The community claude-code-harness project codifies the pattern as a 5-verb workflow (Setup → Plan → Work → Review → Release) with a TypeScript guardrail engine (13 rules) that enforces safety at execution time through hooks. The pattern is converging across multiple sources: the superpowers plugin, OpenFleet's deterministic orchestrator, and harness engineering all implement variants of the same Plan → Execute → Review cycle with runtime enforcement.

## Key Insights

- **Runtime enforcement, not prompt guidance**: The critical distinction is that harness guardrails operate at execution time through hooks, actually blocking dangerous operations (sudo, force-push, .env writes) before they happen. This is fundamentally different from instructions that the model may or may not follow.

- **The 5-verb workflow as universal pattern**: Setup → Plan → Work → Review → Release maps to every structured development approach in the ecosystem: superpowers (brainstorm → plan → execute → verify), OpenFleet (task creation → dispatch → execution → review → completion), and the research wiki's own ingestion pipeline (extract → analyze → synthesize → write → integrate).

- **13 guardrail rules (R01-R13)**: Denial rules (block sudo, .git/.env writes, force-push), Query rules (flag out-of-scope writes), Security rules (prevent --no-verify, direct main pushes), Post-execution checks (warn assertion tampering). These rules are TypeScript, not prompts — they execute as hooks with real enforcement.

- **CLI+Skills over MCP is emerging consensus**: Multiple sources converge: CLI tools with Skills (loaded contextually when relevant) are more token-efficient, more accurate, and cheaper than MCP servers (which load all tool schemas into context upfront). This is a significant architectural insight for any project exposing tools to LLM agents.

- **Planning discussion reduces rework**: The harness's Breezing mode adds Planner + Critic roles that review task quality before coding. ~5.5x token cost vs ~4x without discussion, but justified by reduced rework. Same principle as the wiki's "guided" ingestion mode — invest upfront in understanding to avoid downstream errors.

- **Agent teams with shared communication**: Beyond isolated subagents, both harness engineering and OpenFleet implement cross-agent communication channels. The harness uses hook-driven signals, OpenFleet uses IRC channels. Both solve the same problem: coordinating parallel workers.

## Deep Analysis

### The Harness Pattern Hierarchy

The ecosystem implements harness engineering at increasing levels of sophistication:

| Level | Implementation | Enforcement | Example |
|-------|---------------|-------------|---------|
| 0. Prompt guidance | CLAUDE.md, SKILL.md | Model compliance (hope) | Research wiki conventions |
| 1. Status monitoring | Context progress bar | Human intervention at threshold | "Claude Code Works Better" tips |
| 2. Workflow orchestration | superpowers, pipeline.py | Skill-enforced sequencing | This project's pipeline chains |
| 3. Runtime guardrails | Hooks, TypeScript engine | Execution-time blocking | claude-code-harness R01-R13 |
| 4. Deterministic orchestration | OpenFleet brain | Zero-LLM state machine | OpenFleet 30s cycle |

Each level adds stronger guarantees. This project currently operates at levels 0-2. The harness engineering pattern suggests level 3 (hook-based runtime guardrails) as the natural next step — before the eventual level 4 (deterministic orchestration).

### CLI vs MCP: Architectural Implications

The emerging CLI > MCP consensus has direct implications for the research wiki's MCP server (tools/mcp_server.py). The MCP server exposes 13 tools whose schemas load into every conversation. A CLI+Skills alternative would:
- Only load wiki tool instructions when the user invokes `/wiki-agent` skill
- Reduce baseline context overhead from ~2K tokens (MCP schemas) to near-zero
- Be inherently cross-platform (Python CLI works everywhere)

However, MCP has advantages for programmatic composition (chain/group/tree) that CLI lacks. The right answer may be both: MCP for pipeline orchestration, CLI+Skills for human conversations.

## Open Questions

- At what point does harness complexity become a net negative for productivity? (Requires: empirical data or external research on harness overhead at scale; the Rework Prevention page documents the break-even math for planning overhead but not for harness infrastructure overhead specifically)

### Answered Open Questions

**Q: Should this project adopt the TypeScript guardrail engine for runtime safety, or implement equivalent rules in Python hooks?**

Cross-referencing the `Decision: MCP vs CLI for Tool Integration` and `Immune System Rules` pages: the answer is Python hooks, not TypeScript. The `Decision: MCP vs CLI for Tool Integration` page establishes the ecosystem's tooling preference: "CLI tools invoked via Bash, guided by skills loaded on demand" and "The CLI tools already exist as Python modules." The `Immune System Rules` page documents that OpenFleet's doctor.py (the production immune system) is pure Python with zero LLM calls — "Python provides: (1) Infrastructure-level enforcement; (2) Session-level tracking; (3) Full audit trail." The TypeScript guardrail engine is appropriate for Claude Code projects running in a JavaScript/TypeScript codebase (where hooks can intercept build system operations natively). This project's entire toolchain is Python. Implementing equivalent rules in Python hooks via Claude Code's `settings.json` hook configuration (`PreToolUse`, `PostToolUse` hooks) keeps the enforcement language consistent with the rest of the tooling, avoids a Node.js runtime dependency, and makes rules maintainable by the same engineers who maintain the pipeline. The `Immune System Rules` page also notes the potential for a YAML rule file format as a shareable abstraction — which would be backend-agnostic and could be executed by either Python or TypeScript rule engines.

**Q: Can the 13 guardrail rules be adapted to protect wiki operations (e.g., block deletion of pages with high connectivity)?**

Cross-referencing the `Context-Aware Tool Loading` and `Knowledge Evolution Pipeline` pages: yes, and the mechanism is the Claude Code hooks system documented in `Claude Code Best Practices`. The rule categories map directly to wiki operations. The most valuable adaptations: (1) **Deny rule**: block `rm` or file deletion on any wiki page with relationship count above a threshold (equivalent to R01 blocking force-push — protect high-connectivity hubs from accidental deletion); (2) **Query rule**: flag any write to `wiki/domains/*/` that does not update the domain's `_index.md` (detects orphan page creation, equivalent to R05's out-of-scope write detection); (3) **Post-execution check**: after any wiki write, run `python3 -m tools.validate` and block completion on non-zero exit (equivalent to R11-R13 post-execution checks). The `Knowledge Evolution Pipeline` page identifies "canonical" maturity pages as the highest-value assets — adapting the TypeScript rule that blocks direct pushes to main (R09) to block deletion of `maturity: canonical` pages without explicit override would protect the wiki's most evolved knowledge. The `Context-Aware Tool Loading` page notes hooks as "contextual safety" — implementing these as `PreToolUse` hooks in `settings.json` would be the correct mechanism, firing only when relevant file operations are attempted.

**Q: How do harness engineering patterns change when the agent is running autonomously (OpenFleet) vs interactively (Claude Code)?**

Cross-referencing the `OpenFleet`, `Immune System Rules`, and `Rework Prevention` pages: the fundamental pattern stays the same (Plan-Execute-Review with deterministic enforcement), but the enforcement mechanism shifts from hooks-at-boundaries to continuous-monitoring. In interactive Claude Code (human present): harness enforcement runs at phase transitions — a PreToolUse hook blocks a dangerous command before the human sees it, a PostToolUse hook validates output after each step. The human can observe and intervene. In autonomous OpenFleet (no human present): enforcement must be continuous and proactive — doctor.py runs every 30 seconds, the 3-strike rule accumulates evidence over multiple cycles before escalating, and the security scan checks every new/changed task before dispatch. The `Immune System Rules` page states this distinction precisely: "A task flagged by the doctor accumulates a strike; at 3 strikes it is quarantined before ever reaching dispatch. This is a preemptive immune response, not a reactive one." The key architectural difference: interactive harness = reactive enforcement (catch violations as they occur); autonomous harness = proactive enforcement (detect violation precursors before they occur). The `Rework Prevention` page quantifies why: in autonomous multi-agent systems with sequential dependencies, one undetected violation can cascade to 5 downstream reworks, making proactive detection orders of magnitude cheaper than reactive correction.

## Relationships

- EXTENDS: [[Claude Code Best Practices]]
- EXTENDS: [[Claude Code Skills]]
- BUILDS ON: [[Claude Code]]
- PARALLELS: [[OpenFleet]]
- RELATES TO: [[Research Pipeline Orchestration]]
- RELATES TO: [[MCP Integration Architecture]]
- RELATES TO: [[OpenClaw]]

## Backlinks

[[Claude Code Best Practices]]
[[Claude Code Skills]]
[[Claude Code]]
[[OpenFleet]]
[[Research Pipeline Orchestration]]
[[MCP Integration Architecture]]
[[OpenClaw]]
[[Agent Orchestration Patterns]]
[[Always Plan Before Executing]]
[[Context Management Is the Primary LLM Productivity Lever]]
[[Deterministic Shell, LLM Core]]
[[Hooks Lifecycle Architecture]]
[[Immune System Rules]]
[[Infrastructure as Code Patterns]]
[[Model Guide: MCP + CLI Integration]]
[[Model: Claude Code]]
[[Model: Quality and Failure Prevention]]
[[Model: Skills, Commands, and Hooks]]
[[Per-Role Command Architecture]]
[[Plan Execute Review Cycle]]
[[Rework Prevention]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Synthesis: Playwright MCP for Visual Development Testing]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
