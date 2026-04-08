---
title: "AI Models — Domain Overview"
type: domain-overview
domain: ai-models
layer: spine
status: synthesized
confidence: medium
maturity: seed
created: 2026-04-08
updated: 2026-04-08
sources: []
tags: [domain-overview, ai-models]
---

# AI Models — Domain Overview

## Summary

The ai-models domain covers LLMs, embeddings, quantization, fine-tuning, and model evaluation — the foundational layer that all agent and knowledge system operations depend on. This is the least developed domain in the wiki, with a single concept page (Local LLM Quantization) and one associated source synthesis. The sparse coverage reflects the project's current focus: the ecosystem consumes models rather than building or evaluating them, so model knowledge is accumulated incidentally through other domains (AICP documents model routing, OpenFleet uses hermes-3b and bge-m3, LightRAG requires 32B+ context). The Local LLM Quantization page is well-sourced (TurboQuant-MLX article + Gemma 4 + SearXNG YouTube transcript) and establishes an important capability threshold: consumer hardware can now run 122B MoE models at usable speeds, and small models (Gemma 4 E4B, 9.6GB) now reliably handle multi-step agentic tool calling. This domain should grow significantly as AICP's LocalAI independence roadmap advances and the fleet transitions away from Claude API dependency.

## State of Knowledge

**Strong coverage:**
- Local LLM Quantization — two-source synthesis covering TurboQuant-MLX (122B on MacBook M4 Max), Ollama/GGUF convenience path, Gemma 4 E2B/E4B/26B capabilities, MoE architecture enabling large local models, and AICP/OpenFleet integration implications. Confidence: medium (technical details solid, ecosystem integration implications are forward-looking).

**Thin coverage (known gaps drawn from other domains):**
- Embedding models — bge-m3, nomic-embed, text-embedding-3-large are all used in AICP and LightRAG but there is no dedicated comparison or selection guidance.
- Reranking models — bge-reranker-v2-m3 is referenced in LightRAG but not documented at depth.
- Model routing and complexity scoring — AICP's backend router implements complexity-based routing but the routing logic itself is documented in tools-and-platforms, not here where the model evaluation knowledge belongs.
- Fine-tuning — not covered at all; relevant as OpenFleet approaches Stage 4-5 of LocalAI independence.
- Model evaluation frameworks — no coverage of benchmarking methodologies, task-specific evaluation, or quality degradation measurement.
- Claude API specifics — context window sizes, token pricing, rate limits, model differences (Sonnet vs Opus vs Haiku) are assumed knowledge but not documented.

## Maturity Map

**Established content (pre-maturity system):**
- Local LLM Quantization — sole concept page; medium confidence; covers the quantization landscape adequately

**Sources (processed):**
- Synthesis: TurboQuant 122B LLM on MacBook — source synthesis corresponding to Local LLM Quantization
- Synthesis: Gemma 4 + SearXNG for Free Private OpenClaw — source synthesis covering Gemma 4 agentic tool calling

## Gaps

- **Embedding model comparison**: bge-m3 vs nomic-embed vs text-embedding-3-large — latency, quality, cost, and hardware requirements for wiki-scale indexing.
- **Model selection guide for agent tasks**: Which local model (Qwen3 family, Gemma4 family, Hermes) for which task (heartbeat processing, code review, deep analysis, embedding, reranking)?
- **Claude model tier guide**: Haiku vs Sonnet vs Opus for different task complexity levels — cost vs quality tradeoff documentation for the backend routing decision.
- **Fine-tuning viability**: Can fine-tuning on OpenFleet's 219 KB entries improve agent inference quality? Is this worth pursuing vs better prompting?
- **Quantization quality curves**: What is the practical quality degradation at 2-bit vs 4-bit vs 8-bit for reasoning, code generation, and agentic tool calling specifically?
- **Multi-model serving**: AICP runs 9 models simultaneously on LocalAI. What are the memory, latency, and throughput implications of concurrent model serving?

## Priorities

1. **Embedding model comparison** — Select the right model for wiki-scale LightRAG indexing; direct dependency for the LightRAG integration priority
2. **Model selection guide** — Document which model serves which task type across AICP's 9 loaded models; high operational value
3. **Claude model tier tradeoffs** — Cost vs quality vs speed for Haiku/Sonnet/Opus; feeds into AICP routing thresholds
4. **Quantization quality curves** — Systematic evaluation of TurboQuant bit-width vs reasoning quality; feeds AICP Stage 3-4
5. **Fine-tuning investigation** — Assess whether fine-tuning on ecosystem KB data is viable and cost-effective

## Key Pages

1. **[Local LLM Quantization](../../domains/ai-models/local-llm-quantization.md)** — The only page in this domain. Covers TurboQuant-MLX for 122B models on MacBook, Ollama/GGUF convenience path, Gemma 4 capability breakthrough, and ecosystem implications.

## Relationships

- ENABLES: AI Agents
- ENABLES: Knowledge Systems
- ENABLES: Tools And Platforms
- ENABLES: Automation
- RELATES TO: Devops

## Backlinks

[[AI Agents]]
[[Knowledge Systems]]
[[Tools And Platforms]]
[[Automation]]
[[Devops]]
