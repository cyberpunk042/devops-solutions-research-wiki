---
title: "Methodology Is Flexible — Multiple Chains, Not One Fixed Pipeline"
type: note
domain: log
note_type: directive
status: active
confidence: high
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [log, directive, methodology, flexibility, chains, conditions]
---

# Methodology Is Flexible — Multiple Chains, Not One Fixed Pipeline

## Summary

The methodology model page presents a SINGLE fixed 5-stage pipeline as if it's the entire methodology. But the user explicitly said the methodology is FLEXIBLE — it can contain multiple chains/groups of stages for various cases, with conditions that determine which pattern applies. The current model page is making the same mistake as the first LLM Wiki model — getting lost in one specific case instead of presenting the framework.

## Operator Directive (verbatim)

> your methodology doesn't work... I told you it was flexible and its was possible to have multiple chains / group of stage for various cases and there was conditions possible like way to determine which pattern is applied to which methodology sequence...
> You did a similar as you had done the first time with llm-wiki, you got lost into a precise case.....

## What Failed

The Methodology model page presents:
- ONE 5-stage sequence (document → design → scaffold → implement → test) as THE methodology
- Task types that select SUBSETS of that one sequence
- But NOT: multiple completely different stage sequences for different situations
- But NOT: conditions that determine which sequence applies
- But NOT: the composability that was discussed (sequential, nested, conditional, parallel)

The Methodology Framework page (wiki/domains/cross-domain/methodology-framework.md) DOES cover composability, but the Model: Methodology page collapsed it back into one fixed pipeline.

## What It Should Be

The methodology is a FRAMEWORK for defining work processes, not a single process:
- Multiple named sequences (e.g., "research" = document→design, "feature-dev" = all 5, "hotfix" = implement→test, "knowledge-evolution" = document→implement)
- Conditions that select which sequence applies (task_type is ONE condition, but also: project phase, domain, scale, urgency)
- Ability to compose sequences (run A then B, nest B inside A's stage, branch conditionally)
- The 5-stage sequence is ONE INSTANCE, not the whole framework
