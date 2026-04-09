---
title: "Model Guide: Ecosystem Architecture"
type: learning-path
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [ecosystem, model-guide, learning-path, openfleet, aicp, openarms, devops-control-plane, multi-project, integration, spine]
---

# Model Guide: Ecosystem Architecture

## Summary

The Ecosystem Architecture model describes how five projects — OpenFleet, AICP, devops-control-plane, the research wiki, and OpenArms — form a self-sustaining system where each project has a single primary role and defined integration points. OpenFleet runs the agents. AICP routes inference cheaply. devops-control-plane holds operational wisdom. The wiki synthesizes knowledge and feeds the agent intelligence graph. OpenArms provides multi-channel personal access. Projects integrate via files and shared protocols, not tightly coupled APIs — enabling independent evolution while maintaining system coherence. This model is the map of the entire ecosystem: understand it to understand why each other model in this wiki exists.

## Prerequisites

- Familiarity with the concept of AI agent fleets (multiple specialized agents working on shared infrastructure)
- Basic understanding of the four-project context (you are a user of at least one of these projects)
- No deep knowledge of any individual project required — this model is the starting point for ecosystem orientation

## Sequence

### L1 — Primary Sources

- `wiki/sources/src-openfleet-local.md` — OpenFleet CLAUDE.md; the authoritative definition of the orchestration system, agent roles, and fleet architecture
- `wiki/sources/src-aicp-local.md` — AICP CLAUDE.md; the AI control platform, local inference routing, and cost reduction model
- `wiki/sources/src-openarms-local.md` — OpenArms documentation; multi-channel access, the personal AI assistant layer
- `wiki/sources/src-devops-control-plane-local.md` — devops-control-plane README; the operational governance origin

### L2 — Core Concepts

Read in this order:

1. **Four-Project Ecosystem** ([[Four-Project Ecosystem]]) — The complete ecosystem map: each project's role, architecture, integration points, and the file-based coupling model. The wiki as active intelligence infrastructure (not passive docs). All projects running on WSL2 on a single machine. Start here.
2. **OpenFleet** ([[OpenFleet]]) — The agent workforce: 10 specialized agents, deterministic orchestrator (zero LLM calls, 30s cycle), seven-layer architecture, dual-board synchronization with Plane, LightRAG knowledge graph integration.
3. **AICP** ([[AICP]]) — The AI control platform: LocalAI for routine inference, Claude for complex reasoning, 5-stage cost reduction roadmap targeting 80%+ Claude token reduction, skills export to fleet agent tooling.
4. **OpenArms** (`wiki/domains/devops/openarms.md`) — Multi-channel AI access: 20+ messaging channels (Telegram, Discord, Slack, iMessage) routing to the same agent runtime; personal AI assistant layer; how the human interacts with the fleet from any device.
5. **OpenClaw** ([[OpenClaw]]) — The WebSocket gateway that all Claude Code fleet agents connect through; the connection layer between Mission Control and individual agents.
6. **devops-control-plane** ([[devops-control-plane]]) — The operational DNA donor: 24 rules from 16 post-mortems became OpenFleet's immune system (doctor.py); where lessons become law; the governance origin point.
7. **Multi-Channel AI Agent Access** (`wiki/domains/ai-agents/multi-channel-ai-agent-access.md`) — How OpenArms routes messages across channels to the same underlying agent runtime; the channel-agnostic agent model.
8. **Immune System Rules** ([[Immune System Rules]]) — How operational post-mortems become enforceable fleet governance rules; the doctor.py implementation; the control-plane → OpenFleet knowledge flow.

### L3 — Comparisons

- **Wiki Knowledge Graph** ([[Wiki Knowledge Graph]]) — How the wiki's `## Relationships` sections are parsed by kb_sync.py into the LightRAG graph that feeds OpenFleet's agent intelligence.

### L4 — Lessons (Validated Insights)

- **Lesson: Automation Is the Bridge Between Knowledge and Action** (`wiki/lessons/lesson-hub-—-automation.md`) — The ecosystem thesis: knowledge in the wiki only has value if it crosses into agent behavior; automation is the bridge.

### L5 — Patterns (Structural Templates)

- **Gateway-Centric Routing** ([[Gateway-Centric Routing]]) — OpenClaw as the single connection point for all fleet agents; why gateway-centricity simplifies fleet governance and observability.
- **Deterministic Shell + LLM Core** ([[Deterministic Shell, LLM Core]]) — The architectural pattern that makes the fleet reliable: deterministic orchestrator handles all operational mechanics (state, dispatch, budget, security); LLM handles only reasoning where determinism is insufficient.

## Project Integration Map

For quick reference when navigating cross-project work:

| From | To | Mechanism | What Transfers |
|------|----|-----------|---------------|
| Wiki | OpenFleet | kb_sync.py reads `## Relationships` | 2,295 explicit relationships → LightRAG graph |
| AICP | Fleet agents | Skills export | Tooling and inference profiles |
| devops-control-plane | OpenFleet | doctor.py import | 24 governance rules from post-mortems |
| OpenFleet | AICP | Inference routing | Tasks dispatched to LocalAI vs Claude by complexity |
| OpenArms | Fleet | WebSocket via OpenClaw | User messages from 20+ channels |

## Outcomes

After completing this learning path you will understand:

- Each project's single primary role and why minimal overlap is a deliberate design choice
- The file-based integration model: why projects communicate via files and shared protocols rather than coupled APIs
- How the wiki functions as active intelligence infrastructure — not documentation, but a live knowledge graph that feeds agent decision-making
- The deterministic shell + LLM core pattern: what the orchestrator handles without LLM calls, and where LLM reasoning is genuinely needed
- The cost economics: how AICP's local inference routing makes running 10 agents continuously financially sustainable
- How OpenArms completes the human interface layer: any device, any messaging channel, same agent runtime
- Why the control-plane → OpenFleet knowledge flow is the ecosystem's operational immune system

## Relationships

- FEEDS INTO: [[Model Guide: Claude Code]]
- FEEDS INTO: [[Model Guide: LLM Wiki]]
- FEEDS INTO: [[Model Guide: Methodology]]
- BUILDS ON: [[Four-Project Ecosystem]]
- BUILDS ON: [[OpenFleet]]
- BUILDS ON: [[Gateway-Centric Routing]]
- BUILDS ON: Deterministic Shell + LLM Core
- RELATES TO: [[Model Guide: MCP + CLI Integration]]
- RELATES TO: [[Model Guide: Skills + Commands + Hooks]]

## Backlinks

[[Model Guide: Claude Code]]
[[Model Guide: LLM Wiki]]
[[Model Guide: Methodology]]
[[Four-Project Ecosystem]]
[[OpenFleet]]
[[Gateway-Centric Routing]]
[[Deterministic Shell + LLM Core]]
[[Model Guide: MCP + CLI Integration]]
[[Model Guide: Skills + Commands + Hooks]]
[[Model Guide: Second Brain]]
[[Model: Claude Code]]
[[Model: LLM Wiki]]
