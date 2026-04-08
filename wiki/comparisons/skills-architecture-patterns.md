---
title: "Skills Architecture Patterns"
type: comparison
domain: cross-domain
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-claude-notebooklm-content-team
    type: youtube-transcript
    file: wiki/sources/src-claude-notebooklm-content-team.md
    title: "Claude + NotebookLM = Your 24/7 Content Team"
  - id: src-shanraisshan-claude-code-best-practice
    type: documentation
    file: wiki/sources/src-shanraisshan-claude-code-best-practice.md
    title: "shanraisshan/claude-code-best-practice"
  - id: src-obsidian-claude-code-second-brain
    type: youtube-transcript
    file: wiki/sources/src-obsidian-claude-code-second-brain.md
    title: "Obsidian + Claude Code: The Second Brain Setup That Actually Works"
  - id: src-kepano-obsidian-skills
    type: documentation
    file: wiki/sources/src-kepano-obsidian-skills.md
    title: "kepano/obsidian-skills"
  - id: src-axton-obsidian-visual-skills
    type: documentation
    file: wiki/sources/src-axton-obsidian-visual-skills.md
    title: "axtonliu/axton-obsidian-visual-skills"
  - id: src-pablo-mano-obsidian-cli-skill
    type: documentation
    file: wiki/sources/src-pablo-mano-obsidian-cli-skill.md
    title: "pablo-mano/Obsidian-CLI-skill"
  - id: src-claude-world-notebooklm-skill
    type: documentation
    file: wiki/sources/src-claude-world-notebooklm-skill.md
    title: "claude-world/notebooklm-skill"
  - id: src-pleaseprompto-notebooklm-skill
    type: documentation
    file: wiki/sources/src-pleaseprompto-notebooklm-skill.md
    title: "PleasePrompto/notebooklm-skill"
  - id: src-token-hacks-claude-code
    type: youtube-transcript
    file: wiki/sources/src-token-hacks-claude-code.md
    title: "18 Claude Code Token Hacks in 18 Minutes"
tags: [skills, architecture, patterns, cross-domain, claude-code, obsidian, notebooklm, SKILL-md, agent-extensibility, composition]
---

# Skills Architecture Patterns

## Summary

Across 8 sources spanning 3 skill ecosystems (Claude Code core, Obsidian, NotebookLM), a consistent set of architectural patterns has emerged for extending AI agent capabilities through skills. This page synthesizes these patterns by comparing how skills are structured, composed, distributed, and evolved across the different ecosystems. Despite being developed independently by different authors, the skill implementations converge on shared design principles while diverging on scope and complexity in ways that reveal the maturation trajectory of the skills pattern.

## Comparison Matrix

| Criteria | Claude Code Core Skills | Obsidian Skills Ecosystem | NotebookLM Skills Ecosystem |
|----------|------------------------|--------------------------|----------------------------|
| Definition format | SKILL.md markdown | SKILL.md markdown | SKILL.md markdown |
| Trigger mechanism | Auto-detected from description field | Manual invocation or agent selection | Manual invocation or pipeline step |
| Complexity ceiling | Full pipeline (multi-agent orchestration) | Full pipeline (130+ CLI commands, pablo-mano) | Full pipeline (11 CLI + 13 MCP tools, claude-world) |
| Composition model | Hierarchical: Command → Agent → Skill | Layered: format → generate → control | Complementary: pipeline vs ad-hoc query |
| Context cost model | Loaded every message if active; fork for isolation | Loaded when referenced | Pipeline skills load for duration; query skills per-question |
| Distribution channel | Claude Code marketplace, npx, manual | agentskills.io, GitHub, marketplace | GitHub repositories |
| Standard body | Anthropic / agentskills.io (kepano) | agentskills.io (kepano) | None — community-driven |
| Production form | Folder with references/, scripts/, examples/ | Single file (kepano) to comprehensive folder (pablo-mano) | Single skill file or CLI+MCP pipeline (claude-world) |
| Best for | Coding agents, DevOps automation, multi-step workflows | Vault management, note generation, Obsidian-specific workflows | Research synthesis, NotebookLM source management, content production |

## Key Insights

- All three ecosystems (Claude Code, Obsidian, NotebookLM) independently converged on SKILL.md markdown as the universal definition format
- Skills follow a complexity spectrum: tool wrapper → tool + guidance → multi-tool orchestration → full pipeline
- Three-layer stratification emerges independently: specification layer, generation layer, control layer
- Skills are compressed knowledge that LLMs expand into operational behavior at runtime — the same pattern as the LLM Wiki applied to agent behavior
- Context cost is the primary constraint on skill complexity — active skills consume tokens on every message
- Composition (skills referencing skills) remains largely unsolved across all ecosystems

## Cross-Ecosystem Comparison

### Structural Patterns

| Pattern | Claude Code Core | Obsidian Ecosystem | NotebookLM Ecosystem |
|---|---|---|---|
| Definition format | SKILL.md (markdown) | SKILL.md (markdown) | SKILL.md (markdown) |
| Simple form | Single markdown file | Single markdown file | Single markdown file |
| Production form | Folder with references/, scripts/, examples/ | Varies: single file (kepano) to comprehensive (pablo-mano 130+ commands) | Pipeline with CLI + MCP (claude-world) or skill-only (PleasePrompto) |
| Trigger mechanism | Description field written for the model | Manual invocation or agent selection | Manual invocation or pipeline step |
| Context cost model | Loaded on every message if active; context: fork for isolation | Loaded when referenced | Pipeline skills load for pipeline duration; query skills load per-question |
| Distribution | Claude Code marketplace, npx, manual | agentskills.io spec, GitHub, marketplace | GitHub repositories |

### Complexity Spectrum

All three ecosystems independently demonstrate a skill complexity spectrum that follows the same progression:

1. **Tool wrappers** (simplest): A skill that teaches the agent to use a single external tool. Examples: kepano's obsidian-markdown (format spec), PleasePrompto's NotebookLM query skill (ask one question, get one answer).

2. **Tool + guidance**: A skill that wraps a tool and adds domain-specific knowledge like design systems or formatting preferences. Examples: the NotebookLM content team skill (tool wrapper + slide design specifications with named style presets).

3. **Multi-tool orchestration**: A skill that coordinates multiple tools and data sources with conditional logic. Examples: the "onboard projects" skill from the second brain video (Gmail API + local filesystem + user input, with duplicate detection and conditional processing).

4. **Full pipeline skills**: A skill that implements an end-to-end workflow with multiple phases. Examples: claude-world/notebooklm-skill (source discovery, research, content generation, multi-platform publishing with 11 CLI commands and 13 MCP tools).

This spectrum was not designed by any single author -- it emerged independently across ecosystems, suggesting it reflects inherent complexity boundaries in how much instruction an LLM can reliably follow.

### Composition Patterns

Three distinct composition patterns appear across the ecosystems:

- **Layered composition** (Obsidian): kepano defines formats, axton generates content in those formats, pablo-mano provides programmatic vault control. Each layer builds on the one below. A user installs all three for comprehensive coverage.

- **Complementary composition** (NotebookLM): claude-world handles content production pipelines; PleasePrompto handles ad-hoc knowledge queries. Different use cases, same platform, no overlap.

- **Hierarchical composition** (Claude Code core): Commands orchestrate, Agents execute in isolation, Skills provide knowledge. The Command-Agent-Skill hierarchy is explicit and designed, not emergent.

### The SKILL.md Convergence

All three ecosystems use SKILL.md as the primary definition format. This is notable because there was no central authority mandating this -- kepano's agentskills.io specification is one standardization effort, but pablo-mano and the NotebookLM skill authors arrived at the same format independently. The convergence suggests that markdown-as-skill-definition is a natural attractor for LLM agent extensibility.

Key properties that make SKILL.md effective:
- Human-readable and human-editable (no compilation step)
- LLM-native (the agent reads the same format it outputs)
- Portable across agents (pablo-mano's skill works with 8+ agent platforms by pasting SKILL.md into system prompts)
- Version-controllable with Git
- Iteratively refinable through conversation ("change the slide style from orange to navy blue")

### Tensions and Contradictions

**Single file vs. folder structure**: The content team video presents skills as "just a markdown file," while shanraisshan's best practices insist skills should be "folders with subdirectories (references/, scripts/, examples/)." This is not a contradiction but a maturity spectrum -- skills start as single files and graduate to folders as they accumulate scripts, references, and gotchas. The practical boundary appears to be when a skill needs to coordinate between multiple code artifacts (the "onboard projects" skill bundles custom Gmail scripts alongside instructions).

**Context cost vs. capability breadth**: Every loaded skill consumes context window tokens. The best practices recommend context: fork for isolation, but this spawns a sub-agent at 7-10x token cost. MCP-based skills (claude-world's 13 tools) add tool definitions on every message. There is no free lunch -- more capable skills cost more tokens. This tension is the skills-specific instance of the broader context management challenge.

**Official vs. community quality**: kepano's official Obsidian skills follow the agentskills.io spec but are thinner than community skills. pablo-mano's community skill covers 130+ CLI commands vs. kepano's basic CLI coverage. axton's visual skills are labeled experimental. The ecosystem benefits from both official standards and community depth, but quality variance in community skills creates reliability uncertainty.

## Deep Analysis

The skills pattern across all three ecosystems reveals a fundamental principle: **skills are compressed knowledge that LLMs expand into operational behavior at runtime**. The NotebookLM content team video makes this explicit -- a skill's design specifications (color schemes, fonts, layouts) are compressed into a few lines of markdown, but Claude Code expands them into detailed multi-slide prompts with specific parameters at execution time. The user never writes these detailed prompts.

This compression-expansion dynamic is what makes skills powerful and also what limits them. The LLM must be able to reliably decompress the skill's intent into correct action sequences. As skill complexity increases, the decompression becomes less reliable -- the upper bound on skill complexity is the point where the LLM can no longer reliably interpret the compressed instructions. None of the sources have empirically measured this boundary, making it the most important open question in skills architecture.

The cross-ecosystem convergence on SKILL.md is also significant from a knowledge-systems perspective. Skills are effectively a specialized form of the LLM Wiki Pattern applied to agent behavior rather than domain knowledge. Where wiki pages store knowledge about the world, skills store knowledge about how to act. Both use markdown, both are LLM-maintained, both compound over time through iterative refinement. This suggests that the LLM Wiki Pattern is not just a knowledge management approach but a general pattern for LLM-readable persistent artifacts.

The connection to context management is the critical constraint that shapes all skill architecture decisions. Every skill loaded into a session has a per-message token cost. A session with 5 active skills, 3 MCP servers, and a 200-line CLAUDE.md may consume 100,000+ tokens before any work begins. This economic pressure drives the architectural patterns: progressive disclosure (only load details when needed), context forking (isolate skill execution), and the Command-Agent-Skill hierarchy (use the lightest-weight mechanism that works).

## Open Questions

- What is the empirical complexity ceiling for skills -- at what point does the LLM's decompression of skill instructions become unreliable?
- Will agentskills.io become the universal standard, or will platform-specific skill formats fragment the ecosystem?
- Can skills be automatically generated from observed user workflows (skill induction)?
- How should skill versioning work -- semantic versioning for breaking changes in instruction format?
- Can the compression-expansion pattern be measured -- what is the ratio of skill file size to effective prompt size at runtime?
- How do skills interact with the memory lifecycle -- should frequently-used skills be promoted to procedural memory in the LLM Wiki v2 model?

## Relationships

- SYNTHESIZES: Claude Code Skills
- SYNTHESIZES: Obsidian Skills Ecosystem
- SYNTHESIZES: NotebookLM Skills
- RELATES TO: Claude Code Best Practices
- RELATES TO: Claude Code Context Management
- RELATES TO: AI-Driven Content Pipeline
- RELATES TO: LLM Wiki Pattern

## Backlinks

[[Claude Code Skills]]
[[Obsidian Skills Ecosystem]]
[[NotebookLM Skills]]
[[Claude Code Best Practices]]
[[Claude Code Context Management]]
[[AI-Driven Content Pipeline]]
[[LLM Wiki Pattern]]
[[Infrastructure as Code Patterns]]
[[Pattern: Skills + Obsidian]]
