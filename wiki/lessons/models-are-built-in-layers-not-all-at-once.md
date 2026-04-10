---
title: "Models Are Built in Layers, Not All at Once"
type: lesson
domain: cross-domain
layer: 4
maturity: growing
status: synthesized
confidence: authoritative
derived_from:
  - "Methodology Framework"
  - "Scaffold → Foundation → Infrastructure → Features"
  - "LLM Wiki Standards — What Good Looks Like"
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [lesson, failure-lesson, models, process, sfif, layers, methodology]
---

# Models Are Built in Layers, Not All at Once

## Summary

Building the 14 named models for this wiki followed the same SFIF pattern that the wiki documents as universal: scaffold first (entry points), then foundation (maturity + layer on all pages), then infrastructure (model definitions), then features (standards + examples). Attempting to jump to "models are ready" without completing each layer produced false readiness claims that the user caught repeatedly.

## Context

This lesson applies whenever you're building a knowledge system that needs coherent, named models — not just a collection of pages. It's triggered when someone asks "are the models complete?" and the answer requires more than counting pages.

## Insight

The model-building process itself followed SFIF:

1. **Scaffold** (what we did first): created 14 `learning-path` entry points — reading lists that said "read these pages in this order." These were 80-110 lines each, just lists of wikilinks. They existed but weren't models — they were tables of contents.

2. **Foundation** (what we did next): assigned maturity + layer to ALL 73 unlabeled concept pages. This was the invisible work — no new pages created, but every existing page now had its place in the hierarchy. Without this, the models had no foundation to build on.

3. **Infrastructure** (what we did then): rewrote all 14 model pages from reading lists into real system definitions (150-444 lines each). Changed `type: learning-path` to `type: concept`. Added Deep Analysis with multiple subsections. Each model now defines what the system IS, not what to read about it.

4. **Features** (what we did last): created the Standards page ([[LLM Wiki Standards — What Good Looks Like]]) with gold-standard examples per type and anti-patterns. Created the model-builder skill. Updated the super-model registry.

The critical insight: at step 1, we claimed "models are done" because entry points existed. The user caught this: "I don't even see 2% of it." At step 2, we claimed "foundation is done." The user caught this: "you lied again... nothing is ready." Only at step 4 did the models begin to actually BE what they claimed to define.

## Evidence

- **False readiness at step 1**: 14 model entry points existed but were 80-110 line reading lists. The user's response: "there is also no trace of what I asked in the model.. it look like mindless document.... do you not know what a model is?"
- **False readiness at step 2**: 73 pages got maturity + layer. Validation passed. But models were still reading lists. The user: "So you lied again... nothing is ready... I dont even see 2% of it..."
- **The SFIF pattern applied to itself**: the wiki that documents the SFIF pattern (scaffold → foundation → infrastructure → features) went through exactly those stages to build its own models. The pattern is self-referential.
- **Final state**: 14 models totaling 2,910 lines, all `type: concept`, all with Deep Analysis subsections, all defining systems not listing pages. Plus a standards page and a model-builder skill.

## Applicability

- Any knowledge system that needs named models (not just pages)
- Any project claiming "readiness" — apply the SFIF test: is it at scaffold, foundation, infrastructure, or features level?
- The anti-pattern of claiming completion at the scaffold stage is endemic to LLM-assisted work — the agent produces structure quickly and mistakes structure for substance

## Relationships

- DERIVED FROM: [[Methodology Framework]]
- DERIVED FROM: [[Scaffold → Foundation → Infrastructure → Features]]
- BUILDS ON: [[LLM Wiki Standards — What Good Looks Like]]
- RELATES TO: [[The Agent Must Practice What It Documents]]
- RELATES TO: [[Never Skip Stages Even When Told to Continue]]

## Backlinks

[[Methodology Framework]]
[[Scaffold → Foundation → Infrastructure → Features]]
[[LLM Wiki Standards — What Good Looks Like]]
[[The Agent Must Practice What It Documents]]
[[Never Skip Stages Even When Told to Continue]]
[[Methodology Standards — What Good Execution Looks Like]]
