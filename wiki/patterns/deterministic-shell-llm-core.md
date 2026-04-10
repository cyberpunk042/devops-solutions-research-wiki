---
title: "Deterministic Shell, LLM Core"
type: pattern
domain: ai-agents
layer: 5
status: synthesized
confidence: high
maturity: growing
derived_from:
  - "OpenFleet"
  - "Harness Engineering"
  - "AICP"
instances:
  - page: "OpenFleet"
    context: "Deterministic Python orchestrator (zero LLM calls, pure state machine, 30-second cycle) surrounds 10 LLM-powered agents. The orchestrator handles dispatch, security scanning, anomaly detection, and budget gating; agents handle reasoning, synthesis, and code generation."
  - page: "AICP"
    context: "Python complexity router and circuit breaker (deterministic) selects which LLM backend handles each task. The router evaluates keywords, history depth, and profile thresholds; the selected LLM backend (LocalAI or Claude) handles the actual reasoning."
  - page: "Research Pipeline Orchestration"
    context: "Python pipeline tools (tools/pipeline.py, tools/validate.py, tools/manifest.py) form the deterministic shell: they orchestrate, validate, and route. Claude Code generates page content and performs synthesis — the creative and reasoning core."
  - page: "Harness Engineering"
    context: "13 TypeScript guardrail rules (R01-R13) form the deterministic enforcement shell: they block dangerous operations, query out-of-scope writes, and enforce the Plan→Work→Review cycle at execution time. The LLM (Claude) executes within the guardrail boundaries."
created: 2026-04-08
updated: 2026-04-10
sources:
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
  - id: src-aicp-local
    type: documentation
    file: ../devops-expert-local-ai/CLAUDE.md
    title: "AICP — Local Project Documentation"
tags: [deterministic, orchestration, llm-core, shell-pattern, guardrails, harness, openfleet, aicp, reliability, separation-of-concerns, agent-architecture]
---

# Deterministic Shell, LLM Core

## Summary

Deterministic Shell, LLM Core is the architectural pattern of wrapping LLM inference inside a deterministic orchestration layer that handles all operational mechanics — routing, validation, scheduling, security scanning, budget gating — while delegating only reasoning, synthesis, and generation to the LLM. The shell is predictable, auditable, and cheap to operate; the core is creative, context-sensitive, and expensive to operate. The pattern's value is that it constrains the LLM to the tasks where non-determinism is acceptable and beneficial, while keeping everything that must be reliable outside the LLM's execution context.

## Pattern Description

> [!abstract] Two execution domains sharing a boundary
>
> | Domain | Characteristics | Handles |
> |--------|----------------|---------|
> | **Deterministic Shell** | Zero LLM, explicit state, unit-testable, auditable, same inputs → same outputs | Routing, validation, scheduling, security, budget gating, failure handling |
> | **LLM Core** | Inference, context-dependent, quality assessed by humans/validators | Synthesis, reasoning, generation, creative tasks requiring model capability |

The boundary between shell and core is the pattern's critical design decision. Too much in the LLM core produces a system that is expensive, slow, and unreliable for operational tasks — the LLM is being asked to do bookkeeping it should not do. Too much in the deterministic shell produces a system that is brittle and rule-bound, unable to handle novel cases that require judgment. The correct boundary places in the shell everything that can be deterministically specified (validation rules, routing criteria, scheduling logic, safety checks) and in the core everything that genuinely requires model intelligence.

The Harness Engineering page frames this as a hierarchy of enforcement levels: Level 0 is prompt guidance (LLM compliance, unreliable); Level 1 is status monitoring (human intervention required); Level 2 is workflow orchestration (skill-enforced sequencing); Level 3 is runtime guardrails (execution-time blocking); Level 4 is deterministic orchestration (zero-LLM state machine). The Deterministic Shell, LLM Core pattern operates at Levels 3–4: the shell enforces at execution time or through a state machine; the core operates at the LLM execution level.

The pattern requires explicit boundary documentation. In OpenFleet, the boundary is documented in the architecture description: "Deterministic brain, not LLM-driven: The orchestrator runs every 30 seconds with zero LLM calls." In AICP, the boundary is the complexity scorer: "The router evaluates complexity signals automatically and applies profile-based thresholds consistently — the routing decision is deterministic." In the wiki pipeline, the boundary is the post-chain: `tools.validate`, `tools.manifest`, `tools.lint`, `tools.obsidian` are all deterministic Python; Claude Code generates the page content that these tools then validate.

The shell's validation step is what makes the boundary trustworthy. Without validation, the deterministic shell is just an orchestrator — it routes tasks to the LLM but accepts whatever the LLM produces. With validation (schema checking, quality scoring, contradiction detection), the shell can catch LLM output that fails to meet defined quality criteria and either reject it, flag it for human review, or trigger a retry. The wiki's `tools.validate` returning exit code 1 on errors is the concrete implementation of this validation gate.

## Instances

### OpenFleet — Deterministic Orchestrator with LLM Agents

The most mechanically pure instantiation in the ecosystem. The 9-step orchestrator cycle runs on a 30-second interval using zero LLM calls. Pure Python state evaluation handles: storm monitoring, gateway duplication checking, fleet mode gating, context pre-computation (embedding full per-agent data to disk), behavioral security scanning, immune system checks (3-strike rule, anomaly detection), review approval enforcement, and task dispatch (max 2 per cycle). All of this is the deterministic shell.

The LLM core consists of the 10 specialized agents (fleet-ops, project-manager, architect, software-engineer, qa-engineer, etc.) who execute within the boundaries the shell enforces. An agent cannot receive a task that has not passed the security scan and doctor checks — the shell gates access to the core. The agent cannot exceed the budget gate — the shell enforces the cost boundary. The seven-layer architecture explicitly names this separation: L1 Deterministic Brain governs the shell; L3 Agent Execution is the LLM core.

The pattern's robustness is demonstrated by the documented failure mode: when LocalAI and LightRAG are both down, "the orchestrator's 12 deterministic steps continue unaffected because they make zero LLM calls." The shell degrades gracefully without the core; the core is silently unavailable when its services are down. The two execution domains fail independently.

### AICP — Complexity Router as Deterministic Shell

AICP implements the pattern at the request level rather than the orchestration level. For every incoming task, the deterministic router (Python, zero LLM inference) evaluates: task complexity score (keyword analysis, history depth, context size), circuit breaker state per backend (CLOSED/OPEN/HALF_OPEN), active profile thresholds, and failover chain configuration. This evaluation produces a routing decision: LocalAI (free, fast) or Claude (powerful, paid).

The selected LLM backend is the core. AICP's shell handles all the mechanics of making the right model available for the right task; the model itself handles the reasoning. The guardrails pipeline (path protection, response filtering, pre/post execution checks) is additional shell functionality that operates on the model's output — the shell validates that the core's outputs do not contain leaked secrets, forbidden paths, or unsafe operations before delivering them.

The 5-stage LocalAI independence roadmap is a planned shift of where the shell/core boundary sits. At Stage 5 (near-independent operation), more complex tasks will be handled by higher-capability local models, moving the boundary such that the Claude core handles a smaller fraction of tasks. The shell's routing logic is what operationalizes this boundary shift — no code changes to the core are needed, only profile threshold adjustments in the shell.

### Wiki Pipeline — Python Tools as Deterministic Shell

The research wiki's pipeline implements the pattern at the knowledge management level. The deterministic shell consists of all the Python pipeline tools: `tools/pipeline.py` (orchestration and routing), `tools/validate.py` (schema validation, hard gate), `tools/manifest.py` (index regeneration), `tools/lint.py` (quality checks), `tools/obsidian.py` (wikilink regeneration), `tools/watcher.py` (change detection and post-chain trigger). None of these make LLM calls. They operate on file state, YAML schema, and relationship graphs deterministically.

The LLM core is Claude Code, which generates page content (synthesis, deep analysis, relationships), performs cross-reference analysis, and executes the evolution pipeline. The `pipeline post` command is the shell's validation pass on the core's outputs: it runs all six deterministic steps after every LLM-generated write to catch any output that violates schema, creates orphans, or fails lint checks.

### Harness Engineering — TypeScript Rules as Runtime Shell

The claude-code-harness project implements the pattern at the tool execution level. The 13 TypeScript guardrail rules (R01-R13) form the deterministic shell: they execute as hooks at tool call time, blocking (denial rules), flagging (query rules), or checking post-execution (security rules). The rules are TypeScript functions, not prompts — they execute deterministically regardless of what the LLM is trying to do.

The LLM (Claude) is the core: it executes within the guardrail boundaries. It can generate code, modify files, run commands — but the shell blocks `sudo`, prevents `.env` writes, enforces branch protection, and catches assertion tampering. The Breezing mode's Planner + Critic roles add an inner deterministic conversation structure (shell-level workflow) around the LLM's creative execution (core-level generation).

## When To Apply

Apply Deterministic Shell, LLM Core when:

- **Operational reliability is non-negotiable**: systems that must operate continuously (orchestrators, watcher daemons, routing layers) cannot depend on LLM inference in their critical path. LLM calls add latency, cost, and non-determinism to every operation. Placing these operations in a deterministic shell preserves reliability independent of model availability or quality.
- **Security and safety must be mechanically enforced**: prompt-level safety instructions can be social-engineered or ignored. Shell-level enforcement (guardrails, path protection, permission gating) executes independently of model behavior. The Immune System Rules page documents this explicitly: "A deterministic security scan cannot be social-engineered via a crafted task description. An LLM-based security layer can be prompted around."
- **Cost must be controlled at the infrastructure level**: routing budget gates and complexity scoring belong in the shell, not in a prompt. When cost control is enforced by the shell (circuit breakers, profile thresholds, budget gating), it is reliable regardless of what the LLM generates. When cost control depends on the LLM following budget instructions, it is advisory.
- **Autonomous operation without human supervision**: orchestrators and watcher daemons must operate correctly when no human is watching. Deterministic shell logic is auditable and testable; LLM-driven orchestration is not. OpenFleet's entire design philosophy — "the orchestrator runs with zero LLM calls" — exists to enable reliable autonomous operation.
- **The validation boundary can be made explicit**: the shell's value scales with how precisely the boundary between deterministic-acceptable and LLM-required tasks can be specified. If the domain does not permit this specification, the shell/core boundary cannot be cleanly drawn.

## When Not To

Avoid or over-engineering Deterministic Shell, LLM Core when:

- **The system is primarily exploratory**: interactive research, prototyping, and conversational Q&A do not benefit from a deterministic shell. The human IS the shell in these contexts — they evaluate outputs, reject poor results, and guide the next prompt. Adding a formal shell layer adds overhead without reliability benefits.
- **The task set is too diverse to specify shell rules**: if the range of operations is broad and novel (general-purpose assistants, open-ended research agents), the cost of specifying comprehensive shell rules exceeds their value. Shell rules work best in bounded task domains with known failure modes.
- **The LLM core's output is not validatable**: if there is no downstream validation that can distinguish correct from incorrect LLM output, the shell's validation gate cannot be closed. The pattern requires that the shell can assess core output quality — either via schema validation, deterministic tests, or a human review gate.
- **Premature optimization**: building a sophisticated deterministic shell before the LLM core's task boundaries are understood wastes engineering effort. Start with minimal shell (basic validation) and grow the shell as failure modes are discovered empirically. OpenFleet's 24 rules were derived from 16 post-mortems — the shell grew in response to observed failures, not from upfront design.

## Relationships

- DERIVED FROM: [[OpenFleet]]
- DERIVED FROM: [[Harness Engineering]]
- DERIVED FROM: [[AICP]]
- RELATES TO: [[Plan Execute Review Cycle]]
- RELATES TO: [[Immune System Rules]]
- RELATES TO: [[Research Pipeline Orchestration]]
- ENABLES: [[Infrastructure as Code Patterns]]
- RELATES TO: [[Agent Orchestration Patterns]]
- BUILDS ON: [[Claude Code Best Practices]]
- FEEDS INTO: [[Gateway-Centric Routing]]

## Backlinks

[[OpenFleet]]
[[Harness Engineering]]
[[AICP]]
[[Plan Execute Review Cycle]]
[[Immune System Rules]]
[[Research Pipeline Orchestration]]
[[Infrastructure as Code Patterns]]
[[Agent Orchestration Patterns]]
[[Claude Code Best Practices]]
[[Gateway-Centric Routing]]
[[Lesson: Agent Orchestration Is the Highest-Connected Concept in the Wiki]]
[[Model: Ecosystem Architecture]]
[[Model: Quality and Failure Prevention]]
[[Scaffold → Foundation → Infrastructure → Features]]
[[Skyscraper, Pyramid, Mountain]]
