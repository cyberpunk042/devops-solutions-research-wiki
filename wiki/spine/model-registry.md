---
title: "Model Registry"
type: reference
domain: cross-domain
layer: spine
status: synthesized
confidence: authoritative
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [models, registry, index, navigation, spine, entry-point]
---

# Model Registry

## Summary

This is the entry point for all named models in the wiki. A model is a coherent system definition — not a reading list but a real specification with standards, schemas, adoption guidance, and real examples. Each model has a companion standards page that defines what GOOD looks like for that domain. Use this page to find any model and assess its maturity.

## The Three-Layer Pattern

Every model follows the same three-layer structure:

| Layer | What it defines | Example |
|-------|----------------|---------|
| **System definition** (model page) | WHAT the system IS — architecture, components, member pages, adoption | [[Model: Methodology]] |
| **Execution standards** (standards page) | What GOOD looks like — gold standards, anti-patterns, checklists | [[Methodology Standards — What Good Execution Looks Like]] |
| **Visual design** | How pages LOOK — callout vocabulary, layout patterns | Covered by [[Wiki Design Standards — What Good Styling Looks Like]] for all models |

## Model Catalog

| Model | Lines | Standards Page | Maturity | Domain |
|-------|-------|---------------|----------|--------|
| [[Model: LLM Wiki]] | 444 | [[LLM Wiki Standards — What Good Looks Like]] | growing | Content structure |
| [[Model: Methodology]] | 568 | [[Methodology Standards — What Good Execution Looks Like]] | growing | Work processes |
| [[Model: Wiki Design]] | 368 | [[Wiki Design Standards — What Good Styling Looks Like]] | seed | Visual design |
| [[Model: Claude Code]] | 494 | [[Claude Code Standards — What Good Agent Configuration Looks Like]] | growing | Agent runtime |
| [[Model: Quality and Failure Prevention]] | 370 | [[Quality Standards — What Good Failure Prevention Looks Like]] | growing | Operational quality |
| [[Model: Skills, Commands, and Hooks]] | 349 | [[Extension Standards — What Good Skills, Commands, and Hooks Look Like]] | growing | Extension system |
| [[Model: Knowledge Evolution]] | 279 | [[Evolution Standards — What Good Knowledge Promotion Looks Like]] | growing | Evolution pipeline |
| [[Model: MCP and CLI Integration]] | 283 | — | growing | Tool integration |
| [[Model: Ecosystem Architecture]] | 293 | — | growing | Project topology |
| [[Model: Design.md and IaC]] | 174 | — | growing | Agent config patterns |
| [[Model: NotebookLM]] | 172 | — | growing | Research tooling |
| [[Model: SFIF and Architecture]] | 170 | — | growing | Build lifecycle |
| [[Model: Second Brain]] | 163 | — | growing | PKM theory |
| [[Model: Local AI ($0 Target)]] | 147 | — | growing | Cost reduction |
| [[Model: Automation and Pipelines]] | 144 | — | growing | Pipeline orchestration |

**Status:** 7 models done with full depth + standards pages. 8 models need the full treatment (document → design → implement → test).

## The Super-Model

The [[Model: Methodology]] is the super-model — it GOVERNS how all work proceeds. Every other model operates WITHIN its framework. When starting with this wiki, read Methodology first.

## How to Use This Registry

**If you're an agent from another project:**
1. Start here. Find the model relevant to your question.
2. Read the model page for the system definition.
3. Read the standards page (if it exists) for what good looks like.
4. Follow the adoption section to apply the model to your project.

**If you're building or reviewing a model:**
1. Use the `/build-model` command or invoke the `model-builder` skill.
2. Follow the model-builder skill's workflow: Document → Design → Scaffold → Implement → Test.
3. Every model needs: Key Pages table, Lessons Learned, State of Knowledge, How to Adopt (invariant vs per-project).
4. After the model is complete, create the companion standards page.

## Relationships

- RELATES TO: [[Model: Methodology]] (the super-model)
- RELATES TO: [[Model: LLM Wiki]] (the content structure model)
- RELATES TO: [[Model: Wiki Design]] (the visual design model)
- ENABLES: All models in this wiki

## Backlinks

[[Model: Methodology]]
[[Model: LLM Wiki]]
[[Model: Wiki Design]]
[[All models in this wiki]]
