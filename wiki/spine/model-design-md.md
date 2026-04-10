---
title: "Model: Design.md and IaC"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-10
sources:
  - id: src-awesome-design-md
    type: documentation
    url: "https://github.com/VoltAgent/awesome-design-md"
    file: raw/articles/voltagentawesome-design-md.md
    title: "VoltAgent/awesome-design-md — 58 Design Systems"
tags: [model, spine, design-md, iac, markdown-config, claude-md, agents-md, soul-md, ai-configuration, infrastructure-as-code]
---

# Model: Design.md and IaC

## Summary

The Design.md and IaC model describes the convergence of Infrastructure as Code with AI agent configuration: markdown files at the project root serve as binding specifications that AI agents read and execute. ==This pattern generalizes from traditional IaC (Terraform, Ansible) into the AI domain== — producing a companion file ecosystem: CLAUDE.md (behavioral constraints), DESIGN.md (visual design system), AGENTS.md (architecture), and SOUL.md (agent identity). The 9-section DESIGN.md standard, documented in 58+ production implementations including Claude (Anthropic)'s 312-line specification, is the most complete instance.

## Key Insights

- **Markdown files at the project root are now IaC.** CLAUDE.md is configuration, not documentation. DESIGN.md is a constraint set, not a style guide. The executor is an LLM instead of Terraform, but the principle is identical: human writes spec, machine reads it as binding.

- **The companion file ecosystem is four files.** CLAUDE.md (behavior), DESIGN.md (visual), AGENTS.md (architecture), SOUL.md (identity). Together they give any AI agent complete project context across four dimensions.

- **Semantic color naming is an AI vocabulary decision.** Colors get NAME + HEX + ROLE + RATIONALE. "Use Parchment" survives refactors that "use #f5f4ed" does not. The name becomes the agent's working vocabulary.

- **Do's and Don'ts is the guardrail layer.** Without explicit prohibitions, AI agents revert to training-data averages. 10 concrete Don'ts counteract specific AI tendencies toward generic UI.

- **58+ production implementations exist now.** VoltAgent/awesome-design-md covers Claude, Stripe, Vercel, Linear, Figma, Spotify, Tesla. Immediately usable as templates.

## Deep Analysis

### The 9-Section DESIGN.md Standard

> [!info] **Based on Claude (Anthropic)'s 312-line implementation**
> | Section | What it defines | Why it matters |
> |---------|----------------|----------------|
> | **1. Visual Theme** | Atmospheric prose + 4-6 adjectives | Gives the AI a holistic "feel" as a prior |
> | **2. Color Palette** | NAME → HEX → ROLE → WHY | Semantic names survive refactors |
> | **3. Typography** | 16-role hierarchy table | Lookup structure, not inference |
> | **4. Component Styles** | Named button variants with exact CSS | Zero ambiguity in generation |
> | **5. Layout Principles** | 8px base, grid, whitespace, border-radius scale | Structural rules governing component relationships |
> | **6. Depth & Elevation** | 5-level shadow system | Which interactions warrant visual weight |
> | **7. Do's and Don'ts** | 10 concrete rules each | Guardrails against training-data defaults |
> | **8. Responsive Behavior** | 5 breakpoints with collapse strategy | Cannot be inferred from color palette |
> | **9. Agent Prompt Guide** | Ready-to-paste component prompts + usage rules | Built-in manual for AI consumption |

> [!tip] **Section 9 is unique to DESIGN.md**
> No other design spec format (Figma tokens, Storybook, design tokens JSON) includes a built-in usage manual for AI. Claude's DESIGN.md has 5 complete component prompts baked in — the file teaches the AI how to use itself.

See [[Design.md Pattern]] for full depth and the 312-line Claude example.

---

### The Do's and Don'ts as Constraint Engineering

> [!warning] **Without explicit prohibitions, AI agents generate generic UI**
> Training-data averages look like: subtle gradients, bold serifs, cool grays, drop shadows everywhere, blue for all interactive elements. Not wrong — generic. The statistical consensus from millions of web pages, not your design language.

The Do's reinforce explicit choices. The Don'ts prohibit the defaults that fill gaps. Each Don't is a documented failure mode — a specific visual decision the AI WILL make if unconstrained.

> [!example]- **Claude's Don'ts (from the 312-line DESIGN.md)**
> - No gradients in backgrounds
> - No mixing Anthropic Serif with system fonts in the same element
> - No literal hex values in prompts (use semantic names)
> - No ring shadows where drop shadows were specified
> - No cool grays where warm grays are defined
>
> Each prohibits a specific AI tendency. The Don'ts section is not pessimistic — it is precise.

> [!tip] **How to author Don'ts for a new project**
> Generate UI with a blank context (no DESIGN.md). Audit the output against your design language. The 10 differences are your Don'ts. This identifies the exact AI defaults your design system contradicts.

---

### The Broader IaC Spectrum

> [!info] **Companion files sit on a continuous spectrum with traditional IaC**
> | Spec file | Executor | Domain |
> |-----------|----------|--------|
> | `main.tf` | Terraform | Cloud infrastructure |
> | `docker-compose.yml` | Docker | Container orchestration |
> | `CLAUDE.md` | Claude Code | AI agent behavior |
> | `DESIGN.md` | Claude / Cursor / Stitch | Visual design system |
> | `AGENTS.md` | Claude Code | Architecture conventions |
> | `SOUL.md` | OpenFleet | Agent identity |
> | `config/schema.yaml` | tools/validate.py | Wiki page schema |
> | `.env.example` | setup.py | Environment configuration |
> | `services/*.conf` | systemd | Daemon configuration |
>
> The common pattern: human writes spec at a standard location; executor reads it as binding constraints. The executor type doesn't change the pattern.

---

### The Companion File Ecosystem

> [!info] **Four files, four non-overlapping scopes**
> | File | Question it answers | Scope |
> |------|-------------------|-------|
> | **CLAUDE.md** | "How should this agent behave?" | Commands, conventions, quality gates, prohibited actions |
> | **DESIGN.md** | "How should this project look?" | Colors, typography, spacing, components, responsive behavior |
> | **AGENTS.md** | "How should this project be built?" | Architecture decisions, module structure, dependency patterns |
> | **SOUL.md** | "Who is this agent?" | Identity, values, expertise, decision-making principles |

Separated by scope deliberately — no single file handles behavior AND visual AND architecture AND identity. Each stays readable and at a size appropriate for always-loaded context.

> [!abstract] **Context budget math**
> CLAUDE.md ~200 lines + DESIGN.md ~300 lines + AGENTS.md ~100 lines + SOUL.md ~150 lines = ~750 lines = ~4,000 tokens = <3% of 190K context. Worthwhile for sessions that need all four.

---

### The Two-Tier Configuration Model

Maps to [[Context-Aware Tool Loading]]:

> [!info] **Tier 1 vs Tier 2**
> | Tier | Loading | Cost | Contents |
> |------|---------|------|----------|
> | **Tier 1 — Static** | Always loaded | Permanent (every message) | CLAUDE.md, DESIGN.md, schema.yaml |
> | **Tier 2 — Dynamic** | On invocation | Zero until needed | Skills, detailed workflows, domain-specific instructions |

> [!warning] **DESIGN.md loaded into every session has a real cost even when not generating UI**
> Correct model: load DESIGN.md only in UI-focused sessions — either as a skill or by accepting the overhead as worthwhile when UI generation is dominant.

---

### Key Pages

| Page | Layer | Role in the model |
|------|-------|-------------------|
| [[Design.md Pattern]] | L2 | The foundational concept — 9-section standard, Claude example, Do's/Don'ts |
| [[Infrastructure as Code Patterns]] | L2 | The IaC spectrum — traditional and AI-agent configuration as one pattern |
| [[Context-Aware Tool Loading]] | L5 | Loading pattern — eager vs deferred, governs Tier 1 vs Tier 2 decision |
| [[Claude Code Best Practices]] | L2 | CLAUDE.md structure guidance — under 200 lines, routing table pattern |
| [[Synthesis: awesome-design-md]] | L1 | Source: 58+ production DESIGN.md implementations |

---

### Lessons Learned

| Lesson | What was learned |
|--------|-----------------|
| [[Infrastructure Must Be Reproducible, Not Manual]] | Companion files ARE IaC. Manual agent configuration that isn't in CLAUDE.md/DESIGN.md is invisible, unrepeatable config. |
| [[The Agent Must Practice What It Documents]] | CLAUDE.md must contain the rules the agent follows, not just rules it documents. Config files are operational, not aspirational. |
| [[Never Synthesize from Descriptions Alone]] | Reading awesome-design-md (a catalog of DESIGN.md files) ≠ reading a DESIGN.md file. We read the actual 312-line Claude example. |

---

### State of Knowledge

> [!success] **Well-covered**
> - 9-section DESIGN.md standard with Claude's 312-line reference
> - Do's and Don'ts as constraint engineering (with authoring methodology)
> - Companion file ecosystem (CLAUDE.md, DESIGN.md, AGENTS.md, SOUL.md)
> - IaC spectrum (traditional → AI agent configuration)
> - 58+ production implementations as evidence base
> - Two-tier configuration model (static vs dynamic context)

> [!warning] **Thin or unverified**
> - AGENTS.md and SOUL.md are newer conventions — less ecosystem evidence than CLAUDE.md/DESIGN.md
> - Interaction behavior spec (animations, state transitions) — not captured in current 9-section structure
> - Context overhead measurement — the "4,000 tokens = 3%" math is estimated, not measured
> - DESIGN.md value as LLMs improve — does constraint engineering remain valuable when models get better at visual design?
> - No DESIGN.md exists in this ecosystem yet — the model is based on external research, not internal practice

---

### How to Adopt

> [!info] **Adding the companion file ecosystem to a project**
> 1. **CLAUDE.md** — start here. Project structure, conventions, commands, quality gates. Under 200 lines.
> 2. **DESIGN.md** — if the project has UI. Copy from awesome-design-md for a known design system, or author from scratch following the 9-section standard.
> 3. **AGENTS.md** — if the project has multi-agent or complex build conventions. Architecture decisions, module structure.
> 4. **SOUL.md** — if the project uses fleet agents. Identity, values, expertise domain.

> [!warning] **INVARIANT — never change these**
> - Config files are at the project root (standard location for all executors)
> - CLAUDE.md under 200 lines (always-loaded = always-costing)
> - Do's and Don'ts section is mandatory in DESIGN.md (without it, the file is preferences, not constraints)
> - Semantic naming for colors and components (literal values break on refactor)
> - Companion files have non-overlapping scopes (behavior ≠ visual ≠ architecture ≠ identity)

> [!tip] **PER-PROJECT — always adapt these**
> - Which companion files exist (not every project needs all four)
> - DESIGN.md section depth (a simple project may skip Responsive Behavior and Depth & Elevation)
> - Whether DESIGN.md is always-loaded or skill-loaded (depends on how often UI is generated)
> - The specific Do's and Don'ts (derived from auditing AI output against YOUR design language)
> - AGENTS.md scope (simple projects may put architecture notes in CLAUDE.md)

## Open Questions

> [!question] **When does the companion file ecosystem tip into context overhead?**
> Four files at ~750 lines total = ~4,000 tokens. At what point does this overhead measurably degrade accuracy? Is there a project-specific threshold? (Requires: measuring accuracy with and without companion files loaded)

> [!question] **Is there a DESIGN.md equivalent for interaction behavior?**
> Animations, state transitions, loading patterns, micro-interactions — the current 9-section structure doesn't capture these. Should it be a 10th section or a separate INTERACTIONS.md? (Requires: surveying how AI agents handle interaction specs)

> [!question] **Does DESIGN.md value decrease as LLMs improve at visual design?**
> If models get better at generating consistent UI without constraints, does DESIGN.md become unnecessary? Or does the "design reasoning capture" (WHY columns) remain durable? (Requires: longitudinal comparison)

## Relationships

- BUILDS ON: [[Design.md Pattern]]
- BUILDS ON: [[Infrastructure as Code Patterns]]
- BUILDS ON: [[Context-Aware Tool Loading]]
- RELATES TO: [[Model: Claude Code]]
- RELATES TO: [[Model: Skills, Commands, and Hooks]]
- RELATES TO: [[Model: SFIF and Architecture]]
- RELATES TO: [[Model: Quality and Failure Prevention]]
- ENABLES: [[Claude Code Best Practices]]

## Backlinks

[[Design.md Pattern]]
[[Infrastructure as Code Patterns]]
[[Context-Aware Tool Loading]]
[[Model: Claude Code]]
[[Model: Skills, Commands, and Hooks]]
[[Model: SFIF and Architecture]]
[[Model: Quality and Failure Prevention]]
[[Claude Code Best Practices]]
