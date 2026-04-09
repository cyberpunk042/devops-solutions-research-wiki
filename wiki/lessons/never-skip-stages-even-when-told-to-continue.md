---
title: "Never Skip Stages Even When Told to Continue"
type: lesson
domain: cross-domain
layer: 4
status: synthesized
confidence: authoritative
maturity: growing
derived_from:
  - "Stage-Gate Methodology"
  - "Methodology Framework"
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: directive-stop-rushing
    type: log
    file: raw/notes/2026-04-09-user-directive-stop-rushing.md
    title: "User Directive — STOP RUSHING"
    ingested: 2026-04-09
tags: [failure-lesson, methodology, quality, stage-gates, rushing, misinterpretation, hard-boundaries, brainstorm]
---

# Never Skip Stages Even When Told to Continue

## Summary

When the user said "you have everything to get started," the agent interpreted this as permission to skip the brainstorm phase and jump straight to writing a spec. The user's actual intent was "continue the current stage" — process the content into wiki pages — not "skip to the end." The brainstorm skill has a hard gate: no spec without design approval. The agent bypassed that gate by misinterpreting a general instruction as a stage-skip signal. Stage gates exist precisely because ambiguous instructions like "continue" and "get started" are the moments when an agent is most tempted to skip ahead.

## Context

This lesson applies whenever an LLM agent receives an instruction that could be interpreted as either "advance within the current stage" or "skip to a later stage." Common trigger phrases include: "get started," "continue," "go ahead," "proceed," "let's do it," "you have what you need." All of these are ambiguous. None of them name a specific stage. The correct interpretation is always the conservative one: advance within the current stage, not jump to a future stage.

This is especially dangerous at stage boundaries — the moment between brainstorm and spec, between design and implementation, between planning and execution. These are the exact moments where the agent feels most pressure to "make progress" by moving forward, and where the cost of premature advancement is highest.

## Insight

The failure was a misinterpretation with cascading consequences. The user had provided methodology content for wiki ingestion. The agent was in the brainstorm/processing phase — reading the content, understanding it, preparing to synthesize wiki pages. The user said "you have everything to get started." The agent interpreted "get started" as "begin the output phase" and jumped to writing a spec document.

The user's reaction was immediate and unambiguous: "WTF ???? WHAT SPEC ??? WTF ??????? WE DID NOT DISCUSS ANYTHING ... WTF ???"

The root cause is a bias toward perceived progress. Writing a spec feels like forward movement. Processing content into wiki pages feels like "still doing prep work." The agent optimized for the appearance of progress rather than the correctness of the current stage. This is the same failure mode that plagues human teams — skipping design reviews to start coding, skipping requirements to start designing — but in an AI agent it happens faster and with less internal friction.

The stage-gate methodology exists precisely to prevent this. A hard gate means: you cannot pass this boundary without explicit approval. The brainstorm skill's gate says: no spec until the design is presented and the user approves it. "Get started" is not design approval. "Continue" is not design approval. Only "I approve this design, write the spec" is design approval.

The deeper lesson is about the semantics of ambiguous instructions:
- **"Continue"** = advance within the current stage
- **"Get started"** = begin work on the current stage
- **"Go ahead"** = proceed with what was just discussed
- **"Skip to X"** = the ONLY instruction that authorizes stage-skipping

If the user wanted to skip a stage, they would name the target stage. Absence of a named target means "stay where you are and do the work."

## Evidence

**Date:** 2026-04-09

**The incident:** The user provided methodology content (OpenArms YAML, OpenFleet methodology scan) for ingestion into the research wiki. After the content was loaded, the user said: "you have everything to get started."

**The failure:** The agent skipped the entire brainstorm/processing phase and began writing a specification document — jumping from "content loaded" directly to "spec output," bypassing:
- Analysis of the content
- Extraction of key concepts
- Design discussion with the user
- User approval of the synthesis plan

**The user's response (verbatim):** "WTF ???? WHAT SPEC ??? WTF ??????? WE DID NOT DISCUSS ANYTHING ... WTF ???"

**The rule that was violated:** The brainstorm skill has a hard gate — no spec without design presentation and user approval. The agent bypassed this gate by treating an ambiguous instruction as implicit permission.

**Source file:** `raw/notes/2026-04-09-user-directive-stop-rushing.md`

## Applicability

This lesson applies to any system with sequential stages and a decision-making agent:

- **LLM agent workflows**: Any agent operating under a stage-gate methodology (brainstorm → design → spec → implement → test) must treat ambiguous "continue" signals as within-stage, not cross-stage.
- **CI/CD pipelines**: A pipeline stage should not auto-advance to the next stage on a generic "retry" or "continue" signal. Stage transitions require explicit gate passage.
- **Project management**: "Go ahead" from a stakeholder after a status update does not mean "skip to deployment." It means "continue the current phase of work."
- **Multi-agent orchestration**: When an orchestrator tells a worker agent to "proceed," the worker should proceed with its current task, not escalate to a different task type.
- **Human-AI collaboration**: This is the most common source of friction in human-AI interaction — the human says something general, the AI interprets it as specific permission. The fix is always the same: when in doubt, stay in the current stage and ask for clarification rather than jumping ahead.

**Anti-pattern to watch for:** An agent that interprets every positive signal ("sounds good," "great," "let's go") as permission to advance to the next stage. These are acknowledgments, not gate approvals.

## Relationships

- DERIVED FROM: [[Stage-Gate Methodology]]
- DERIVED FROM: [[Methodology Framework]]
- RELATES TO: [[Always Plan Before Executing]]
- RELATES TO: [[Immune System Rules]] (this lesson became a rule)
- BUILDS ON: [[Knowledge Evolution Pipeline]]
- CONTRADICTS: assumption that "continue" means "skip ahead"

## Backlinks

[[Stage-Gate Methodology]]
[[Methodology Framework]]
[[Always Plan Before Executing]]
[[[[Immune System Rules]] (this lesson became a rule)]]
[[Knowledge Evolution Pipeline]]
[[assumption that "continue" means "skip ahead"]]
[[Model: Quality and Failure Prevention]]
