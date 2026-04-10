# Wiki Design — Markdown + Obsidian + Remark Syntax Research

Compiled: 2026-04-09
Sources: obsidian.md/help, markdownguide.org, github.com/remarkjs/remark

---

## Layer 1: Standard Markdown (universal)

### Text Formatting
- **Bold**: `**text**` or `__text__`
- *Italic*: `*text*` or `_text_`
- ***Bold+Italic***: `***text***`
- ~~Strikethrough~~: `~~text~~`
- `Inline code`: `` `code` ``
- Escape: `\*` for literal characters

### Structure
- Headings: `#` through `######`
- Paragraphs: blank line between
- Line breaks: two spaces + Enter, or `<br>`
- Horizontal rules: `---`, `***`, `___`
- Blockquotes: `> text`
- Nested blockquotes: `>> text`

### Lists
- Unordered: `- `, `* `, `+ ` (don't mix)
- Ordered: `1. `, `2. ` (start with 1)
- Task lists: `- [ ]` unchecked, `- [x]` checked
- Nesting: indent with Tab

### Code
- Inline: single backticks
- Blocks: triple backticks with language (```python)
- Nested blocks: outer uses more backticks than inner

### Links + Images
- Links: `[text](URL "title")`
- Reference links: `[text][label]` + `[label]: URL`
- Images: `![alt](URL "title")`
- Auto-link: `<https://example.com>`

### Tables
- Pipes and hyphens: `| Head | Head |` / `| --- | --- |`
- Alignment: `:--` left, `:--:` center, `--:` right
- Formatting inside cells: links, bold, italic, code — yes. Headings, lists — no.

### Extended
- Footnotes: `[^1]` inline + `[^1]: text` reference
- Heading IDs: `### Heading {#custom-id}`
- Definition lists: term + `: definition`
- ==Highlight==: `==text==` (not universal)
- Subscript: `H~2~O` / Superscript: `X^2^`
- Emoji: `:shortcode:` or paste directly

## Layer 2: Obsidian-Specific (Obsidian Flavored Markdown)

### Wikilinks
- `[[Page Name]]` — internal link
- `[[Page Name|Display Text]]` — aliased link
- `[[Page Name#Heading]]` — link to heading
- `[[Page Name#^block-id]]` — link to block
- `![[Page Name]]` — embed entire page
- `![[Image.png|640]]` — embed image with width

### Highlights
- `==highlighted text==` — renders with yellow background

### Comments
- `%% hidden text %%` — visible in edit mode only, invisible in reading view

### Callouts (the styling powerhouse)
14 built-in types:

| Type | Aliases | Color | Icon |
|------|---------|-------|------|
| note | — | Gray | Pencil |
| abstract | summary, tldr | Teal | Clipboard |
| info | — | Blue | Info circle |
| todo | — | Blue | Checkbox |
| tip | hint, important | Cyan | Flame |
| success | check, done | Green | Check |
| question | help, faq | Yellow | Question circle |
| warning | caution, attention | Orange | Alert triangle |
| failure | fail, missing | Red | X |
| danger | error | Red | Zap |
| bug | — | Red | Bug |
| example | — | Purple | List |
| quote | cite | Gray | Quote |

Syntax:
```
> [!type] Optional Custom Title
> Content here. Supports **all markdown** inside.
```

Foldable:
```
> [!type]+ Expanded by default
> [!type]- Collapsed by default
```

Nesting: nest callouts with additional `>` levels.

Custom callouts via CSS snippets:
```css
.callout[data-callout="model"] {
    --callout-color: 0, 120, 200;
    --callout-icon: lucide-box;
}
```

### Math/LaTeX
- Inline: `$E = mc^2$`
- Block: `$$` on own lines wrapping expression

### Mermaid Diagrams
- Flow charts, sequence diagrams, timelines, mind maps
- Code block with `mermaid` language
- Internal links via `internal-link` class on nodes

### Inline Footnotes
- `^[inline footnote text]` — reading view only

## Layer 3: Remark / Advanced Ecosystem

### remark-directive (:::container syntax)
Three directive types:
- **Container**: `:::name[label]{attrs}` + content + `:::`
- **Leaf**: `::name[label]{attrs}`
- **Text**: `:name[label]{attrs}`

Used for: tabs, admonitions, custom components, widget injection.

Example tabs:
```
:::tabs
::tab[Tab 1]
Content for tab 1
::tab[Tab 2]
Content for tab 2
:::
```

### remark-gfm
GitHub Flavored Markdown: tables, strikethrough, task lists, autolinks.

### remark-frontmatter
YAML/TOML frontmatter parsing.

### remark-toc
Auto-generate table of contents from headings.

### MDX
Markdown + JSX — embed React components directly in markdown.
Not directly relevant to Obsidian but relevant if wiki content needs to render in web contexts.

## Compatibility Matrix

| Feature | Standard MD | GFM | Obsidian | Remark |
|---------|-----------|-----|----------|--------|
| Bold/italic | ✓ | ✓ | ✓ | ✓ |
| Tables | ✗ | ✓ | ✓ | plugin |
| Task lists | ✗ | ✓ | ✓ | plugin |
| Strikethrough | ✗ | ✓ | ✓ | plugin |
| Highlight | ✗ | ✗ | ✓ | plugin |
| Callouts | ✗ | ✗ | ✓ | plugin |
| Wikilinks | ✗ | ✗ | ✓ | plugin |
| Math/LaTeX | ✗ | ✗ | ✓ | plugin |
| Mermaid | ✗ | ✓ | ✓ | plugin |
| Footnotes | ✗ | ✗ | ✓ | plugin |
| Comments | ✗ | ✗ | ✓ | ✗ |
| Embeds | ✗ | ✗ | ✓ | ✗ |
| Directives (:::) | ✗ | ✗ | ✗ | plugin |
| MDX/JSX | ✗ | ✗ | ✗ | plugin |

## Additional Findings (second research pass)

### Obsidian Properties (special frontmatter)
- `tags: [list]` — searchable tags (MUST be plural, list format since Obsidian 1.9)
- `aliases: [list]` — alternative names for the page
- `cssclasses: [list]` — CSS classes applied to the page. Enables per-page-type styling via CSS snippets.
  E.g., `cssclasses: [model-page]` + a snippet targeting `.model-page` can style all model pages consistently.

### Tags with hierarchy
- `#tag/subtag` — hierarchical tags for organization
- Searchable via Obsidian search and Dataview

### Block References
- `^block-id` at end of any paragraph — makes it linkable
- `[[Page#^block-id]]` — link to specific block
- `![[Page#^block-id]]` — embed specific block

### Dataview (if installed)
- Inline fields: `Key:: Value` anywhere in text
- Queries: ```dataview ... ``` code blocks
- Can generate tables, lists, task views from frontmatter

### Canvas (Obsidian-native)
- `.canvas` files — infinite canvas with cards
- Cards can contain markdown, links to notes, embeds
- JSON format — can be generated programmatically

### Remark Directive Syntax (for Docusaurus/web contexts)
Container directive:
```
:::note[Title]
Content here
:::
```

Leaf directive:
```
::youtube[Video Title]{#video-id}
```

Text directive:
```
:abbr[HTML]{title="HyperText Markup Language"}
```

Tabs:
```
:::tabs
::tab[JavaScript]
```js
console.log('hello');
```
::tab[Python]
```python
print('hello')
```
:::
```

Admonitions (similar to Obsidian callouts but in Docusaurus):
```
:::tip
Some content
:::

:::danger
Warning content
:::
```

### Key Distinction
- **Obsidian callouts** (`> [!type]`) = blockquote-based, works in Obsidian
- **Remark directives** (`:::type`) = container-based, works in Docusaurus/web
- Both achieve similar visual results but different syntax
- For this wiki (Obsidian-first), callouts are primary
- For future web rendering, remark directives would be the equivalent

### CSS Snippets Path
`.obsidian/snippets/` — any `.css` file here is loaded by Obsidian.
Can define:
- Custom callout types with colors and Lucide icons
- Per-page styling via cssclasses
- Table styling, heading styling, tag colors
- Graph view customization
