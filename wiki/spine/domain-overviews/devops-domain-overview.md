---
title: "Devops — Domain Overview"
type: domain-overview
domain: devops
layer: spine
status: synthesized
confidence: medium
maturity: growing
created: 2026-04-08
updated: 2026-04-10
sources: []
tags: [domain-overview, devops]
---

# Devops — Domain Overview

## Summary

The devops domain covers CI/CD, deployment, monitoring, infrastructure-as-code, and SRE practices — the operational backbone of the four-project ecosystem. This is the sparsest domain in the wiki, with a single concept page (devops-control-plane) despite devops being the stated domain of the entire ecosystem. The sparse coverage is explained by scope: this wiki is a knowledge synthesis system, not an operational runbook. The devops-control-plane page is authoritative — sourced directly from the live project's README — and documents a sophisticated layered architecture with auto-detection of 20 technology stacks, AES-256-GCM encrypted vaults, append-only audit ledgers, and the 24 post-mortem-derived immune system rules that became OpenFleet's doctor.py. The domain's thin wiki coverage reflects that operational devops knowledge lives in code (scripts/, IaC files, CI configs) rather than documentation, but the synthesis gap is real: the ecosystem's devops patterns, failure modes, and operational lessons are insufficiently captured.

## State of Knowledge

> [!question] Why Is DevOps the Sparsest Domain?
> The sparse wiki coverage reflects that operational devops knowledge lives in code (scripts/, IaC files, CI configs) rather than documentation, but the synthesis gap is real: the ecosystem's devops patterns, failure modes, and operational lessons are insufficiently captured.

**Strong coverage:**
- devops-control-plane — sourced from the live README. Architecture (layered: interfaces → core → policy → adapters → infrastructure), 20 stack definitions, dual vault system, audit ledger, 29 service packages. Confidence: authoritative for the platform design; medium for operational practice.

**Known gaps drawn from other domains:**
- OpenFleet's IaC approach (42+ scripts/, setup.sh, zero-manual-commands philosophy) is documented in the ai-agents domain but not here where it belongs as a devops pattern.
- CI/CD pipelines — the ecosystem projects use GitHub Actions but no wiki page covers their pipeline designs, testing strategies, or deployment workflows.
- Docker Compose and Kubernetes — both used (OpenFleet services, Plane self-hosting, AICP LocalAI) but no devops-domain synthesis of the container orchestration approach.
- Monitoring and observability — OpenFleet's 9-service architecture (PostgreSQL, Redis, LocalAI, LightRAG, IRC, Mission Control) requires monitoring but no coverage exists.
- The 24 immune system rules — documented as originating in devops-control-plane and implemented in OpenFleet's doctor.py but never extracted as a standalone devops pattern.

## Maturity Map

**Established content (pre-maturity system):**
- devops-control-plane — sole concept page; authoritative for platform architecture; gaps in operational practice documentation

## Gaps

- **IaC patterns**: The ecosystem-wide approach to Infrastructure-as-Code (scripts/, setup.sh, Compose files) needs documentation. OpenFleet's 42+ scripts represent significant operational knowledge that is not synthesized.
- **Immune system rules as pattern**: The 24 rules derived from 16 post-mortems are a transferable devops asset. A dedicated pattern page (or decisions page) would make them reusable beyond OpenFleet.
- **CI/CD architecture**: GitHub Actions pipelines across the four projects — what they test, how they deploy, what quality gates they enforce — are completely undocumented in the wiki.
- **Service dependency map**: The production service topology (PostgreSQL → Mission Control, Redis → RQ queue, LocalAI → fleet agents, LightRAG → navigator) is described in OpenFleet but not consolidated as a devops architectural view.
- **Secrets management**: The devops-control-plane vault (AES-256-GCM) is described but its role as a potential centralized credential store for all ecosystem projects hasn't been evaluated.
- **WSL2 devops constraints**: The ecosystem runs on WSL2 (Windows Subsystem for Linux). This affects service startup, networking, inotify availability, and daemon management in ways that standard Linux devops documentation doesn't cover.

## Priorities

1. **Immune system rules page** — Extract the 24 post-mortem-derived rules as a transferable devops pattern; high signal from a real operational track record
2. **IaC patterns synthesis** — Document the ecosystem-wide scripting philosophy and the key patterns in OpenFleet's scripts/
3. **Service dependency map** — Consolidate the production service topology across the ecosystem
4. **WSL2 devops constraints** — Document where standard devops assumptions break on WSL2 and what the workarounds are
5. **CI/CD architecture** — Survey and document the GitHub Actions workflows across the four projects

## Key Pages

1. **[devops-control-plane](../../domains/devops/devops-control-plane.md)** — The only page in this domain. Covers the unified solution management platform, 20 stack auto-detection, encrypted vaults, audit ledger, and the post-mortem-derived immune system rules that became OpenFleet's doctor.py.

## FAQ

### Q: What is devops-control-plane and how does it relate to OpenFleet?
devops-control-plane is the unified solution management platform underlying the ecosystem — it provides the 20 stack auto-detection, AES-256-GCM encrypted vaults, and audit ledger. Its 24 post-mortem-derived immune system rules were adopted directly into OpenFleet's doctor.py as the agent guardrail system. See [[devops-control-plane]] and [[OpenFleet]].

### Q: What are the 24 immune system rules and where should I apply them?
The 24 rules originated from 16 real post-mortems across projects. They cover failure modes like runaway loops, permission drift, stale state reads, and cost spikes. They are implemented in OpenFleet's doctor.py and are transferable to any agent harness as a checklist. A standalone pattern page distilling these rules is a documented priority. See [[Harness Engineering]].

### Q: How does the ecosystem handle secrets and credentials across four projects?
devops-control-plane implements a dual vault system with AES-256-GCM encryption and append-only audit ledgers. Whether this vault can serve as a centralized credential store for all four projects (OpenFleet, AICP, DSPD, devops-control-plane) is an open question — it is architecturally plausible but not yet evaluated. See [[devops-control-plane]].

### Q: What WSL2-specific devops constraints should I know about?
The ecosystem runs on WSL2 (Windows Subsystem for Linux), which affects service startup (no systemd by default), networking (bridged vs NAT), inotify watch limits (relevant for the wiki watcher daemon), and daemon lifecycle management. Standard Linux devops documentation often does not account for these constraints — this is a documented gap in the wiki.

## Relationships

- ENABLES: AI Agents — Domain Overview
- ENABLES: Tools And Platforms — Domain Overview
- ENABLES: Automation — Domain Overview
- RELATES TO: Knowledge Systems — Domain Overview
- UNDERPINS: AI Models — Domain Overview

## Backlinks

[[AI Agents — Domain Overview]]
[[Tools And Platforms — Domain Overview]]
[[Automation — Domain Overview]]
[[Knowledge Systems — Domain Overview]]
[[AI Models — Domain Overview]]
[[Cross-Domain — Domain Overview]]
