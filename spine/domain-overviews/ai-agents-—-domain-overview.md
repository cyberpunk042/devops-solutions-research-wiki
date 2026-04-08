---
title: "AI Agents — Domain Overview"
type: domain-overview
domain: ai-agents
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-08
sources: []
tags: [domain-overview, ai-agents]
---

# AI Agents — Domain Overview

## Summary

The ai-agents domain covers the theory, patterns, and practice of building, operating, and orchestrating AI coding agents in a multi-project DevOps context. It is the most developed domain in this wiki, with 8 concept pages spanning Claude Code's internals, multi-agent fleet design (OpenFleet), agent harness engineering, skills architecture, context management, and knowledge linting. The domain directly underpins the entire four-project ecosystem: Claude Code is the runtime for every operation, OpenFleet defines how fleets of 10 agents are governed, and harness engineering describes the control systems that keep both safe and productive. Coverage is authoritative for Claude Code itself and high-confidence for OpenFleet — both drawn from primary source documentation.

## State of Knowledge

**Strong coverage:**
- Claude Code internals — tool-use loop, extension system (skills, hooks, MCP, subagents, memory), CLAUDE.md, plans/todos. Two independent source transcripts (Karpathy, token hacks) plus the official best-practices repo. Confidence: authoritative.
- OpenFleet architecture — 7-layer design, deterministic orchestrator, 10 specialized agents, LightRAG integration, kb_sync bypass, dual-board sync. Sourced directly from the live project's CLAUDE.md. Confidence: authoritative.
- Harness engineering — 5-verb workflow, 13 TypeScript guardrail rules, CLI-vs-MCP architectural insight, enforcement hierarchy. Three sources including a YouTube transcript and GitHub repo.
- Claude Code skills — SKILL.md format, skills ecosystem, agentskills.io. Synthesized from multiple sources.
- Claude Code best practices and context management — separate pages with dedicated coverage of compaction, subagent isolation, token economy.

**Thin coverage:**
- OpenClaw — only a concept page stub; the 352k-star framework deserves deeper treatment covering gateway architecture, agent session management, and Mission Control UI.
- LLM Knowledge Linting — present as a concept but not yet connected to a concrete implementation plan for this wiki.
- Memory lifecycle management — covered in knowledge-systems domain; cross-domain connection could be stronger here.
- No coverage of agent evaluation frameworks, agent benchmarking, or failure mode analysis beyond what's embedded in OpenFleet's doctor.py rules.

## Maturity Map

**Established content (pre-maturity system):**
- Claude Code — foundational, authoritative, frequently referenced
- OpenFleet — foundational, authoritative, architectural cornerstone
- Harness Engineering — well-synthesized, cross-source convergence
- Claude Code Best Practices — synthesized, multi-source
- Claude Code Context Management — synthesized
- Claude Code Skills — synthesized
- OpenClaw — concept-level, needs depth
- LLM Knowledge Linting — concept-level, needs implementation path

**Lessons (evolved layer):**
- Lesson: Convergence on Claude Code Best Practices — cross-source validation
- Lesson: Convergence on Claude Code Skills — cross-source validation

## Gaps

- **OpenClaw depth**: The 352k-star framework is mentioned across many pages but the domain lacks a page covering its gateway architecture, agent session lifecycle, Mission Control integration, and WebSocket protocol.
- **Agent evaluation**: No coverage of how to measure agent quality, compare agent configurations, or benchmark harness rule effectiveness. OpenFleet's post-mortem-derived rules hint at this but don't make it explicit.
- **Failure mode taxonomy**: Agent death analysis exists in OpenFleet's doctor.py (24 rules, 16 post-mortems) but isn't documented as a standalone knowledge asset.
- **Claude Code Scheduling**: Listed as an ai-agents concern but the page lives in automation domain — cross-domain link is present but the scheduling pattern for agents specifically (HEARTBEAT.md, 30s cycles) deserves ai-agents treatment.
- **Agent identity and trust**: SOUL.md, HEARTBEAT.md, earned trust, permissions — only touched in OpenFleet. A dedicated pattern page for agent identity lifecycle would be valuable.
- **Subagent coordination patterns**: Mentioned in Claude Code and Harness Engineering but no dedicated synthesis of how subagents communicate, share state, and merge results.

## Priorities

1. **OpenClaw deep-dive** — Gateway architecture, agent sessions, Mission Control; essential for understanding the fleet execution layer
2. **Agent failure modes and immune system** — Distill OpenFleet's 24 doctor.py rules into a transferable pattern
3. **LLM Knowledge Linting implementation** — Connect the concept to a concrete pipeline step for this wiki
4. **Agent identity lifecycle pattern** — SOUL.md, HEARTBEAT.md, trust, permissions as a transferable pattern
5. **Subagent coordination patterns** — Consolidate the parallel-worker model across Claude Code, OpenFleet, and harness engineering

## Key Pages

1. **[Claude Code](../../domains/ai-agents/claude-code.md)** — The execution engine behind every operation. Essential first read for understanding the tool-use loop, extension system, and context management.
2. **[OpenFleet](../../domains/ai-agents/openfleet.md)** — How 10 agents are governed via a deterministic orchestrator. The production implementation of multi-agent coordination at scale.
3. **[Harness Engineering](../../domains/ai-agents/harness-engineering.md)** — Runtime guardrails, enforcement hierarchy, and the CLI-vs-MCP architectural insight. Synthesizes patterns from multiple projects.
4. **[Claude Code Skills](../../domains/ai-agents/claude-code-skills.md)** — The transferable knowledge mechanism. How skills encode expertise and enable consistent agent behavior.
5. **[Claude Code Best Practices](../../domains/ai-agents/claude-code-best-practices.md)** — Operational patterns validated across multiple sources. Direct input into this project's CLAUDE.md conventions.

## FAQ

### Q: What is the difference between a skill, a hook, and an MCP server in Claude Code?
Skills encode reusable procedural knowledge as markdown files loaded into context. Hooks inject deterministic code at lifecycle events (pre-tool, post-tool) without LLM overhead. MCP servers expose external tools as native capabilities across all conversations. See [[Claude Code Skills]] and [[Harness Engineering]].

### Q: How does OpenFleet govern 10 concurrent agents without them stepping on each other?
OpenFleet uses a deterministic orchestrator that reads HEARTBEAT.md and BOARD.md state files every 30 seconds — zero LLM calls in the coordination loop. Agents write to separate working directories and update shared state only through the orchestrator. See [[OpenFleet]].

### Q: When should I use a subagent vs a direct Claude Code session?
Use subagents for isolating risky operations, parallel workloads, or tasks that would pollute the parent context. Direct sessions are cheaper (7-10x lower token cost than spawning a subagent). The boundary is: if the task could dirty the context or benefits from parallel execution, fork it. See [[Claude Code Context Management]].

### Q: What is the context degradation curve and why does it matter?
AI accuracy drops as the context window fills: high at ~20% capacity, unreliable at ~60%, hallucinations common at 80%+. Manage it via compact sessions, subagent isolation, and loading only the skills you need for the current task. See [[Claude Code Best Practices]].

### Q: What are the 24 immune system rules and where do they come from?
The 24 rules in OpenFleet's doctor.py were distilled from 16 post-mortems of real agent failures. They cover runaway loops, stale state, cost spikes, and permission drift. They are the most operationally validated guardrail set in the ecosystem. See [[Harness Engineering]] and [[OpenFleet]].

## Relationships

- FEEDS INTO: Knowledge Systems
- FEEDS INTO: Automation
- ENABLES: Tools And Platforms
- RELATES TO: Devops
- BUILDS ON: AI Models
- PARALLELS: Cross-Domain

## Backlinks

[[Knowledge Systems]]
[[Automation]]
[[Tools And Platforms]]
[[Devops]]
[[AI Models]]
[[Cross-Domain]]
