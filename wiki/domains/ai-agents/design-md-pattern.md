---
title: "Design.md Pattern"
type: concept
layer: 2
maturity: growing
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-09
sources:
  - id: src-design-md-research
    type: article
    url: "https://github.com/VoltAgent/awesome-design-md"
    file: raw/articles/design-md-pattern-research.md
    title: "Design.md Pattern Research"
    ingested: 2026-04-08
  - id: src-google-stitch-design-md
    type: article
    url: "https://www.mindstudio.ai/blog/what-is-google-stitch-design-md-file"
    title: "What Is Google Stitch's Design.md File?"
    ingested: 2026-04-08
  - id: src-awesome-design-md
    type: documentation
    url: "https://github.com/VoltAgent/awesome-design-md"
    file: raw/articles/voltagentawesome-design-md.md
    title: "VoltAgent/awesome-design-md — 58 Design Systems"
    ingested: 2026-04-09
  - id: src-claude-design-md-example
    type: documentation
    file: raw/articles/claude-design-md-example.md
    title: "Claude (Anthropic) Design.md — 312-line machine specification"
    ingested: 2026-04-09
tags: [design-md, design-system, ai-agents, claude-md, google-stitch, markdown-config, ui-consistency, agent-context]
---

# Design.md Pattern

## Summary

Design.md is a plain-text design system document introduced by Google Stitch that AI coding agents read to generate consistent UI. It captures an entire visual design system — colors, typography, spacing, component patterns, responsive behavior — in a single markdown file placed at the project root. When an AI agent generates UI code, it reads Design.md as binding constraints rather than making arbitrary visual decisions. This extends the CLAUDE.md pattern (project instructions for agent behavior) into the visual design domain, and represents a broader convergence on "markdown files as AI configuration."

## Key Insights

- **9-section standard structure — with concrete content**: Visual Theme (atmospheric description + key characteristics list), Color Palette (named colors with hex + functional role + design rationale), Typography (16-role hierarchy table with size/weight/line-height/letter-spacing per role), Component Styles (5+ button variants with exact padding/radius/shadow CSS), Layout Principles (spacing scale, grid, whitespace philosophy, 7-level border-radius scale), Depth & Elevation (5-level system from flat to inset), Do's and Don'ts (10 concrete rules each with specific values), Responsive Behavior (5 breakpoints with collapse strategy), and Agent Prompt Guide (quick color reference + ready-to-paste component prompts + 7-rule iteration guide). The Claude DESIGN.md is 312 lines — not a summary, a complete machine specification.

- **Semantic color naming as AI vocabulary**: Every color in a DESIGN.md gets a NAME (Parchment, Terracotta Brand, Olive Gray), a HEX value (#f5f4ed, #c96442, #5e5d59), a FUNCTIONAL ROLE (primary background, brand CTA, secondary body text), and a DESIGN RATIONALE ("warm cream with a yellow-green tint that feels like aged paper"). The name becomes the agent's working vocabulary: prompt says "use Parchment" not "use #f5f4ed." This gives the AI a shared language with the designer.

- **Constraint-based generation**: Google Stitch passes the full Design.md as context alongside every prompt to Gemini. The model treats it as binding constraints — your specific hex values, font families, and spacing scales, not generic defaults.

- **58+ design systems already captured**: The VoltAgent/awesome-design-md repository contains Design.md files for Claude, Stripe, Vercel, Linear, Figma, Spotify, Tesla, and dozens more. Drop one into a project and AI agents build matching UI.

- **Companion files ecosystem**: DESIGN.md (how it should look) complements CLAUDE.md (how the agent should behave) and AGENTS.md (how to build). Together they give an AI agent complete project context without stuffing everything into a single file.

- **Tool-agnostic**: Consumed by Google Stitch, Claude Code, Cursor, Gemini CLI, and Antigravity. The markdown format is the interoperability layer — any tool that reads markdown can use it.

- **Preview artifacts**: Each Design.md comes with preview.html and preview-dark.html files that render the design system visually, allowing human verification before AI generates code.

- **The Agent Prompt Guide section is unique to DESIGN.md**: No other design spec format (Figma tokens, Storybook, design tokens JSON) includes a section of ready-to-paste AI prompts. Claude's DESIGN.md includes 5 complete component prompts with exact values baked in ("Create a hero section on Parchment (#f5f4ed) with a headline at 64px Anthropic Serif weight 500, line-height 1.10...") plus a 7-rule iteration guide that teaches the agent HOW to use the file (e.g., "Reference specific color names — 'use Olive Gray (#5e5d59)' not 'make it gray'"). This is a design file that contains its own usage manual for AI.

- **DESIGN.md captures design reasoning, not just design decisions**: The ring shadow philosophy in Claude's DESIGN.md specifies `0px 0px 0px 1px` patterns as "borders that are technically shadows" — a shadow pretending to be a border, or a border that's technically a shadow. CSS source code alone records the values; DESIGN.md records the WHY. This preserved reasoning prevents AI from replacing ring shadows with drop shadows (which are visually similar but philosophically wrong for this design system).

- **The gradient-free declaration — DESIGN.md captures what you DON'T do**: Claude's design explicitly states it is "gradient-free in the traditional sense." The Do's and Don'ts section is enforcement guardrails for the AI. 10 Don'ts with specific values: "Don't use cool blue-grays anywhere," "Don't use bold (700+) weight on Anthropic Serif," "Don't apply heavy drop shadows." Without this section, an AI generating UI would naturally reach for gradients, bold headings, and drop shadows — the three most common defaults in generated UIs. DESIGN.md's Don'ts section prevents regression to the mean.

## Deep Analysis

### What a Real DESIGN.md Looks Like: Claude's 312-Line Specification

The Claude (Anthropic) DESIGN.md is a concrete reference for what production-grade DESIGN.md files contain. It is not a summary — it is a machine specification.

**Section 1 — Visual Theme & Atmosphere**: Opens with a prose description of the design intent ("a literary salon reimagined as a product page — warm, unhurried, and quietly intellectual"), then a Key Characteristics bullet list with 7 items. This prose is not decoration — it is the semantic frame the AI uses to resolve ambiguous decisions not covered by explicit rules.

**Section 2 — Color Palette & Roles**: 16 named colors across 6 groups (Primary, Secondary & Accent, Surface & Background, Neutrals & Text, Semantic & Accent, Gradient System). Each entry has: semantic name, hex value, functional role, and rationale. Example: "Parchment (`#f5f4ed`): The primary page background — a warm cream with a yellow-green tint that feels like aged paper. The emotional foundation of the entire design." The Gradient System entry explicitly states the design is gradient-free, explaining the deliberate architectural choice.

**Section 3 — Typography Rules**: A 16-row table covering every text role from Display/Hero (64px, Anthropic Serif, weight 500, line-height 1.10) to Micro (9.6px, Anthropic Sans). Each row specifies: role name, font family, size, weight, line-height, letter-spacing, and notes. Followed by 5 typography principles explaining the reasoning (e.g., "Single weight for serifs: All Anthropic Serif headings use weight 500 — no bold, no light. This creates a consistent 'voice' across all headline sizes").

**Section 4 — Component Stylings**: 5 named button variants (Warm Sand, White Surface, Dark Charcoal, Brand Terracotta, Dark Primary) with full CSS-ready specs: background hex, text hex, padding values, radius, and complete shadow syntax. Example: `#e8e6dc 0px 0px 0px 0px, #d1cfc5 0px 0px 0px 1px`. Also covers Cards & Containers, Inputs & Forms, Navigation, Image Treatment, and 3 Distinctive Components.

**Section 5 — Layout Principles**: Base unit (8px), full spacing scale (3px through 30px), container max-width, and a 7-level border-radius scale (4px sharp through 32px maximum rounded). Each radius level has a name ("comfortably rounded," "generously rounded," "very rounded") that becomes the AI's vocabulary.

**Section 6 — Depth & Elevation**: A 5-level system (Flat → Contained → Ring → Whisper → Inset) as a table with treatment and use cases. The shadow philosophy prose explains that ring shadows are "borders that are technically shadows" — this design rationale cannot be inferred from CSS values alone.

**Section 7 — Do's and Don'ts**: 9 Do's and 10 Don'ts, each with specific values. "Don't use bold (700+) weight on Anthropic Serif — weight 500 is the ceiling for serifs." These are enforcement guardrails that prevent AI regression to generic defaults (gradients, drop shadows, cool grays, bold serif headings).

**Section 8 — Responsive Behavior**: 5 breakpoints (<479px through 992px+) as a table with key changes per breakpoint. Collapse strategy for each component type (navigation, feature sections, hero text, model cards). Touch target minimum (44x44px).

**Section 9 — Agent Prompt Guide**: The section unique to DESIGN.md. Contains: (1) a Quick Color Reference table with 8 most-used colors by role name + hex, (2) 5 complete ready-to-paste component prompts with all values baked in, and (3) a 7-rule iteration guide teaching the AI how to use the file effectively. Rule 2: "Reference specific color names — 'use Olive Gray (#5e5d59)' not 'make it gray'." This section converts the design system into an operational playbook.

### The Broader Pattern: Markdown as AI Configuration

Design.md is not an isolated innovation — it's part of an emerging pattern where project-root markdown files serve as persistent AI context. The timeline:

1. **CLAUDE.md** — First mover. Project instructions, coding conventions, test commands. Read at session start by Claude Code.
2. **DESIGN.md** — Visual design system. Colors, typography, components. Read by design-aware agents (Stitch, Cursor).
3. **AGENTS.md** — Build instructions. How to construct the project, deployment patterns, architecture decisions.

Each file addresses a different dimension of AI agent context. The key insight is that these are NOT documentation for humans — they're configuration files for AI agents that happen to be human-readable. The markdown format serves both audiences.

### Implications for Knowledge Systems

For this wiki project, Design.md validates a hypothesis: structured markdown files are the optimal interface between human intent and AI execution. CLAUDE.md already proved this for coding conventions. Design.md proves it for visual design. The wiki itself is proving it for knowledge management.

The pattern suggests that any domain where an AI agent needs persistent, structured context will converge on a project-root markdown file. Future candidates: TESTING.md (test strategy), SECURITY.md (security constraints), DEPLOY.md (deployment rules).

### Integration with Skills Architecture

Design.md files are static context (loaded at session start). Skills are dynamic context (loaded when relevant). The optimal architecture uses both: Design.md provides the persistent visual constraints, while a "design review" skill provides the workflow for when and how to apply them. This mirrors the CLAUDE.md + Skills relationship already documented in the wiki.

## Open Questions

- Should this wiki adopt a DESIGN.md for its own Obsidian vault appearance (graph colors, note styling)? (Requires: decision by the curator; technically feasible but not yet prioritized in the wiki's IaC layer)
- How does Design.md interact with component libraries like Tailwind or Shadcn that already encode design decisions? (Requires: external research on Design.md + Tailwind integration patterns; not covered in existing wiki pages)

## Answered Open Questions

### Will AGENTS.md become a standard alongside CLAUDE.md for Claude Code projects?

Cross-referencing `Infrastructure as Code Patterns`: the IaC patterns page documents that AGENTS.md is already part of the established companion file ecosystem: "DESIGN.md (how it should look) complements CLAUDE.md (how the agent should behave) and AGENTS.md (how to build). Together they give an AI agent complete project context without stuffing everything into a single file." The `Infrastructure as Code Patterns` page lists AGENTS.md explicitly in its IaC spectrum table alongside SOUL.md and HEARTBEAT.md (OpenFleet agent configuration files), confirming it is already in active use within the ecosystem. The IaC patterns page also documents that markdown-as-configuration has become the dominant format precisely because it is "simultaneously human-readable and machine-parsable." AGENTS.md is unlikely to remain niche — the same forces that drove CLAUDE.md adoption (clarity, portability, tool-agnostic consumption) apply equally to it.

### What's the token cost of loading a full Design.md into context? Does it suffer the same context pollution as MCP schemas?

Cross-referencing `Context-Aware Tool Loading` and `CLI Tools Beat MCP for Token Efficiency`: Design.md is a static context file (always loaded at session start), which means it behaves like an MCP schema rather than a deferred-loaded skill. The `Context-Aware Tool Loading` pattern states: "eager loading: load at startup, always available, always consuming context." A full Design.md with 9 sections (visual theme, palette, typography, components, layout, depth, dos/don'ts, responsive, agent prompt guide) plus hex values, font specifications, and component examples could easily reach 1,000-3,000 tokens. The `CLI Tools Beat MCP for Token Efficiency` lesson documents that Claude Code accuracy drops significantly at 40% context usage — a large Design.md consumes budget before the first task token. The mitigation from existing wiki knowledge: treat Design.md like CLAUDE.md — keep it concise (under ~200 lines), reference detailed component specifications in a separate file loaded on demand via a "design review" skill, and reserve the full design file for sessions where UI generation is the primary task. For non-UI sessions, Design.md should not be in the active context.

### Can Design.md be used with local models (e.g., via AICP routing) or is it too context-heavy for smaller models?

Cross-referencing `Infrastructure as Code Patterns` and `Agent Orchestration Patterns`: the `Infrastructure as Code Patterns` page documents that CLAUDE.md's constraint is that "every token in CLAUDE.md costs context budget... This creates an implicit pressure to keep it concise — verbosity has a real cost." The same constraint applies to Design.md with local models, but more severely: the `Agent Orchestration Patterns` page documents OpenFleet's model tiering — "indexing uses Claude (quality), querying uses LocalAI hermes-3b (cheap)" — suggesting smaller local models are used for tasks with bounded context requirements, not tasks that require loading large design system specifications. A 2,000-token Design.md may represent 5-10% of a smaller local model's effective context window (typically 4K-8K tokens for hermes-3b class models), significantly degrading performance on the actual generation task. The practical guidance from existing wiki knowledge: use Design.md with larger models (Claude, GPT-4 class) for design-intensive generation, and provide a compressed design summary (key hex values, font choices only) when routing through AICP to smaller local models.

## Relationships

- EXTENDS: [[Claude Code Best Practices]] (CLAUDE.md is the same pattern for coding)
- RELATES TO: [[Skills Architecture Patterns]] (static vs dynamic AI context)
- RELATES TO: [[Harness Engineering]] (project-root config as agent guardrails)
- RELATES TO: [[Claude Code Context Management]] (context budget considerations)
- ENABLES: [[MCP Integration Architecture]] (Design.md + MCP Stitch server)
- RELATES TO: [[LLM Wiki Pattern]] (markdown as AI-native knowledge format)

## Backlinks

[[[[Claude Code Best Practices]] (CLAUDE.md is the same pattern for coding)]]
[[[[Skills Architecture Patterns]] (static vs dynamic AI context)]]
[[[[Harness Engineering]] (project-root config as agent guardrails)]]
[[[[Claude Code Context Management]] (context budget considerations)]]
[[[[MCP Integration Architecture]] (Design.md + MCP Stitch server)]]
[[[[LLM Wiki Pattern]] (markdown as AI-native knowledge format)]]
[[Hooks Lifecycle Architecture]]
[[Infrastructure as Code Patterns]]
[[Model: Design.md + IaC]]
[[Model: Skills, Commands, and Hooks]]
[[Never Synthesize from Descriptions Alone]]
