---
title: "Model: Local AI ($0 Target)"
type: learning-path
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [model, learning-path, spine, local-ai, aicp, zero-cost, backend-routing]
---

# Model: Local AI ($0 Target)

## Summary

The Local AI model describes the ecosystem's strategy for reducing Claude API costs toward zero by routing routine operations to locally-run quantized models. AICP (AI Control Platform) is the orchestration layer: it scores task complexity, checks circuit breaker states, and routes simple operations (status checks, heartbeats, index updates) to LocalAI while reserving Claude for complex reasoning (architecture decisions, deep synthesis, security review). The current hardware baseline (8GB VRAM) supports the Qwen3 and Gemma4 model families; the planned upgrade to 19GB VRAM unlocks Stage 3 of AICP's 5-stage LocalAI independence roadmap (progressive offload targeting 80%+ Claude token reduction). The model is partially blocked pending the hardware upgrade — but the routing infrastructure is already implemented.

## Prerequisites

- Understanding of AICP's role in the four-project ecosystem
- Familiarity with LocalAI as an OpenAI-compatible inference server (GGUF models, GPU acceleration)
- Understanding of circuit breaker patterns and complexity-based routing

## Sequence

### Layer 2 — Core Concepts

1. **AICP** ([[AICP]])
   Entry point. Explains the "You → AICP → (LocalAI | Claude Code) → Your Project" architecture. Covers the three permission modes (Think/Edit/Act), backend routing with complexity scoring, the 5-stage LocalAI independence roadmap, circuit breaker per backend (CLOSED → OPEN → HALF_OPEN), 9 operational profiles, and the 11 MCP tools exposed for fleet integration. Stage 1 (LocalAI functional) and Stage 2 (routing implemented) are complete.

2. **Local LLM Quantization** ([[Local LLM Quantization]])
   The enabling technology. Explains how MoE architectures (only activating a subset of parameters per token) make large models feasible on consumer hardware. TurboQuant-MLX (44 tok/s for 122B MoE on M4 Max) vs Ollama/GGUF (one-command simplicity). Gemma 4 E4B breakthrough: a 9.6GB model reliably executes multi-step agentic tool calling. Hardware implications: current 8GB VRAM vs target 19GB.

3. **OpenClaw** ([[OpenClaw]])
   How LocalAI models are exposed as an OpenAI-compatible endpoint for fleet agents. The Gemma 4 + SearXNG configuration that creates a fully local, private, zero-cost agent runtime.

4. **Gateway-Centric Routing** ([[Gateway-Centric Routing]])
   The routing pattern that AICP implements. Single ingress point, per-request backend selection, circuit breaker isolation. Generalizes beyond AICP to any multi-backend AI system.

### Layer 6 — Decisions

5. **Decision: Local Model vs Cloud API for Routine Operations** ([[Decision: Local Model vs Cloud API for Routine Operations]])
   The explicit decision: route deterministically-validatable tasks (index updates, manifest regeneration, lint checks, simple summarization) to LocalAI; route tasks requiring novel synthesis, security analysis, or architectural reasoning to Claude. Quality threshold is profile-configurable in AICP, not a single fixed value.

### Layer 4 — Lessons (partial — hardware-blocked)

6. **Lesson: Context Management Is the Primary LLM Productivity Lever** (`wiki/lessons/lesson-hub-—-automation.md`)
   Relevant to backend routing: smaller local models have tighter context windows (4K-8K for hermes-3b class), which means task scoping for local routing must be more aggressive than for Claude. Context budget is the hidden routing constraint.

## Status Note

Subsystem 3 (local inference as primary backend) is blocked pending the 8GB → 19GB VRAM hardware upgrade. The routing infrastructure (AICP Stage 2) is implemented and functional for available models. After the upgrade: Gemma 4 26B (18GB model, 24GB VRAM budget) becomes viable for complex agent reasoning, expanding the local-first surface area substantially.

## Outcomes

After completing this path you understand:

- How AICP's complexity scorer decides LocalAI vs Claude on every request
- The 5-stage LocalAI independence roadmap and where it stands today
- What quantization models are running (Qwen3 family, Gemma4 family) and their capability boundaries
- Why Gemma 4 E4B's tool-calling reliability is a capability breakthrough for local agentic operations
- The hardware constraint (VRAM) as the primary blocker for expanding local inference coverage
- How to configure AICP profiles to adjust routing thresholds per workload type

## Relationships

- BUILDS ON: [[AICP]]
- BUILDS ON: [[Local LLM Quantization]]
- FEEDS INTO: [[Model: Automation + Pipelines]]
- FEEDS INTO: [[Model: Quality + Failure Prevention]]
- RELATES TO: [[Model: SFIF + Architecture]]
- COMPARES TO: [[Decision: Local Model vs Cloud API for Routine Operations]]

## Backlinks

[[AICP]]
[[Local LLM Quantization]]
[[Model: Automation + Pipelines]]
[[Model: Quality + Failure Prevention]]
[[Model: SFIF + Architecture]]
[[Decision: Local Model vs Cloud API for Routine Operations]]
[[Model: Knowledge Evolution]]
[[Model: NotebookLM]]
[[Model: Quality and Failure Prevention]]
