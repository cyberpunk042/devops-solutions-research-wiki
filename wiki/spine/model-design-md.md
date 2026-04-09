---
title: "Model: Design.md + IaC"
type: learning-path
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [model, learning-path, spine, design-md, iac, markdown-config, claude-md, agents-md]
---

# Model: Design.md + IaC

## Summary

The Design.md + IaC model describes how markdown files placed at the project root serve as AI configuration — binding constraints that AI agents read and execute rather than documentation humans write and forget. The pattern started with CLAUDE.md (project instructions, coding conventions, quality gates) and extended with DESIGN.md (visual design systems with semantic color naming, typography tables, and do/don't guardrails) and AGENTS.md (build and architecture instructions). The awesome-design-md repository catalogues 58 design systems captured in this format, including Claude (Anthropic)'s own 312-line DESIGN.md. Together these files represent a generalization of Infrastructure as Code into the AI agent domain: the human writes the specification, the agent reads it as binding constraints.

## Prerequisites

- Understanding of how CLAUDE.md is consumed by Claude Code at session start
- Familiarity with context budget constraints (token cost of always-loaded files)
- Basic UI/design vocabulary helpful but not required for the IaC principles

## Sequence

### Layer 2 — Core Concepts

1. **Design.md Pattern** ([[Design.md Pattern]])
   Entry point. Explains the 9-section standard structure with concrete content from Claude's 312-line DESIGN.md: Visual Theme (prose intent + characteristics), Color Palette (16 named colors with hex + role + rationale), Typography (16-role table), Component Styles (5 named button variants with full CSS), Layout Principles (8px base unit, 7-level border-radius scale), Depth & Elevation (5-level system), Do's and Don'ts (10 concrete rules each), Responsive Behavior (5 breakpoints), and the unique Agent Prompt Guide section (ready-to-paste component prompts + 7-rule iteration guide). Key insight: DESIGN.md captures design reasoning (WHY ring shadows over drop shadows), not just design decisions (what hex values to use).

2. **Infrastructure as Code Patterns** ([[Infrastructure as Code Patterns]])
   The broader pattern. Places CLAUDE.md, DESIGN.md, AGENTS.md, SOUL.md, HEARTBEAT.md, config/schema.yaml, stacks/*.yml, .env.example, setup.py, and service templates all on the same IaC spectrum. The core principle: if a system needs to be configured, write a specification file. The executor might be Terraform, systemctl, Claude Code, or a Python validator — specification → execution is the pattern.

3. **Claude Code Best Practices** ([[Claude Code Best Practices]])
   CLAUDE.md verbosity tradeoffs: every token in CLAUDE.md costs context budget on every turn. Accuracy degrades at 40% context usage, becomes unreliable at 60%+. Practical guidance: keep always-loaded CLAUDE.md under ~200 lines; put detailed workflows in skills loaded on demand. This wiki's CLAUDE.md (~250+ lines) is at the upper boundary.

4. **Context-Aware Tool Loading** ([[Context-Aware Tool Loading]])
   The two-tier configuration model: static context (CLAUDE.md, DESIGN.md — loaded at session start, always present, always consuming budget) vs dynamic context (skills — loaded when relevant, zero overhead when not invoked). Design.md as static context is only appropriate when UI generation is the primary session task.

### Layer 4 — Lessons

5. **Skills Architecture Is the Dominant LLM Extension Pattern** ([[Skills Architecture Is the Dominant LLM Extension Pattern]])
   The distilled lesson: static markdown config (CLAUDE.md) and dynamic skill loading (skills/) form a two-tier IaC stack. The skill system handles the 80% of context that is only needed sometimes — keeping the always-loaded layer lean and accurate.

6. **Infrastructure Must Be Reproducible, Not Manual** ([[Infrastructure Must Be Reproducible, Not Manual]])
   CLAUDE.md, DESIGN.md, and setup.py are only IaC if they are version-controlled and actually executed. Manual setup steps that exist only in developer memory are the anti-pattern this model eliminates.

### Layer 6 — Decisions

7. **Decision: MCP vs CLI for Tool Integration** ([[Decision: MCP vs CLI for Tool Integration]])
   Directly relevant: MCP server schemas load into every session (like an oversized static DESIGN.md). The decision to prefer CLI+Skills for wiki operations is the IaC model applied to tooling selection — load only what is needed, when it is needed.

## Evidence: The awesome-design-md Corpus

The VoltAgent/awesome-design-md repository contains 58+ Design.md files for real production design systems: Claude (Anthropic), Stripe, Vercel, Linear, Figma, Spotify, Tesla, and dozens more. Each includes preview.html and preview-dark.html for human verification. This corpus provides concrete templates for any project that wants AI agents to generate consistent, on-brand UI without specification drift.

Key pattern from the corpus: every DESIGN.md includes a Do's and Don'ts section with 10+ concrete rules. This section is the guardrail layer — it prevents AI from regressing to generic defaults (gradients, bold serifs, cool grays, drop shadows) that are absent from the explicit specification but implied by training data averages.

## Outcomes

After completing this path you understand:

- How DESIGN.md, CLAUDE.md, and AGENTS.md form a companion file ecosystem for complete AI agent context
- The 9-section standard structure and what each section achieves (semantic naming, enforcement guardrails, design reasoning)
- Why semantic color naming ("use Parchment" not "use #f5f4ed") matters for AI agent consistency
- The context budget constraint and the rule of thumb: keep static config lean, defer details to skills
- How config/schema.yaml, stacks/*.yml, and service templates extend IaC into the AI-native domain
- Where to find 58+ production-grade Design.md templates (awesome-design-md)

## Relationships

- BUILDS ON: [[Design.md Pattern]]
- BUILDS ON: [[Infrastructure as Code Patterns]]
- RELATES TO: [[Model: Quality + Failure Prevention]]
- RELATES TO: [[Model: SFIF + Architecture]]
- RELATES TO: [[Model: Automation + Pipelines]]
- ENABLES: [[Claude Code Best Practices]]

## Backlinks

[[Design.md Pattern]]
[[Infrastructure as Code Patterns]]
[[Model: Quality + Failure Prevention]]
[[Model: SFIF + Architecture]]
[[Model: Automation + Pipelines]]
[[Claude Code Best Practices]]
[[Model: NotebookLM]]
[[Model: Quality and Failure Prevention]]
