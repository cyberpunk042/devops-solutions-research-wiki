---
title: "Model: SFIF and Architecture"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-10
sources: []
tags: [model, spine, sfif, architecture, quality-tiers, build-lifecycle, skyscraper, pyramid, mountain, recursive, cross-domain]
---

# Model: SFIF and Architecture

## Summary

The SFIF and Architecture model describes the universal 4-stage build lifecycle (Scaffold → Foundation → Infrastructure → Features) and the 3-tier quality analogy (Skyscraper/Pyramid/Mountain) that together form a complete framework for building, auditing, and improving software systems. ==SFIF is recursive — it applies at project, feature, component, and design levels simultaneously, each advancing at its own pace.== The four ecosystem projects each have documented SFIF instances making the abstract pattern concrete.

## Key Insights

- **The pattern is recursive by design.** A backend may be Skyscraper-tier while the frontend it serves is Mountain-tier. "Where is this project?" requires specifying the layer of granularity.

- **Stage boundaries are structural commitments, not completion percentages.** Foundation is complete when there's a single entry point — not when 70% of code is written. Exit criteria are about stability, not volume.

- **Mountain is the natural entropy state.** POC decisions never revisited. Hotfixes layered. Features added without structural investment. SFIF prevents the default entropy.

- **Pyramid is the practitioner's art.** Improving a Mountain into a Pyramid without stopping delivery — principled compromises around immovable constraints. Most real engineering lives here.

- **POC → Production without rewrite is the critical failure pattern.** Mountain code deployed as production, then scaled as if Skyscraper, produces emergency rewrites at 10x cost.

## Deep Analysis

### The Four SFIF Stages

> [!info] **Four stages with structural exit criteria**
> | Stage | Question it answers | Exit criterion | What it is NOT |
> |-------|-------------------|---------------|----------------|
> | **Scaffold** | "Where is this project headed?" | Direction decided, documented. Project is *joinable*. | Running code |
> | **Foundation** | "Does this work at its simplest?" | Single entry point manages everything. System is *operable*. | All functionality implemented |
> | **Infrastructure** | "Can other things depend on this?" | Cross-cutting concerns handled transparently. System is *dependable*. | Features |
> | **Features** | "What specialized value does this deliver?" | No terminal criterion — ongoing work on the stable base. | Infrastructure |

> [!warning] **The Infrastructure/Feature boundary is the most commonly violated**
> Infrastructure ENABLES. Features USE what infrastructure enables. Auth logic in a feature controller = infrastructure that was skipped. Retry logic in every API call = infrastructure that was never built.

See [[Scaffold → Foundation → Infrastructure → Features]] for full stage descriptions, anti-patterns per stage, and the recursive property.

---

### The Three Quality Tiers

> [!success] **Skyscraper — all SFIF stages complete and clean**
> Scaffold artifacts exist and are current. Single entry point. Infrastructure is stable. Features build clearly on infrastructure. The system can grow upward without structural compromise. Requires conditions: greenfield, authorized refactor, or layer-by-layer rebuild.

> [!warning] **Pyramid — functional, built around real constraints**
> Legacy database that can't be migrated. Team that can't pause delivery. Third-party integration forcing compromise. ==Pyramid decisions are principled (tradeoff understood and documented), not random (tradeoff unknown).== Pyramid is not failure — it is the art of improving a Mountain without stopping delivery.

> [!bug]- **Mountain — accumulated mass, no structure**
> Spaghetti code, deprecated patterns on ad-hoc fixes, no scaffold or stale scaffold, multiple entry points, auth everywhere, no consistent error handling. Works, but only the builders understand why. Mountain is what happens when SFIF stages get skipped.
>
> **Mountain is reversible** — but the reversal is expensive. The correct path: Mountain → Pyramid (stabilize around constraints) → Skyscraper (when conditions allow full refactor).

See [[Skyscraper, Pyramid, Mountain]] for the full tier analysis and the improvement path.

---

### The Four Ecosystem Instances

> [!info] **SFIF across the ecosystem**
> | Project | Scaffold | Foundation | Infrastructure | Features |
> |---------|----------|-----------|----------------|----------|
> | **Research Wiki** | CLAUDE.md, wiki/ structure, schema | tools/common.py, validation, manifest.json | pipeline.py post-chain, MCP server, lint, obsidian | Evolve pipeline, watcher, sync, export |
> | **OpenFleet** | SOUL.md + HEARTBEAT.md, monorepo layout | Deterministic orchestrator, agent base model | doctor.py (24 rules), IRC routing, OpenClaw gateway | 10 specialized agents, Mission Control UI |
> | **AICP** | Profile system, CLAUDE.md, venv | Backend router, circuit breaker, complexity scorer | MCP tools, guardrails pipeline | Voice pipeline, 5-stage LocalAI roadmap, 78 skills |
> | **Front↔Mid↔Back** | Per-layer design decisions | Per-layer component library, routing | Per-layer auth, state, API contracts | Per-layer screens, flows, logic |

---

### Auditing a System Against SFIF

> [!tip] **Audit checklist per stage**
> - **Scaffold**: Does CLAUDE.md match the actual system? Can a new person understand the project's intent from scaffold artifacts alone? If no → scaffold is absent or stale.
> - **Foundation**: Is there ONE entry point? If there are 5 ways to start the app → foundation is incomplete. Binary: single entry or not.
> - **Infrastructure**: Can you add a feature WITHOUT touching shared concerns (auth, retry, logging)? If adding an endpoint requires modifying infra → infrastructure is incomplete.
> - **Features**: Are features using infrastructure or re-implementing it? Copied auth, bespoke retry, hardcoded config = features built before infrastructure.

> [!info] **Tier indicators**
> | Tier | What you see |
> |------|-------------|
> | **Mountain** | No scaffold, multiple entry points, auth/retry in feature code, no schema, no tests or tests against implementation |
> | **Pyramid** | Scaffold exists but partially outdated, clear foundation with 1-2 legacy entry points, 80% infra coverage with documented exceptions |
> | **Skyscraper** | Scaffold current, single entry point, all cross-cutting at infra layer, features are pure feature logic, tests verify behavior contracts |

---

### The Recursive Property

> [!abstract] **SFIF applies at every granularity simultaneously**
> - A *project* traverses Scaffold → Foundation → Infrastructure → Features
> - Each *feature* within the project traverses the same four stages
> - Each *component* within a feature traverses them again
> - The *design system* independently traverses: decisions (S) → component library (F) → responsive grid (I) → specialized screens (F)
>
> Structural quality can exist at one level and not another. The wiki is Skyscraper at the system level but individual pages can be Mountain. Per-level audit is required, not a single verdict.

---

### Relationship to the Knowledge Layer

The SFIF pattern has a direct analog in the wiki's 6-layer knowledge architecture:

> [!info] **Knowledge SFIF**
> | Knowledge stage | SFIF analog | Exit criterion |
> |----------------|-------------|---------------|
> | Raw notes | Scaffold | Direction captured |
> | Source synthesis | Foundation | Single-source grounded understanding |
> | Concepts | Infrastructure | Multi-source synthesis others can depend on |
> | Lessons/Patterns/Decisions | Features | Specialized value on the stable conceptual base |

A wiki page that skips Foundation (jumping from raw notes to a pattern) produces the knowledge equivalent of a Mountain: pattern-typed content that is a single-source restatement with no cross-linking. See [[Progressive Distillation]].

---

### Key Pages

| Page | Layer | Role in the model |
|------|-------|-------------------|
| [[Scaffold → Foundation → Infrastructure → Features]] | L5 | The pattern definition — 4 stages, exit criteria, recursive property, 4 instances |
| [[Skyscraper, Pyramid, Mountain]] | L2 | The quality tier framework — structural state assessment |
| [[Progressive Distillation]] | L5 | Knowledge analog — same density-increasing structure applied to knowledge |
| [[Four-Project Ecosystem]] | L2 | The projects that implement SFIF instances |
| [[Models Are Built in Layers, Not All at Once]] | L4 | Lesson: model-building follows SFIF — scaffold ≠ substance |
| [[Infrastructure as Code Patterns]] | L2 | IaC as the scaffold layer's primary artifact class |

---

### Lessons Learned

| Lesson | What was learned |
|--------|-----------------|
| [[Models Are Built in Layers, Not All at Once]] | Building this wiki's models followed SFIF: scaffold (entry points) → foundation (maturity assignment) → infrastructure (system definitions) → features (standards pages). Claiming "done" at scaffold level was a documented failure. |
| [[Infrastructure Must Be Reproducible, Not Manual]] | Infrastructure stage artifacts must be IaC. Manual infra = Mountain-tier infrastructure that drifts silently. |
| [[Never Skip Stages Even When Told to Continue]] | "Continue" means advance within the current SFIF stage, not skip to Features. Stage skipping is how Mountains are built. |

---

### State of Knowledge

> [!success] **Well-covered**
> - Four SFIF stages with structural exit criteria (not completion percentages)
> - Three quality tiers with concrete indicators per tier
> - Four ecosystem instances with per-stage artifact examples
> - Audit procedure (scaffold/foundation/infrastructure/feature checks)
> - Recursive property demonstrated across 4 granularity levels
> - Knowledge layer analog via Progressive Distillation

> [!warning] **Thin or unverified**
> - SFIF as a tooling check — could validation detect "infrastructure masquerading as features"?
> - Pyramid → Skyscraper boundary — is it a discrete refactor or continuous improvement?
> - SFIF for data pipelines and ML deployment — where is the Foundation/Infrastructure boundary?
> - No automated SFIF audit tool exists — currently manual evaluation only

---

### How to Adopt

> [!info] **Applying SFIF to a new or existing project**
> 1. **Audit current state** — per stage, per layer (use the checklist above)
> 2. **Identify the weakest stage** — that's where structural debt lives
> 3. **Fix from the bottom up** — don't add features to fix foundation problems. Fix the foundation first.
> 4. **Choose your quality tier honestly** — Pyramid is fine if the constraints are real and documented. Mountain is the failure mode.

> [!warning] **INVARIANT — never change these**
> - Stage exit criteria are structural, not percentage-based
> - Infrastructure ≠ Features (the most violated boundary)
> - Mountain is the default without intervention (entropy applies)
> - Per-level audit, not single-verdict assessment
> - POC code is Mountain-tier by design and MUST be rewritten for production

> [!tip] **PER-PROJECT — always adapt these**
> - Which stages need emphasis (greenfield = Scaffold first; legacy = audit Foundation first)
> - Quality tier target (Skyscraper for new systems; Pyramid-improving for legacy)
> - Granularity of recursive application (project + feature level is usually sufficient)
> - The specific exit criteria per stage (domain-specific artifacts)

## Open Questions

> [!question] **Can SFIF be detected automatically?**
> Could `tools/validate` or a static analysis tool detect "infrastructure in features" (auth in controllers, retry in handlers)? (Requires: defining detectable anti-patterns per stage)

> [!question] **Where is the Pyramid → Skyscraper boundary?**
> Is it a discrete architectural decision (refactor sprint) or continuous improvement? Can a system cross the boundary without anyone noticing? (Requires: observing the transition in a real project)

## Relationships

- BUILDS ON: [[Scaffold → Foundation → Infrastructure → Features]]
- BUILDS ON: [[Skyscraper, Pyramid, Mountain]]
- BUILDS ON: [[Progressive Distillation]]
- RELATES TO: [[Model: Design.md and IaC]]
- RELATES TO: [[Model: Quality and Failure Prevention]]
- RELATES TO: [[Model: Knowledge Evolution]]
- RELATES TO: [[Model: Methodology]]
- RELATES TO: [[Four-Project Ecosystem]]

## Backlinks

[[Scaffold → Foundation → Infrastructure → Features]]
[[Skyscraper, Pyramid, Mountain]]
[[Progressive Distillation]]
[[Model: Design.md and IaC]]
[[Model: Quality and Failure Prevention]]
[[Model: Knowledge Evolution]]
[[Model: Methodology]]
[[Four-Project Ecosystem]]
[[Model: Local AI ($0 Target)]]
