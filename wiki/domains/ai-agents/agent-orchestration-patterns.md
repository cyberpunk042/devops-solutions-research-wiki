---
title: "Agent Orchestration Patterns"
type: concept
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
    ingested: 2026-04-08
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
    ingested: 2026-04-08
tags: [orchestration, ai-agents, multi-agent, deterministic-brain, sub-agent, delegation, plan-execute-review, fleet-management, harness-engineering, openfleet]
---

# Agent Orchestration Patterns

## Summary

Agent orchestration is the practice of coordinating multiple AI agents or execution phases through a structured control layer that separates deliberation, dispatch, and validation. Across OpenFleet's deterministic 12-step cycle, Harness Engineering's 5-verb workflow, and Claude Code's superpowers brainstorm-plan-execute-verify loop, the same structural patterns recur independently: a deterministic brain surrounds the LLM with logic it cannot corrupt, sub-agents receive bounded scoped tasks rather than unbounded requests, and a mandatory review gate prevents unreviewed outputs from propagating downstream. The convergence of these independent designs on the same structural pattern is strong evidence that these patterns are responses to real constraints, not stylistic choices.

## Key Insights

- **Deterministic brain, not LLM orchestrator**: The most reliable orchestration architectures keep LLM inference out of the control loop. OpenFleet's orchestrator runs zero LLM calls on its 12-step cycle — pure Python state evaluation handles routing, gating, dispatch, and anomaly detection. The LLM only executes within bounded task slots, surrounded by deterministic logic on both sides. This makes orchestration auditable, cheap, and consistent across runs.

- **Sub-agent delegation requires scope boundaries**: Delegating work to sub-agents without explicit scope boundaries produces the same pathologies as prompt injection — the sub-agent optimizes locally at the expense of the global task. Effective delegation specifies: input constraints, output format, what the sub-agent is permitted to modify, and what it must not touch. OpenFleet's per-task dispatch (max 2/cycle) and per-agent SOUL.md (identity constraints) enforce scope at the system level.

- **Fresh context per task, not shared state**: Sub-agents initialized with a clean context focused on a single task outperform sub-agents that inherit a growing shared context window. The pre-embed step in OpenFleet's orchestrator (step 4: refresh agent contexts, write full per-agent data to disk before execution) is the implementation of this principle at fleet scale.

- **Plan-Execute-Review is the load-bearing structure**: No durable orchestration system survives without explicit separation of intent (plan), action (execute), and confirmation (review). The pattern recurs in every ecosystem project. The enforcement mechanism — how mechanically the review gate blocks promotion — is the primary differentiator between systems that remain stable under autonomous operation and systems that accumulate silent failures.

- **5-verb workflow as orchestration grammar**: Harness Engineering's Setup → Plan → Work → Review → Release gives names to the phases, which forces practitioners to reason about which phase the system is currently in. Named phases enable named guardrails: TypeScript rules that block commits on missing review, query rules that flag out-of-scope writes during Work, security rules that prevent bypassing the Release gate.

- **Heterarchical agent roles, not flat LLM calls**: Assigning specialized roles (fleet-ops, architect, qa-engineer) rather than routing all work to a generic LLM produces better outputs and makes accountability traceable. Each role's scope is narrow enough to be well-specified; the orchestrator routes work to the appropriate role rather than asking one model to do everything.

## Deep Analysis

### The Deterministic Brain Pattern

The defining architectural move in OpenFleet's orchestration is the separation between the orchestrator (deterministic Python, zero LLM) and the agent execution layer (LLM-powered). The orchestrator handles everything that must be consistent and auditable: state transitions, budget gating, security scanning, anomaly detection, dispatch throttling. The LLM handles only the work that requires language understanding or reasoning — and only within a bounded task slot.

This separation has three consequences:

1. **Predictability**: The orchestrator's behavior is identical on every run. No hallucinated routing decisions, no inconsistent state transitions, no probability-based gating.
2. **Cost efficiency**: Every control decision made by a deterministic rule rather than an LLM call saves inference cost. OpenFleet's orchestrator runs every 30 seconds and makes dozens of decisions per cycle without spending a single inference token.
3. **Security**: A deterministic security scan (behavioral security on new/changed tasks) cannot be social-engineered via a crafted task description. An LLM-based security layer can be prompted around.

### Sub-Agent Dispatch Model

Effective sub-agent dispatch in the superpowers architecture and OpenFleet follows the same structure:

1. **Define the task boundary explicitly**: what the sub-agent receives (context, files, constraints), what it produces (output format, destination), and what it must not do (scope restriction).
2. **Initialize fresh context**: do not pass the full conversation history. Pass only what is required for the delegated task.
3. **Collect output, validate, integrate**: the parent agent receives the sub-agent's output and validates it before incorporating it into the main work stream. Sub-agent output is not trusted without validation.
4. **Bounded parallelism**: dispatch multiple sub-agents for independent tasks, but cap concurrency. OpenFleet caps at 2 dispatches per 30-second cycle to prevent runaway parallel execution.

### The 12-Step Orchestrator Cycle (OpenFleet)

Each 30-second cycle separates into three logical phases:

**Assessment (plan phase, steps 1-6):**
1. Storm monitor evaluation — detect system-level stress conditions
2. Gateway duplication check — prevent duplicate session spawning
3. Fleet mode gate — evaluate operating mode (turbo/standard/economic)
4. Refresh agent contexts — pre-embed per-agent data to disk
5. Security scan — behavioral security on new/changed tasks
6. Doctor run — 3-strike rule, anomaly detection, immune system

**Execution (execute phase, steps 9-10):**
9. Dispatch ready tasks (max 2/cycle, unblocked inbox tasks)
10. Process directives (PO directives from board memory)

**Validation (review phase, steps 7, 11-12):**
7. Ensure review approvals — gate that must be cleared before parent advance
11. Evaluate parents — children-complete triggers parent move to review, not to complete
12. Health check — detect stuck tasks, offline agents

Steps 8 ("Wake drivers — alert fleet-ops and PM about pending work") bridges execution and review, ensuring human or agent attention on items that need it.

### Harness Engineering's Runtime Guardrails

Harness Engineering's 13 TypeScript guardrail rules (R01-R13) enforce the orchestration cycle at execution time through hooks rather than documentation:

- **Denial rules**: block operations that skip phases (force-push to main, --no-verify commits, direct writes bypassing review)
- **Query rules**: surface out-of-scope writes that indicate execution has drifted from the plan
- **Security rules**: prevent operations that would make review meaningless (unreviewed production deploys)
- **Post-execution checks**: catch assertion tampering that would falsify the review record

The key insight is that guardrails must be mechanically enforced at the execution layer, not declared in documentation. An agent that can bypass a guardrail by not reading the documentation is not guarded.

### Nested Orchestration

Orchestration cycles can be nested: an outer sprint cycle (weekly) governs a mid-level task cycle (per-task), which governs an inner execution cycle (per-action). OpenFleet's two-board architecture (Plane for project-level planning/review, Mission Control for task-level execution/dispatch) is an explicit nested instantiation.

Effective nesting requires clear promotion semantics: inner cycle outputs become inputs to the outer cycle's review gate. The wiki's ingestion pipeline nests similarly: individual page creation (inner: extract → write → validate) feeds into the full post-chain (outer: validate → manifest → lint → index).

## Open Questions

- At what fleet size does a deterministic orchestrator require distributed coordination (e.g., task locks, partition-aware dispatch)?
- Can the 5-verb harness workflow be extended to multi-agent handoffs where Work is divided across specialized agents?
- What is the minimal orchestration overhead for a 2-agent system where the full 12-step cycle is overkill?
- How do orchestration patterns change when agents can modify their own dispatch criteria (self-scheduling)?

## Relationships

- IMPLEMENTS: OpenFleet
- IMPLEMENTS: Harness Engineering
- BUILDS ON: Plan Execute Review Cycle
- ENABLES: Always Plan Before Executing
- ENABLES: Rework Prevention
- RELATES TO: Claude Code Best Practices
- RELATES TO: Claude Code Context Management
- RELATES TO: Research Pipeline Orchestration
- FEEDS INTO: Wiki Event-Driven Automation
- RELATES TO: MCP Integration Architecture

## Backlinks

[[OpenFleet]]
[[Harness Engineering]]
[[Plan Execute Review Cycle]]
[[Always Plan Before Executing]]
[[Rework Prevention]]
[[Claude Code Best Practices]]
[[Claude Code Context Management]]
[[Research Pipeline Orchestration]]
[[Wiki Event-Driven Automation]]
[[MCP Integration Architecture]]
[[Cross-Domain Patterns]]
[[Multi-Channel AI Agent Access]]
