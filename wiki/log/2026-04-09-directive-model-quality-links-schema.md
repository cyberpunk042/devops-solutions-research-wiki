---
title: "Model Quality + Links + Schema Naming Issues"
type: note
domain: log
note_type: directive
status: active
confidence: high
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [log, directive, quality, links, schema, models]
---

# Model Quality + Links + Schema Naming Issues

## Summary

Three quality issues identified during model review: (1) broken backlinks formatting with double-bracket corruption, (2) the LLM Wiki model page conflates project-specific tooling with the universal model definition, and (3) schema.yaml naming conventions will cause confusion when adopted by other codebases in the ecosystem.

## Operator Directive (verbatim)

> (about the links) Can we make sure this doesn't happens ? directives and/or automated
>
> Also the backlinks there is a weird thing happening too ([[ and ]] everywhere, sometimes one "[" part of the link sometimes not?):
> [[Knowledge Evolution Pipeline]] [[Progressive Distillation]] [[Model: Automation + Pipelines]] Model: Local AI ($0 Target) [[Decision: Wiki-First with LightRAG Upgrade Path]]
>
> Also the model you produced is too vague and corrupted.... there are whole sections that make no sense like the "Pipeline Commands"... as if it was part of the model ? wtf ? a model is for everyone, not just for our current project... stop conflating everything.... the most important pieces are in the schema.yaml.. which you should call otherwise... it will be way too confusing..... wtf lol... as if it was going to be the only schema in a codebase....
> your page is passable at best, clearly not ready

## Issues

1. **Broken backlinks**: Obsidian.py generates `[[double-bracketed]]` backlinks when Relationship targets already have `[[]]`. Also some targets missing brackets entirely.
2. **Model conflates project with universal**: Pipeline Commands, interface tables, /commands — these are THIS project's implementation, not the universal LLM Wiki model. A model is transferable. Project-specific tooling is an instance.
3. **schema.yaml naming**: Calling it `config/schema.yaml` will collide with any other schema in a project. Needs a wiki-specific name like `wiki-schema.yaml` or `wiki/config/schema.yaml`.
