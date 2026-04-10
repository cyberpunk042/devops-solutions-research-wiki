---
title: "Immune System Rules"
type: concept
layer: 2
maturity: growing
domain: devops
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-devops-control-plane-local
    type: documentation
    file: ../devops-control-plane/README.md
    title: "devops-control-plane — Local Project Documentation"
    ingested: 2026-04-08
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
    ingested: 2026-04-08
tags: [devops, immune-system, post-mortem, doctor.py, operational-rules, behavioral-security, 3-strike, anomaly-detection, agent-safety, openfleet]
---

# Immune System Rules

## Summary

The Immune System Rules are 24 operational governance rules derived from 16 post-mortems and agent death analyses, codified in OpenFleet's doctor.py. They implement the 3-strike rule, task state anomaly detection, and behavioral security — turning hard-won failure modes into automated, deterministic guardrails that run on every 30-second orchestrator cycle. These rules are a transferable devops pattern: any agent harness or orchestration system benefits from a codified set of operational invariants enforced at the infrastructure level rather than the model level.

## Key Insights

- **Origin: 16 post-mortems, not intuition**: The 24 rules were extracted from real incident analysis in the devops-control-plane project. Each rule has a known failure mode behind it. This provenance makes them high-confidence operational knowledge, not theoretical best practices.

- **3-strike rule as the core enforcement mechanism**: An agent or task that violates an operational invariant is not immediately killed. Three violations within a window trigger escalation. This tolerates transient anomalies (network blips, brief loop spikes) while catching persistent failures. The strike window prevents both false positives and silent degradation.

- **Task state anomaly detection**: doctor.py monitors the multi-dimensional state of every task across 6 axes (lifecycle, execution, progress, readiness, validation, context). Impossible state combinations (e.g., task marked "complete" but children still pending, or task in execution for more than N cycles) trigger anomaly flags.

- **Behavioral security as a rule category**: Beyond health checks, a subset of the rules covers behavioral violations — agents acquiring permissions beyond their role, tasks writing to paths they should not access, cost spikes from runaway loops. These rules treat agent behavior like network traffic: expected patterns are allowed, anomalies are flagged and rate-limited.

- **Deterministic, not LLM-driven**: doctor.py runs with zero LLM calls. Rules are pure Python: state comparisons, threshold checks, counter increments. This makes the immune system fast (microseconds per check), cheap (no token cost), and auditable (no inference variability). An LLM immune system would be unreliable by design.

- **Integrated into the orchestrator cycle**: doctor.py runs at step 6 of the 9-step orchestration cycle, after security scan and before review approvals. This ensures every dispatch decision is preceded by a health sweep — no task is dispatched to an agent currently in violation.

- **Transferable beyond OpenFleet**: The same rule categories apply to any orchestration system managing long-running agents: runaway loop detection, stale state reads, permission drift, cost spike detection, heartbeat timeouts. The specific thresholds vary per system; the rule categories are universal.

## Deep Analysis

### Rule Categories (Synthesized from Post-Mortem Analysis)

24 rules cluster into 5 categories. Each category catches a different failure class:

> [!info] **The 5 categories**
> | Category | What it detects | Example rules |
> |----------|----------------|---------------|
> | **1. Liveness** | Agents alive in state, dead in practice | Heartbeat timeout, stuck execution, stale session ID |
> | **2. Loop detection** | Runaway cycles and retry storms | Retry count exceeded, dispatch-without-completion, circular dependencies |
> | **3. State integrity** | Impossible state combinations | Parent complete + children pending, review with no reviewer, blocked with no blocker |
> | **4. Behavioral security** | Permission and scope violations | Out-of-scope path writes, cost spikes, capability acquisition beyond spec |
> | **5. Resource exhaustion** | Degraded conditions | Circuit breaker open, external service down, disk/memory pressure |

### Integration Point: doctor.py in the Orchestrator Cycle

```
Orchestrator 30-second cycle:
  1. Storm monitor evaluation
  2. Gateway duplication check
  3. Fleet mode gate
  4. Refresh agent contexts
  5. Security scan (behavioral security on new/changed tasks)
  6. Doctor run ← immune system sweep HERE
  7. Ensure review approvals
  8. Wake drivers
  9. Dispatch ready tasks
 10. Process directives
 11. Evaluate parents
 12. Health check
```

The placement matters: doctor.py runs after the security scan has flagged behavioral anomalies (step 5) and before any dispatch (step 9). A task flagged by the doctor accumulates a strike; at 3 strikes it is quarantined before ever reaching dispatch. This is a preemptive immune response, not a reactive one.

### Why Post-Mortem-Derived Rules Are Superior

> [!warning] **Why prompt-level guardrails fail**
> 1. LLMs can be distracted out of prompt constraints under adversarial inputs
> 2. Prompt guardrails apply per-call, not per-session — state drift accumulates across calls
> 3. No audit trail — a bypassed constraint leaves no record

> [!success] **Why code-level rules work**
> 1. Infrastructure-level enforcement — cannot be bypassed by any model
> 2. Session-level tracking — counters persist across the entire task lifecycle
> 3. Full audit trail — every rule check writes to the append-only ledger

### From devops-control-plane to OpenFleet

The transfer path is documented: devops-control-plane is where operational incidents were analyzed and rules were written. OpenFleet adopted them via doctor.py. This represents the ecosystem's knowledge transfer mechanism for operational wisdom: the control-plane serves as an incident laboratory; OpenFleet operationalizes the resulting rules at scale.

This is a model for how operational knowledge should flow in any multi-project ecosystem: centralize incident analysis in one place, extract transferable rules, implement them as shared infrastructure code.

## Open Questions

- What is the full text of all 24 rules? The number is documented but the specific rule definitions are not yet in the wiki. (Requires: direct inspection of openfleet/doctor.py source; not yet ingested into wiki)
- What is the median time-to-detection for each rule category? This would quantify the operational value. (Requires: empirical data from OpenFleet production operation; not available in existing wiki pages)

### Answered Open Questions

> [!success] **3-strike window scaling with cycle speed (turbo=5s vs economic=60s)**
> Cross-referencing `OpenFleet` and `Agent Orchestration Patterns`: the `OpenFleet` page documents three cycle speeds: turbo=5s, standard=30s, economic=60s. The `Agent Orchestration Patterns` page documents the 12-step cycle and confirms the doctor runs at step 6 on every cycle. The 3-strike window is defined as a number of violations within a window — if the window is time-based (e.g., 3 violations in 90 seconds), turbo mode (5s cycles) would detect violations ~6x faster than standard mode but may also trigger more false positives from transient blips that resolve quickly. If the window is cycle-count-based (e.g., 3 violations in 3 consecutive cycles), turbo mode accumulates strikes 6x faster than standard mode in wall-clock time, while economic mode takes 3 minutes. The `Immune System Rules` page documents that the strike window "prevents both false positives and silent degradation" — implying the window is tuned for the standard 30s cycle. At turbo speed, the window likely requires recalibration to avoid false escalation on transient anomalies that resolve within a few seconds. This remains a noted design concern without a canonical answer in the wiki.

> [!success] **Shared library for OpenFleet + AICP — feasible via YAML rule definitions**
> Cross-referencing `AICP` and `devops-control-plane`: the `AICP` page documents that AICP implements a circuit breaker (CLOSED → OPEN → HALF_OPEN) per backend, and that OpenFleet's doctor.py already applies the AICP circuit breaker pattern at fleet level: "LLM backend circuit breaker open (AICP pattern applied at fleet level)" is listed as a Resource Rule. The `devops-control-plane` page confirms the immune system rules "originated from control-plane incident analysis" and were transferred to OpenFleet. The architectural pattern for sharing already exists — the control-plane is the "incident laboratory," OpenFleet is the consumer. A shared library would require extracting the rule-checking logic from doctor.py into a Python package that both OpenFleet and AICP could import. The `Infrastructure as Code Patterns` page raises this directly: "Should the 24 immune system rules be expressed as a YAML rule file (machine-executable) rather than Python logic in doctor.py?" — suggesting that YAML rule definitions would be the more shareable format. The answer: technically feasible, architecturally aligned with the ecosystem's IaC philosophy, but not yet implemented.

> [!success] **Static human maintenance, not ML evolution — determinism is the point**
> Cross-referencing `devops-control-plane` and `Agent Orchestration Patterns`: the `Immune System Rules` page's own analysis provides the core answer: "Post-mortem-derived rules codified in Python provide: (1) Infrastructure-level enforcement — cannot be bypassed by any model; (2) Session-level tracking — counters persist across the entire task lifecycle; (3) Full audit trail — every rule check writes to the append-only ledger." The `devops-control-plane` page confirms the append-only audit ledger as the definitive record. Automatic ML evolution would make the rules non-deterministic — exactly the property the immune system was designed to avoid. The `Agent Orchestration Patterns` page reinforces: "A deterministic security scan cannot be social-engineered via a crafted task description. An LLM-based security layer can be prompted around." Applying this principle to rule evolution: ML-driven rule mutation introduces the same reliability risks as LLM-based enforcement. The answer from existing wiki knowledge: rules should remain statically maintained via human post-mortem review. The human review gate in the knowledge evolution pipeline (`--review` flag) is the same principle applied to wiki pages — automation handles bookkeeping, humans handle high-stakes decisions. ML could assist by surfacing anomaly candidates for human review, but should not auto-modify rule thresholds.

## Relationships

- DERIVED FROM: [[devops-control-plane]]
- IMPLEMENTS: [[OpenFleet]]
- RELATES TO: [[Harness Engineering]]
- RELATES TO: [[AICP]]
- ENABLES: [[Plan Execute Review Cycle]]
- RELATES TO: [[Always Plan Before Executing]]
- BUILDS ON: [[Rework Prevention]]

## Backlinks

[[devops-control-plane]]
[[OpenFleet]]
[[Harness Engineering]]
[[AICP]]
[[Plan Execute Review Cycle]]
[[Always Plan Before Executing]]
[[Rework Prevention]]
[[Backlog Hierarchy Rules]]
[[Deterministic Shell, LLM Core]]
[[Execution Modes and End Conditions]]
[[Four-Project Ecosystem]]
[[Infrastructure Must Be Reproducible, Not Manual]]
[[Infrastructure as Code Patterns]]
[[Model: Ecosystem Architecture]]
[[Model: Quality and Failure Prevention]]
[[Never Skip Stages Even When Told to Continue]]
[[Never Synthesize from Descriptions Alone]]
[[Shallow Ingestion Is Systemic, Not Isolated]]
[[Stage-Gate Methodology]]
[[Task Lifecycle Stage-Gating]]
[[Task Type Artifact Matrix]]
[[The Agent Must Practice What It Documents]]
