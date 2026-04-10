---
title: "Harness Engineering"
type: concept
layer: 2
maturity: growing
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-10
sources:
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    file: raw/articles/building-claude-code-harness-engineering.md
    title: "Building Claude Code with Harness Engineering"
    ingested: 2026-04-08
  - id: src-harness-engineering-github
    type: documentation
    url: "https://github.com/Chachamaru127/claude-code-harness"
    title: "claude-code-harness GitHub"
    ingested: 2026-04-08
  - id: src-claude-code-accuracy-tips
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=D5bRTv6GhXk"
    file: raw/transcripts/claude-code-works-better-when-you-do-this.txt
    title: "Claude Code Works Better When You Do This"
    ingested: 2026-04-08
tags: [harness-engineering, guardrails, plan-work-review, runtime-safety, agent-orchestration, claude-code, spec-driven, typescript]
---

# Harness Engineering

## Summary

Harness engineering is the practice of building structured control systems around LLM coding agents — moving beyond prompt engineering to runtime guardrails, quality validation, and rerunnable verification that keep development on a defined path. The pattern converges across independent implementations: Anthropic's Claude Code (permission-governed tool dispatch), the community claude-code-harness project (13 TypeScript guardrail rules), superpowers plugin (brainstorm-plan-execute-verify cycle), and OpenFleet (deterministic 30-second orchestrator). The convergence is the signal — when 10+ independent frameworks arrive at the same Plan → Execute → Review cycle with runtime enforcement, the pattern is inherent to effective AI-assisted development, not one team's preference.

## Key Insights

- **Runtime enforcement, not prompt guidance.** The critical distinction: harness guardrails operate at execution time through hooks, BLOCKING dangerous operations before they complete. This is fundamentally different from instructions the model may or may not follow. The compliance gap is measurable: ~60% for instructions vs ~98% for hooks.

- **The 5-verb workflow is universal.** Setup → Plan → Work → Review → Release maps to every structured approach in the ecosystem. The convergence across 10+ open-source frameworks confirms this is inherent to the domain, not arbitrary.

- **Planning investment reduces total cost.** The harness's Breezing mode adds Planner + Critic roles before coding — ~5.5x token cost vs ~4x without. But the reduced rework makes it net cheaper. Boris Cherny: "Do not make any changes until you have 95% confidence in what you need to build." The planning overhead is a rework insurance premium.

- **The harness is a SYSTEM, not a feature set.** CLAUDE.md + Skills + Hooks + Commands + Subagents working together as coordinated enforcement. Each level catches what the others miss. A collection of independent guardrails is not a harness — a harness is the coordination.

## Deep Analysis

### The Enforcement Hierarchy

> [!info] **Five levels from hope to certainty**
> | Level | Mechanism | Compliance | How it enforces |
> |-------|-----------|-----------|----------------|
> | 0 | Prompt guidance (CLAUDE.md, SKILL.md) | ~60% | Model reads instructions; may ignore under context pressure |
> | 1 | Status monitoring (context progress) | ~70% | Human sees the problem; intervenes manually |
> | 2 | Workflow orchestration (skills, pipeline chains) | ~80% | Steps are sequenced; but each step relies on model compliance |
> | 3 | Runtime guardrails (hooks, TypeScript engine) | ~98% | Execution-time blocking; model cannot complete the forbidden operation |
> | 4 | Deterministic orchestration (state machine) | 100% | No LLM in the loop; pure code decides |

> [!tip] **How to read this hierarchy**
> Each level is strictly stronger than the one below. A project's harness maturity = how much enforcement has migrated upward from Level 0 toward Level 4. This wiki operates at Levels 0-2. OpenFleet operates at Level 4 for its orchestration loop. The natural next step for any project is one level up from where it currently operates.

---

### The 5-Verb Universal Workflow

Every effective AI development harness implements this cycle, regardless of what they call it:

> [!info] **The 5 verbs and their ecosystem implementations**
> | Verb | What happens | superpowers | OpenFleet | This wiki | claude-code-harness |
> |------|-------------|-------------|-----------|-----------|-------------------|
> | **Setup** | Environment prepared, context loaded | Project scan, CLAUDE.md read | Agent identity loaded (SOUL.md) | Session resume, pipeline status | TypeScript config, rule loading |
> | **Plan** | Work scoped, approach chosen | Brainstorm → spec → plan | Task creation, backlog prioritization | Ingestion mode selection, gap analysis | Planner + Critic review |
> | **Work** | Implementation executed | Subagent-driven implementation | Agent execution cycle | Source processing, page writing | Code generation with guardrails |
> | **Review** | Output verified against standard | Spec compliance + code quality review | doctor.py immune check, human gate | `pipeline post` validation, lint | R11-R13 post-execution checks |
> | **Release** | Work committed and integrated | Branch merge, PR creation | Task completion, readiness update | Commit, backlink rebuild, sync | Merge with verified state |

> [!abstract] **Why this converges**
> 10+ independent frameworks (Everything Claude Code, Superpowers, Spec Kit, gstack, Get Shit Done, BMAD-METHOD, OpenSpec, oh-my-claudecode, Compound Engineering, HumanLayer) arrived at this cycle independently. The convergence is structural: AI agents need scoped intent (Plan), monitored execution (Work), and verified output (Review). The verbs may differ; the cycle does not.

---

### The 13 Guardrail Rules (R01-R13)

The claude-code-harness project implements 13 TypeScript rules as PreToolUse hooks. These are the Level 3 reference implementation:

> [!info] **Denial rules — block unconditionally**
> | Rule | What it blocks | Why it's unconditional |
> |------|---------------|----------------------|
> | R01 | `sudo` execution | Escalation to root is never justified in agent context |
> | R02 | Writes to `.git/` internals | Git internals should be modified via git commands, never directly |
> | R03 | Writes to `.env` files | Credentials must not be modified by automated agents |
> | R04 | `git push --force` | Force-push can destroy upstream work irreversibly |

> [!info] **Query rules — flag for confirmation**
> | Rule | What it flags | Decision |
> |------|-------------|----------|
> | R05 | Writes outside declared project scope | `ask` — escalate to user |
> | R06 | Unexpected package installations | `ask` — could introduce supply chain risk |
> | R07 | Large file operations (>threshold) | `ask` — context cost assessment |

> [!info] **Security rules — block bypasses**
> | Rule | What it blocks | What it prevents |
> |------|---------------|-----------------|
> | R08 | `--no-verify` flag | Bypassing git hooks (which may contain security checks) |
> | R09 | Direct pushes to main/master | Bypassing branch protection and review gates |
> | R10 | Files matching credential patterns | Accidental credential exposure |

> [!info] **Post-execution checks — warn on quality erosion**
> | Rule | What it detects | Response |
> |------|----------------|----------|
> | R11 | Assertion counts decreased in test files | Warn — test weakening |
> | R12 | Test files deleted or skipped | Warn — coverage erosion |
> | R13 | Coverage metrics decreased | Warn — quality regression |

> [!warning] **The design principle**
> Denial rules (R01-R04) return `block` — no reasoning around them. Query rules (R05-R07) return `ask` — the human decides. Security rules (R08-R10) return `block` — bypass prevention. Post-execution checks (R11-R13) return `warn` — the agent should know, the human should know, but work isn't blocked. The graduated response (block/ask/warn) matches the severity of the violation.

---

### The Breezing Mode: Planning as Rework Insurance

The harness's most expensive mode adds a Planner and Critic agent before any code is written:

> [!example]- **How Breezing mode works**
> 1. User describes the task
> 2. **Planner agent** decomposes the task into steps, identifies risks, proposes approach
> 3. **Critic agent** reviews the plan — challenges assumptions, identifies missing considerations
> 4. Planner revises based on critique
> 5. Only after plan approval does the **Worker agent** begin implementation
> 6. Post-implementation, the **Reviewer agent** checks against the original plan
>
> Token cost: ~5.5x vs ~4x without Breezing. But rework rate drops significantly — the planning discussion catches errors that would compound during implementation. The break-even: if Breezing prevents even one major rework cycle per session, it pays for itself.

This is the same principle as the wiki's "guided" ingestion mode: invest upfront in understanding to avoid downstream errors. And the same principle as the Methodology model's "always plan before executing" lesson.

---

### This Ecosystem's Harness

What the research wiki's own harness looks like — a concrete Level 0-2 implementation:

> [!info] **Current harness configuration**
> | Level | What we use | What it enforces |
> |-------|-----------|-----------------|
> | 0 — Prompt | CLAUDE.md (~180 lines) | Stage gates, quality gates, naming conventions, depth verification |
> | 0 — Prompt | `.claude/rules/` | Additional rules split from CLAUDE.md |
> | 1 — Skills | 5 skills (wiki-agent, evolve, continue, model-builder, notebooklm) | Workflow-specific methodology, quality bars |
> | 1 — Memory | Cross-session directives | "Never synthesize from descriptions alone", "never skip stages" |
> | 2 — Pipeline | `pipeline post` (6-step chain with exit code enforcement) | Schema validation, wikilink integrity, lint checks |
> | 2 — Pipeline | `pipeline evolve --score` (deterministic scorer) | Evolution candidate ranking without LLM |
> | 2 — Pipeline | `tools/validate.py` (exit code blocks) | Zero-tolerance for schema violations |

> [!warning] **What's missing (the Level 3 gap)**
> No PreToolUse hooks for stage-gate enforcement. The methodology says "no implementation during document stage" but nothing BLOCKS Write calls to `tools/` during the document stage. This is the gap between Level 2 (instruction-enforced) and Level 3 (hook-enforced). See [[Model: Quality and Failure Prevention]] for the planned hook-based enforcement design.

---

### Interactive vs Autonomous Harness

> [!abstract] **The enforcement mechanism shifts with the operating mode**
> | Dimension | Interactive (Claude Code) | Autonomous (OpenFleet) |
> |-----------|--------------------------|----------------------|
> | **Timing** | Enforcement at phase transitions | Continuous monitoring (every 30 seconds) |
> | **Detection** | Reactive — catch violations as they occur | Proactive — detect precursors before they occur |
> | **Escalation** | `ask` → user decides in real time | 3-strike accumulation → quarantine before dispatch |
> | **Recovery** | User fixes immediately | Circuit breaker failover + auto-retry |
> | **Cost of miss** | One rework (human catches quickly) | Cascade — one violation triggers 5 downstream reworks |

The cost asymmetry is why autonomous systems need proactive enforcement. In an interactive session, a human catches a mistake in the next turn. In an autonomous fleet, a mistake propagates through 5 dependent tasks before anyone notices.

## Open Questions

> [!question] **At what point does harness complexity become net negative?**
> Hooks + skills + commands + methodology.yaml + agent-directive.md is significant infrastructure. At what point does maintaining the harness cost more than the rework it prevents? (Requires: tracking harness maintenance hours vs rework hours prevented)

> [!question] **Should this ecosystem implement R01-R04 as Python hooks?**
> The answered question below recommends Python over TypeScript. But implementing even the 4 denial rules would be the first Level 3 enforcement in this ecosystem. Is the effort justified by the risk surface? (Requires: auditing how often dangerous operations are attempted in practice)

### Answered Open Questions

> [!success] **Python hooks, not TypeScript, for this ecosystem**
> Cross-referencing [[Decision: MCP vs CLI for Tool Integration]] and [[Immune System Rules]]: the ecosystem's toolchain is pure Python. doctor.py (24 production rules) is Python with zero LLM calls. Implementing equivalent rules in Python hooks via Claude Code's `settings.json` configuration keeps enforcement language consistent, avoids Node.js dependency, and makes rules maintainable by the same engineers who maintain the pipeline. A YAML rule file format could be a backend-agnostic abstraction executed by either Python or TypeScript engines.

> [!success] **Yes, guardrail rules can protect wiki operations**
> Cross-referencing [[Context-Aware Tool Loading]] and [[Knowledge Evolution Pipeline]]: (1) **Deny rule**: block deletion of wiki pages with relationship count above threshold (protect high-connectivity hubs). (2) **Query rule**: flag writes to `wiki/domains/` that don't update `_index.md` (detect orphan creation). (3) **Post-execution check**: run `tools/validate` after wiki writes, block on non-zero exit. (4) **Canonical protection**: block deletion of `maturity: canonical` pages without explicit override. All implementable as PreToolUse hooks.

> [!success] **Interactive = reactive enforcement; autonomous = proactive enforcement**
> Cross-referencing [[OpenFleet]], [[Immune System Rules]], [[Rework Prevention]]: the Plan-Execute-Review cycle stays the same, but interactive harness catches violations as they occur (PreToolUse at boundaries) while autonomous harness detects precursors before they occur (doctor.py every 30 seconds, 3-strike accumulation). The cost difference: one undetected autonomous violation cascades to ~5 downstream reworks, making proactive detection orders of magnitude cheaper.

## Relationships

- EXTENDS: [[Claude Code Best Practices]]
- EXTENDS: [[Claude Code Skills]]
- BUILDS ON: [[Claude Code]]
- PARALLELS: [[OpenFleet]]
- RELATES TO: [[Immune System Rules]]
- RELATES TO: [[Research Pipeline Orchestration]]
- RELATES TO: [[MCP Integration Architecture]]
- RELATES TO: [[Plan Execute Review Cycle]]
- RELATES TO: [[Rework Prevention]]
- FEEDS INTO: [[Model: Claude Code]]
- FEEDS INTO: [[Model: Quality and Failure Prevention]]

## Backlinks

[[Claude Code Best Practices]]
[[Claude Code Skills]]
[[Claude Code]]
[[OpenFleet]]
[[Immune System Rules]]
[[Research Pipeline Orchestration]]
[[MCP Integration Architecture]]
[[Plan Execute Review Cycle]]
[[Rework Prevention]]
[[Model: Claude Code]]
[[Model: Quality and Failure Prevention]]
[[Agent Orchestration Patterns]]
[[Always Plan Before Executing]]
[[Claude Code Standards — What Good Agent Configuration Looks Like]]
[[Context Management Is the Primary LLM Productivity Lever]]
[[Design.md Pattern]]
[[Deterministic Shell, LLM Core]]
[[Hooks Lifecycle Architecture]]
[[Infrastructure as Code Patterns]]
[[Model: MCP and CLI Integration]]
[[Model: Skills, Commands, and Hooks]]
[[Per-Role Command Architecture]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Spec-Driven Development]]
[[Synthesis: Playwright MCP for Visual Development Testing]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
