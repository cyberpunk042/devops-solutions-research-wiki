---
title: "Model: Local AI ($0 Target)"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [model, concept, spine, local-ai, aicp, zero-cost, backend-routing, complexity-scoring, vram]
---

# Model: Local AI ($0 Target)

## Summary

The Local AI model describes the ecosystem's strategy for reducing Claude API costs toward zero by routing routine operations to locally-run quantized models. [[AICP]] (AI Control Platform) is the orchestration layer: it scores task complexity, checks circuit breaker states, and routes deterministically-validatable tasks (status checks, index rebuilds, manifest regeneration, lint) to LocalAI, while reserving Claude for complex reasoning (architecture decisions, deep synthesis, security review). The current hardware baseline (8GB VRAM) supports Qwen3 and Gemma4 model families with Stages 1 and 2 of the 5-stage LocalAI independence roadmap complete. Stage 3 (progressive offload targeting 80%+ Claude token reduction) is blocked pending the 8GB → 19GB VRAM hardware upgrade, but the routing infrastructure is already operational.

## Key Insights

- **The $0 target is achievable for routine operations, not all operations.** The routing split is not 100% local — it is local for mechanical tasks and cloud for reasoning tasks. The 80% Claude token reduction target means ~80% of invocations are free; the remaining ~20% (synthesis, evolution, architecture) still use Claude. This is the sustainable equilibrium, not a transitional phase.

- **AICP's complexity scorer is the production routing mechanism.** Every request is scored on task signals: deterministic output? validatable by downstream tools? short context window sufficient? If yes → LocalAI. If no → Claude. The thresholds are profile-configurable, not hardcoded. Profiles like `fleet-light` and `offline` push more to local; `thorough` and `code-review` push more to cloud.

- **Circuit breakers provide reliability without compromising the model.** Each backend (LocalAI, Claude) runs an independent circuit breaker in three states: CLOSED (healthy, route freely), OPEN (failed, route away), HALF_OPEN (recovering, probe cautiously). This means a LocalAI crash does not take down the ecosystem — requests fail over to Claude automatically and circuit closes again when LocalAI recovers.

- **9 loaded models cover distinct capability tiers.** The Qwen3 family (8B, 4B, 30B MoE, fast variant) covers most text tasks. The Gemma4 family (e2b, e4b, 26B MoE) adds multimodal and stronger agentic tool-calling — particularly Gemma 4 E4B's breakthrough reliable multi-step tool execution on 9.6GB. Legacy models (hermes, codellama) cover specialized domains. Embedding models (nomic-embed, bge-reranker) enable semantic search without cloud calls.

- **VRAM is the primary physical constraint.** The Gemma 4 26B model requires 18GB VRAM minimum. The current 8GB baseline makes it unrunnable. The planned upgrade to 19GB unlocks Stage 3: running complex agent reasoning locally, which is the step that moves the routing split from ~40% local to ~80% local.

- **Gemma 4 E4B's tool-calling reliability is the key capability breakthrough.** Prior local models failed unpredictably on multi-step agentic operations (tool calls, structured output, sequential reasoning). Gemma 4 E4B at 9.6GB changed this. It reliably executes multi-step tool sequences — meaning it can run the post-chain, invoke lint, scaffold pages, and update manifests without a human in the loop.

## Deep Analysis

### The 5-Stage LocalAI Independence Roadmap

[[AICP]] defines a concrete roadmap with current status:

> [!info] Roadmap status
>
> | Stage | Goal | Status |
> |-------|------|--------|
> | 1 | Make LocalAI functional — models loaded, GPU acceleration, health endpoint | Complete |
> | 2 | Route simple operations to LocalAI — complexity scorer implemented | Complete |
> | 3 | Progressive offload — heartbeats, reviews, status checks, index rebuilds | **Blocked: needs 19GB VRAM** |
> | 4 | Reliability and failover — circuit breakers tuned, DLQ implemented | Planned |
> | 5 | Near-independent operation — 80%+ Claude token reduction achieved | Target state |

Stage 1 and 2 are done. Stage 3 is the hardware-blocked inflection point. Until then, the system routes ~40% of operations locally; after the VRAM upgrade, target is ~80%.

### The Routing Decision Framework

The [[Decision: Local Model vs Cloud API for Routine Operations]] formalizes the routing logic:

> [!tip] Route to LocalAI when:
> - Output is deterministically validatable (e.g., `tools.validate` will catch errors)
> - Task fits in a short context window (4K-8K tokens)
> - Task is mechanical and repeatable (manifest regeneration, lint, scaffold generation)
> - Latency matters more than quality (heartbeats, status polling)
> - Cost matters (batch operations over many wiki pages)

> [!warning] Route to Claude when:
> - Task requires novel cross-domain synthesis
> - Output is not externally validatable (architectural decisions, security review)
> - Context window is large (full codebase analysis, deep-dive evolution)
> - The task is a one-off judgment call rather than a routine operation
> - Stakes are high and failure is expensive

**The quality threshold is per-profile, not global.** The `fleet-light` profile aggressively pushes to local (threshold 0.3); `code-review` pulls toward cloud (threshold 0.8). A wiki post-chain run uses `fleet-light`; an evolution synthesis session uses `thorough`.

### The Backend Architecture

AICP's routing stack:

```
Request → Complexity Scorer → Profile Threshold Check
    ↓ below threshold           ↓ above threshold
  LocalAI Circuit Breaker     Claude Circuit Breaker
    ↓ CLOSED                    ↓ CLOSED
  LocalAI (free, fast)         Claude (paid, powerful)
    ↓ OPEN (circuit tripped)
  Fallback to Claude
```

The circuit breaker prevents cascading failures. If LocalAI becomes unavailable (model loading, GPU OOM, network issue on the OpenAI-compatible endpoint), the circuit trips, and all traffic flows to Claude until LocalAI recovers. This keeps the ecosystem operational even when the local backend is unhealthy.

### The 9 Loaded Models and Their Roles

The current model inventory reflects deliberate capability coverage:

- **Qwen3-8B** — General text tasks, fast inference, default routing target
- **Qwen3-4B** — Ultra-fast, for simple status checks and heartbeats
- **Qwen3-30B MoE** — Higher-quality reasoning locally, for tasks just below the cloud threshold
- **Qwen3-fast** — Optimized for latency-sensitive operations
- **Gemma4-E2B** — Lightweight multimodal
- **Gemma4-E4B** — Reliable multi-step tool calling (the Stage 3 unlock)
- **Gemma4-26B MoE** — Complex agent reasoning locally (blocked on 19GB VRAM)
- **Hermes-3B / CodeLlama** — Specialized legacy models
- **nomic-embed + bge-reranker** — Semantic search and reranking without cloud

### What Remains Cloud-Only

After Stage 5, these operations will still route to Claude:
- First-pass synthesis of novel concepts with no existing wiki coverage
- Cross-domain pattern recognition requiring >100K token context
- Security review of system architecture changes
- Evolution of seed pages to canonical status (judgment-heavy)
- Resolving contradictions between existing pages

The $0 target is for routine wiki maintenance and fleet operations, not for knowledge creation. Knowledge creation remains Claude's domain; maintenance becomes local's domain.

### Hardware Dependency and the Upgrade Path

The VRAM constraint is not an architectural flaw — it is a deliberate design choice to build the routing infrastructure first and scale the hardware second. AICP Stages 1 and 2 were built on 8GB VRAM intentionally, to validate the routing model before investing in hardware. The upgrade from 8GB to 19GB VRAM is the single biggest capability unlock in the roadmap, enabling:

- Gemma4-26B MoE for complex local reasoning
- Running two medium models simultaneously (embed + generate)
- Larger context windows for multi-file local analysis
- Stage 3–4 progressive offload

### Key Pages

| Page | Layer | Role in the model |
|------|-------|-------------------|
| [[AICP]] | concept | The orchestration and routing platform |
| [[Local LLM Quantization]] | concept | How large models run on consumer hardware |
| [[Decision: Local Model vs Cloud API for Routine Operations]] | decision | The formal routing decision framework |
| [[Gateway-Centric Routing]] | pattern | Architectural pattern for traffic routing |
| [[Deterministic Shell, LLM Core]] | pattern | Wrapper pattern keeping LLM inside deterministic orchestration |

### Lessons Learned

| Lesson | What was learned |
|--------|-----------------|
| Build routing infrastructure before scaling hardware | AICP Stages 1-2 were built on 8GB VRAM intentionally — validate the model before investing in hardware |
| The $0 target applies to maintenance, not creation | Knowledge creation remains Claude's domain; routine wiki operations become free |

### State of Knowledge

> [!success] Well-covered
> - The 5-stage roadmap with clear status per stage
> - Routing decision framework (when local vs cloud)
> - Circuit breaker reliability model (CLOSED/OPEN/HALF_OPEN)
> - The 9 loaded models and their distinct capability tiers

> [!warning] Thin or missing
> - Empirical routing split data (Stage 3 not yet operational)
> - Context window overflow handling strategy
> - Profile auto-selection logic (manual vs automatic per operation)

### How to Adopt

> [!info] What you need
> - LocalAI or compatible OpenAI-endpoint server running locally
> - AICP installed with complexity scorer and circuit breaker modules
> - At minimum 8GB VRAM for Stages 1-2; 19GB for Stage 3+
> - Routing profiles configured per operation type

> [!warning] Invariants (do not change per project)
> - Complex reasoning, security review, and novel synthesis always route to cloud
> - Circuit breakers must be active on every backend — no routing without health checks
> - The complexity scorer threshold is the routing mechanism, not manual selection

> [!tip] Per-project adaptations
> - Profile thresholds vary by risk tolerance (`fleet-light` at 0.3 vs `code-review` at 0.8)
> - Model selection depends on available VRAM and task mix
> - The "what remains cloud-only" list may shrink as local models improve

## Open Questions

> [!question] Empirical routing split after Stage 3
> The 80% target is an estimate. Actual measurement requires Stage 3 to be operational.

> [!question] Can the post-chain run entirely on local models?
> Stage 3 targets this, but validation of complex relationship synthesis may still require Claude.

> [!question] Context window as a hidden routing constraint
> Qwen3-8B has a 32K context limit; tasks involving full wiki analysis exceed this. How should the router handle context overflow — split the task, or escalate to cloud?

> [!question] Profile auto-selection
> Should the pipeline auto-select the AICP profile based on the operation being run, or should profiles be set manually per session?

## Relationships

- BUILDS ON: [[AICP]]
- BUILDS ON: [[Local LLM Quantization]]
- FEEDS INTO: [[Model: Automation and Pipelines]]
- FEEDS INTO: [[Model: Quality and Failure Prevention]]
- RELATES TO: [[Model: SFIF and Architecture]]
- IMPLEMENTS: [[Decision: Local Model vs Cloud API for Routine Operations]]
- COMPARES TO: [[Gateway-Centric Routing]]

## Backlinks

[[AICP]]
[[Local LLM Quantization]]
[[Model: Automation and Pipelines]]
[[Model: Quality and Failure Prevention]]
[[Model: SFIF and Architecture]]
[[Decision: Local Model vs Cloud API for Routine Operations]]
[[Gateway-Centric Routing]]
[[Model: NotebookLM]]
