---
title: "Always Plan Before Executing"
type: lesson
domain: ai-agents
layer: 4
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
    ingested: 2026-04-08
  - id: src-harness-engineering-github
    type: documentation
    url: "https://github.com/Chachamaru127/claude-code-harness"
    title: "claude-code-harness GitHub"
    ingested: 2026-04-08
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
    ingested: 2026-04-08
derived_from:
  - "Harness Engineering"
  - "OpenFleet"
  - "Claude Code"
  - "Synthesis: Claude Code Harness Engineering"
tags: [planning, agent-behavior, harness-engineering, openfleet, claude-code, plan-work-review, orchestration, rework-prevention, spec-driven]
---

# Always Plan Before Executing

## Summary

LLM agents produce dramatically better results when they produce an explicit plan before taking action — not as a soft heuristic, but as an enforced workflow step. This lesson is validated independently across three systems (OpenFleet, Harness Engineering, superpowers) that all converged on the same Plan → Execute → Review structure, each finding that skipping the planning phase causes rework, scope drift, and low-quality output that is expensive to recover from.

## Context

This lesson applies whenever an LLM agent is about to undertake a task with meaningful scope: modifying multiple files, dispatching subagents, ingesting a complex source, or making architectural decisions. It is most critical in autonomous or semi-autonomous contexts where human oversight is low and correction is expensive. It is less critical for trivial, single-step, easily reversible actions.

The triggering signal is any task that has multiple possible approaches, unclear scope, or downstream consequences that are hard to undo. In those cases, an agent that jumps directly to execution is likely to produce output that requires rework — which costs more tokens, more time, and more human attention than the planning step would have.

## Insight

LLM agents are token-greedy executors by default: given a task, the model's natural tendency is to start doing. This is efficient for simple tasks but catastrophic for complex ones, because the model's early decisions narrow the solution space in ways that may be incorrect, and partial work is often harder to correct than starting over.

Planning forces the agent to make its assumptions explicit before those assumptions are baked into actions. A written plan — whether a spec, an acceptance criteria list, or a decomposition into steps — surfaces ambiguity that the agent can resolve cheaply via a single question, rather than discovering the ambiguity mid-execution after multiple file edits have already been made.

The planning step is also the correct place for critic roles and review: a Planner + Critic reviewing a proposed approach before coding begins costs roughly 5.5x the tokens of the planning alone, but avoids rework whose cost would be far higher. Investing upfront in understanding consistently beats investing downstream in correction. This principle holds whether the "agent" is a single Claude Code session, a harness-orchestrated multi-worker flow, or a 10-agent deterministic fleet.

## Evidence

**Harness Engineering (claude-code-harness, Chachamaru127):**
The 5-verb workflow makes planning non-optional at the tool level: `/harness-plan` is a distinct phase that produces a spec with acceptance criteria before any coding begins via `/harness-work`. In Breezing mode, a Planner and Critic agent review the task quality before the coding worker executes. The ~5.5x token cost of the planning discussion (vs ~4x without) is explicitly justified as rework prevention. The workflow mirrors the superpowers pattern (brainstorm → plan → execute → verify) and the wiki's own ingestion pipeline (extract → analyze → synthesize → write → integrate).

**OpenFleet Deterministic Orchestrator:**
The 12-step 30-second orchestration cycle separates task definition from task dispatch. Tasks are created, blocked, scheduled, and reviewed through distinct states before they reach an agent for execution. The orchestrator never dispatches a task that has not passed the "readiness" state axis — a deterministic gate that enforces planning before execution at the system level, completely independent of any LLM's judgment. The multi-dimensional state model (lifecycle, execution, progress, readiness, validation, context) exists precisely to prevent premature dispatch.

**Superpowers Workflow:**
The superpowers skill set encodes planning as a required phase (`superpowers:writing-plans`, `superpowers:brainstorming`) that precedes execution (`superpowers:executing-plans`). These are separate skills with separate invocation — the architecture itself enforces the sequence. The `superpowers:brainstorming` skill is marked as something that "MUST" be used before any creative or implementation work, reflecting a hard-won understanding that skipping it degrades output quality.

**Claude Code Context Management:**
Even at the individual agent level, Claude Code's best practices recommend using Plans and Todos to externalize work structure before beginning complex tasks. This converts an implicit "I'll figure it out as I go" approach into an explicit decomposition that can be reviewed, corrected, and tracked. The plan becomes an external memory artifact that survives context compression and keeps the agent on track across a long session.

## Applicability

**Domains:** This lesson applies to any domain where an LLM agent has meaningful autonomy and actions have non-trivial cost or reversibility. Strongest applicability: coding agents, ingestion pipelines, deployment automation, multi-agent orchestration.

**Projects in the ecosystem:**
- **OpenFleet** — Already implements this at the orchestration layer via readiness gating. Lesson is confirmed, not new, for this project.
- **Research wiki ingestion** — The `guided` and `smart` ingestion modes implement planning gates (show extraction plan, wait for approval). The `auto` mode skips this and is appropriate only for high-confidence, low-complexity sources.
- **AICP / DSPD** — Any Claude Code session working on multi-file changes benefits from explicit `/plan` before `/execute`.
- **devops-control-plane** — Post-mortem analysis (24 rules from 16 post-mortems) represents the lesson encoded as system policy.

**When to skip:** Single-step reversible actions (reading a file, running a status command, generating a manifest). The overhead of formal planning exceeds the benefit when the action space is trivially small.

**Anti-pattern to avoid:** Treating planning as an optional courtesy step ("here's what I'm going to do...") rather than an enforced workflow gate. The lesson's value comes from making planning a blocker on execution, not a preamble that can be skimmed or skipped.

## Relationships

- DERIVED FROM: Harness Engineering
- DERIVED FROM: OpenFleet
- DERIVED FROM: Claude Code
- DERIVED FROM: Synthesis: Claude Code Harness Engineering
- RELATES TO: Claude Code Best Practices
- RELATES TO: Claude Code Skills
- RELATES TO: Research Pipeline Orchestration
- ENABLES: Rework Prevention
- BUILDS ON: Agent Orchestration Patterns

## Backlinks

[[Harness Engineering]]
[[OpenFleet]]
[[Claude Code]]
[[Synthesis: Claude Code Harness Engineering]]
[[Claude Code Best Practices]]
[[Claude Code Skills]]
[[Research Pipeline Orchestration]]
[[Rework Prevention]]
[[Agent Orchestration Patterns]]
[[Context Management Is the Primary LLM Productivity Lever]]
