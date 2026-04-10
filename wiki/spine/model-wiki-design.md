---
title: "Model: Wiki Design"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: seed
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: src-obsidian-basic-syntax
    type: documentation
    url: "https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax"
    file: raw/articles/obsidian-basic-formatting-syntax.md
    title: "Obsidian Basic Formatting Syntax"
    ingested: 2026-04-09
  - id: src-obsidian-advanced-syntax
    type: documentation
    url: "https://help.obsidian.md/Editing+and+formatting/Advanced+formatting+syntax"
    file: raw/articles/obsidian-advanced-formatting-syntax.md
    title: "Obsidian Advanced Formatting Syntax"
    ingested: 2026-04-09
  - id: src-obsidian-callouts
    type: documentation
    url: "https://help.obsidian.md/Editing+and+formatting/Callouts"
    file: raw/articles/obsidian-callouts-reference.md
    title: "Obsidian Callouts Reference"
    ingested: 2026-04-09
  - id: src-markdown-basic
    type: documentation
    url: "https://www.markdownguide.org/basic-syntax/"
    title: "Markdown Guide — Basic Syntax"
    ingested: 2026-04-09
  - id: src-markdown-extended
    type: documentation
    url: "https://www.markdownguide.org/extended-syntax/"
    title: "Markdown Guide — Extended Syntax"
    ingested: 2026-04-09
  - id: src-remarkjs
    type: documentation
    url: "https://github.com/remarkjs/remark"
    file: raw/articles/remarkjsremark.md
    title: "remarkjs/remark — Markdown processor with plugins"
    ingested: 2026-04-09
tags: [wiki-design, model, formatting, obsidian, markdown, callouts, styling, remark, visual-design, standards, emerging]
---

# Model: Wiki Design

## Summary

The Wiki Design model defines the VISUAL layer of the knowledge system — how pages look and feel, not just what they contain. It is the third standard layer alongside [[Model: LLM Wiki]] (content structure via schema) and [[LLM Wiki Standards — What Good Looks Like]] (content quality via gold standards). This model covers: a semantic emphasis hierarchy (what bold vs italic vs highlight vs callout MEANS), a callout vocabulary mapping 8 types to semantic purposes, per-page-type layout patterns, and a clear separation between three formatting contexts (universal markdown for baseline, Obsidian extensions for the wiki, remark/Docusaurus for public docs). ==This model is an emerging standard — marked `maturity: seed`.== It evolves as the wiki applies the patterns and discovers what works.

## Key Insights

- **Three formatting contexts coexist, not compete.** Universal markdown (baseline), Obsidian Flavored Markdown (wiki), remark/Docusaurus (public docs). Different outputs, different syntax, same underlying content. They are not evolution stages — they coexist for different purposes.

- **Formatting is SEMANTIC, not decorative.** Every formatting choice carries meaning. Bold = importance. Italic = emphasis. Highlight = critical attention. Callout type = information category. Choosing a format is a MEANING decision, not a visual preference.

- **Callouts are the primary visual structuring tool.** 14 built-in Obsidian callout types with colors, icons, foldability, and nesting. We use 8 with defined semantic purposes. They transform walls of text into scannable, layered information.

- **`cssclasses` enables systematic per-page-type styling.** A frontmatter field that applies CSS classes to the page, enabling consistent visual treatment across all pages of the same type.

- **Graceful degradation is a hard constraint.** Core content must be readable outside Obsidian. Callouts degrade to blockquotes. Wikilinks degrade to plain text. Never put critical content ONLY in a styling feature.

## Deep Analysis

### The Three Standard Layers (where this model fits)

| Layer | What it defines | Where it lives | Example |
|-------|----------------|----------------|---------|
| **Content Structure** | Types, fields, sections, schema | `config/wiki-schema.yaml` + [[Model: LLM Wiki]] | "A lesson requires: Summary, Context, Insight, Evidence, Applicability, Relationships" |
| **Content Quality** | What "good" looks like per type | [[LLM Wiki Standards — What Good Looks Like]] | "A lesson's Evidence section must have ≥3 independent data points" |
| **Visual Design** | How pages look in Obsidian | **This model** | "Use `> [!example]-` for real instances, always foldable" |

Structure says WHAT sections exist. Quality says HOW GOOD the content is. Design says HOW IT LOOKS. They don't overlap — a page can have correct structure (passes validation), good quality (meets the gold standard), but ugly design (walls of raw text). This model fixes the third dimension.

### The Three Formatting Contexts

#### Context 1: Universal Markdown (baseline)

The shared floor. Works in Obsidian, GitHub, VS Code, Docusaurus, any text editor. This wiki assumes the reader knows markdown — the rules below are about HOW we use it, not what it is.

> [!info] **Emphasis hierarchy for this wiki**
> | Level | Syntax | Semantic meaning | Use for |
> |-------|--------|-----------------|---------|
> | 1 (highest) | `==highlight==` | ==Critical attention== | Must-not-miss rules, critical warnings. RARE. |
> | 2 | `> [!type]` title text | Callout title | Section-level categorization (info, tip, warning, etc.) |
> | 3 | `**bold**` | **Importance** | Key terms, field names, critical rules within prose |
> | 4 | `*italic*` | *Emphasis* | Stress, nuance, first use of a term, titles of works |
> | 5 | `` `code` `` | `Technical reference` | File names, commands, field values, syntax |
> | 6 (lowest) | plain text | Normal prose | Everything else |
>
> **Anti-pattern:** using bold for everything. If everything is bold, nothing is important. Reserve bold for terms that would confuse the reader if missed.

> [!tip] **When to use which structural element**
> | Need | Use | Not |
> |------|-----|-----|
> | Compare 2+ things across dimensions | **Table** | Prose paragraphs describing each |
> | List discrete items (order matters) | **Ordered list** | Table with one column |
> | List discrete items (no order) | **Unordered list** | Numbered list |
> | Explain WHY something works | **Prose** | Table or list |
> | Track completion | **Task list** `- [x]` | Ordered list |
> | Separate catalog entries | **Horizontal rule** `---` | Extra blank lines |
> | Show code | **Fenced code block** with language | Inline code for multi-line |
> | Quote an actual person/source | **Blockquote** `>` | Callout (callouts are for categories, not quotes) |

> [!warning] **Structural anti-patterns**
> - Skipping heading levels (H1 → H3) — breaks hierarchy and Obsidian outline
> - Tables with only one column — use a list
> - Ordered lists where order doesn't matter — use unordered
> - Inline code for emphasis — use bold or italic
> - Footnotes for critical information — put it in the body
> - Walls of prose without any structural elements — break it up

#### Context 2: Obsidian Flavored Markdown (for the wiki)

Everything Obsidian adds. These render in Obsidian and Obsidian Publish; they degrade gracefully elsewhere.

> [!info] **Wikilinks — our linking standard**
> | Syntax | Purpose | When |
> |--------|---------|------|
> | `[[Page Title]]` | Link to wiki page | ALL relationship targets, all page references in body text |
> | `[[Page\|Display Text]]` | Aliased link | When the page title is too long for inline use |
> | `[[Page#Heading]]` | Section link | Deep references to specific parts |
> | `[[Page#^block-id]]` | Block link | Referencing one specific paragraph |
> | `![[Page#Heading]]` | Embed section | When the reader NEEDS to see it inline |
>
> **Rule:** NEVER use file paths (`wiki/path/file.md`) in body text. Always `[[Page Title]]`.

> [!info] **Other Obsidian features we use**
> | Feature | Syntax | When |
> |---------|--------|------|
> | ==Highlight== | `==text==` | Critical information that must not be missed. Rarer than bold. |
> | Comments | `%% text %%` | Editorial notes, WIP markers. Invisible in reading view. |
> | Properties | `cssclasses: [type]` | Per-page-type CSS styling via snippets |
> | Tags | `#tag/subtag` | Hierarchical tags for search and organization |
> | Aliases | `aliases: [alt-name]` | Alternative names for search discovery |
> | Block refs | `^block-id` | Making specific paragraphs linkable |

#### Context 3: Remark / Docusaurus (for public docs)

NOT for the wiki. For `docs/` content rendered via Docusaurus or similar static site generators. Different syntax, similar visual results.

| Obsidian (wiki) | Remark/Docusaurus (docs) | Purpose |
|-----------------|------------------------|---------|
| `> [!tip] Title` | `:::tip[Title]` | Admonition/callout |
| `> [!warning]` | `:::danger` | Warning block |
| `[[Page Title]]` | `[text](./path)` | Internal link |
| Fenced code block | Same | Code |
| N/A | `:::tabs` + `::tab[X]` | Tabbed content |
| N/A | `::youtube{#id}` | Component injection |
| N/A | MDX / JSX | React components in markdown |

> [!abstract] **The remark ecosystem**
> remark is a markdown processor with 150+ plugins operating on ASTs. Key plugins: remark-gfm (tables, strikethrough), remark-directive (:::containers, tabs), remark-frontmatter (YAML), remark-toc (auto table of contents), remark-rehype (markdown → HTML), MDX (React components). For projects using Docusaurus, remark extends markdown into a full component system.

### The Callout Vocabulary

8 callout types with defined semantic purposes. This is the STANDARD for this wiki:

> [!info] **`[!info]` — Context, definitions, reference**
> Blue ℹ️. Use when introducing a concept, providing context, or presenting reference data. "Here is information to absorb."

> [!abstract] **`[!abstract]` — Summary, conditions, TL;DR**
> Teal 📋. Use for condensed information — selection conditions, preconditions, executive summaries. "Here is the distilled essence."

> [!tip] **`[!tip]` — Guidance, best practices, insights**
> Cyan 💡. Use for actionable advice — what to DO with the information. "Here is something useful to apply."

> [!warning] **`[!warning]` — Cautions, anti-patterns, risks**
> Orange ⚠️. Use for things that can go WRONG. "Be careful here."

> [!example]- **`[!example]-` — Real instances, demonstrations** (always foldable)
> Purple 📖. Use for concrete instances from the ecosystem. ALWAYS foldable (`-` suffix) — collapsed for scanning, expandable for detail. "Here is proof."

> [!success] **`[!success]` — Verified outcomes, confirmed facts**
> Green ✅. Use for things that are PROVEN — test results, selection outcomes, validated decisions. "This is verified."

> [!bug]- **`[!bug]-` — Failures, incidents, bugs** (always foldable)
> Red 🐛. Use for real failures from operation. Always foldable. "This went wrong."

> [!question] **`[!question]` — Open items, needs research**
> Purple ❓. Use for genuinely unresolved questions. "This is not yet answered."

> [!warning] **Callout anti-patterns**
> - Using `[!info]` for everything — choose the specific type
> - Non-foldable examples that are 20+ lines — always fold examples
> - Callout title without body when the content is important — title-only works for labels, not for content
> - Putting critical content ONLY in a callout title — won't survive degradation to plain text
> - Nesting more than 2 levels — becomes unreadable
> - Using `[!note]` (gray, generic) when a specific type exists
> - Using blockquotes (`>`) for non-quotes — use callouts for semantic boxes, blockquotes for actual quotations

> [!tip] **Callout syntax quick reference**
> ```markdown
> > [!type] Custom Title         ← always visible
> > Body content                 ← visible (or hidden if folded)
>
> > [!type]- Collapsed by default  ← fold with -
> > [!type]+ Expanded by default   ← fold with +
> ```
> Nesting: add `>` levels. Custom types: CSS snippets in `.obsidian/snippets/`.

### Page Layout Patterns

How each page type should be visually structured. These patterns use the callout vocabulary above:

> [!example]- **Model catalog entry** (as used in [[Model: Methodology]])
> 1. `> [!info]` — stage overview + purpose (blue header)
> 2. Markdown table — stages with artifacts and gates (structured data)
> 3. `> [!abstract]` — selection conditions (when this model runs)
> 4. `> [!example]-` — real instance, foldable, with numbered steps
> 5. `> [!tip]` or `> [!warning]` — design insight or caution
>
> Provides: scannable headers → structured data → context → proof → guidance.

> [!example]- **Lesson page**
> 1. H2 Summary — plain prose, the lesson stated clearly
> 2. H2 Context — plain prose, when this applies
> 3. H2 Insight — plain prose, the core learning (depth here)
> 4. H2 Evidence — each evidence item as **bold source label** + specific claim + `(source-id)`
> 5. H2 Applicability — bullet list of domains where this applies + `> [!tip]` for "when NOT to apply"
> 6. H2 Relationships — `[[wikilinks]]` with ALL_CAPS verbs

> [!example]- **Decision page**
> 1. H2 Summary — the recommendation in 2-3 sentences
> 2. H2 Decision — `> [!success]` callout with the clear decision statement
> 3. H2 Alternatives — each alternative as `> [!abstract]-` foldable with why it was rejected
> 4. H2 Rationale — evidence-backed prose with `**bold source labels**`
> 5. H2 Reversibility — `> [!info]` stating how hard to undo
> 6. H2 Dependencies — bullet list of downstream impacts

> [!example]- **Comparison page**
> 1. H2 Summary — what's being compared and why
> 2. H2 Comparison Matrix — markdown TABLE (never prose). Rows = criteria, columns = alternatives.
> 3. H2 Key Insights — bullet points from the comparison
> 4. H2 Deep Analysis — per-alternative or per-criteria deep dives
> 5. `> [!tip]` — decision guidance ("use X when..., use Y when...")

> [!example]- **Bug/failure report** (as used in Methodology bugs section)
> Each bug: `> [!bug]-` foldable. Title = bug name + design input + version.
> Body: what happened → how found → what the fix was.
> Collapsed view = scannable bug list. Expanded = full detail.

> [!example]- **Worked example / selection walkthrough**
> `> [!example]-` foldable with scenario title.
> Inside: condition evaluation table (dimension | value | why).
> `> [!success]` nested = the result.

> [!example]- **Source-synthesis page**
> 1. H2 Summary — what the source IS and the headline finding
> 2. H2 Key Insights — each insight as a **bold label** + prose. Group into subsections for deep sources.
> 3. H2 Open Questions — each with `(Requires: ...)` tag
> 4. H2 Relationships — `[[wikilinks]]`
>
> For deep sources (250+ lines): subsection headings within Key Insights, not just bullets.

> [!example]- **Domain overview page**
> 1. H2 Summary — domain scope
> 2. H2 State of Knowledge — what's known, what's thin
> 3. H2 Gaps — `> [!question]` callouts for major gaps
> 4. H2 Key Pages — table of essential reading
> 5. H2 FAQ — each Q as `### Q: Question?` with 2-3 sentence answer linking to deeper pages

> [!example]- **Backlog task**
> Short and focused. H2 Summary + H2 Done When (task list `- [ ]`).
> Frontmatter carries the state: `status`, `task_type`, `current_stage`, `readiness`, `stages_completed`, `artifacts`.
> No callouts needed — tasks are minimal by design.

### CSS Customization

> [!info] **What's available (not yet implemented)**
> `.obsidian/snippets/` — any `.css` file loaded by Obsidian.
>
> **Custom callout types:**
> ```css
> .callout[data-callout="model"] {
>     --callout-color: 0, 120, 200;
>     --callout-icon: lucide-box;
> }
> ```
>
> **Per-page-type styling via cssclasses:**
> ```css
> .model-page h2 { border-bottom: 2px solid var(--interactive-accent); }
> ```
> Apply with `cssclasses: [model-page]` in frontmatter.

> [!warning] **Status: aspirational**
> No CSS snippets have been created yet. The callout vocabulary works with built-in types. Custom CSS is a future enhancement when the vocabulary stabilizes.

### Graceful Degradation

| Feature | Obsidian | GitHub | VS Code | Plain text |
|---------|----------|--------|---------|------------|
| `**bold**` | ✓ | ✓ | ✓ | `**visible**` |
| `==highlight==` | Yellow bg | `==visible==` | `==visible==` | `==visible==` |
| `> [!tip] Title` | Styled box | Blockquote | Blockquote | `>` prefix |
| `[[Page]]` | Link | `[[visible]]` | `[[visible]]` | `[[visible]]` |
| Mermaid | Diagram | Diagram | Code block | Code block |
| `%% comment %%` | Hidden | Visible | Visible | Visible |

> [!warning] **Hard constraint**
> Never put critical content ONLY in a callout title, an embed, or a highlight. The INFORMATION must survive in plain text. Styling enhances; it must not be required for comprehension.

### Before/After: The Impact of Styling

The [[Model: Methodology]] page demonstrates the difference. Its Model Catalog section went through three versions:

**Version 1 (raw):** Plain bold labels + prose paragraphs. A wall of text. 9 models listed as paragraphs with no visual structure. You had to read every word to find what you needed.

**Version 2 (tables):** Each model got a stage/artifact/gate table + bold "Selected when" + bold "Real instance." Structured but still visually flat — every section looked the same.

**Version 3 (callouts):** Each model gets `> [!info]` (blue header), table (data), `> [!abstract]` (conditions), `> [!example]-` (foldable instance). NOW each section has visual hierarchy: the blue header catches your eye, the table gives structure, the abstract gives context, and examples hide behind folds until you need them.

The information is the same in all three versions. The USABILITY is dramatically different.

### Compatibility Reference

Features we USE in this wiki (core set):

| Feature | Works in Obsidian | Degrades to |
|---------|------------------|-------------|
| Bold, italic, code, tables, lists | ✓ | Same everywhere |
| Callouts `> [!type]` | Styled boxes | Blockquotes |
| Wikilinks `[[Page]]` | Clickable links | Plain text |
| Highlights `==text==` | Yellow background | `==visible==` |
| Mermaid diagrams | Rendered | Code block (GitHub renders) |
| Comments `%% %%` | Hidden | Visible |
| Properties/cssclasses | Interpreted | YAML block |
| Foldable callouts `+`/`-` | Fold/expand | Always visible |

Features we're AWARE OF but don't use in the wiki (docs context):

| Feature | Where it works | What it does |
|---------|---------------|-------------|
| Remark directives `:::` | Docusaurus | Custom containers, admonitions |
| Tabs `:::tabs` | Docusaurus | Tabbed content panels |
| MDX/JSX | Docusaurus/React | Component injection in markdown |
| Custom directives | Remark plugins | Arbitrary syntax extensions |

## Open Questions

- Should we create custom callout types via CSS (e.g., `[!model]`, `[!stage]`) or keep to the 8 built-in types? (Requires: testing whether custom types add value or confusion)
- Should `cssclasses` be standardized per page type? (Requires: designing and testing a CSS snippet)
- Should model pages include Mermaid diagrams for selection flows? (Requires: testing readability in Obsidian)
- How should the callout vocabulary evolve as we apply it to more pages? (Requires: more pages styled → patterns emerge)

## Relationships

- BUILDS ON: [[Model: LLM Wiki]]
- BUILDS ON: [[LLM Wiki Standards — What Good Looks Like]]
- RELATES TO: [[Design.md Pattern]]
- RELATES TO: [[Infrastructure as Code Patterns]]
- RELATES TO: [[Model: Methodology]]
- ENABLES: All model and wiki pages

## Backlinks

[[Model: LLM Wiki]]
[[LLM Wiki Standards — What Good Looks Like]]
[[Design.md Pattern]]
[[Infrastructure as Code Patterns]]
[[Model: Methodology]]
[[All model and wiki pages]]
[[Model Registry]]
[[Wiki Design Standards — What Good Styling Looks Like]]
