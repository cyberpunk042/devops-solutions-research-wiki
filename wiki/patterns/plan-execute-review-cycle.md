---
title: "Plan Execute Review Cycle"
type: pattern
domain: cross-domain
layer: 5
status: synthesized
confidence: high
maturity: growing
derived_from:
  - "Harness Engineering"
  - "OpenFleet"
  - "Claude Code"
  - "Research Pipeline Orchestration"
instances:
  - page: "OpenFleet"
    context: "Deterministic 9-step orchestrator cycle: storm monitor → security scan → doctor run → ensure review approvals → dispatch ready tasks → evaluate parents. Review is structurally enforced before task completion."
  - page: "Harness Engineering"
    context: "5-verb workflow: Setup → Plan → Work → Review → Release. Runtime guardrails (13 TypeScript rules R01-R13) enforce the cycle at execution time, not just as model instructions."
  - page: "Claude Code"
    context: "Superpowers plugin brainstorm → plan → execute → verify cycle. Plans and todos externalize state from context window, structuring the cycle explicitly across sessions."
  - page: "Research Pipeline Orchestration"
    context: "Wiki-agent 5-stage pipeline: EXTRACT → ANALYZE → SYNTHESIZE → WRITE → INTEGRATE, with 6-step post-chain that enforces validation and review after every write."
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
  - id: src-karpathy-claude-code-10x
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=7sInxhTDA7U"
    title: "Andrej Karpathy Just 10x'd Everyone's Claude Code"
  - id: src-user-directive-integration
    type: notes
    file: raw/notes/2026-04-08-user-directive-integration-vision.md
    title: "User Directive — Integration Vision & Service Architecture"
tags: [plan-execute-review, orchestration, agent-workflow, feedback-loop, guardrails, deterministic, multi-pass, cross-domain, harness-engineering, openfleet]
---

# Plan Execute Review Cycle

## Summary

The Plan→Execute→Review cycle is a recurring structural pattern observed independently across AI agent orchestration systems, coding harnesses, and knowledge pipelines: every durable system that involves autonomous or semi-autonomous execution enforces a discrete planning phase before action, a bounded execution phase, and a mandatory review/validation gate before state is committed or promoted. This pattern emerges not from shared design but from shared necessity — unconstrained execution without planning produces drift, and execution without review produces silent failure. The pattern's strength scales directly with how mechanically review is enforced: systems that treat review as a suggestion degrade over time, while systems that treat review as a hard gate remain stable and auditable.

## Pattern Description

At its core, the Plan→Execute→Review cycle separates three fundamentally different cognitive modes: **deliberation** (what should happen and in what sequence), **action** (doing the work within bounded scope), and **verification** (confirming the result matches intent before propagating). Each phase has a distinct failure mode when absent or collapsed.

Without an explicit plan phase, execution becomes prompt-reactive — the system takes the most locally plausible action rather than the globally correct one. This produces correct-looking results that accumulate into wrong outcomes. Without an explicit review gate, execution results are accepted and promoted based on recency bias rather than correctness. Errors compound silently until they become systemic.

The pattern is recognizable by three structural signals: (1) a separation boundary between intent and execution — tasks are defined before they are dispatched, (2) a review gate that must be cleared before state promotion — completed work is not finished until reviewed, and (3) some form of enforcement — the review gate is mechanically blocked, not just recommended.

The enforcement mechanism is the key differentiator between weak and strong implementations. Weak implementations state the cycle in documentation (CLAUDE.md, README, team norms). Strong implementations mechanically enforce it: OpenFleet's deterministic brain will not dispatch a task until it passes the security scan and doctor checks; the harness guardrail engine blocks commit operations that skip the review verb; the wiki post-chain blocks completion if validate returns non-zero.

The cycle can be instantiated at any granularity — a 30-second orchestrator tick, a multi-day sprint, a single ingestion run — and nested: an outer Plan→Execute→Review governs a project sprint while an inner one governs each individual task within it. Nesting is visible in OpenFleet's two-board architecture (Plane governs the planning/review layer; Mission Control governs the execution/dispatch layer).

## Instances

### OpenFleet — Deterministic Orchestrator Cycle

OpenFleet's 30-second orchestrator tick is the most mechanically pure implementation in the ecosystem. The 9-step cycle (expanded to 12 steps in the deep analysis) enforces the pattern at runtime with zero LLM involvement:

- **Plan phase**: Steps 1-6 constitute situational assessment — storm monitor evaluation, gateway duplication check, fleet mode gate, context refresh, security scan (behavioral security on new/changed tasks), doctor run (immune system: 3-strike rule, anomaly detection). No task moves forward until these pass.
- **Execute phase**: Steps 9-10 — dispatch ready tasks (max 2/cycle) and process PO directives. Bounded: max 2 dispatches per cycle prevents runaway execution.
- **Review phase**: Step 7 (ensure review approvals) and Step 11 (evaluate parents — when all children are done, parent moves to review, not to complete). The parent task can only advance once the review approval gate is cleared.

The cycle's determinism is the architectural achievement. OpenFleet's insight is that the plan/review phases should not involve LLM inference — they should be pure Python state evaluation, making them auditable, fast, and cheap. The LLM operates only within the execute phase (L3 Agent Execution), surrounded by a deterministic shell on both sides.

### Harness Engineering — 5-Verb Workflow with Runtime Guardrails

The claude-code-harness project codifies the pattern as explicit named verbs: **Setup → Plan → Work → Review → Release**. The naming itself is the first insight: giving each phase a proper name forces practitioners to acknowledge which phase they are in and resist collapsing them.

The 13 TypeScript guardrail rules (R01-R13) enforce the cycle at execution time through hooks. Denial rules block operations that would bypass review (force-push, --no-verify). Query rules flag out-of-scope writes that indicate execution has drifted from plan. Security rules prevent operations that would make review meaningless (direct main pushes). Post-execution checks catch assertion tampering that would falsify the review record.

The Breezing mode adds a Planner + Critic role pair that review task quality before the Work phase begins — an inner plan/review cycle nested inside the outer Planning phase. At ~5.5x token cost vs ~4x without the discussion, this is a deliberate trade: front-load verification cost to reduce rework cost downstream. This is structurally identical to the wiki's "guided" ingestion mode, which shows an extraction plan and waits for approval before writing any pages.

### Claude Code — Superpowers Brainstorm→Plan→Execute→Verify

The Claude Code superpowers plugin externalizes the cycle as explicit slash commands: brainstorm → plan → execute → verify. The plan is written to a file before any execution begins. The verify step is invoked after execution to check results against the written plan. This externalization solves the context window problem: the plan persists across compactions and subagent invocations, maintaining cycle coherence even when the model's working memory is reset.

Plans and todos serve a structural function beyond task management: they are the boundary object between the plan phase and the execute phase. Once a plan is written and approved, it constrains what the execute phase can legitimately do. Deviations require explicit plan updates, surfacing scope creep as a visible event rather than silent drift.

### Research Pipeline Orchestration — Extract→Analyze→Synthesize→Write→Integrate

The wiki's ingestion pipeline is a 5-stage instantiation of the cycle: **EXTRACT → ANALYZE → SYNTHESIZE → WRITE → INTEGRATE**. The plan phase is EXTRACT+ANALYZE (read source material, identify key concepts, map to existing knowledge). The execute phase is SYNTHESIZE+WRITE (create page content). The review phase is INTEGRATE (post-chain: validate schema → regenerate manifest → lint → rebuild indexes — all six steps must pass before the ingestion is considered complete).

The post-chain's validation step is a hard gate: `python3 -m tools.validate` returns exit code 1 on errors, blocking completion. This is the same structural principle as OpenFleet's review approval gate — completion is not granted, it must be cleared.

The multi-pass ingestion directive ("ingestion is multi-pass, not one-shot") extends the pattern to multiple nested cycles: Pass 1 extracts individual pages (plan→execute→review per page), Pass 2 runs cross-reference analysis (plan: gap analysis → execute: update relationships → review: validate all links), and future passes deepen thin pages. The outer cycle's review phase feeds back into the next cycle's plan phase, creating a compounding knowledge loop.

## When To Apply

Apply this pattern when:

- **Execution has side effects that are expensive or hard to reverse**: database writes, git commits, published content, task dispatches. The review gate prevents irreversible errors from propagating.
- **The executor (human or AI) is operating with bounded context or partial information**: the plan phase surfaces assumptions before action; the review phase detects where assumptions were wrong.
- **Work spans multiple sessions or agents**: an externalized plan (file, board, todo list) maintains cycle coherence when the executor's working memory is reset or when work is handed between agents.
- **Quality must be auditable post-hoc**: the separation of plan, execute, and review creates a traceable record of intent vs. outcome.
- **Execution is parallel or concurrent**: review gates prevent race conditions where one worker's unreviewed output becomes another worker's input before validation.
- **The system must remain stable under autonomous operation**: deterministic review gates (like OpenFleet's orchestrator) allow autonomous execution without human supervision because quality is enforced mechanically, not by human attention.

## When Not To

Avoid or simplify this pattern when:

- **Execution is inherently exploratory and reversible**: interactive debugging, prototyping, brainstorming. Enforcing plan/review on exploratory work adds friction without safety benefit. The wiki's `auto` ingestion mode (no review gates) is appropriate for low-risk, high-confidence sources.
- **The plan phase cannot be meaningfully separated from execution**: some tasks are only understood by doing them. Forcing upfront planning produces fake plans that are immediately abandoned. In these cases, defer to a lighter checkpoint-review pattern rather than full plan/execute/review.
- **Review latency exceeds the cost of occasional errors**: in high-frequency, low-stakes loops (e.g., 30-second telemetry polling), mandatory human review at each cycle is counterproductive. OpenFleet's solution is automated review (deterministic checks), not skipped review.
- **The review gate becomes a rubber stamp**: if review approvals are granted automatically or without genuine checking, the gate provides false assurance while adding overhead. This is worse than no review gate — it makes errors look reviewed. The harness engineering insight applies: review must be mechanically enforced, not just socially expected.
- **Nesting depth exceeds human comprehension**: deeply nested plan/execute/review cycles (outer sprint → inner sprint → task → subtask) can make it unclear which level's review gate applies. Limit nesting to 2-3 levels; collapse deeper levels into flat task lists.

## Relationships

- DERIVED FROM: Harness Engineering
- DERIVED FROM: OpenFleet
- DERIVED FROM: Claude Code
- DERIVED FROM: Research Pipeline Orchestration
- RELATES TO: Wiki Ingestion Pipeline
- RELATES TO: Claude Code Best Practices
- RELATES TO: Claude Code Skills
- RELATES TO: MCP Integration Architecture
- ENABLES: Wiki Event-Driven Automation
- BUILDS ON: Agent Orchestration Patterns

## Backlinks

[[Harness Engineering]]
[[OpenFleet]]
[[Claude Code]]
[[Research Pipeline Orchestration]]
[[Wiki Ingestion Pipeline]]
[[Claude Code Best Practices]]
[[Claude Code Skills]]
[[MCP Integration Architecture]]
[[Wiki Event-Driven Automation]]
[[Agent Orchestration Patterns]]
[[Context Management Is the Primary LLM Productivity Lever]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
