---
title: "Rework Prevention"
type: concept
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
    ingested: 2026-04-08
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
    ingested: 2026-04-08
tags: [rework-prevention, planning, quality-gates, spec-compliance, agent-behavior, harness-engineering, openfleet, test-driven, context-management, cost-of-rework]
---

# Rework Prevention

## Summary

Rework prevention is the practice of designing AI agent workflows so that work requiring repetition — due to misaligned scope, incorrect assumptions, failed quality gates, or context drift — is caught and corrected before it propagates into irreversible state. The cost of rework is not linear: it compounds as revert + re-plan + re-execute + re-verify, and each cycle of rework degrades the agent's remaining context budget while consuming wall-clock time. The primary prevention strategies are planning before execution (surfacing assumptions early), quality gates at phase boundaries (preventing unreviewed work from advancing), spec-compliance review (ensuring execution matched intent), and context management (preventing context drift that causes agents to diverge from the original plan).

## Key Insights

- **Rework costs compound, not add**: A single rework cycle on a 3-hour coding task costs more than 3 hours. The revert must be clean (often non-trivial for multi-file changes), the cause of failure must be diagnosed, the plan must be revised, execution must restart, and the review gate must be re-cleared. In a multi-agent context with sequential dependencies, one task's rework can cascade: downstream tasks built on incorrect state must also be reverted.

- **Prevention is orders of magnitude cheaper than correction**: The Harness Engineering evidence is quantitative — the Breezing mode's Planner+Critic review before coding starts costs ~5.5x the planning tokens, versus ~4x without the pre-review. This sounds like overhead. But if the pre-review catches a scoping error that would require reworking 2 hours of coding, the cost ratio inverts dramatically. Any rework that consumes more than 5.5 planning cycles' worth of effort was cheaper to prevent.

- **The failure modes of each phase produce different rework signatures**: If the planning phase is skipped, rework appears as scope creep — execution produces correct-looking partial work that is missing critical requirements. If the review phase is skipped, rework appears as silent accumulation — errors compound across multiple cycles before becoming visible. If context management is neglected, rework appears as regression — early decisions are forgotten, re-made incorrectly, and conflict with later work.

- **Quality gates must be hard, not advisory**: Soft quality gates (documentation says "should review before committing") are routinely skipped under time pressure or when the agent has high local confidence. Hard quality gates (the harness TypeScript rule blocks the commit operation if the review verb was not executed) cannot be skipped without deliberate circumvention. Hard gates prevent the single most common rework trigger: "I thought it was fine but it wasn't."

- **Spec compliance review is a distinct step from functional review**: Functional review asks "does this work?" Spec compliance review asks "does this match what was asked for?" These questions have different answers surprisingly often. An agent implementing a caching layer that works perfectly but uses the wrong eviction policy has passed functional review and failed spec compliance review. Spec compliance review requires comparing output against the written spec, not just running tests.

- **Test-driven development shifts rework cost forward**: Writing tests before implementation forces explicit thinking about acceptance criteria before any code is written. This is a planning-phase investment. When the implementation is complete, the tests are the spec compliance review gate — any deviation from the spec is caught automatically. TDD essentially automates spec compliance review at the unit level.

## Deep Analysis

### The Compound Cost Model

Let T = time to complete the task once correctly.

Without rework prevention, a task that requires one rework cycle costs approximately:

```
Total cost = T (first attempt) + R (revert) + D (diagnosis) + P (re-plan) + T (re-execute) + V (re-verify)
           ≈ 2.5T to 3.5T depending on how clean the revert is
```

With a cascade (downstream tasks also need to be reverted):

```
Total cost = 2.5T (first task rework) + Σ(downstream rework costs)
```

In a multi-agent fleet with 5 dependent tasks, a single root-cause rework can trigger 5 downstream reworks. The fleet's output is corrupted until all 5 are corrected. This is why OpenFleet's orchestrator invests heavily in upstream quality (security scan, doctor run, readiness gating) before dispatch — a single task dispatched in bad state can corrupt the entire sprint.

The prevention investment for a single task:
```
Prevention cost ≈ 0.5x to 1.5x of the planning phase (spec review, Planner+Critic, pre-checks)
                ≈ 0.2T to 0.4T for a typical task
```

Break-even: Prevention is net-positive if it reduces rework probability by more than `0.3T / 2.5T = 12%`. Given that experienced engineers report rework rates of 20-40% on complex tasks without explicit gates, prevention ROI is strongly positive in almost all realistic scenarios.

### Prevention Strategy Layer

**Layer 1 — Planning Quality (prevent scope drift)**

- Write an explicit spec or acceptance criteria before beginning
- Use a Planner+Critic review of the approach before execution starts
- Identify all files/systems that will be modified and confirm scope is correct
- Flag any ambiguity in the task description and resolve it before action

**Layer 2 — Execution Guardrails (prevent silent drift)**

- Use TypeScript/bash hooks that detect out-of-scope writes during execution
- Limit execution scope: max N files changed per task, operations confined to declared targets
- Checkpoint progress at natural phase boundaries rather than running to completion unchecked
- Maintain a running todo/plan that tracks executed vs. planned steps

**Layer 3 — Review Gates (prevent unreviewed output from advancing)**

- Hard gate: review step must be explicitly completed before output is promoted
- Spec compliance review: compare output against written spec, not just functional tests
- Integration tests that verify the change within its downstream context
- OpenFleet's "ensure review approvals" step (step 7 in the 12-step cycle) is the fleet-scale implementation

**Layer 4 — Context Management (prevent regression)**

- Externalize plans and todos to files that survive context compression
- Reset context at phase boundaries for long-running tasks: end of Plan phase → start of Execute phase with fresh context containing the plan
- Use sub-agents with scoped context rather than accumulating all task history in one growing window
- Periodically re-read the original spec during long execution sessions to prevent drift

### Rework Patterns and Their Remedies

| Rework Pattern | Root Cause | Prevention |
|---|---|---|
| "It works but it's the wrong thing" | Missing spec compliance review | Write acceptance criteria before execution; compare output against spec |
| "It was fine then something broke it" | Context drift; forgotten earlier decisions | Externalize decisions to files; re-read spec periodically |
| "The scope kept growing" | No scope gate during execution | Guardrail rules that flag out-of-scope writes; bounded task dispatch |
| "It passed tests but failed in production" | Integration context not considered | Integration tests; spec includes deployment context |
| "I had to redo it because requirements changed" | Premature execution before requirements stable | Guided/smart ingestion modes; confirm spec before work begins |
| "Multiple agents produced conflicting output" | No canonical state between agents | Single source of truth; agent output validated before becoming canonical |

### Rework Prevention in This Wiki's Ingestion Pipeline

The wiki's three ingestion modes directly encode different rework prevention postures:

- **guided mode**: Shows extraction plan (spec) and waits for human approval before writing any pages. This is maximum rework prevention — any misalignment is caught before execution begins. Cost: higher latency per ingestion.

- **smart mode** (default): Auto-proceeds when confident; escalates to guided when: new domain (higher chance of structural misclassification), contradictions detected (risk of creating pages that conflict with existing knowledge), ambiguity (risk of scope drift), low-quality source (risk of creating thin pages that need immediate rework). Smart mode is a risk-calibrated version of the same prevention strategy.

- **auto mode**: No gates. Appropriate only for high-confidence, low-complexity sources where rework risk is low and throughput is valued. The `post` chain's validation step (exit code 1 on errors) is the only hard gate in auto mode — it prevents malformed pages from entering the wiki but does not prevent content misalignment.

The 6-step post-chain (`post` command) is itself a rework prevention mechanism: validation, manifest, lint, and index checks run after every ingestion. If any step fails, the ingestion is not complete. This is the equivalent of the harness's commit gate — work is not "done" until the quality checks pass.

### Connection to Planning

Rework prevention and planning are the same investment viewed from different angles. Planning before execution is rework prevention in the future tense — "if I plan now, I avoid reworking later." Rework prevention analysis is planning in the past tense — "if I had planned better, I would not be here now."

The Harness Engineering insight that quantifies this: 5.5x planning overhead at the start of a task vs. 2.5x rework cost later. This means planning-as-rework-prevention breaks even at a rework probability of only 5.5/2.5 = 22%. If rework probability exceeds 22%, planning always wins. For LLM agents on complex tasks, rework probability without explicit planning is typically well above 22%.

## Open Questions

- Is there a way to measure rework rate per agent or per task type empirically, enabling calibrated prevention investment?
- Should the wiki's `smart` ingestion mode learn from past rework instances — tracking which source types or domains triggered rework — to refine its escalation heuristics?
- What is the rework cost model for an incorrect decision in `wiki/decisions/` that affects multiple downstream wiki pages?
- Can post-execution spec compliance review be automated — comparing generated pages against their source material programmatically?

## Relationships

- ENABLED BY: Always Plan Before Executing
- BUILDS ON: Agent Orchestration Patterns
- RELATES TO: Harness Engineering
- RELATES TO: OpenFleet
- RELATES TO: Plan Execute Review Cycle
- RELATES TO: Claude Code Best Practices
- RELATES TO: Wiki Ingestion Pipeline
- FEEDS INTO: Research Pipeline Orchestration

## Backlinks

[[Always Plan Before Executing]]
[[Agent Orchestration Patterns]]
[[Harness Engineering]]
[[OpenFleet]]
[[Plan Execute Review Cycle]]
[[Claude Code Best Practices]]
[[Wiki Ingestion Pipeline]]
[[Research Pipeline Orchestration]]
