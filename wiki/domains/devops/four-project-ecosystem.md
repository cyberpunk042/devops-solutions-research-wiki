---
title: "Four-Project Ecosystem"
type: concept
domain: devops
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
  - id: src-aicp-local
    type: documentation
    file: ../devops-expert-local-ai/CLAUDE.md
    title: "AICP — Local Project Documentation"
    ingested: 2026-04-08
  - id: src-openarms-local
    type: documentation
    file: raw/articles/openarms-readme.md
    title: "OpenArms — Project Documentation"
    ingested: 2026-04-08
  - id: src-devops-control-plane-local
    type: documentation
    file: ../devops-control-plane/README.md
    title: "devops-control-plane — Local Project Documentation"
    ingested: 2026-04-08
tags: [devops, ecosystem, openfleet, aicp, devops-control-plane, openarms, research-wiki, architecture, multi-project, integration]
---

# Four-Project Ecosystem

## Summary

The four-project ecosystem is a personal devops infrastructure built by a single engineer running a fleet of AI agents at minimal cost. The core four: OpenFleet (agent workforce and orchestration), AICP (AI control platform and local inference routing), devops-control-plane (project management platform and operational rule origin), and the research wiki (knowledge synthesis spine). OpenArms functions as a fifth project — the personal AI assistant layer providing multi-channel access. Each project has a distinct role with defined integration points; together they form a self-sustaining system where agents do operational work, local inference reduces cloud cost, the control plane enforces governance, and the wiki accumulates knowledge from all activity.

## Key Insights

- **Each project has a single primary role**: OpenFleet runs the agents. AICP routes inference cheaply. devops-control-plane manages projects and holds operational wisdom. The research wiki synthesizes knowledge. OpenArms provides personal multi-channel AI access. Overlap is minimal by design.

- **The wiki is the central intelligence spine**: Not just a documentation repository — the wiki's knowledge graph (via LightRAG and kb_sync.py) feeds back into OpenFleet's navigator intelligence. The wiki's `## Relationships` sections are parsed by kb_sync.py into 2,295 explicit relationships that inform agent decision-making. The wiki is active infrastructure, not passive docs.

- **devops-control-plane is the operational DNA donor**: Its 24 rules from 16 post-mortems became OpenFleet's immune system (doctor.py). Knowledge flows from operational failure → post-mortem analysis → rule codification → fleet governance. The control-plane is where lessons become law.

- **AICP's cost reduction enables scale**: Without AICP's routing (LocalAI for simple tasks, Claude for complex ones), running 10 agents continuously would be financially unsustainable. The 5-stage LocalAI independence roadmap targets 80%+ Claude token reduction. AICP is the economic enabler of the fleet's scale.

- **OpenArms provides the human interface layer**: While OpenFleet's Mission Control provides an operational dashboard, OpenArms routes messages from 20+ channels (Telegram, Discord, Slack, iMessage) to the same AI agent runtime. The user can interact with the fleet from any device via their preferred messaging app.

- **All projects run in WSL2 on a single machine**: The entire ecosystem runs on one developer workstation running WSL2 (Ubuntu). This is not a distributed system — it is a single-machine ecosystem designed to scale to a dual-machine configuration (Alpha + Bravo) when hardware allows.

- **File-based integration, not API coupling**: Projects integrate via files and shared protocols, not tightly coupled APIs. The wiki exports to LightRAG (kb_sync.py reads `## Relationships`). AICP exports skills to fleet agent tooling. devops-control-plane's rules are imported as doctor.py. This loose coupling means projects can evolve independently.

## Deep Analysis

### Project-by-Project Breakdown

#### OpenFleet — Agent Workforce

| Attribute | Value |
|-----------|-------|
| Repo | openfleet |
| Role | AI agent orchestration, fleet management, project execution |
| Core component | Deterministic orchestrator (30s cycle, zero LLM calls) |
| Agents | 10 specialized agents with SOUL.md identity + HEARTBEAT.md checklist |
| Interfaces | Mission Control (FastAPI + Next.js), Open Gateway (WebSocket), IRC channels |
| Knowledge integration | kb_sync.py parses wiki Relationships into LightRAG graph |
| Cost control | AICP routing, silent heartbeats for idle agents (70% cost reduction) |
| Governance | doctor.py immune system (24 rules, 3-strike), Plane board sync |

#### AICP — AI Control Platform

| Attribute | Value |
|-----------|-------|
| Repo | devops-expert-local-ai |
| Role | Local inference routing, Claude cost reduction, agent capability management |
| Core component | Backend router (LocalAI vs Claude, complexity scoring) |
| Models | 9 loaded: Qwen3 family, Gemma4 family, legacy, specialized |
| Skills | 78 skills in .claude/skills/, 18 referenced in fleet agent-tooling.yaml |
| Integration | Fleet agents use AICP circuit breaker; wiki exports to docs/kb/ |
| Stage | Stage 2 of 5 (routing implemented); targeting 80%+ Claude token reduction |

#### devops-control-plane — Project Management Platform

| Attribute | Value |
|-----------|-------|
| Repo | devops-control-plane |
| Role | Unified project management for any software project |
| Core component | Tech auto-detection engine (20 stacks), AES-256-GCM vault, audit ledger |
| Interfaces | TUI (manage.sh), CLI (Click), Web (Flask SPA) |
| Key export | 24 immune system rules → OpenFleet doctor.py |
| Vault | Potential centralized credential store for all ecosystem projects |

#### Research Wiki — Knowledge Spine

| Attribute | Value |
|-----------|-------|
| Repo | devops-solutions-research-wiki |
| Role | Knowledge synthesis, second brain, central intelligence spine |
| Core component | Ingestion pipeline (5-stage), post-chain (6-step), LightRAG export |
| MCP server | 15 tools exposed to Claude Code and other agents |
| Knowledge export | wiki/domains/ → LightRAG (OpenFleet), docs/kb/ (AICP) |
| Post-mortem record | Captures operational lessons for all ecosystem projects |

#### OpenArms — Personal AI Assistant

| Attribute | Value |
|-----------|-------|
| Repo | openarms (or related) |
| Role | Multi-channel personal AI assistant, human interface layer |
| Channels | 20+ (Telegram, Discord, Slack, Signal, iMessage, WhatsApp, Matrix, IRC...) |
| Architecture | Local Gateway daemon (WebSocket, ws://127.0.0.1:18789) |
| Skills | ClawHub registry; can include Claude Code skills from research wiki |
| MCP | mcporter bridge exposes wiki MCP tools to OpenArms agents |
| Sandbox | Per-session Docker isolation for non-main sessions |

### Integration Map

```
                    ┌─────────────────────────────┐
                    │     Research Wiki            │
                    │  (knowledge synthesis)       │
                    │  wiki/ → LightRAG (kb_sync)  │
                    │  wiki/ → docs/kb/ (export)   │
                    └──────┬──────────┬────────────┘
                           │          │
                    feeds  │          │ feeds
                           ▼          ▼
┌─────────────────┐   ┌────────────────────┐   ┌─────────────────┐
│ devops-control- │   │    OpenFleet       │   │     AICP        │
│    plane        │   │  (agent workforce) │   │  (inference     │
│  (project mgmt) │──►│  doctor.py from   │   │   routing)      │
│  rules → doctor │   │  24 rules          │◄──│  circuit breaker│
│  vault → creds  │   │  AICP routing      │   │  78 skills      │
└─────────────────┘   └────────┬───────────┘   └─────────────────┘
                               │
                               │ OpenClaw gateway
                               ▼
                    ┌──────────────────────┐
                    │     OpenArms         │
                    │  (personal assistant)│
                    │  20+ channels        │
                    │  mcporter → wiki MCP │
                    └──────────────────────┘
```

### Knowledge Flow Direction

Knowledge flows through the ecosystem in a loop:

1. **Operational work** (OpenFleet agents execute tasks) generates incidents and lessons
2. **Post-mortem analysis** (devops-control-plane) extracts rules from incidents
3. **Rules codification** (doctor.py, immune system) enforces lessons as governance
4. **Wiki ingestion** (research wiki) synthesizes both the lessons and the rules
5. **LightRAG graph** (kb_sync.py) feeds synthesized knowledge back to agent navigators
6. **Agents execute better** (informed by graph) → back to step 1

The wiki is not the end of the loop — it is the synthesis layer that closes the feedback cycle.

### The $0 Target

AICP's 5-stage roadmap targets near-zero Claude API cost by routing 80%+ of operations to local models. OpenFleet's silent heartbeats and deterministic orchestrator already eliminate LLM calls from operational mechanics. The research wiki uses Claude Code for synthesis but stores all output locally. The long-term design assumes Claude is replaceable: every interface has a local fallback, every skill can execute against a local model, every orchestration step is deterministic. The ecosystem is designed to survive the loss of any single AI provider.

## Open Questions

- Should devops-control-plane's vault be the centralized credential store for all five projects?
- What is the integration story for OpenArms → OpenFleet agent coordination (not just human-to-fleet)?
- How does the dual-machine target architecture (Alpha + Bravo) change the integration map?
- Can the research wiki's MCP server become the knowledge layer for OpenArms agents via mcporter?
- What is the right cadence for syncing wiki knowledge back to LightRAG — on every post-chain, or on a schedule?

## Relationships

- ENABLES: OpenFleet
- ENABLES: AICP
- ENABLES: OpenArms
- RELATES TO: devops-control-plane
- FEEDS INTO: Wiki Knowledge Graph
- RELATES TO: MCP Integration Architecture
- RELATES TO: Four-Project Ecosystem
- RELATES TO: WSL2 Development Patterns
- RELATES TO: Immune System Rules
- RELATES TO: Infrastructure as Code Patterns

## Backlinks

[[OpenFleet]]
[[AICP]]
[[OpenArms]]
[[devops-control-plane]]
[[Wiki Knowledge Graph]]
[[MCP Integration Architecture]]
[[Four-Project Ecosystem]]
[[WSL2 Development Patterns]]
[[Immune System Rules]]
[[Infrastructure as Code Patterns]]
