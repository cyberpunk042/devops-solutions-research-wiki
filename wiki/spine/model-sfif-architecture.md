---
title: "Model: SFIF + Architecture"
type: learning-path
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [model, learning-path, spine, sfif, architecture, quality-tiers, build-lifecycle]
---

# Model: SFIF + Architecture

## Summary

The SFIF + Architecture model describes the recursive build lifecycle that every project in the ecosystem follows: Scaffold (direction decided, documented) → Foundation (single entry point established) → Infrastructure (common components present and reliable) → Features (specialized value built on the base). The pattern is fractal — it applies at the project level, the feature level, the sub-component level, and the design level simultaneously. Alongside SFIF, the Skyscraper/Pyramid/Mountain quality tier analogy describes the structural state of any codebase: Skyscraper (clean, intentional, all stages complete), Pyramid (pragmatic compromise under real constraints), Mountain (accumulated mass with no structure). The four ecosystem projects — this wiki, OpenFleet, AICP, and Front-Middleware-Backend — each have documented SFIF instances at different stages of completion.

## Prerequisites

- Familiarity with the four-project ecosystem (wiki, OpenFleet, AICP, devops-control-plane)
- Basic software architecture vocabulary (entry point, dependency, interface contract)
- Understanding that POC code is Mountain-tier by design and must be rewritten before scaling

## Sequence

### Layer 5 — Patterns

1. **Scaffold → Foundation → Infrastructure → Features** ([[Scaffold → Foundation → Infrastructure → Features]])
   Entry point. Defines the four stages with concrete exit criteria: Scaffold exits when direction is documented and joinable; Foundation exits when a single entry point manages everything; Infrastructure exits when dependencies can reliably depend on it; Features have no terminal exit (ongoing work). Documents four real instances: Research Wiki (CLAUDE.md → tools/common.py + schema.yaml → pipeline.py + MCP server → evolve pipeline + sync + watcher), OpenFleet (SOUL.md template → orchestrator base → doctor.py + IRC + gateway → 10 specialized agents), AICP (profile system → backend router + circuit breaker → MCP tools + guardrails → voice pipeline + 5-stage roadmap), and Front-Middleware-Backend (each layer independently traverses SFIF). The recursive property: each layer advances at its own pace.

2. **Skyscraper, Pyramid, Mountain** ([[Skyscraper, Pyramid, Mountain]])
   The quality tier analogy. Skyscraper: all SFIF stages complete and clean, can grow upward without structural compromise. Pyramid: functional and livable, built around real constraints, pragmatic but principled tradeoffs — the practitioner's art. Mountain: accumulated mass, spaghetti, deprecated patterns layered on ad-hoc fixes, no scaffold artifacts. The critical failure pattern: POC-to-Production without a rewrite (Mountain code deployed as an MVP, then scaled as if Skyscraper). Per-layer evaluation: a system's frontend can be Mountain-tier while its backend is Skyscraper-tier. Evaluate at the layer granularity, not the whole-system level.

### Layer 2 — Core Concepts

3. **Four-Project Ecosystem** ([[Four-Project Ecosystem]])
   The concrete context. How the wiki, OpenFleet, AICP, and devops-control-plane relate as a system. Integration interfaces (file-based export, MCP bridges, shared skills). The shared design vocabulary that SFIF creates across projects.

4. **WSL2 Development Patterns** (`wiki/domains/devops/wsl2-development-patterns.md`)
   Infrastructure-layer reality: tools/watcher.py as a systemd user service, tools/sync.py for WSL↔Windows Obsidian sync, WSL2 filesystem constraints that affect polling vs inotify decisions. This is the infrastructure layer of the wiki project instantiated.

5. **Progressive Distillation** ([[Progressive Distillation]])
   The knowledge-layer equivalent of SFIF: raw → synthesis → concepts → patterns → decisions follows the same density-increasing, layer-by-layer structure. Understanding SFIF in code helps understand why the wiki's maturity layers (seed → growing → mature → canonical) work the way they do.

### Layer 4 — Lessons

6. **Never Skip Stages Even When Told to Continue** ([[Never Skip Stages Even When Told to Continue]])
   The SFIF lesson in operational form: skipping Foundation before building Infrastructure produces brittle features. Skipping Infrastructure before building Features produces hardcoded dependencies. The stage sequence is the quality guarantee.

## The Four SFIF Instances at a Glance

| Project | Scaffold | Foundation | Infrastructure | Features Stage |
|---------|---------|-----------|---------------|---------------|
| Research Wiki | CLAUDE.md, wiki/ structure, schema choice | tools/common.py, schema.yaml, validate.py, manifest.json | pipeline.py post-chain, MCP server (15 tools), lint, obsidian | evolve pipeline, watcher, sync, export |
| OpenFleet | SOUL.md + HEARTBEAT.md template, monorepo layout | Deterministic orchestrator, agent base model | doctor.py (24 rules), IRC routing, Open Gateway | 10 specialized agents, Mission Control UI |
| AICP | Profile system, venv, CLAUDE.md | Backend router, circuit breaker, complexity scorer | MCP tools, guardrails pipeline (path protection, response filter) | Voice pipeline, 5-stage LocalAI roadmap, 78 skills |
| Front-Mid-Back | Per-layer design decisions | Per-layer component foundation | Per-layer routing and auth contracts | Per-layer specialized screens and flows |

## Outcomes

After completing this path you understand:

- The four SFIF stage definitions and their exit criteria (not "code is written" — "structural commitment is stable")
- What makes something Infrastructure vs Feature: infrastructure enables, features use what infrastructure enables
- The Mountain → Pyramid → Skyscraper improvement path: iterative structural improvement without stopping delivery
- How to audit a project: which SFIF stage does each component actually occupy? Infrastructure masquerading as features signals structural debt.
- The recursive property: a mature backend with a Mountain frontend is a normal state — evaluate each layer independently
- How POC, MVP, and Production map to Mountain, Pyramid, and Skyscraper quality tiers

## Relationships

- BUILDS ON: [[Scaffold → Foundation → Infrastructure → Features]]
- BUILDS ON: [[Skyscraper, Pyramid, Mountain]]
- RELATES TO: [[Model: Design.md + IaC]]
- RELATES TO: [[Model: Quality + Failure Prevention]]
- RELATES TO: [[Model: Knowledge Evolution]]
- FEEDS INTO: Model: Local AI ($0 Target)
- RELATES TO: [[Four-Project Ecosystem]]

## Backlinks

[[Scaffold → Foundation → Infrastructure → Features]]
[[[[Skyscraper]]
[[Pyramid]]
[[Mountain]]]]
[[Model: Design.md + IaC]]
[[Model: Quality + Failure Prevention]]
[[Model: Knowledge Evolution]]
[[Model: Local AI ($0 Target)]]
[[Four-Project Ecosystem]]
[[Model: Quality and Failure Prevention]]
