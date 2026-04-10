---
title: "Wiki Design Standards — What Good Styling Looks Like"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: seed
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [wiki-design, standards, styling, callouts, examples, gold-standard, anti-patterns, visual-design]
---

# Wiki Design Standards — What Good Styling Looks Like

## Summary

This page defines the quality bar for VISUAL DESIGN in the wiki. Where [[Model: Wiki Design]] defines the system (callout vocabulary, formatting contexts, layout patterns), this page shows what GOOD looks like — and it does so by BEING what good looks like. ==Every technique documented on this page is demonstrated by this page.== That is the contract. If a technique doesn't appear here in its natural form, it hasn't earned its place in the standard.

## Key Insights

- **Styling is not decoration — it is information architecture.** A styled page is scannable in 10 seconds. A raw page demands reading every word. The reader's time is the resource being optimized.

- **Every callout carries semantic meaning.** Blue (`[!info]`) = context. Green (`[!success]`) = verified. Orange (`[!warning]`) = danger. Purple (`[!example]-`) = proof. Red (`[!bug]-`) = failure. Using the wrong color misleads faster than using no color.

- **Foldability is the key to scale.** A page with 9 model entries or 7 bug reports is usable ONLY if those entries collapse. Foldable callouts (`-` suffix) let a page be both scannable AND deep — the table of contents lives in the callout titles.

- **The before/after test is definitive.** If you can't see the difference between the raw and styled version of a section, the styling adds no value. If the styled version is harder to scan than the raw, the styling is wrong.

## Deep Analysis

### The Transformation — Why Styling Exists

Here is the same content in three forms. This is a real entry from [[Model: Methodology]]'s catalog.

> [!example]- **Version 1: Raw markdown** (click to see the problem)
> ```markdown
> #### Feature Development
> **Stages:** document → design → scaffold → implement → test
> The full 5-stage model for complex work. Used when the solution
> isn't already known and needs to be designed, built, and verified.
>
> | Stage | What you produce | Gate |
> |-------|-----------------|------|
> | document | Wiki page + gap analysis | Page exists |
> | design | Spec or design decision | Spec reviewed |
> | scaffold | Types, schemas, empty tests | No business logic |
> | implement | Working code wired to runtime | Lint passes |
> | test | All tests pass | 0 failures |
>
> **Selected when:** task_type = epic, module, or refactor.
>
> **Real instance: Building the wiki backlog system**
> 1. Document — Read OpenArms methodology, map the gap
> 2. Design — Brainstorm with user, spec written
> 3. Scaffold — Schema changes, directory structure
> 4. Implement — Python validation, commands, MCP tools
> 5. Test — pipeline post clean, 0 errors
> ```
>
> Everything has the same visual weight. No hierarchy. No scannability. The reader must read every paragraph to find what they need. Bold labels help but don't create STRUCTURE.

Now the same content, styled with the callout vocabulary:

> [!info] **Feature Development:** document → design → scaffold → implement → test
> The full 5-stage model for complex work. Used when the solution isn't already known and needs to be designed, scaffolded, built, and verified.

| Stage | What you produce | Gate |
|-------|-----------------|------|
| document | Wiki page + gap analysis | Page exists |
| design | Spec or design decision | Spec reviewed |
| scaffold | Types, schemas, empty tests | No business logic |
| implement | Working code wired to runtime | Lint passes |
| test | All tests pass | 0 failures |

> [!abstract] **Selected when**
> task_type = `epic`, `module`, or `refactor`. Any complex work where the solution isn't already known.

> [!example]- **Real instance: Building the wiki backlog system**
> 1. **Document** — Read OpenArms methodology model, understand what we need, map the gap between our wiki and OpenArms' backlog structure
> 2. **Design** — Brainstorm with user (5 design sections, each approved), spec written to `docs/superpowers/specs/`
> 3. **Scaffold** — Schema changes (4 new types, 7 new statuses, 5 new enums), directory structure (`wiki/backlog/`, `wiki/log/`, `wiki/config/`)
> 4. **Implement** — Python validation, pipeline `backlog` command, `/backlog` + `/log` slash commands, `wiki_backlog` + `wiki_log` MCP tools
> 5. **Test** — `pipeline chain health` clean, `pipeline backlog` shows 2 epics + 1 task, 0 validation errors

> [!tip] **What changed**
> The blue `[!info]` header catches your eye first — you know WHAT this model is in 2 seconds. The table gives structured data. The teal `[!abstract]` gives selection context. The purple `[!example]-` hides proof behind a fold — expand only when you need it. Four semantic layers, each doing one job. The raw version has the same information but zero layers — everything looks the same.

---

### Technique 1: Choosing the Right Callout

The 8 callout types are not interchangeable. Each has a semantic purpose, a color, and a reader expectation. Using the wrong type is worse than using no callout — it misleads.

> [!info] **`[!info]` — Context and definitions** — Blue
> Use for introducing concepts, providing reference data, or stating facts the reader needs before understanding what follows. "Here is information to absorb."
>
> This callout itself IS the example. It introduces the info type, provides its definition, and gives context. The blue color signals "neutral information" — no action required, just understanding.
>
> **Used in**: [[Model: Wiki Design]] emphasis hierarchy reference card, [[Model: Methodology]] model headers.

> [!abstract] **`[!abstract]` — Conditions and summaries** — Teal
> Use for distilled essence — selection conditions, preconditions, executive summaries, TL;DRs. "Here is when this applies."
>
> **Used in**: [[Model: Methodology]] — every model catalog entry has `[!abstract] Selected when` stating its trigger conditions.

> [!tip] **`[!tip]` — Guidance and best practices** — Cyan
> Use for actionable advice — what to DO with the information. Design insights, recommendations, heuristics. "Here is something useful to apply."
>
> **Used in**: [[Model: Methodology]] — "Why it stops at design" tips explain non-obvious design choices after model entries.

> [!warning] **`[!warning]` — Cautions and anti-patterns** — Orange
> Use for things that can go WRONG. Misuse patterns, common mistakes, dangerous assumptions. "Be careful here."
>
> **Used in**: [[Model: Wiki Design]] — structural anti-patterns, callout anti-patterns, emphasis soup warning.

> [!example]- **`[!example]-` — Real instances and demonstrations** — Purple (always foldable)
> Use for concrete instances from the ecosystem. ==Always foldable== (`-` suffix) — collapsed for scanning, expandable for proof. "Here is evidence."
>
> **Why always foldable**: Examples are PROOF, not primary content. A page with 9 models and 9 expanded examples is 9x too long to scan. Folded, the 9 model headers are a scannable catalog. The reader expands only the one they need.
>
> **Used in**: Every model catalog entry in [[Model: Methodology]], every worked example in model selection.

> [!success] **`[!success]` — Verified outcomes and confirmed facts** — Green
> Use for things that are PROVEN — selection outcomes, test results, validated decisions. "This is verified."
>
> **Used in**: [[Model: Methodology]] model selection — `[!success] Result → Research model` confirms which model was selected after condition evaluation.

> [!bug]- **`[!bug]-` — Failures and incidents** — Red (always foldable)
> Use for real failures from operation. What happened, how it was found, what the fix was. Always foldable — failures are reference material, not primary reading.
>
> **Used in**: [[Model: Methodology]] "What Goes Wrong" — 7 bugs, each a `[!bug]-` with title showing the design input and version bump. Scannable as a list, expandable per bug.

> [!question] **`[!question]` — Open items and unresolved questions** — Yellow
> Use for genuinely unresolved questions that need research or testing. "This is not yet answered."
>
> **Used in**: Open Questions sections across all pages. Also appropriate for knowledge gaps in domain overviews.

---

### Technique 2: Progressive Disclosure with Foldable Callouts

The `-` suffix is the single most important styling feature. It turns a 500-line page into a 50-line scannable page — with all 500 lines still one click away.

> [!info] **The principle**
> Primary content stays visible. Supporting evidence, detailed examples, and reference data fold behind expandable titles. The page becomes a TABLE OF CONTENTS where every entry can expand into full detail.

**How the Methodology page uses this:**

The Model Catalog has 9 models. Each model's real instance is collapsed:

```
> [!info] Feature Development: document → design → scaffold → implement → test
> ...description...
  table...
> [!abstract] Selected when: task_type = epic, module, or refactor
> [!example]- Real instance: Building the wiki backlog system    ← COLLAPSED
```

Nine of these in sequence. The reader scans all 9 info headers in 15 seconds. They expand only the one they need. Without foldability, those 9 instances would add ~200 lines of inline content, burying the model headers in a wall of text.

**The 7 bugs section uses the same principle:**

```
> [!bug]- Bug 1: Binary status → stage-level tracking (v2)      ← COLLAPSED
> [!bug]- Bug 2: Epic status manual → computed hierarchy (v3)    ← COLLAPSED
> [!bug]- Bug 3: Rogue task creation → operator-only (v3)       ← COLLAPSED
> [!bug]- Bug 4: Lost files → commit immediately (v3)           ← COLLAPSED
> [!bug]- Bug 5: Stage boundary violation → ALLOWED/FORBIDDEN    ← COLLAPSED
> [!bug]- Bug 6: Orphaned implementation → integration req (v5) ← COLLAPSED
> [!bug]- Bug 7: Unreadable logs → observability tooling (v5)   ← COLLAPSED
```

Seven bug titles visible at a glance. Each title tells you the bug name AND the design input. Expand any one for the full story. This is what makes 7 detailed failure reports fit on a page without overwhelming it.

> [!warning] **When NOT to fold**
> - Primary content that the reader MUST see — never fold the main insight or the decision statement
> - Short content (1-3 lines) — the fold action costs more than just reading it inline
> - The only example on a page — if there's just one, show it. Foldability solves the MANY problem, not the ONE problem.

---

### Technique 3: Tables Inside Callouts — Reference Cards

A bare table floating in prose looks like data. A table inside `[!info]` looks like a REFERENCE CARD — something you come back to repeatedly.

> [!info] **Emphasis hierarchy for this wiki**
> | Level | Syntax | Semantic meaning | Use for |
> |-------|--------|-----------------|---------|
> | 1 (highest) | `==highlight==` | ==Critical attention== | Must-not-miss rules. RARE. |
> | 2 | `> [!type]` | Callout title | Section-level categorization |
> | 3 | `**bold**` | **Importance** | Key terms, field names |
> | 4 | `*italic*` | *Emphasis* | Stress, nuance, first use |
> | 5 | `` `code` `` | `Technical reference` | Files, commands, field values |
> | 6 (lowest) | plain text | Normal prose | Everything else |

That table above is from [[Model: Wiki Design]]. Without the `[!info]` wrapper, it would be indistinguishable from a one-time comparison. Inside the blue callout, it reads as "this is reference material you should internalize." The callout provides semantic framing — it tells the reader HOW to read the table.

> [!example]- **The markdown that produces a reference card**
> ```markdown
> > [!info] **Emphasis hierarchy for this wiki**
> > | Level | Syntax | Semantic meaning | Use for |
> > |-------|--------|-----------------|---------|
> > | 1 (highest) | `==highlight==` | ==Critical attention== | RARE. |
> > | 2 | `> [!type]` | Callout title | Section-level categorization |
> > ...remaining rows...
> ```
> Every `>` prefix keeps the table inside the callout boundary. The bold title becomes the reference card's label.

---

### Technique 4: Nested Callouts — Results Inside Context

Nesting creates a conversation between callout types. The outer callout provides context; the inner callout provides the punchline.

**From the Methodology model selection section:**

> [!example]- **Worked example: "Build the backlog system for this wiki"**
> | Dimension | Value | Why |
> |-----------|-------|-----|
> | task_type | `epic` | Large initiative |
> | phase | Infrastructure | Wiki has its foundation, adding infra |
> | domain | tools-and-platforms | Python tooling |
> | scale | new subsystem | Schema, directories, pipeline, commands, MCP |
> | urgency | normal | Not a hotfix |
>
> > [!success] **Result → Feature Development model** (all 5 stages)
> > Document → Design (brainstorm → spec) → Scaffold (schema changes, directory structure) → Implement (Python code, commands, MCP tools) → Test (pipeline health check). Each stage with its own commit, artifacts, and gate.

The `[!example]-` provides context (the condition evaluation table). The nested `[!success]` provides the verified result. Collapsed, the reader sees "Worked example: Build the backlog system" — they know WHAT the example demonstrates without expanding. Expanded, they see the full evaluation AND the confirmed selection. Two semantic layers, one coherent unit.

> [!warning] **Nesting limit: 2 levels maximum**
> Each nesting level steals indentation. By level 3, the content area shrinks to ~30 characters per line. Sentences wrap every few words, and the eye loses track of which level it's reading. If you need a third level, restructure — pull the innermost content out as a separate section.

---

### Technique 5: Emphasis Hierarchy in Practice

All 6 emphasis levels working together in one passage. This is from the description of the Feature Development model:

> The **Feature Development** model uses 5 stages: `document` → `design` → `scaffold` → `implement` → `test`. It is selected when *the solution isn't already known* and the task_type is `epic`, `module`, or `refactor`. ==Stage boundaries are enforced, not suggested== — the `scaffold` stage FORBIDS business logic (see [[Model: Methodology]], Bug 5). The model traces to OpenArms' first autonomous agent run, where 7 bugs in one day hardened every stage boundary.

**What each level does in that passage:**
- **Bold** marks key terms: **Feature Development** — the name you need to recognize
- `Code` marks technical values: `document`, `scaffold`, `epic` — things you'd type in a config file
- *Italic* adds stress: *the solution isn't already known* — emphasis within prose, not a key term
- ==Highlight== marks the critical rule: ==Stage boundaries are enforced, not suggested== — the must-not-miss takeaway
- [[Wikilinks]] connect: [[Model: Methodology]] — follow for depth
- Plain text carries the narrative between emphasis points

> [!bug]- **Anti-pattern: emphasis soup**
> "**The** *methodology* `model` **is** a **framework** for *defining* **work** *processes* and **applying** them **consistently**."
>
> When everything is emphasized, nothing is. The reader can't tell what matters. Bold should appear on ~5-10% of terms — the KEY terms. Code marks TECHNICAL values. Italic adds STRESS. Highlight marks CRITICAL RULES. Each format has its own lane. Cross the lanes and you create noise, not hierarchy.

---

### Page Layout Showcases

Complete layout patterns from real pages in this wiki. Each demonstrates how a different page type achieves visual structure.

> [!example]- **Model catalog entry** — from [[Model: Methodology]]
> The standard for presenting a named methodology model:
>
> 1. `> [!info]` — **Blue header** with stage overview + purpose. Reader sees "Feature Development: document → design → scaffold → implement → test" and knows WHAT this is in 2 seconds.
> 2. **Markdown table** — stages x artifacts x gates. Structured data scannable row by row. NOT inside a callout — tables are already structured.
> 3. `> [!abstract]` — **Teal conditions**. "Selected when: task_type = epic, module, or refactor." Reader knows WHEN this applies.
> 4. `> [!example]-` — **Purple foldable instance**. Real ecosystem example with numbered steps. COLLAPSED by default — the page stays scannable.
> 5. `> [!tip]` or `> [!warning]` — **Contextual guidance**. Optional — only when there's a non-obvious design insight.
>
> 9 models follow this exact pattern. The reader scans all 9 by reading info headers. Dive deep by expanding any example.

> [!example]- **Lesson page** — from [[CLI Tools Beat MCP for Token Efficiency]]
> The gold-standard lesson (122 lines, 9 relationships):
>
> 1. **Summary** — the lesson in ONE actionable sentence. "CLI tools paired with skill files consistently outperform MCP server integrations on token cost and output accuracy."
> 2. **Context** — 5 specific trigger conditions, not "useful in many situations." WHICH situations.
> 3. **Insight** — the MECHANISM. WHY CLI beats MCP, not just THAT it does. "Schema tokens from unused tools occupy space that could hold task context — this is context pollution."
> 4. **Evidence** — 8 discrete items. Each: **bold source label** + specific claim with data + `(source-id)` parenthetical. E.g., "12x cost differential" from the Playwright comparison.
> 5. **Applicability** — 4 domains where it applies + "When MCP is still the right choice" with 4 counterexamples. Honest about boundaries.
> 6. **Relationships** — includes CONTRADICTS (brave — most pages only use soft verbs).
>
> **The bar**: Evidence section needs ≥3 independent sources. If only one source, it's an observation, not a lesson. Insight explains the MECHANISM (why), not just the observation (what).

> [!example]- **Decision page** — from [[Decision: MCP vs CLI for Tool Integration]]
> The gold-standard decision (121 lines, 9 relationships):
>
> 1. **Decision** — ONE clear statement. "Default to CLI+Skills for project-internal tooling. Use MCP for external service bridges."
> 2. **Alternatives** — 3 rejected options, each with specific rejection reasoning. "MCP-First rejected because: loads all schemas at startup regardless of use."
> 3. **Rationale** — evidence-backed. 12x cost differential, Microsoft's own recommendation, Google Trends convergence, harness engineering principle.
> 4. **Reversibility** — `reversibility: easy` with honest explanation: "swap a config." Cost of being wrong is transparent.
> 5. **Dependencies** — 6 downstream effects if reversed. CLAUDE.md, MCP server scope, skill design, agent teams, Context7, future 1M context window.
>
> **The bar**: ≥2 alternatives with concrete rejection reasons. Rationale references specific evidence, not general reasoning. Reversibility is honest.

> [!example]- **Pattern page** — from [[Scaffold → Foundation → Infrastructure → Features]]
> The gold-standard pattern (176 lines, 13 relationships):
>
> 1. **Summary** — names the 4 stages with exit criteria in one paragraph.
> 2. **Pattern Description** — each stage as a subsection: what it is, exit criterion, key artifacts, anti-patterns. TESTABLE criteria: "scaffold is done when direction is set."
> 3. **Instances** — 4 concrete occurrences (Research Wiki, OpenFleet, AICP, Front-Middleware-Backend). Each expanded into a multi-paragraph deep dive showing stage-by-stage progression.
> 4. **When To Apply** — 5 specific scenarios with reasoning.
> 5. **When Not To** — 3 honest exceptions: POCs, hotfixes, exploratory scripts. The When Not To is as thoughtful as When To Apply.
>
> **The bar**: ≥2 concrete instances with page references. A pattern without instances is a hypothesis. The When Not To section must exist and be honest.

---

### Anti-Pattern Gallery

Each anti-pattern shown as it appears in the wild, then fixed.

> [!bug]- **Bold everything**
> "**The** *methodology* `model` **is** a **framework** for *defining* **work** *processes* and **applying** them **consistently**."
>
> When every other word is bold, nothing stands out. The eye scans for bold to find key terms — if everything is bold, that scanning mechanism is destroyed.
>
> **Fix:** Bold only key terms — ~5-10% of text. "The **methodology model** is a framework for defining work processes and applying them consistently."

> [!bug]- **Wrong callout type**
> Using `> [!info]` for a bug report. Using `> [!bug]` for general guidance. Using `> [!success]` for unverified claims.
>
> Colors carry meaning. Blue = neutral context. Red = failure. Green = verified. When a reader sees green, they trust the content is confirmed. A green callout around an unverified claim is a lie in color.
>
> **Fix:** Match type to purpose per the callout vocabulary in [[Model: Wiki Design]].

> [!bug]- **Non-foldable long examples**
> A 30-line real instance expanded inline, blocking the page flow. The reader scrolls past it to reach the next section. Context is lost, flow is broken.
>
> **Fix:** Always use `[!example]-` (foldable) for examples longer than 5 lines. The `-` costs nothing to write and saves the reader's attention.

> [!bug]- **Callout for everything**
> ```markdown
> > [!info] Introduction
> > This page covers styling.
>
> > [!info] Background
> > Styling matters because...
>
> > [!info] Details
> > The details are...
> ```
>
> When every paragraph lives in a callout, callouts lose meaning. They become wallpaper — the blue boxes blur together into visual noise.
>
> **Fix:** Callouts for semantic CATEGORIES (context, conditions, examples, warnings). Prose for narrative flow. The contrast between callout and prose IS the visual hierarchy.

> [!bug]- **Nested 3+ deep**
> ```markdown
> > [!example]- Outer
> > > [!info] Middle
> > > > [!tip] Inner — line width is now ~30 characters
> ```
>
> Each nesting level steals indentation. By level 3, content area is so narrow that every sentence wraps after a few words. The reader loses track of which level they're reading.
>
> **Fix:** Maximum 2 nesting levels. Need a third? Pull it out as a sibling section.

> [!bug]- **Bare table as catalog**
> ```markdown
> | Model | Stages | When |
> |-------|--------|------|
> | Feature Dev | doc→design→scaffold→impl→test | Epics |
> | Research | doc→design | Spikes |
> | ...7 more rows... |
> ```
>
> Tables work for comparison. They fail as a CATALOG where each entry needs description, artifacts, real instances, and depth. Table cells force everything flat, killing hierarchy and foldability.
>
> **Fix:** The model catalog entry pattern: `[!info]` header + table + `[!abstract]` conditions + `[!example]-` instance. Each entry gets its own visual structure with four semantic layers.

> [!bug]- **Heading skip**
> ```markdown
> # Title
> ### Subsection (skipped H2)
> ```
>
> Breaks the Obsidian outline panel — shows an indentation gap. Violates HTML heading hierarchy. Confuses both the reader and the navigation.
>
> **Fix:** Always use sequential heading levels: H1 → H2 → H3. Never skip.

> [!bug]- **Meaning lives only in styling**
> - A `> [!success]` callout with body "Yes." — strip the callout, the reader sees `> Yes` with no context.
> - A foldable with no title summary — collapsed, the reader sees `> [!example]-` and nothing about WHAT it demonstrates.
> - Critical information only in `==highlight==` — in plain text, it's surrounded by `==` which may confuse.
>
> **Fix:** The TEXT must carry the meaning. Callouts ADD structure. Test: strip all callouts from the page. Can you still understand it? If not, the styling is carrying too much load.

---

### The Styling Checklist

> [!tip] **Run this before marking any page as styled**
> - [ ] Every callout type matches its semantic purpose (info=context, warning=caution, example=proof, bug=failure, etc.)
> - [ ] All examples longer than 5 lines are foldable (`[!example]-` or `[!bug]-`)
> - [ ] No more than 2 nesting levels anywhere on the page
> - [ ] Bold used for key terms only (~5-10% of text), not emphasis-of-everything
> - [ ] Tables inside `[!info]` when they're reference data; bare tables for one-time comparisons
> - [ ] Heading levels are sequential — no skips (H1 → H2 → H3)
> - [ ] Page is scannable in 10 seconds by reading callout titles and headings alone
> - [ ] Page degrades gracefully — strip callouts mentally, content still makes sense
> - [ ] `==Highlight==` used at most 1-2 times on the entire page (rare, critical rules only)
> - [ ] Prose sections exist between callout groups — callouts don't touch callouts without breathing room

---

### The Self-Referential Test

This page uses all 8 callout types in their natural semantic contexts:

| Callout | How it's used on this page |
|---------|---------------------------|
| `[!info]` | Emphasis hierarchy reference card, the disclosure principle, callout type definitions |
| `[!abstract]` | Selection conditions in the model catalog showcase |
| `[!tip]` | The styling checklist, design insights after the transformation |
| `[!warning]` | When NOT to fold, nesting limits |
| `[!example]-` | Raw markdown source, page layout showcases, the transformation before/after |
| `[!success]` | Model selection result nested inside a worked example |
| `[!bug]-` | Every anti-pattern in the gallery |
| `[!question]` | Open questions below |

If any type were missing, the page would fail its own standard. ==This page demonstrates everything it teaches.==

## Open Questions

> [!question] **Should there be a formal "styling review" gate?**
> Before pages are marked `growing`, should styling be checked against this standard? Currently quality reviews focus on content (evidence, specificity, relationships). Adding a visual quality dimension would catch raw pages earlier but adds process overhead. (Requires: testing with a review workflow on 5+ pages)

> [!question] **When do we create CSS snippets?**
> Custom CSS could define new callout types — `[!model]`, `[!stage]` — with unique colors and Lucide icons. But the 8 built-in types need to stabilize across 20+ styled pages first. Premature CSS is premature optimization. (Requires: callout vocabulary stability across 20+ styled pages)

> [!question] **Should before/after examples include Obsidian screenshots?**
> Markdown source shows what you TYPE. Screenshots show what you SEE. Both are valuable, but screenshot tooling in WSL to Windows adds workflow friction. (Requires: screenshot pipeline or accepting the manual overhead)

## Relationships

- BUILDS ON: [[Model: Wiki Design]]
- BUILDS ON: [[LLM Wiki Standards — What Good Looks Like]]
- RELATES TO: [[Model: Methodology]] (first page to demonstrate all callout patterns)
- RELATES TO: [[The Agent Must Practice What It Documents]]
- RELATES TO: [[CLI Tools Beat MCP for Token Efficiency]] (lesson layout reference)
- RELATES TO: [[Decision: MCP vs CLI for Tool Integration]] (decision layout reference)
- RELATES TO: [[Scaffold → Foundation → Infrastructure → Features]] (pattern layout reference)

## Backlinks

[[Model: Wiki Design]]
[[LLM Wiki Standards — What Good Looks Like]]
[[Model: Methodology]]
[[The Agent Must Practice What It Documents]]
[[CLI Tools Beat MCP for Token Efficiency]]
[[Decision: MCP vs CLI for Tool Integration]]
[[Scaffold → Foundation → Infrastructure → Features]]
[[Methodology Standards — What Good Execution Looks Like]]
