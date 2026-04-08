---
title: "devops-control-plane"
type: concept
domain: devops
status: synthesized
confidence: authoritative
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-devops-control-plane-local
    type: documentation
    file: ../devops-control-plane/README.md
    title: "devops-control-plane — Local Project Documentation"
    ingested: 2026-04-08
tags: [devops, control-plane, project-management, tech-detection, vault, encryption, audit, multi-interface, adapters, infrastructure]
---

# devops-control-plane

## Summary

The devops-control-plane is a unified solution management platform that provides one place to see, manage, and evolve any software project (mono-repo or single-stack). It replaces scattered scripts, manual environment setup, fragmented dashboards, and tool-specific knowledge with a single system that auto-detects technologies (20 stacks: Python, Node, Go, Rust, Docker, Terraform, K8s, etc.) and provides full visibility, management, and evolution tools. Three interfaces: interactive TUI (manage.sh), CLI (Click-based, Python), and web dashboard (Flask SPA). Features AES-256-GCM encrypted vaults (secrets + content), append-only audit ledger, 6 SSG page builders, and a pluggable adapter architecture. Its immune system rules (24 rules from 16 post-mortems) are codified in OpenFleet's doctor.py.

## Key Insights

- **Layered architecture**: Interfaces (thin: manage.sh, CLI, Web) → Core Domain (pure: Models/Pydantic, Services, Engine, Use-Cases) → Policy (data: project.yml, stacks/*.yml) → Adapter Layer (pluggable: Shell, VCS, Containers) → Invariant Infrastructure (Reliability, Observability, Security, Persistence).

- **20 technology stack definitions**: Each with detection rules, integration guidance, and health checks. Python, Node, Go, Rust, Docker, Kubernetes, Terraform, and more. Auto-detection scans project directories and reports capabilities.

- **Dual vault system**: Secret/Variable Vault (AES-256-GCM, PBKDF2-SHA256, 100,000 KDF iterations, auto-lock) and Content Vault (per-file encryption). Vaults enable secure credential management without external services.

- **Append-only audit ledger**: Every operation writes to ledger.ndjson. Provides complete operation history, compliance trail, and debugging timeline. Data flow: Load config → Detect → Plan → Execute → Persist → Audit.

- **Three interfaces, same core**: TUI (manage.sh with interactive menus), CLI (Click-based for scripting), Web (Flask SPA at localhost:8000). All three use the same core services — the interface is a thin shell.

- **Pluggable adapter protocol**: Base adapter ABC with implementations for Shell, VCS (Git), Containers (Docker), Languages (Python, Node). Adapters can be swapped or mocked for testing without changing core logic.

- **29 service packages in core**: Vault, content encryption, pages (6 SSG builders), Git/GitHub, Kubernetes, Docker, Terraform, CI/CD, backup, security audit (L0/L1/L2 detection + scoring), changelog, secrets (with GitHub Secrets sync).

- **Origin of fleet immune system**: 24 rules derived from 16 post-mortems and agent death analysis. These rules are codified in OpenFleet's doctor.py (3-strike rule, task state anomaly detection, behavioral violations). The control-plane is where operational lessons became codified governance.

## Deep Analysis

### Relationship to the Ecosystem

The devops-control-plane occupies a foundational role:

1. **Operational DNA donor**: Its post-mortem-derived rules became OpenFleet's immune system (doctor.py). The 3-strike rule, behavioral security, and anomaly detection patterns originated from control-plane incident analysis.

2. **General-purpose vs specialized**: The control-plane manages ANY software project. OpenFleet, AICP, DSPD, and the research wiki are specific projects that could each be managed by the control-plane. But in practice, each project has its own management mechanisms — OpenFleet has the orchestrator, DSPD has Plane, the wiki has its own tools.

3. **Infrastructure management**: The control-plane's stack detection, Docker management, Kubernetes operations, and Terraform integration are infrastructure capabilities that the other projects use in various forms. OpenFleet's scripts/ echo the control-plane's IaC philosophy.

4. **Vault as shared service potential**: The encrypted vault could serve as the credential store for all ecosystem projects — API keys for NotebookLM, Claude, LocalAI, GitHub, Plane.

### Technology Stack

- Python 3.12 (requires >=3.11)
- Click (CLI), Flask + Jinja2 (Web), Pydantic v2 (validation)
- cryptography library (AES-256-GCM)
- pytest, ruff, mypy (testing + quality)
- GitHub Actions (CI)

## Open Questions

- Should the control-plane become the infrastructure management layer for all ecosystem projects, or remain standalone?
- Can the vault system be exposed as an MCP server for centralized credential management?
- How does the control-plane's project detection compare to OpenFleet's context assembly for understanding project state?

## Relationships

- ENABLES: OpenFleet
- RELATES TO: AICP
- RELATES TO: Plane
- RELATES TO: Claude Code
- RELATES TO: Wiki Ingestion Pipeline

## Backlinks

[[OpenFleet]]
[[AICP]]
[[Plane]]
[[Claude Code]]
[[Wiki Ingestion Pipeline]]
