---
title: "Synthesis: Claude Code Harness Engineering"
type: source-synthesis
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
tags: [harness-engineering, claude-code, guardrails, plan-work-review, agent-teams, typescript, runtime-safety, spec-driven]
---

# Synthesis: Claude Code Harness Engineering

## Summary

Harness engineering is the practice of building structured control systems around an LLM coding agent — not just prompt engineering but runtime guardrails, quality validation, and rerunnable verification. Anthropic's own Claude Code uses a streaming agent loop, permission-governed tool dispatch, and context management layer. The community claude-code-harness project (Chachamaru127) implements this as a 5-verb workflow (Setup → Plan → Work → Review → Release) with a TypeScript guardrail engine enforcing 13 rules (R01-R13) at execution time through hooks. The project supports parallel workers, 4-perspective code review (security, performance, quality, accessibility), and agent team orchestration. Claude Code crossed $1B annualized revenue within 6 months of launch.

## Key Insights

- **Harness = runtime guardrails, not prompts**: The distinction between prompt-based guidance and runtime enforcement is critical. Harness engineering operates at execution time through hooks, blocking dangerous operations before they happen (sudo, force-push, .env writes) rather than hoping the model follows instructions.

- **Anthropic's core harness**: Single-threaded master loop (perception → reasoning → tool execution → feed results back → repeat until terminal state), typed tool dispatch registry with strict input schemas, context management for long sessions.

- **5-verb community framework**: /harness-setup (init), /harness-plan (spec with acceptance criteria), /harness-work (parallel workers with self-checks), /harness-review (4-perspective analysis), /harness-release (changelog + version + GitHub release). This is a more structured version of the superpowers workflow.

- **13 TypeScript guardrail rules**: Denial (block sudo, .git writes, force-push), Query (flag out-of-scope writes), Security (prevent --no-verify, direct main pushes), Post-execution (warn assertion tampering). Rules execute at hook level, independent of Claude's own safety.

- **CLI over MCP is emerging consensus**: Multiple sources now converge on CLI+Skills being more token-efficient and accurate than MCP for tool integration. Skills load contextually (only when relevant), MCP loads all schemas upfront. This affects the research wiki's own MCP server design — consider a CLI+Skills alternative.

- **Agent teams with planning discussion**: Breezing mode adds Planner + Critic roles that review task quality before coding begins. ~5.5x token cost vs ~4x without discussion, justified as rework-reducing investment.

- **Plan→Work→Review is becoming default**: The harness makes the orchestrated workflow the default operating model, not an optional add-on. This parallels superpowers' brainstorm → plan → execute → verify and OpenFleet's deterministic orchestrator cycle.

## Relationships

- DERIVED FROM: src-harness-engineering-article
- DERIVED FROM: src-harness-engineering-github
- EXTENDS: Claude Code Best Practices
- EXTENDS: Claude Code Skills
- RELATES TO: Claude Code
- RELATES TO: OpenFleet
- RELATES TO: OpenClaw

## Backlinks

[[Cross-Domain Patterns]]
[[Harness Engineering]]
[[Claude Code Best Practices]]
[[Claude Code Skills]]
[[Claude Code]]
[[OpenFleet]]
[[OpenClaw]]
[[Always Plan Before Executing]]
[[CLI Tools Beat MCP for Token Efficiency]]
[[Context Management Is the Primary LLM Productivity Lever]]
[[Decision: MCP vs CLI for Tool Integration]]
