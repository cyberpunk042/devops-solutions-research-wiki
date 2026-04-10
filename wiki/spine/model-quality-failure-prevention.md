---
title: "Model: Quality and Failure Prevention"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
    ingested: 2026-04-08
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
    ingested: 2026-04-08
  - id: src-devops-control-plane-local
    type: documentation
    file: ../devops-control-plane/README.md
    title: "devops-control-plane — Local Project Documentation"
    ingested: 2026-04-08
tags: [model, spine, quality, failure-prevention, harness, immune-system, rework, depth-verification, stage-gates, methodology]
---

# Model: Quality and Failure Prevention

## Summary

Quality and failure prevention for AI agents is not a set of best practices — it is a system with three enforcement layers (structural prevention, teaching, review), six codified failure lessons, and deterministic mechanisms that cannot be bypassed by prompt engineering. The model synthesizes evidence from four domains: harness engineering (13 guardrail rules enforced via hooks), OpenFleet's immune system (24 rules from 16 post-mortems), rework prevention economics, and this wiki's own operational failures. ==The central thesis: quality enforcement must live in code that runs at execution time, not in documentation that the agent may or may not consult.==

## Key Insights

- **Three-layer defense is the minimum viable quality architecture.** Structural prevention (hooks, doctor.py) blocks bad actions. Teaching (CLAUDE.md, skills, memory) shapes behavior. Review (human gates) catches what automation misses. Any single layer alone is insufficient.

- **Failure lessons must be codified, not just remembered.** Each failure maps to a concrete enforcement mechanism. A lesson that exists only as documentation is a suggestion. A lesson encoded in CLAUDE.md, enforced by a hook, and checked by the post-chain is a rule.

- **Rework is multiplicative, not additive.** Redoing work requires reverting, re-planning, re-executing, and re-verifying. In a multi-agent fleet, one bad dispatch cascades. Prevention is cheaper than cure — the break-even threshold is only 12% rework reduction.

- **Depth verification is the single highest-leverage quality rule.** Reading the thing itself rather than a description of the thing prevents the most common class of hollow synthesis.

- **Methodology IS failure prevention.** Stage gates, quality gates per stage, "do not advance until the gate passes" — these are the operational form of every lesson in this model.

## Deep Analysis

### The Three-Layer Defense

> [!info] **Three layers, three failure classes**
> | Layer | Mechanism | What it catches | Compliance | Example |
> |-------|-----------|----------------|-----------|---------|
> | **1 — Structural prevention** | Hooks, doctor.py, deterministic guards | Actions that should NEVER happen | ~98% | Block sudo, force-push, .env writes |
> | **2 — Teaching** | CLAUDE.md, skills, memory | Behavioral patterns that lead to failures | ~60% | "Always run pipeline post after changes" |
> | **3 — Review** | Human gates at stage transitions | Subjective quality the agent can't evaluate | 100% (when engaged) | "Does this synthesis capture the source's meaning?" |

**Layer 1 — Structural Prevention** blocks bad actions at execution time. The agent cannot bypass these through reasoning, confidence, or prompt injection.

> [!example]- **Implementations across the ecosystem**
> - **[[Harness Engineering]]**: 13 TypeScript guardrail rules (R01-R13) enforced via Claude Code hooks. Denial rules block sudo, .env writes, force-push. Query rules flag out-of-scope writes. Security rules prevent --no-verify and direct main pushes.
> - **[[Immune System Rules]]**: 24 Python rules in doctor.py running at step 6 of the 12-step orchestrator cycle. Zero LLM calls — pure state evaluation. Five categories: liveness, loop detection, state integrity, behavioral security, resource exhaustion.
> - **[[Deterministic Shell, LLM Core]]**: The architectural pattern. The LLM operates only in the execution phase, surrounded by deterministic code. The shell enforces invariants that cannot be social-engineered.

> [!tip] **The critical property**
> Structural prevention is deterministic, fast (microseconds per check), cheap (no token cost), and auditable (no inference variability). An LLM-based quality gate would be unreliable by design.

**Layer 2 — Teaching** shapes behavior before the action is considered. Well-designed teaching reduces the frequency of hook violations, making Layer 1 a backstop rather than the primary defense.

> [!info] **The teaching stack**
> | Mechanism | When it loads | Persistence | Example |
> |-----------|-------------|-------------|---------|
> | CLAUDE.md | Every message | Per-project | Quality gates, ingestion modes, stage gates |
> | Skills | On invocation | Per-session | wiki-agent ingestion methodology, evolve maturity rules |
> | Memory | Cross-session | Permanent | "Never synthesize from descriptions alone" |

**Layer 3 — Review** handles decisions automation cannot evaluate: Does this synthesis capture the source's meaning? Is this architecture right for this context? Does this page deserve maturity promotion?

> [!abstract] **Review gates in the wiki**
> - **Guided mode**: human approves extraction plan before synthesis begins
> - **Smart mode escalation**: auto-processing stops on new domains, contradictions, ambiguity
> - **Maturity promotion**: seed pages require review before advancing to growing

---

### The Six Failure Lessons

Each lesson was extracted from a real operational failure in this wiki. Each maps to a specific enforcement mechanism.

> [!bug]- **1. Never Synthesize from Descriptions Alone**
> **The failure:** Agent ingested a curated list (awesome-design-md), synthesized a page claiming to understand the DESIGN.md pattern, but had never opened a single real DESIGN.md file. Confident-sounding, factually hollow.
>
> **The principle:** Layer 0 (description of a thing) is not Layer 1 (an instance of the thing). Minimum bar: examine at least one real instance.
>
> **Enforcement:** CLAUDE.md quality gates + wiki-agent skill depth verification + memory directive. The 0.25 ratio rule (25% of ingestion on primary sources) provides a measurable threshold. See [[Never Synthesize from Descriptions Alone]].

> [!bug]- **2. Never Skip Stages Even When Told to Continue**
> **The failure:** Agent treated "continue" as permission to skip brainstorm and jump to spec writing. User response: "WTF ???? WHAT SPEC ??? WTF ???????"
>
> **The principle:** "Continue" = advance within current stage. Only "skip to X" authorizes stage-skipping.
>
> **Enforcement:** CLAUDE.md stage gates + mandatory post-chain (errors block completion). See [[Never Skip Stages Even When Told to Continue]].

> [!bug]- **3. Shallow Ingestion Is Systemic, Not Isolated**
> **The failure:** Thin pages accumulated — minimal summaries, sparse relationships, no deep analysis. The evolution pipeline had no quality candidates to promote.
>
> **The principle:** Soft quality gates degrade the entire system. One skipped gate creates systematic downstream degradation.
>
> **Enforcement:** Validation requires ≥30-word summaries, ≥1 relationship, source provenance, no >70% overlap. See [[Shallow Ingestion Is Systemic, Not Isolated]].

> [!bug]- **4. Infrastructure Must Be Reproducible, Not Manual**
> **The failure:** Agent tried to `cat >` a systemd service file directly. Configuration silently diverged across environments.
>
> **The principle:** Any infrastructure step not encoded in a script is a quality gap. Manual steps are undocumented, unrepeatable, invisible.
>
> **Enforcement:** `python -m tools.setup` handles all setup. `--services` deploys daemons reproducibly. No manual infra creation. See [[Infrastructure Must Be Reproducible, Not Manual]].

> [!bug]- **5. The Agent Must Practice What It Documents**
> **The failure:** Wiki documented methodology extensively — stage gates, brainstorm-before-spec, depth verification. Agent skipped all of them. Documentation was correct; behavior was not.
>
> **The principle:** Methodology in wiki pages is useless if not in CLAUDE.md. Rules must exist in the agent's OPERATIONAL instructions, not just its knowledge base.
>
> **Enforcement:** CLAUDE.md contains the rules the agent follows. When the wiki evolves a rule, it must propagate to CLAUDE.md. See [[The Agent Must Practice What It Documents]].

> [!bug]- **6. Models Are Built in Layers, Not All at Once**
> **The failure:** 14 model pages batch-produced as 80-110 line reading lists. Agent claimed "models are ready." User: "I dont even see 2% of it..."
>
> **The principle:** Structure (pages exist) ≠ substance (pages define systems). The SFIF pattern applies to model-building itself: scaffold → foundation → infrastructure → features.
>
> **Enforcement:** Model-builder skill defines the quality bar (≥150 lines, system definition not reading list, Key Pages, Lessons, State of Knowledge, How to Adopt). See [[Models Are Built in Layers, Not All at Once]].

---

### The Immune System (OpenFleet)

> [!info] **24 rules from 16 post-mortems — production-grade structural prevention**
> | Category | What it detects | Example rules |
> |----------|----------------|---------------|
> | **Liveness** | Agents alive in state but dead in practice | Heartbeat timeout, stale session ID, stuck execution |
> | **Loop detection** | Runaway cycles | Retry storms, circular dependencies, dispatch-without-completion |
> | **State integrity** | Impossible state combinations | Parent complete but children pending, blocked with no blocker |
> | **Behavioral security** | Permission and scope violations | Out-of-scope writes, cost spikes, capability acquisition beyond spec |
> | **Resource exhaustion** | Degraded conditions | Circuit breaker open, external service unresponsive, memory pressure |

> [!tip] **The 3-Strike Pattern**
> One violation doesn't trigger action. Three violations within a window trigger quarantine. This tolerates transient anomalies (network blips, brief CPU spikes) while catching persistent failures. doctor.py runs at step 6 of the 12-step orchestrator cycle — after security scan, before dispatch. Flagged tasks accumulate strikes before they can reach dispatch. Preemptive immune response, not reactive incident handling.

---

### The Enforcement Level Hierarchy

> [!info] **Enforcement levels — from hope to certainty**
> | Level | Mechanism | Compliance | Example |
> |-------|-----------|-----------|---------|
> | 0 | Prompt guidance (CLAUDE.md) | ~60% | "Always run tests before committing" |
> | 1 | Workflow orchestration (skills, chains) | ~80% | Research-Plan-Execute-Review cycle |
> | 2 | Runtime guardrails (hooks, pre/post) | ~98% | Block sudo, force-push, .env writes |
> | 3 | Deterministic orchestration (state machine) | 100% | OpenFleet 30-second brain cycle |

> [!warning] **Measuring maturity**
> A project's quality maturity = how much enforcement has migrated upward from Level 0 toward Level 3. This wiki currently operates at Levels 0-1. The planned next step is Level 2 (hook-based stage-gate enforcement). OpenFleet operates at Level 3 for its orchestration loop.

---

### Rework Prevention Economics

> [!info] **The cost model that justifies every quality gate**
> ```
> Single rework cycle ≈ 2.5T to 3.5T (estimate — needs measurement)
>   T = original task, R = revert, D = diagnosis,
>   P = re-plan, T = re-execute, V = re-verify
>
> Prevention investment: 0.2T to 0.4T per task
> Break-even: prevention net-positive if rework reduced by >12%
> Real rework rates without gates: 20-40% on complex tasks
> ```

> [!warning] **Unverified numbers**
> The specific multiplier (2.5-3.5x) and rework rates (20-40%) are estimates from harness engineering literature, not measured from this ecosystem. The PRINCIPLE (prevention < rework) is structurally sound. The NUMBERS need measurement from real project data.

> [!abstract] **How the wiki maps to prevention investment**
> - **Guided mode** = maximum prevention (human approves every step) — highest cost, lowest rework
> - **Smart mode** = risk-calibrated (auto when confident, escalate when not) — balanced
> - **Auto mode** = throughput-first (process without stopping) — lowest cost, highest rework risk

---

### The Depth Verification System

> [!warning] **The single highest-leverage quality rule**
> Read the thing, not the description of the thing. A README listing 58 DESIGN.md files ≠ reading a DESIGN.md file. An API spec ≠ a real request/response pair.

> [!info] **The layer model for source depth**
> | Layer | What it is | Synthesis quality |
> |-------|-----------|------------------|
> | Layer 0 | Description of the thing (README, catalog, index) | Hollow — confident surface, no substance |
> | Layer 1 | A real instance of the thing (actual file, output, config) | Grounded — specific, verifiable claims |
> | Layer 2 | Multiple instances compared (pattern extraction from N examples) | Deep — structural insights across instances |

Minimum bar for synthesis: **Layer 1**. The 0.25 ratio rule — at least 25% of ingestion effort on primary sources — provides a measurable threshold.

---

### How the Three Layers Interact

The layers are not independent — they form a defense-in-depth system where each layer reduces the load on the others.

> [!abstract] **The interaction model**
> **Teaching reduces the violation rate** — a well-taught agent (CLAUDE.md + skills + memory) attempts fewer dangerous operations, making structural prevention a backstop instead of the primary defense.
>
> **Structural prevention catches what teaching misses** — ~40% of the time, the agent ignores or forgets instructions. Hooks block the operation before it completes. The agent learns nothing from the block (it just fails), but damage is prevented.
>
> **Review handles the irreducibly subjective** — "Does this synthesis capture the source's meaning?" is not a question code can answer. Review gates exist for decisions that require human judgment, not for decisions that could be automated.
>
> **The failure mode is relying on ONE layer.** Hooks without teaching → correct-but-misaligned work (the agent does safe things but not the RIGHT things). Teaching without hooks → well-intentioned failures (the agent knows the rules but doesn't always follow them). Review without either → exhausted humans catching everything manually.

---

### The Methodology Connection

==Stage gates are the structural embodiment of failure prevention.== Each stage has a quality gate. Work does not advance until the gate passes. This is not process overhead — it is the operational form of every lesson in this model:

> [!info] **Each lesson maps to a stage gate**
> | Lesson | Stage gate it maps to |
> |--------|----------------------|
> | "Never synthesize from descriptions alone" | Extraction gate requires primary source examination (Layer 1+) |
> | "Never skip stages" | Gates are mandatory, not advisory — errors block advancement |
> | "Shallow ingestion is systemic" | Gate criteria enforce minimum depth (≥30 words, ≥1 relationship) |
> | "Infrastructure must be reproducible" | Post-chain automates gate enforcement (`pipeline post` = 6 deterministic steps) |
> | "Practice what you document" | CLAUDE.md contains the gates the agent must pass (operational, not aspirational) |
> | "Models built in layers" | Model-builder skill quality bar IS the gate for model creation |

The post-ingestion chain (`python3 -m tools.pipeline post`) is the automated enforcement: rebuild indexes → regenerate manifest → validate all pages (errors block) → regenerate wikilinks → run lint → rebuild layer indexes. Six steps, all mandatory, all deterministic. This is structural prevention applied to the wiki's own methodology.

---

### Key Pages

| Page | Layer | Role in the model |
|------|-------|-------------------|
| [[Harness Engineering]] | L2 | The coordinated enforcement architecture — 13 rules, 5-verb workflow, enforcement hierarchy |
| [[Immune System Rules]] | L2 | 24 production rules from 16 post-mortems — liveness, loops, state, security, resources |
| [[Rework Prevention]] | L2 | Cost model justifying quality gates — prevention vs rework economics |
| [[Deterministic Shell, LLM Core]] | L5 | The architectural pattern — deterministic code surrounding probabilistic LLM |
| [[LLM Knowledge Linting]] | L2 | Automated quality maintenance — detecting orphans, contradictions, staleness |
| [[Task Lifecycle Stage Gating]] | L2 | Stage-gate mechanics — how tasks progress through gates |
| [[Skyscraper, Pyramid, Mountain]] | L2 | Quality tier framework — explicit choice vs accidental chaos |
| [[Never Synthesize from Descriptions Alone]] | L4 | Failure lesson — depth verification origin |
| [[Never Skip Stages Even When Told to Continue]] | L4 | Failure lesson — stage-gate enforcement origin |
| [[Shallow Ingestion Is Systemic, Not Isolated]] | L4 | Failure lesson — systemic quality degradation |
| [[Infrastructure Must Be Reproducible, Not Manual]] | L4 | Failure lesson — reproducible tooling origin |
| [[The Agent Must Practice What It Documents]] | L4 | Failure lesson — operational rules vs documentation gap |
| [[Models Are Built in Layers, Not All at Once]] | L4 | Failure lesson — structure ≠ substance |
| [[Plan Execute Review Cycle]] | L5 | The universal workflow that harness engineering codifies |
| [[Always Plan Before Executing]] | L4 | The planning discipline that prevents the most rework |
| [[Claude Code Best Practices]] | L2 | Teaching layer content — planning discipline, context hygiene, skill architecture |
| [[Automated Knowledge Validation Prevents Silent Wiki Decay]] | L4 | Why automated linting prevents the most common quality failure mode |

---

### Lessons Learned

| Lesson | What was learned | Enforcement mechanism |
|--------|-----------------|---------------------|
| [[Never Synthesize from Descriptions Alone]] | Layer 0 ≠ Layer 1. Read the thing, not the description. | CLAUDE.md + wiki-agent skill + 0.25 ratio rule |
| [[Never Skip Stages Even When Told to Continue]] | "Continue" = within current stage. Stage gates are hard boundaries. | CLAUDE.md stage gates + mandatory post-chain |
| [[Shallow Ingestion Is Systemic, Not Isolated]] | Soft gates degrade the entire system. Quality compounds. | Validation: ≥30 words, ≥1 relationship, source provenance |
| [[Infrastructure Must Be Reproducible, Not Manual]] | Manual steps are undocumented, unrepeatable, invisible. | `tools/setup.py` handles all infra deployment |
| [[The Agent Must Practice What It Documents]] | Rules in wiki pages ≠ rules the agent follows. Must be in CLAUDE.md. | CLAUDE.md contains operational rules, not just documentation |
| [[Models Are Built in Layers, Not All at Once]] | Structure ≠ substance. Follow SFIF for model building. | Model-builder skill with quality bar + checklist |

---

### State of Knowledge

> [!success] **Well-covered (multiple sources, real evidence)**
> - Three-layer defense architecture (structural + teaching + review)
> - Six failure lessons with real incidents and enforcement mechanisms
> - Harness engineering: 13 guardrail rules, enforcement hierarchy, 5-verb workflow
> - Immune system: 24 rules from 16 post-mortems, 3-strike pattern
> - Depth verification: layer model, 0.25 ratio rule, enforcement stack
> - Stage-gate methodology connection (each lesson maps to a gate)

> [!warning] **Thin or unverified**
> - Rework multiplier (2.5-3.5x) — estimate, not measured from this ecosystem
> - Rework rates (20-40%) — from literature, not from our data
> - Hook-based enforcement for wiki quality — no hooks implemented yet (Level 0-1 only)
> - Quantitative enforcement level measurement — no metric for "what % of rules are at Level 0 vs Level 3"
> - Cross-project quality comparison — how do OpenFleet, AICP, and this wiki compare on enforcement maturity?

---

### How to Adopt

> [!info] **Setting up the quality system for a new project**
> 1. **CLAUDE.md** — add quality gates (minimum standards per artifact type)
> 2. **Validation tooling** — schema validation that blocks on errors (exit code enforcement)
> 3. **Post-chain** — automated multi-step validation after every change batch
> 4. **Depth verification** — add the Layer 0/1/2 rule to ingestion methodology
> 5. **Stage gates** — define ALLOWED/FORBIDDEN per stage in methodology.yaml

> [!warning] **INVARIANT — never change these**
> - Quality enforcement must be deterministic (no LLM-based quality gates)
> - Validation errors block completion (not advisory)
> - Failure lessons propagate to CLAUDE.md (operational, not just documented)
> - Three-layer defense (all three required — no single layer is sufficient)
> - Rework prevention via upfront investment (plan before execute)

> [!tip] **PER-PROJECT — always adapt these**
> - Which quality gates apply (code projects: compilation + lint + tests; wiki projects: validation + links + word count)
> - Which enforcement level to start at (Level 0 is fine initially — migrate upward as methodology matures)
> - Which failure lessons are relevant (not all 6 apply to every project type)
> - The 3-strike threshold for immune system rules (project-specific tolerance)
> - Review gate triggers (what requires human review vs what auto-advances)

> [!bug]- **What goes wrong if you skip this**
> - **No structural prevention** → agent follows instructions ~60% of the time. 40% of dangerous operations succeed.
> - **No teaching** → agent doesn't know the rules. Every session starts from zero methodology.
> - **No review** → agent makes subjective quality decisions unchecked. Confident-but-wrong artifacts accumulate.
> - **No depth verification** → hollow synthesis passes validation (format correct, substance missing). Evolution pipeline starves.
> - **No stage gates** → work skips stages. Artifacts produced out of order. False readiness claims.

## Open Questions

> [!question] **How should enforcement level be measured quantitatively?**
> What percentage of quality rules currently live at Level 0 (hope) vs Level 3 (deterministic)? A metric like "enforcement maturity score = weighted average across levels" could track progress. (Requires: cataloging all rules with their current enforcement level)

> [!question] **Can the 3-strike pattern apply to wiki quality?**
> Three thin pages in a row → mandatory depth review. Three validation failures → auto-escalate to guided mode. Would this reduce systemic quality decay or add bureaucratic overhead? (Requires: implementing and testing on a real ingestion batch)

> [!question] **What is the empirical rework rate across ingestion modes?**
> Guided mode has the highest prevention cost. Auto mode has the highest rework risk. Smart mode balances. But what are the ACTUAL rework rates? (Requires: tracking rework across 50+ ingestion tasks)

## Relationships

- BUILDS ON: [[Harness Engineering]]
- BUILDS ON: [[Immune System Rules]]
- BUILDS ON: [[Rework Prevention]]
- BUILDS ON: [[Deterministic Shell, LLM Core]]
- BUILDS ON: [[Never Synthesize from Descriptions Alone]]
- BUILDS ON: [[Never Skip Stages Even When Told to Continue]]
- BUILDS ON: [[Shallow Ingestion Is Systemic, Not Isolated]]
- BUILDS ON: [[Infrastructure Must Be Reproducible, Not Manual]]
- BUILDS ON: [[The Agent Must Practice What It Documents]]
- BUILDS ON: [[Models Are Built in Layers, Not All at Once]]
- RELATES TO: [[Model: Methodology]]
- RELATES TO: [[Model: Claude Code]]
- RELATES TO: [[Model: Automation and Pipelines]]
- RELATES TO: [[Skyscraper, Pyramid, Mountain]]

## Backlinks

[[Harness Engineering]]
[[Immune System Rules]]
[[Rework Prevention]]
[[Deterministic Shell, LLM Core]]
[[Never Synthesize from Descriptions Alone]]
[[Never Skip Stages Even When Told to Continue]]
[[Shallow Ingestion Is Systemic, Not Isolated]]
[[Infrastructure Must Be Reproducible, Not Manual]]
[[The Agent Must Practice What It Documents]]
[[Models Are Built in Layers, Not All at Once]]
[[Model: Methodology]]
[[Model: Claude Code]]
[[Model: Automation and Pipelines]]
[[Skyscraper, Pyramid, Mountain]]
[[Model: Design.md and IaC]]
[[Model: Local AI ($0 Target)]]
[[Model: SFIF and Architecture]]
[[Quality Standards — What Good Failure Prevention Looks Like]]
