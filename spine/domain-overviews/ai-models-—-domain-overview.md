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

## FAQ

### Q: What local LLM models are currently in use across the ecosystem?
OpenFleet uses hermes-3b for agent inference and bge-m3 for embeddings. AICP runs 9 models including Qwen3, Gemma4 variants, and bge-reranker-v2-m3 for reranking. The Gemma 4 E4B model (9.6GB, 4-bit quantized) is the current recommended small model for agentic tool calling on consumer hardware. See [[Local LLM Quantization]].

### Q: When does it make sense to run a 122B model locally vs using Claude API?
TurboQuant-MLX enables 122B MoE models on a MacBook M4 Max at usable speeds. For tasks requiring strong reasoning (deep analysis, complex code generation), the quality gap vs Claude Sonnet/Opus may still favor the API. For routine tasks (summaries, format conversion, simple Q&A), local models at 4-bit quantization are adequate and effectively free. See [[Local LLM Quantization]].

### Q: What is the difference between Claude Haiku, Sonnet, and Opus for agent tasks?
This is a documented gap in the wiki — no dedicated comparison page exists yet. AICP's complexity scoring routes simpler tasks to cheaper tiers, but the routing thresholds and quality tradeoffs for each tier have not been formally documented. See the [[AICP]] page for current routing logic.

### Q: What embedding model should I use for LightRAG or wiki indexing?
bge-m3 is the current production choice in both AICP and OpenFleet. text-embedding-3-large (OpenAI) is the cloud alternative. A structured comparison of latency, quality, and hardware requirements for wiki-scale indexing does not yet exist in this wiki — it is a documented priority for this domain. See [[LightRAG]].

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
