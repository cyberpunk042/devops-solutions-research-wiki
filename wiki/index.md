# Research Wiki — Master Index

Central intelligence spine for the devops ecosystem. 175 pages of synthesized
knowledge across AI agents, knowledge systems, devops, automation, and tools.

## How to Browse This Wiki

This wiki is organized like a library. Start at the level that matches what you need:

| Level | What You'll Find | Start Here |
|-------|-----------------|------------|
| **Models** | System definitions — the big picture, 15 named models | [[Model Registry]] |
| **Domains** | Concept pages grouped by topic (53 pages across 7 domains) | Domain list below |
| **Patterns** | Recurring structures validated across 2+ independent systems | [patterns/](patterns/) |
| **Lessons** | Codified experience — what worked, what failed, why | [lessons/](lessons/) |
| **Decisions** | Choice frameworks with alternatives and rationale | [decisions/](decisions/) |
| **Comparisons** | Side-by-side evaluations with structured matrices | [comparisons/](comparisons/) |
| **Sources** | Individual source syntheses — the raw evidence layer | [sources/](sources/) |

**If you're new:** Read [[Model Registry]] first, then [[Model: Methodology]], then the domain that interests you.

**If you're an agent from another project:** [[Model Registry]] → find the relevant model → read it + its standards page → follow the How to Adopt section.

## Models — The Big Picture

15 named models organized into a three-layer pattern: system definition (model page) + execution standards (standards page) + visual design (callout vocabulary).

| Model | What It Defines | Standards |
|-------|----------------|-----------|
| [[Model: Methodology]] | HOW all work proceeds — the super-model | [[Methodology Standards — What Good Execution Looks Like]] |
| [[Model: LLM Wiki]] | WHAT the wiki IS — content structure, schema, operations | [[LLM Wiki Standards — What Good Looks Like]] |
| [[Model: Claude Code]] | The agent runtime — extensions, context, harness | [[Claude Code Standards — What Good Agent Configuration Looks Like]] |
| [[Model: Quality and Failure Prevention]] | Three-layer defense, failure lessons | [[Quality Standards — What Good Failure Prevention Looks Like]] |

See [[Model Registry]] for all 15 models with maturity status and line counts.

## Domains — Knowledge by Topic

| Domain | Pages | What's Inside |
|--------|-------|---------------|
| [ai-agents/](domains/ai-agents/) | 15 | Agent orchestration, Claude Code, harness engineering, skills, hooks, rework prevention |
| [knowledge-systems/](domains/knowledge-systems/) | 11 | LLM Wiki pattern, evolution pipeline, memory lifecycle, graph, PKM theory |
| [tools-and-platforms/](domains/tools-and-platforms/) | 10 | Obsidian, NotebookLM, AICP, OpenArms, Plane |
| [devops/](domains/devops/) | 9 | Stage-gate methodology, SFIF, backlog hierarchy, WSL2, ecosystem |
| [automation/](domains/automation/) | 5 | Pipeline orchestration, MCP integration, scheduling, event-driven automation |
| [cross-domain/](domains/cross-domain/) | 2 | Methodology framework, Skyscraper/Pyramid/Mountain |
| [ai-models/](domains/ai-models/) | 1 | Local LLM quantization |

## Knowledge Layers — Progressive Distillation

Each layer is denser and more actionable than the previous:

| Layer | Directory | Pages | What It Contains |
|-------|-----------|-------|-----------------|
| L0 | `raw/` | 70 files | Unprocessed source material (transcripts, articles, notes) |
| L1 | `sources/` | 24 | One synthesis per source — the evidence layer |
| L2 | `domains/` | 53 | Core concepts — one idea per page, by domain |
| L3 | `comparisons/` | 4 | Structured side-by-side evaluations |
| L4 | `lessons/` | 22 | Codified experience with evidence and applicability |
| L5 | `patterns/` | 11 | Recurring structures with 2+ validated instances |
| L6 | `decisions/` | 5 | Choice frameworks with alternatives and rationale |
| Spine | `spine/` | 31 | Models, standards, overviews, adoption guide |

## Operational

- **Project management**: [backlog/](backlog/) — epics, modules, tasks with stage gates
- **Operator directives**: [log/](log/) — verbatim directives and session summaries
- **Machine-readable**: [manifest.json](manifest.json) — full page inventory with metadata
- **Health check**: `python3 -m tools.pipeline post` → validates, lints, rebuilds indexes
- **Gap analysis**: `python3 -m tools.pipeline gaps` → orphans, thin pages, missing connections
