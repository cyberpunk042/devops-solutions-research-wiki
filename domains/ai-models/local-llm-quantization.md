---
title: "Local LLM Quantization"
type: concept
domain: ai-models
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-turboquant-122b-macbook
    type: article
    url: "https://medium.com/data-science-collective/how-i-run-122b-parameter-llms-on-a-macbook-outperforming-mxfp4-and-standard-quantization-on-apple-0552ee3da1f7"
    file: raw/articles/turboquant-122b-llm-macbook-mlx.md
    title: "How I Run 122B Parameter LLMs on a MacBook"
    ingested: 2026-04-08
  - id: src-gemma4-searxng-openclaw
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=T0CKsU0hQx4"
    file: raw/transcripts/gemma-4-searxng-100-free-amp-private-openclaw-full-setup.txt
    title: "Gemma 4 + SearXNG for OpenClaw"
    ingested: 2026-04-08
tags: [quantization, local-llm, mlx, ollama, apple-silicon, moe, turboquant, gemma4, consumer-hardware, local-first]
---

# Local LLM Quantization

## Summary

Local LLM quantization enables running large language models (up to 122B parameters) on consumer hardware like MacBooks by reducing precision from full floating-point to lower bit-widths. Two approaches dominate: TurboQuant-MLX achieves 44 tok/s for 122B MoE models on M4 Max (64GB RAM), outperforming Apple's native MXFP4 format. Ollama provides a simpler path, packaging quantized models (GGUF format) for one-command download and native integration with AI agent frameworks like OpenClaw. The Gemma 4 family demonstrates that even 7GB models (E2B) can reliably handle multi-step agentic tool calling — a capability that previously required much larger models.

## Key Insights

- **Consumer hardware runs 122B models**: MacBook M4 Max (64GB) runs 122B MoE at 44 tok/s via TurboQuant-MLX. MacBook Pro (24GB) comfortably runs Gemma 4 26B (18GB model file). Even 16GB MacBooks can run Gemma 4 E2B (7GB).

- **MoE architecture enables local large models**: Mixture-of-Experts only activates a subset of parameters per token. A 122B MoE model might only use 13B active parameters per forward pass, making it memory-feasible on consumer hardware despite the large total size.

- **TurboQuant > MXFP4 > standard quantization**: Model-aware quantization (adapted per architecture) outperforms hardware-native formats (Apple's MXFP4) and generic affine quantization. This suggests quantization should be tailored to model structure, not just hardware.

- **Ollama as model distribution**: `ollama pull gemma4:e2b` downloads, quantizes, and serves models with a single command. `ollama list` manages local model inventory. Native integrations with OpenClaw, Open WebUI, and other frameworks eliminate configuration.

- **Small models now do tool calling**: Gemma 4 E4B (9.6GB, designed for phones) reliably executes multi-step agentic tasks: web search → summarize → create report → send email. This was previously unreliable with small models, representing a capability breakthrough.

- **Two quantization paths**: (1) MLX/TurboQuant for maximum performance on Apple Silicon (research-grade, manual setup), (2) Ollama/GGUF for maximum convenience across platforms (one-command, auto-quantized). AICP's model evaluation pipeline tests both paths.

## Deep Analysis

### Implications for the Ecosystem

The local LLM quantization landscape directly affects three ecosystem projects:

**AICP (AI Control Platform):** The 5-stage LocalAI independence roadmap (target: 80% Claude token reduction) becomes more achievable as consumer hardware capabilities grow. AICP already evaluates Qwen3 and Gemma4 models — adding TurboQuant-MLX for MoE models could unlock 122B-class reasoning locally. The backend router can factor quantization performance into its complexity-based routing decisions.

**OpenFleet:** Fleet agents running on LocalAI currently use hermes-3b for queries and bge-m3 for embeddings. If Gemma 4 26B runs comfortably on 24GB hardware with reliable tool calling, it could replace hermes for agent inference — better reasoning at negligible cost. The silent heartbeat optimization (70% cost savings) becomes even more effective when the baseline cost is already zero (local inference).

**Research Wiki:** For the pipeline automation vision, local inference means research operations (web search, summarization, cross-referencing) can run without API calls. A local model could power automated gap analysis and relationship discovery in the pipeline.

## Open Questions

- What is the quality degradation of TurboQuant at 2-bit vs 4-bit vs 8-bit for reasoning tasks specifically?
- Can TurboQuant-MLX be integrated with Ollama for best-of-both-worlds (Ollama distribution + TurboQuant quantization)?
- How does Gemma 4 26B's tool calling reliability compare to Claude Sonnet for OpenFleet agent tasks?
- What is the memory/performance profile of running multiple quantized models simultaneously (e.g., reasoning + embedding + reranking)?

## Relationships

- RELATES TO: AICP
- RELATES TO: OpenFleet
- RELATES TO: OpenClaw
- ENABLES: LightRAG
- RELATES TO: Claude Code

## Backlinks

[[AICP]]
[[OpenFleet]]
[[OpenClaw]]
[[LightRAG]]
[[Claude Code]]
