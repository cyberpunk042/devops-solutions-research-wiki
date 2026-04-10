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

Quality and failure prevention for AI agents is not a set of best practices — it is a system with three enforcement layers (structural prevention, teaching, review), five codified failure lessons, and deterministic mechanisms that cannot be bypassed by prompt engineering. The model synthesizes evidence from four domains: harness engineering (13 guardrail rules enforced via hooks), OpenFleet's immune system (24 rules from 16 post-mortems), rework prevention economics (rework is multiplicative — source unverified, the principle is sound but the specific multiplier needs measurement), and this wiki's own operational failures. The central thesis: quality enforcement must live in code that runs at execution time, not in documentation that the agent may or may not consult.

## Key Insights

- **Three-layer defense is the minimum viable quality architecture.** Structural prevention (hooks, doctor.py) blocks bad actions before they execute. Teaching (CLAUDE.md, skills, memory) shapes behavior before the action is attempted. Review (human gates at stage transitions) catches what automation misses. Any single layer alone is insufficient — hooks without teaching produce correct-but-misaligned work; teaching without hooks produces well-intentioned failures; review without either produces exhausted humans.

- **Failure lessons must be codified, not just remembered.** Each of the five wiki failure lessons maps to a concrete enforcement mechanism. A lesson that exists only as documentation is a suggestion. A lesson encoded in CLAUDE.md, enforced by a hook, and checked by the post-chain is a rule.

- **Rework is multiplicative, not additive.** Rework is multiplicative — redoing work requires reverting, re-planning, re-executing, and re-verifying, compounding cost beyond the original task. In a multi-agent fleet with dependencies, one bad dispatch cascades into downstream reworks. The specific cost multiplier and rework rate percentages are estimates that need measurement from real project data, but the principle that prevention is cheaper than rework is structurally sound.

- **Depth verification is the single highest-leverage quality rule.** Reading the thing itself rather than a description of the thing prevents the most common class of hollow synthesis. The 0.25 ratio rule (at least 25% of ingestion time on primary sources) is a measurable proxy for depth.

- **Methodology is the structural embodiment of failure prevention.** Stage gates, quality gates per stage, and "do not advance until the gate passes" are not process overhead — they are the operational form of every lesson in this model.

## Deep Analysis

### The Three-Layer Defense

The quality system operates at three distinct layers, each catching a different failure class. This architecture emerged from OpenFleet's anti-corruption design, where no single enforcement mechanism proved sufficient against the full range of agent failure modes.

**Layer 1 — Structural Prevention (Hooks and Deterministic Guards)**

Structural prevention blocks bad actions at execution time through code that runs before, during, or after tool use. The agent cannot bypass these mechanisms through reasoning, confidence, or prompt injection.

Implementations across the ecosystem:
- **[[Harness Engineering]]**: 13 TypeScript guardrail rules (R01-R13) enforced via Claude Code hooks. Denial rules block sudo, .env writes, force-push. Query rules flag out-of-scope writes. Security rules prevent --no-verify and direct main pushes. Post-execution checks warn on assertion tampering.
- **[[Immune System Rules]]**: 24 Python rules in doctor.py running at step 6 of the 9-step orchestrator cycle. Zero LLM calls — pure state evaluation. Five rule categories: liveness, loop detection, state integrity, behavioral security, resource exhaustion.
- **[[Deterministic Shell, LLM Core]]**: The architectural pattern. The LLM operates only in the execution phase, surrounded on both sides by deterministic Python. The shell enforces invariants that cannot be social-engineered.

The critical property: structural prevention is deterministic, fast (microseconds per check), cheap (no token cost), and auditable (no inference variability). An LLM-based quality gate would be unreliable by design.

**Layer 2 — Teaching (CLAUDE.md, Skills, Memory)**

Teaching shapes agent behavior before the action is considered. Unlike structural prevention, teaching can be ignored — but well-designed teaching reduces the frequency of hook violations, making the structural layer a backstop rather than the primary defense.

The teaching stack:
- **CLAUDE.md**: Project-level rules loaded into every session. Contains quality gates, ingestion modes, relationship conventions, post-chain requirements. This is the agent's methodology, not just documentation for humans.
- **Skills**: Domain-specific behavior loaded contextually. The wiki-agent skill encodes ingestion methodology. The evolve skill encodes maturity promotion rules. Skills are teaching that activates only when relevant.
- **Memory**: Cross-session persistence of user directives and operational lessons. "Never synthesize from descriptions alone" lives in memory so it survives session boundaries.

**Layer 3 — Review (Human Gates at Stage Transitions)**

Review is the final layer for decisions that automation cannot evaluate: Does this synthesis actually capture the source's meaning? Is this architectural decision the right one for this context? Does this evolved page deserve maturity promotion?

Review gates in the wiki:
- Guided ingestion mode: human approves extraction plan before synthesis begins
- Smart mode escalation: auto-processing stops and requests human input when it encounters new domains, contradictions, or ambiguity
- Maturity promotion: seed pages require review before advancing to growing

The three layers interact: structural prevention catches deterministic violations, teaching reduces the violation rate, and review handles the irreducibly subjective decisions.

### The Five Failure Lessons

Each lesson was extracted from a real operational failure in building this wiki. Each maps to a specific enforcement mechanism that prevents recurrence.

**1. Never Synthesize from Descriptions Alone**

The failure: The agent ingested a curated list (awesome-design-md), synthesized a page claiming to understand the DESIGN.md pattern, but had never opened a single real DESIGN.md file. The synthesis was confident-sounding and factually hollow.

The principle: Layer 0 (description of a thing) is not Layer 1 (an instance of the thing). Metadata about data is not data. The minimum bar for synthesis is examining at least one real instance.

Enforcement: CLAUDE.md requires source provenance. The wiki-agent skill encodes depth verification. Memory carries the directive "always examine a real instance before synthesizing." The 0.25 ratio rule — at least 25% of ingestion effort must be on primary sources, not descriptions of sources — provides a measurable threshold. See [[Never Synthesize from Descriptions Alone]].

**2. Never Skip Stages Even When Told to Continue**

The failure: The agent treated "continue" as permission to skip validation, post-chain steps, and review gates. Quality degraded silently as the wiki accumulated unvalidated pages.

The principle: Forward-pushing instructions ("continue," "keep going," "next") do not override hard quality constraints. The agent must interpret scope, not just direction.

Enforcement: CLAUDE.md defines the post-ingestion chain as mandatory. The post-chain runs validation with exit-code enforcement — errors block completion. "Continue" means "continue within the methodology," not "continue and skip the methodology." See [[Never Skip Stages Even When Told to Continue]].

**3. Shallow Ingestion Is Systemic, Not Isolated**

The failure: Thin pages accumulated — pages with minimal summaries, sparse relationships, and no deep analysis. Each individual page seemed like a minor shortcut. The systemic effect was that the evolution pipeline had no high-quality candidates to promote.

The principle: Quality gates that are soft (advisory) degrade the entire system, not just the individual artifact. One skipped gate creates systematic downstream degradation because later processes depend on the quality of earlier outputs.

Enforcement: Validation requires minimum 30-word summaries, at least 1 relationship, source provenance, and no >70% concept overlap. The lint tool reports summary quality and relationship density. See [[Shallow Ingestion Is Systemic, Not Isolated]].

**4. Infrastructure Must Be Reproducible, Not Manual**

The failure: Setup steps, service deployments, and configuration were done manually. They silently diverged across environments and sessions. The agent would create a systemd service by hand, then forget how it was configured.

The principle: Any infrastructure step not encoded in a script, template, or IaC file is a quality gap. Manual steps are undocumented, unrepeatable, and invisible to auditing.

Enforcement: `python -m tools.setup` handles all environment setup. `--services` deploys sync and watcher daemons reproducibly. No manual systemd/cron creation — everything flows through the tooling. See [[Infrastructure Must Be Reproducible, Not Manual]].

**5. The Agent Must Practice What It Documents**

The failure: The wiki documented methodology extensively — stage gates, brainstorm-before-spec, multi-pass ingestion — but the agent building the wiki skipped those very rules. The documentation was correct; the behavior was not.

The principle: Methodology is worthless if the system that documents it does not enforce it on itself. The gap between "what we say" and "what we do" is the most dangerous form of technical debt because it is invisible in the artifacts.

Enforcement: CLAUDE.md contains the rules the agent follows, not just the rules it documents. The user directive "START BY UPDATING THE CLAUDE AND RULES SO THAT YOU YOURSELF START FOLLOWING THE RULES" is codified in memory. See [[The Agent Must Practice What It Documents]].

### The Harness Engineering System

[[Harness Engineering]] is the coordinated enforcement architecture that turns individual quality rules into a system. The components:

**The 13 Guardrail Rules (R01-R13)**

Implemented as TypeScript hooks that intercept Claude Code tool calls:
- **Denial rules**: Block sudo execution, .env file writes, git force-push — actions that are never acceptable regardless of context
- **Query rules**: Flag writes to files outside the declared scope — actions that might be acceptable but require explicit confirmation
- **Security rules**: Prevent --no-verify flag usage, direct pushes to main — actions that bypass other safety mechanisms
- **Post-execution checks**: Warn when test assertions are weakened or removed — actions that erode the verification layer

**The 5-Verb Workflow**

Setup → Plan → Work → Review → Release. This is not a suggestion — the harness enforces verb ordering. The Review verb must execute before Release is permitted. This maps to the universal pattern across the ecosystem: superpowers (brainstorm → plan → execute → verify), OpenFleet (task creation → dispatch → execution → review → completion), and the wiki's own pipeline (extract → analyze → synthesize → write → integrate).

**Enforcement Level Hierarchy**

- Level 0: CLAUDE.md instructions (hope-based — the agent may or may not follow them)
- Level 1: Skills and memory (contextual — loaded when relevant, consulted when the agent remembers to)
- Level 2: Pre/post hooks (triggered — run automatically on matching tool calls)
- Level 3: Runtime guardrails (blocking — deterministic code that prevents the action)
- Level 4: Deterministic orchestration (structural — the agent never has the option to choose wrong)

Each level is strictly stronger than the one below it. The quality system's maturity can be measured by how much enforcement has migrated upward from Level 0 toward Level 4.

### The Immune System Rules

[[Immune System Rules]] represent the production-grade implementation of structural prevention, extracted from real failures rather than theoretical risk analysis.

**Origin**: 24 rules from 16 post-mortems and agent death analyses in the devops-control-plane project. Each rule traces to a specific incident where an agent failed in a way that was preventable.

**The 5 Rule Categories**:
1. **Liveness** — Detect agents alive in state but dead in practice (heartbeat timeout, stale session ID, stuck execution)
2. **Loop detection** — Detect runaway cycles (retry storms, circular dependencies, dispatch-without-completion loops)
3. **State integrity** — Detect impossible state combinations (parent complete but children pending, review state with no reviewer, blocked with no blocker)
4. **Behavioral security** — Detect permission and scope violations (out-of-scope path writes, cost spikes, capability acquisition beyond spec)
5. **Resource exhaustion** — Detect degraded conditions (circuit breaker open, external service unresponsive, disk/memory pressure)

**The 3-Strike Pattern**: A single violation does not trigger action. Three violations within a window trigger quarantine. This tolerates transient anomalies (network blips, brief CPU spikes) while catching persistent failures. The strike window prevents both false positives (killing healthy agents) and silent degradation (ignoring real problems).

**Integration Point**: doctor.py runs at step 6 of the 12-step orchestrator cycle — after security scan (step 5), before dispatch (step 9). A flagged task accumulates a strike before it can ever reach dispatch. This is preemptive immune response, not reactive incident handling.

### Rework Prevention Economics

[[Rework Prevention]] provides the cost model that justifies every quality gate in the system.

**The Compound Cost Formula**:
```
Single rework cycle = T + R + D + P + T + V ≈ 2.5T to 3.5T
  where T = original task, R = revert, D = diagnosis,
        P = re-plan, T = re-execute, V = re-verify

Cascade rework (N dependent tasks) = 2.5T + Σ(downstream rework costs)
  A fleet with 5 dependent tasks: one bad dispatch corrupts the sprint
```

**Prevention Investment**: 0.2T to 0.4T per task (spec review, pre-checks, Planner+Critic).

**Break-Even Threshold**: Prevention is net-positive if it reduces rework probability by more than 12%. Real rework rates without explicit gates run 20-40% on complex tasks. The ROI is unambiguous.

**Why This Matters for the Wiki**: The wiki's three ingestion modes map directly to the prevention investment curve:
- **Guided mode** = maximum prevention (human approves every step) — highest cost, lowest rework
- **Smart mode** = risk-calibrated prevention (auto when confident, escalate when not) — balanced
- **Auto mode** = throughput-first (process without stopping) — lowest cost, highest rework risk

### The Depth Verification System

Depth verification is the operational rule that prevents the most common quality failure: synthesizing knowledge from secondhand descriptions rather than primary sources.

**The Core Rule**: Read the thing, not the description of the thing. A README that lists 58 DESIGN.md files is not the same as reading a DESIGN.md file. An API spec is not the same as a real request/response pair. A conference talk describing a methodology is not the methodology's actual artifacts.

**The Layer Model**:
- Layer 0: Description of the thing (README, catalog, index)
- Layer 1: A real instance of the thing (actual file, actual output, actual config)
- Layer 2: Multiple instances compared (pattern extraction from N real examples)

Minimum bar for synthesis: Layer 1. Synthesizing from Layer 0 alone produces confident-sounding pages that are factually hollow.

**The 0.25 Ratio Rule**: At least 25% of ingestion time must be spent on primary sources. This is a measurable proxy for depth that can be tracked and enforced.

**Enforcement Stack**: CLAUDE.md (quality gates section), wiki-agent skill (ingestion methodology), memory (cross-session directive persistence). The rule survives session boundaries because it is encoded at all three teaching levels.

### The Methodology Connection

The model's seven components are not independent — they are unified by the stage-gate methodology that structures all work in the wiki.

**Stage gates are the structural embodiment of failure prevention.** Each stage (extract → analyze → synthesize → write → integrate) has a quality gate. The gate defines what "done" means for that stage. Work does not advance until the gate passes. This is not process overhead — it is the operational form of every lesson in this model:

- "Never synthesize from descriptions alone" = the extraction gate requires primary source examination
- "Never skip stages" = gates are mandatory, not advisory
- "Shallow ingestion is systemic" = gate criteria enforce minimum depth
- "Infrastructure must be reproducible" = the post-chain automates gate enforcement
- "Practice what you document" = CLAUDE.md contains the gates the agent must pass

The post-ingestion chain (`python3 -m tools.pipeline post`) is the automated enforcement of stage gates: rebuild indexes, regenerate manifest, validate all pages (errors block), regenerate wikilinks, run lint, rebuild layer indexes. Six steps, all mandatory, all deterministic. This is structural prevention applied to the wiki's own methodology.

## Open Questions

- How should the enforcement level be measured quantitatively? What percentage of quality rules currently live at Level 0 (hope) vs Level 3+ (deterministic)?
- Can the 3-strike pattern from doctor.py be applied to wiki quality? (e.g., three thin pages in a row triggers mandatory depth review)
- What is the empirical rework rate for wiki ingestion across the three modes? Is guided mode's overhead justified by the data?
- Should depth verification have a hook-level enforcement (block page creation if no primary source was read) or is teaching-level sufficient?

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
- RELATES TO: [[Model: Automation + Pipelines]]
- RELATES TO: [[Model: SFIF + Architecture]]
- FEEDS INTO: [[Model: Local AI ($0 Target)]]
- FEEDS INTO: [[Model: Design.md + IaC]]

## Backlinks

[[Harness Engineering]]
[[Immune System Rules]]
[[Rework Prevention]]
[[[[Deterministic Shell]]
[[LLM Core]]]]
[[Never Synthesize from Descriptions Alone]]
[[Never Skip Stages Even When Told to Continue]]
[[[[Shallow Ingestion Is Systemic]]
[[Not Isolated]]]]
[[[[Infrastructure Must Be Reproducible]]
[[Not Manual]]]]
[[The Agent Must Practice What It Documents]]
[[Model: Automation + Pipelines]]
[[Model: SFIF + Architecture]]
[[Model: Local AI ($0 Target)]]
[[Model: Design.md + IaC]]
[[Model: Automation and Pipelines]]
[[Model: Design.md and IaC]]
[[Model: SFIF and Architecture]]
