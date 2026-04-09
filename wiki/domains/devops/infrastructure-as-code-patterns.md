---
title: "Infrastructure as Code Patterns"
type: concept
layer: 2
maturity: growing
domain: devops
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-devops-control-plane-local
    type: documentation
    file: ../devops-control-plane/README.md
    title: "devops-control-plane — Local Project Documentation"
    ingested: 2026-04-08
  - id: src-design-md-research
    type: article
    url: "https://github.com/VoltAgent/awesome-design-md"
    file: raw/articles/design-md-pattern-research.md
    title: "Design.md Pattern Research"
    ingested: 2026-04-08
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
    ingested: 2026-04-08
tags: [devops, iac, infrastructure-as-code, claude-md, design-md, schema-yaml, setup-py, service-templates, agent-configuration, markdown-config]
---

# Infrastructure as Code Patterns

## Summary

Infrastructure as Code (IaC) in the four-project ecosystem extends beyond Terraform and Ansible into a pattern where markdown files, YAML schemas, and Python setup scripts define both operational infrastructure and AI agent behavior. CLAUDE.md, DESIGN.md, AGENTS.md, config/schema.yaml, .env.example, service templates, and setup.sh are all IaC — they are machine-executable specifications for how a system should be configured, behaved, and deployed. The ecosystem consistently applies this pattern: the human writes the specification file; the tooling (or AI agent) reads it as binding constraints and executes accordingly.

## Key Insights

- **CLAUDE.md as agent IaC**: CLAUDE.md is not documentation — it is configuration. Claude Code reads it at session start as binding operational instructions. It defines how the AI agent should behave in this specific project: commands to run, coding conventions, quality gates, prohibited actions. This is IaC for AI-powered systems.

- **Markdown files as the universal IaC format**: The ecosystem converges on markdown for AI-facing configuration (CLAUDE.md, DESIGN.md, AGENTS.md, SOUL.md, HEARTBEAT.md) because it is simultaneously human-readable and machine-parsable. Structured sections become slot-filling constraints for LLMs. The markdown format is the interoperability layer — any tool that reads text can consume it.

- **config/schema.yaml as validation IaC**: This wiki's config/schema.yaml defines what a valid wiki page looks like. The validate tool reads it to enforce quality gates. Schema files are classic IaC: declarative, version-controlled, executable by automated tooling.

- **setup.sh / setup.py as reproducible environment IaC**: OpenFleet's setup.sh produces a zero-to-running fleet from a single command. This wiki's tools/setup.py handles environment setup, dependency installation, and Obsidian configuration. These scripts are IaC for development environments — they encode the exact steps a human would otherwise perform manually, making environments reproducible across machines.

- **Service templates as systemd IaC**: The ecosystem uses service template files to deploy systemd user services (watcher daemon, sync daemon). Writing the service file to ~/.config/systemd/user/ and running systemctl enable is reproducible infrastructure deployment. The template is the specification; the OS is the executor.

- **.env.example as interface IaC**: Every project's .env.example documents required environment variables with placeholder values. This is a contract — a machine-readable specification of what the deployment environment must provide. It serves as both documentation and a checklist for environment provisioning.

- **42+ scripts as scripted IaC**: OpenFleet's scripts/ directory contains 42+ shell scripts for every operational task (setup, deployment, diagnostics, cleanup). No manual commands — IaC-only operations. This scripts/ pattern is an alternative to Makefile or task runners: pure shell, version-controlled, composable.

- **stacks/*.yml as technology-policy IaC**: devops-control-plane defines 20 technology stacks as YAML policy files. Each file specifies detection rules, health checks, and integration guidance. The engine reads these at runtime to auto-detect project capabilities. Stack definitions are IaC for the devops platform itself.

## Deep Analysis

### The IaC Spectrum in the Ecosystem

| File / Pattern | What It Configures | Executor |
|---------------|-------------------|---------|
| CLAUDE.md | AI agent behavior | Claude Code (session start) |
| DESIGN.md | UI visual design constraints | AI coding agents (Stitch, Cursor) |
| AGENTS.md | Build and architecture instructions | AI coding agents |
| SOUL.md | Agent identity and role | OpenFleet orchestrator |
| HEARTBEAT.md | Agent periodic checklist | OpenFleet orchestrator |
| config/schema.yaml | Wiki page validity rules | tools/validate.py |
| stacks/*.yml | Tech stack detection/health rules | devops-control-plane engine |
| .env.example | Required environment variables | Human deployer / CI |
| setup.sh / setup.py | Environment provisioning | Human (once) / CI |
| service templates | Systemd service deployment | OS / setup tooling |
| scripts/*.sh | Operational task automation | Human / orchestrator |
| project.yml | Project-level policy | devops-control-plane |

### The Core Principle: Specification → Execution

Traditional IaC (Terraform, Ansible, CloudFormation) applies this principle to cloud resources. The ecosystem generalizes it: if a system needs to be configured, write a specification file. The executor might be Terraform, systemctl, Claude Code, or a Python validator — the specification-execution model is the same.

This generalization matters for AI-powered systems because AI agents are configurable executors. CLAUDE.md configures an AI agent the same way a Terraform provider block configures a cloud resource: declaratively, in a file, under version control.

### CLAUDE.md vs Traditional Config Files

CLAUDE.md differs from a traditional config file (JSON, YAML, TOML) in three ways:

1. **Natural language content**: Instructions are written in prose, not key-value pairs. This is intentional — LLMs parse prose better than they parse schema references. The markdown structure (headers, bullets) provides enough syntax for the model to segment concerns.

2. **No schema enforcement**: Unlike config/schema.yaml, there is no validator for CLAUDE.md. The "schema" is convention (what sections are expected) enforced by the AI agent's interpretation. This is weaker than validated config but more flexible.

3. **Consumed at runtime by an LLM**: Every token in CLAUDE.md costs context budget. Unlike a YAML config that is parsed into a structured object, CLAUDE.md occupies the prompt. This creates an implicit pressure to keep it concise — verbosity has a real cost.

### Skills as Dynamic IaC

Skills (in skills/ directories across all projects) are a dynamic IaC variant: they are not loaded at session start but invoked when relevant. A skill file instructs the AI agent how to perform a specific operation. Together, CLAUDE.md (static, always loaded) and skills/ (dynamic, context-triggered) form a two-tier IaC stack for AI agent configuration.

The same two-tier pattern appears in devops-control-plane: stacks/*.yml (always loaded at engine start) vs runtime adapter plugins (loaded per-project based on detection results).

### IaC Anti-Pattern: Manual Setup Steps

The ecosystem explicitly rejects manual setup. The feedback principle "Pipeline Not Manual" and OpenFleet's "IaC-only operations" philosophy are the same pattern: if a human performs a step manually, that step should be encoded in a file and automated. The cost of manual steps is reproducibility debt — the next person (or machine, or future session) cannot reliably reproduce the environment.

## Open Questions

- Should CLAUDE.md have a validated schema (like config/schema.yaml for wiki pages) to enforce required sections? (Requires: decision by the ecosystem curator; technically feasible but no existing tooling in the wiki's validate.py supports prose-section validation)
- Can config/schema.yaml be extended to validate skills files, not just wiki pages? (Requires: external research on Claude Code skills file structure conventions; not fully documented in existing wiki pages)

### Answered Open Questions

**Q: How should conflicting CLAUDE.md instructions be resolved when multiple CLAUDE.md files exist in a project hierarchy?**

Cross-referencing `Harness Engineering` and `Design.md Pattern`: the `Harness Engineering` page documents how Claude Code processes CLAUDE.md files — they are read at session start as "binding operational instructions." The `Design.md Pattern` page establishes the companion file ecosystem (CLAUDE.md + DESIGN.md + AGENTS.md) where "each file addresses a different dimension of AI agent context." Claude Code's actual behavior with multiple CLAUDE.md files in a hierarchy (parent directory + project root + subdirectory) is to load all of them, with more-specific (deeper directory) files taking precedence over less-specific ones when there are conflicts — following standard configuration file override semantics. The `Harness Engineering` page notes that harness guardrails operate "at execution time through hooks, actually blocking dangerous operations" independent of CLAUDE.md content, meaning hooks (not CLAUDE.md prose) are the conflict-resolution layer for critical operations. Practical guidance from existing wiki knowledge: structure CLAUDE.md files so they are additive (subdirectory files extend, not override, parent files), and use hooks for critical constraints that must be enforced regardless of CLAUDE.md hierarchy.

**Q: What is the right level of verbosity for a CLAUDE.md before context cost outweighs configuration value?**

Cross-referencing `Context-Aware Tool Loading` and `Design.md Pattern`: the `Context-Aware Tool Loading` pattern provides the quantitative answer. Claude Code accuracy is affected by context utilization (one practitioner reported observing degradation at higher percentages, but this is probabilistic and session-dependent). CLAUDE.md occupies context budget on every turn. The `Design.md Pattern` page documents this explicitly: "every token in CLAUDE.md costs context budget... This creates an implicit pressure to keep it concise — verbosity has a real cost." It also provides the practical guidance: "keep it concise (under ~200 lines), reference detailed component specifications in a separate file loaded on demand via a skill." For CLAUDE.md, the equivalent is: keep the always-loaded CLAUDE.md to the minimum required for session initialization (project type, critical conventions, key commands), and put detailed operational workflows in skills files that load only when that workflow is invoked. The `Context-Aware Tool Loading` pattern's threshold: if information is needed on fewer than ~80% of turns, do not pre-load it in CLAUDE.md — put it in a skill. This wiki's own CLAUDE.md (~250+ lines) is at the upper boundary where additional verbosity would measurably increase per-turn context pressure.

**Q: Should the 24 immune system rules be expressed as a YAML rule file (machine-executable) rather than Python logic in doctor.py?**

Cross-referencing `Immune System Rules` and `devops-control-plane`: the `Immune System Rules` page establishes the core requirement: "doctor.py runs with zero LLM calls. Rules are pure Python: state comparisons, threshold checks, counter increments. This makes the immune system fast (microseconds per check), cheap (no token cost), and auditable." The `devops-control-plane` page documents that the control-plane already uses YAML for stack policy definitions (`stacks/*.yml`): "each file specifies detection rules, health checks, and integration guidance. The engine reads these at runtime to auto-detect project capabilities." This is precisely the precedent for YAML rule files. A YAML format for immune system rules would make them: (1) shareable across OpenFleet and AICP without Python import dependencies, (2) human-reviewable without reading Python logic, (3) modifiable without code changes or deployments. The counter-argument from the `Immune System Rules` page: Python rules have full expressiveness for complex state comparisons that YAML cannot easily capture. The optimal design mirrors the control-plane's pattern: define rule metadata and thresholds in YAML (the "what"), implement the evaluation logic in Python (the "how"), and load YAML at runtime. This gives shareability and editability without sacrificing evaluation power.

## Relationships

- EXTENDS: [[Design.md Pattern]]
- RELATES TO: [[devops-control-plane]]
- RELATES TO: [[OpenFleet]]
- RELATES TO: [[Harness Engineering]]
- RELATES TO: [[Skills Architecture Patterns]]
- BUILDS ON: [[Immune System Rules]]
- ENABLES: [[Claude Code Best Practices]]

## Backlinks

[[Design.md Pattern]]
[[devops-control-plane]]
[[OpenFleet]]
[[Harness Engineering]]
[[Skills Architecture Patterns]]
[[Immune System Rules]]
[[Claude Code Best Practices]]
[[Decision: Local Model vs Cloud API for Routine Operations]]
[[Decision: Polling vs Event-Driven Change Detection]]
[[Deterministic Shell, LLM Core]]
[[Four-Project Ecosystem]]
[[Gateway-Centric Routing]]
[[Infrastructure Must Be Reproducible, Not Manual]]
[[Model: Design.md and IaC]]
[[Scaffold → Foundation → Infrastructure → Features]]
[[Skyscraper, Pyramid, Mountain]]
[[WSL2 Development Patterns]]
