---
title: "OpenFleet"
type: concept
domain: ai-agents
status: synthesized
confidence: authoritative
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
    ingested: 2026-04-08
tags: [openfleet, ai-agents, fleet-management, orchestration, deterministic-brain, vibe-managing, mission-control, openclaw, lightrag, multi-agent]
---

# OpenFleet

## Summary

OpenFleet is an AI-native project lifecycle orchestration framework implementing "Vibe Managing" — the shift from directing individual AI models via prompts to governing a fleet of 10 intelligent agents through declarative systems and deterministic orchestration. The human user (Product Owner) sets direction through structured management boards (tempo, phase, risk posture, budget). A deterministic orchestrator (zero LLM calls, pure Python) handles all operational mechanics on a 30-second cycle. AI agents are first-class assignable contributors — persistent, accountable, with roles, permissions, and earned trust. The system runs on OpenClaw + Mission Control with LightRAG for knowledge graph intelligence, LocalAI for routine inference, and Claude for complex reasoning.

## Key Insights

- **Deterministic brain, not LLM-driven**: The orchestrator runs every 30 seconds with zero LLM calls. Pure Python logic handles state diffing, budget gating, heartbeat scheduling, task dispatch, security scanning, and anomaly detection. This makes orchestration predictable, auditable, and cheap.

- **10 specialized agents**: fleet-ops (board lead, 30m heartbeat), project-manager (sprint planning, Plane bridge), devsecops-expert, architect, software-engineer, qa-engineer, devops, technical-writer, ux-designer, accountability-generator. Each has a SOUL.md (identity) and HEARTBEAT.md (periodic checklist).

- **Seven-layer architecture**: L0 Substrate (persistent state graph) → L1 Deterministic Brain → L2 Orchestration → L3 Agent Execution (LLM-powered) → L4 Capability & Extension (Skills, 13 MCP tools) → L5 Interaction (prompts, @mentions, UI, API) → L6 Observability & Governance.

- **Multi-dimensional state**: 6 orthogonal axes — lifecycle, execution, progress, readiness, validation, context. This replaces the single "status" field that most task systems use, enabling nuanced decisions like "this task is ready for review but blocked by a dependency."

- **kb_sync.py replaces LLM-based entity extraction**: LightRAG's LLM extraction (hermes 7B) produced inconsistent results across runs. kb_sync extracts relationships from the KB's explicit `## Relationships` sections — zero randomness, zero model dependency. 1,545 entities, 2,295 relationships from 219 KB entries.

- **Dual-board synchronization**: Plane (PM board, human-driven planning with sprints, epics, velocity) syncs bidirectionally with Mission Control (ops board, agent-driven execution with tasks, dispatches, heartbeats). 5 sync mechanisms: structural, state, semantic, event-driven, intent.

- **Local-first inference strategy**: LocalAI (hermes-3b for queries, bge-m3 for embeddings, bge-reranker for reranking) handles routine work. Claude handles complex reasoning. Silent heartbeats for idle agents save 70% cost.

- **IaC-only operations**: No manual commands. Everything scripted in `scripts/` (42+ scripts). Zero to running fleet via `setup.sh`.

- **Immune system from devops-control-plane**: doctor.py implements 3-strike rule, task state anomaly detection, behavioral security — codified from 24 rules derived from 16 post-mortems and agent death analysis.

## Deep Analysis

### Orchestrator 9-Step Cycle

Every 30 seconds (configurable: turbo=5s, standard=30s, economic=60s):
1. Storm monitor evaluation
2. Gateway duplication check
3. Fleet mode gate
4. Refresh agent contexts (pre-embed full per-agent data to disk)
5. Security scan (behavioral security on new/changed tasks)
6. Doctor run (immune system: detect + respond to anomalies)
7. Ensure review approvals
8. Wake drivers (alert fleet-ops and PM about pending work)
9. Dispatch ready tasks (unblocked inbox tasks, max 2/cycle)
10. Process directives (parse PO directives from board memory)
11. Evaluate parents (when all children done, parent moves to review)
12. Health check (detect stuck tasks, offline agents)

### Service Infrastructure

| Service | Port | Purpose |
|---------|------|---------|
| Mission Control API | 8000 | FastAPI backend |
| Mission Control UI | 3000 | Next.js frontend |
| Open Gateway | ws://18789 | Agent sessions, heartbeats |
| IRC (miniircd) | 6667 | 10 channels: #fleet, #alerts, #reviews, etc. |
| The Lounge | 9000 | Web IRC client |
| LocalAI | 8090 | 9 models loaded |
| LightRAG | 9621 | Knowledge graph + API |
| PostgreSQL | 5432 | Mission Control DB |
| Redis | 6379 | Caching, RQ queue |

### Knowledge Base

219+ KB entries in `docs/knowledge-map/kb/` organized by branches (systems, tools, hooks, commands, skills, plugins, infrastructure). kb_sync parses these into LightRAG graph. Also indexes AICP SKILL.md files (78 skills from devops-expert-local-ai).

### Four-Project Ecosystem

| Project | Repo | Purpose |
|---------|------|---------|
| Fleet | openfleet | Agent operations, orchestrator, infrastructure |
| AICP | devops-expert-local-ai | AI Control Platform, LocalAI independence |
| DSPD | devops-solution-product-development | Project management via Plane |
| Research Wiki | devops-solutions-research-wiki | Knowledge synthesis, central intelligence spine |

## Open Questions

- What is the optimal heartbeat frequency per agent role for cost vs responsiveness?
- How does fleet performance scale beyond 10 agents (20, 50)?
- Can the deterministic brain's 9-step cycle be extended with plugin hooks?
- What is the failure mode when LightRAG and LocalAI are both down?

## Relationships

- IMPLEMENTS: OpenClaw
- USED BY: AI-Driven Content Pipeline
- BUILDS ON: LightRAG
- BUILDS ON: AICP
- RELATES TO: Plane
- RELATES TO: devops-control-plane
- ENABLES: Claude Code Skills
- RELATES TO: LLM Wiki Pattern
- FEEDS INTO: Wiki Knowledge Graph

## Backlinks

[[OpenClaw]]
[[AI-Driven Content Pipeline]]
[[LightRAG]]
[[AICP]]
[[Plane]]
[[devops-control-plane]]
[[Claude Code Skills]]
[[LLM Wiki Pattern]]
[[Wiki Knowledge Graph]]
[[Always Plan Before Executing]]
[[Claude Code]]
[[Claude Code Scheduling]]
[[Context Management Is the Primary LLM Productivity Lever]]
[[Harness Engineering]]
[[LLM-Maintained Wikis Outperform Static Documentation]]
[[Local LLM Quantization]]
[[MCP Integration Architecture]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[Plan Execute Review Cycle]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Synthesis: Claude Code Harness Engineering]]
[[Synthesis: Gemma 4 + SearXNG for Free Private OpenClaw]]
