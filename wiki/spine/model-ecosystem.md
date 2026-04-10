---
title: "Model: Ecosystem Architecture"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-10
sources:
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
  - id: src-devops-control-plane-local
    type: documentation
    file: ../devops-control-plane/README.md
    title: "devops-control-plane — Local Project Documentation"
tags: [ecosystem, model, openfleet, aicp, openarms, devops-control-plane, multi-project, integration, spine, architecture]
---

# Model: Ecosystem Architecture

## Summary

The Ecosystem Architecture model describes how five projects — OpenFleet, AICP, devops-control-plane, the research wiki, and OpenArms — form a self-sustaining system where each project has a single primary role and defined integration points. Projects integrate via files and shared protocols, not tightly coupled APIs — enabling independent evolution while maintaining system coherence. ==This model is the map of the entire ecosystem: understand it to understand why every other spine model exists.==

## Key Insights

- **Minimal overlap is a design constraint, not an accident.** Each project does one thing. When a project starts doing what another is responsible for, the integration contract breaks. Single-responsibility is what makes the ecosystem evolvable.

- **The wiki is active infrastructure, not passive docs.** The wiki's `## Relationships` sections are parsed by `kb_sync.py` into a LightRAG knowledge graph feeding OpenFleet's navigator. Every wiki page added is a node in the fleet's intelligence graph.

- **devops-control-plane is the operational DNA donor.** 24 rules from 16 post-mortems became OpenFleet's immune system. Knowledge flows: failure → post-mortem → rule → enforcement.

- **AICP is the economic enabler.** Without local inference routing, 10 continuous agents at Claude API rates is unsustainable. The 5-stage LocalAI roadmap targets 80%+ cost reduction.

- **File-based integration is the coherence mechanism.** Markdown exports, LightRAG graph, JSON manifests — not APIs. Any project can be replaced without cascading failures.

## Deep Analysis

### The Five Projects

---

#### OpenFleet — The Agent Workforce

> [!info] **"Vibe Managing" — governing 10 specialized agents via declarative systems**
> A deterministic orchestrator (zero LLM calls, pure Python, 30-second cycle) handles: state diffing, budget gating, heartbeat scheduling, task dispatch, security scanning, anomaly detection. LLM calls happen only inside individual agent executions.

10 agents: fleet-ops, project-manager, devsecops-expert, architect, software-engineer, qa-engineer, devops, technical-writer, ux-designer, accountability-generator. Each has a `SOUL.md` (identity) and `HEARTBEAT.md` (periodic checklist). Connected through OpenClaw (WebSocket gateway), managed via Mission Control UI.

See [[OpenFleet]] for the seven-layer stack and LightRAG integration.

---

#### AICP — The AI Control Platform

> [!info] **Complexity-based inference routing — LocalAI for routine, Claude for complex**
> Complexity scorer assigns 0-10. Below threshold → local (free). Above → Claude (billed). Costs scale with task complexity, not request volume.

5-stage roadmap: routine tasks → complex reasoning → 78 skills migrated → voice pipeline → full local-first. At completion: 80%+ Claude API cost reduction.

See [[AICP]] for routing logic, circuit breaker, and the independence roadmap.

---

#### devops-control-plane — Operational Governance Origin

> [!info] **16 post-mortems → 24 rules → OpenFleet's immune system**
> Not a monitoring system — a governance codification system. When something goes wrong, the lesson gets extracted, formalized as a rule, and committed. `doctor.py` enforces these rules on every agent action.

See [[Immune System Rules]] for the 24 rules and their origins.

---

#### Research Wiki — Central Intelligence Spine

> [!info] **Dual role: knowledge synthesis + agent intelligence**
> 1. Raw sources → structured pages (concepts, lessons, patterns, decisions) via ingestion + evolution pipeline
> 2. `## Relationships` → `kb_sync.py` → LightRAG graph → OpenFleet navigator intelligence

The wiki is not documentation. It is infrastructure that feeds agent intelligence. Every page, relationship, and promoted pattern strengthens fleet decision-making.

---

#### OpenArms — Personal AI Assistant Layer

> [!info] **Multi-channel access to the agent runtime from any device**
> Routes messages from 20+ channels (Telegram, Discord, Slack, iMessage) to the same agent runtime via OpenClaw. Channel is irrelevant — same intelligence responds regardless of interface.

Completes the human interface layer. The fleet operates autonomously; the human inspects, directs, and queries from any messaging channel.

---

### The Integration Map

> [!info] **How projects connect**
> | From | To | Mechanism | What transfers |
> |------|----|-----------|----------------|
> | Wiki | OpenFleet | `kb_sync.py` reads `## Relationships` | Knowledge graph edges → LightRAG navigation |
> | devops-control-plane | OpenFleet | `doctor.py` rule import | 24 governance rules from 16 post-mortems |
> | AICP | Fleet agents | Skills export | Inference profiles + tooling configurations |
> | OpenFleet | AICP | Task dispatch | Tasks routed by complexity score to LocalAI vs Claude |
> | OpenArms | Fleet via OpenClaw | WebSocket | User messages from 20+ channels → agent runtime |
> | Wiki | AICP | File export | `docs/kb/` via export profile for agent knowledge base |

---

### The Knowledge Feedback Loop

> [!abstract] **The self-reinforcing cycle that compounds ecosystem value**
> 1. **Operations generate events** — agents execute tasks, encounter failures, hit edge cases
> 2. **Events generate lessons** — post-mortems extract principles; successful patterns get documented
> 3. **Lessons enter the wiki** — structured pages with relationships, scored for evolution
> 4. **Wiki feeds the fleet** — `kb_sync.py` parses relationships into LightRAG; evolved pages become high-value graph nodes
> 5. **Fleet makes better decisions** — navigator intelligence improves as the graph densifies

> [!warning] **This loop means wiki health directly affects fleet quality**
> A sparse, poorly linked wiki → sparse knowledge graph → uninformed agent decisions. A dense, well-evolved wiki → rich graph → contextually grounded decisions. The wiki is not optional infrastructure — it is the fleet's intelligence source.

---

### The Deterministic Shell + LLM Core Pattern

The [[Deterministic Shell, LLM Core]] pattern appears throughout the ecosystem:

> [!info] **Four implementations of the same pattern**
> | System | Deterministic shell | LLM core | What it prevents |
> |--------|-------------------|----------|-----------------|
> | OpenFleet orchestrator | Python: state diff, budget, heartbeat, dispatch, security, anomaly | Individual agent execution | Hallucinated orchestration state |
> | AICP complexity scorer | 0-10 scoring, threshold routing | Agent task execution | LLM deciding its own routing |
> | Wiki evolution scorer | 6 deterministic signals, composite ranking | Page generation after selection | LLM picking its own evolution candidates |
> | doctor.py governance | 24 static rules, pure conditionals | Agent actions being governed | LLM reasoning around safety rules |

> [!tip] **Why this pattern matters**
> Deterministic shells are predictable, auditable, cheap, immune to hallucination. LLM cores are contextually intelligent, expensive, probabilistic. Separating them gives reliability AND intelligence without the failure modes of either.

---

### File-Based Coupling

> [!tip] **Projects communicate via files and shared protocols, not tight API contracts**
> - **Wiki → OpenFleet**: `kb_sync.py` reads `wiki/` for `## Relationships`. No API, no service dependency.
> - **devops-control-plane → OpenFleet**: rules are static files `doctor.py` imports at runtime
> - **Wiki → AICP**: `tools/export.py` writes to `docs/kb/`. AICP reads at its own cadence.
> - **OpenFleet → OpenClaw**: WebSocket protocol. Agents connect as clients. Gateway is lightweight, not a service mesh.
>
> Any component can be taken offline, rewritten, or replaced without cascading failures. The interfaces are durable even when implementations change.

---

### WSL2 Deployment Reality

All five projects run on a single machine: WSL2 on Windows. This is intentional for a single-engineer ecosystem.

> [!info] **Practical implications**
> | Aspect | How it works |
> |--------|-------------|
> | **File watching** | WSL2 inotify → `tools/watcher.py` triggers post-chain on wiki edits |
> | **Sync boundary** | `tools/sync.py` maintains wiki in WSL2 (tooling) + Windows (Obsidian) |
> | **Cost model** | Local inference via LocalAI, fleet via WebSocket, wiki via file ops — all on one machine |
> | **Service management** | `python -m tools.setup --services` deploys systemd user services reproducibly |

---

### Key Pages

| Page | Layer | Role in the model |
|------|-------|-------------------|
| [[Four-Project Ecosystem]] | L2 | The foundational concept — why 5 projects, single responsibility per project |
| [[OpenFleet]] | L2 | Agent workforce — 10 agents, deterministic orchestrator, OpenClaw |
| [[AICP]] | L2 | Inference routing — complexity scorer, LocalAI independence roadmap |
| [[Immune System Rules]] | L2 | 24 governance rules from 16 post-mortems |
| [[OpenArms]] | L2 | Multi-channel personal access via OpenClaw |
| [[Gateway-Centric Routing]] | L5 | Pattern: single gateway for fleet governance |
| [[Deterministic Shell, LLM Core]] | L5 | Pattern: deterministic orchestration wrapping LLM reasoning |
| [[Scaffold → Foundation → Infrastructure → Features]] | L5 | Pattern: universal build lifecycle across all 5 projects |
| [[Decision: Wiki-First with LightRAG Upgrade Path]] | L6 | Scale decision for wiki → fleet knowledge integration |

---

### Lessons Learned

| Lesson | What was learned |
|--------|-----------------|
| [[Infrastructure Must Be Reproducible, Not Manual]] | All 5 projects deploy via IaC tooling, not manual config. Learned from early sync service failures. |
| [[The Agent Must Practice What It Documents]] | The wiki documents methodology that all projects follow. When the wiki agent didn't follow its own rules, the entire ecosystem's credibility was undermined. |
| [[Models Are Built in Layers, Not All at Once]] | The ecosystem itself was built in SFIF layers — scaffold (5 project shells), foundation (core tooling), infrastructure (integration points), features (agent fleet + evolution pipeline). |

---

### State of Knowledge

> [!success] **Well-covered**
> - Five-project topology with single-responsibility roles
> - Integration map with concrete mechanisms (kb_sync, doctor.py, export profiles)
> - Knowledge feedback loop (operations → lessons → wiki → fleet → better decisions)
> - Deterministic shell + LLM core pattern across 4 implementations
> - File-based coupling model (durable interfaces, replaceable implementations)
> - WSL2 deployment reality

> [!warning] **Thin or unverified**
> - `kb_sync.py` performance at scale — untested beyond 200 pages
> - OpenArms routing to specialized agent pools — single runtime currently
> - AICP ↔ OpenFleet integration formality — currently informal skills export + dispatch
> - Cross-wiki evolution — can AICP's wiki evolve from this wiki's pages?
> - Multi-machine deployment — everything is single-machine currently; no distributed architecture tested

---

### How to Adopt

> [!info] **Replicating the ecosystem pattern for a new multi-project system**
> 1. **Define single responsibilities** — one project per concern. If two projects overlap, merge or split until overlap is zero.
> 2. **Choose file-based integration** — markdown exports, JSON manifests, shared protocols. No tight API coupling between projects.
> 3. **Establish the knowledge spine first** — the wiki (or equivalent) feeds everything else. Without the knowledge loop, projects evolve in isolation.
> 4. **Extract governance from failures** — post-mortems → rules → enforcement. The devops-control-plane pattern.
> 5. **Apply deterministic shell + LLM core** — orchestration is deterministic. Reasoning is LLM. Never mix them.

> [!warning] **INVARIANT — never change these**
> - Single responsibility per project (overlap = integration debt)
> - File-based integration (tight coupling = cascading failures)
> - Knowledge loop active (wiki feeds fleet intelligence, not just human reading)
> - Deterministic orchestration (no LLM in the orchestration loop)
> - Governance from real failures (rules from post-mortems, not from theory)

> [!tip] **PER-PROJECT — always adapt these**
> - Which projects exist (not every ecosystem needs 5 — start with wiki + one operational project)
> - Integration mechanisms (kb_sync is this ecosystem's; yours may be different)
> - Deployment model (single-machine WSL2 is this ecosystem's; cloud or multi-machine may be yours)
> - Agent count and specialization (10 agents is OpenFleet's; start with 1-3)

## Open Questions

> [!question] **Will `kb_sync.py` scale beyond 200 pages?**
> Full-graph parse on every sync may need to shift to incremental updates. What's the performance boundary? (Requires: benchmarking at 200, 500, 1000 pages)

> [!question] **How does OpenArms routing evolve with specialized agent pools?**
> Currently routes to a single runtime. If OpenFleet scales to domain-specific pools, OpenArms needs routing intelligence. (Requires: multi-pool architecture design)

> [!question] **Should AICP ↔ OpenFleet have a formal integration contract?**
> Currently informal. As both mature, is an explicit contract (API spec, version compatibility) worth the coupling cost? (Requires: assessing integration friction)

## Relationships

- BUILDS ON: [[Four-Project Ecosystem]]
- BUILDS ON: [[OpenFleet]]
- BUILDS ON: [[AICP]]
- BUILDS ON: [[Immune System Rules]]
- BUILDS ON: [[Gateway-Centric Routing]]
- BUILDS ON: [[Deterministic Shell, LLM Core]]
- RELATES TO: [[Model: MCP and CLI Integration]]
- RELATES TO: [[Model: Knowledge Evolution]]
- RELATES TO: [[Model: Skills, Commands, and Hooks]]
- RELATES TO: [[Model: Methodology]]
- FEEDS INTO: [[Model: Claude Code]]
- FEEDS INTO: [[Model: LLM Wiki]]

## Backlinks

[[Four-Project Ecosystem]]
[[OpenFleet]]
[[AICP]]
[[Immune System Rules]]
[[Gateway-Centric Routing]]
[[Deterministic Shell, LLM Core]]
[[Model: MCP and CLI Integration]]
[[Model: Knowledge Evolution]]
[[Model: Skills, Commands, and Hooks]]
[[Model: Methodology]]
[[Model: Claude Code]]
[[Model: LLM Wiki]]
