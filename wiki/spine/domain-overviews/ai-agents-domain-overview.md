---
title: "AI Agents — Domain Overview"
type: domain-overview
domain: ai-agents
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-10
sources: []
tags: [domain-overview, ai-agents]
---

# AI Agents — Domain Overview

## Summary

The ai-agents domain covers the theory, patterns, and practice of building, operating, and orchestrating AI coding agents. With 15 concept pages, it is the largest and most developed domain in the wiki. Coverage spans Claude Code's runtime and extension system, multi-agent fleet design (OpenFleet), harness engineering guardrails, stage-gate methodology enforcement, spec-driven development, rework prevention, and knowledge linting. The domain underpins the entire ecosystem: Claude Code is the runtime, OpenFleet defines fleet governance, and harness engineering describes the control systems.

> [!info] Domain at a glance
>
> | Metric | Value |
> |--------|-------|
> | Concept pages | 15 |
> | Related model pages | [[Model: Claude Code]], [[Model: Skills, Commands, and Hooks]], [[Model: Quality and Failure Prevention]] |
> | Decision pages | [[Decision: Per-Role Command Design Decisions]], [[Decision: Hooks Design Decisions]], [[Decision: Extension System Operational Decisions]] |
> | Related lessons | 8+ (CLI Beats MCP, Always Plan, Practice What You Document, Never Skip Stages, etc.) |

## State of Knowledge

**Authoritative coverage:**
- Claude Code runtime — tool-use loop, extension system (5-tier reference card), context management (budget thresholds, session lifecycle, compaction strategy). Multiple sources, heavily cross-referenced.
- OpenFleet — 7-layer architecture, deterministic orchestrator (12-step cycle), 10 specialized agents, multi-dimensional state, kb_sync.py, dual-board sync. Sourced from live project CLAUDE.md.
- Harness Engineering — 13 guardrail rules (R01-R13), 5-verb workflow, enforcement hierarchy (Level 0-4). Three independent sources.
- Stage-gate enforcement — comprehensive coverage of both OpenFleet (MCP blocking) and OpenArms (protocol + commits) approaches.

**Good coverage:**
- Claude Code Skills — architecture, complexity spectrum, context economics, three-loader taxonomy.
- Context Management — token budget reference card, session lifecycle phases, compaction strategy.
- Rework Prevention — compound cost model, 4-layer prevention strategy, diagnostic table.
- Spec-Driven Development — 10-framework convergence on spec-first workflow.
- Hooks Lifecycle — 26 events across 7 categories, PreToolUse enforcement, handler types.

**Thin coverage:**
- OpenClaw — concept page exists but doesn't cover gateway architecture in depth.
- LLM Knowledge Linting — concept-level, no implementation plan for this wiki's own lint pipeline extension.

## Maturity Map

| Maturity | Pages |
|----------|-------|
| **growing** (all 15) | Claude Code, Claude Code Skills, Context Management, Best Practices, Hooks Lifecycle, Per-Role Commands, Design.md Pattern, Agent Orchestration, Harness Engineering, Task Lifecycle Stage-Gating, Spec-Driven Development, Rework Prevention, LLM Knowledge Linting, OpenFleet, OpenClaw |

All pages assigned maturity. All styled with callout vocabulary. All have standard sections.

## Gaps

- **Agent evaluation frameworks** — no coverage of measuring agent quality, comparing configurations, or benchmarking harness rule effectiveness
- **Subagent coordination patterns** — mentioned in Claude Code and Harness Engineering but no dedicated synthesis of how subagents share state and merge results
- **Agent identity lifecycle** — SOUL.md, HEARTBEAT.md, earned trust only touched in OpenFleet
- **OpenClaw depth** — gateway architecture, session lifecycle, Mission Control integration deserve dedicated treatment

## Priorities

1. Resolve remaining open questions via cross-referencing (several already resolved in decision pages)
2. OpenClaw deep-dive — essential for understanding the fleet execution layer
3. Subagent coordination pattern — would connect to the Agent Orchestration Patterns hub

## Key Pages

Start with these in order:
1. [[Agent Orchestration Patterns]] — the structural patterns every agent system converges on
2. [[Claude Code]] — the agent runtime powering the entire ecosystem
3. [[Harness Engineering]] — how to build guardrails around autonomous agents
4. [[Task Lifecycle Stage-Gating]] — phase boundaries and enforcement mechanisms
5. [[Claude Code Skills]] — the primary extension mechanism

## Relationships

- FEEDS INTO: [[Knowledge Systems — Domain Overview]]
- FEEDS INTO: [[Automation — Domain Overview]]
- ENABLES: [[Tools And Platforms — Domain Overview]]
- RELATES TO: [[Devops — Domain Overview]]
- BUILDS ON: [[AI Models — Domain Overview]]
- PARALLELS: [[Cross-Domain — Domain Overview]]

## Backlinks

[[Knowledge Systems — Domain Overview]]
[[Automation — Domain Overview]]
[[Tools And Platforms — Domain Overview]]
[[Devops — Domain Overview]]
[[AI Models — Domain Overview]]
[[Cross-Domain — Domain Overview]]
