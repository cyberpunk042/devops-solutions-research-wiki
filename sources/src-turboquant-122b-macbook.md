---
title: "Synthesis: TurboQuant 122B LLM on MacBook"
type: source-synthesis
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
tags: [quantization, turboquant, mlx, apple-silicon, moe, local-llm, m4-max, 122b-parameters]
---

# Synthesis: TurboQuant 122B LLM on MacBook

## Summary

TurboQuant, originally Google's quantization technique, has been adapted for Apple Silicon via MLX and extended to Mixture-of-Experts (MoE) architectures, enabling 122B parameter models to run on a MacBook M4 Max (64GB RAM) at 44 tokens/second. The method outperforms both MXFP4 (Apple's native mixed-precision format) and standard affine quantization across multiple bit-widths. This represents a significant milestone for local-first AI: consumer hardware can now run models that rival cloud-hosted inference in size, with competitive throughput.

## Key Insights

- **122B parameters on consumer hardware**: MacBook M4 Max with 64GB RAM runs a 122B MoE model at 44 tok/s. This is fast enough for interactive use and agent workflows.

- **TurboQuant > MXFP4 > standard quantization**: The technique outperforms Apple's own native format (MXFP4) which was designed for Apple Silicon. This suggests that model-aware quantization (adapted per architecture) beats hardware-native formats.

- **MoE architecture is key**: MoE models (Mixtral, Qwen-MoE, GPT-OSS family) only activate a subset of parameters per token, making them memory-efficient despite large total parameter counts. TurboQuant's extension to MoE specifically unlocks this class of models for consumer hardware.

- **MLX framework**: Apple's ML framework designed for Apple Silicon. Previous TurboQuant-MLX work covered dense models (1B-7B). This extends to MoE at 122B — a 17x parameter jump.

- **Implications for AICP**: If MacBooks can run 122B models at 44 tok/s, the AICP LocalAI independence roadmap (80%+ Claude token reduction) becomes more feasible. Complex reasoning tasks that currently require Claude could potentially be handled by local MoE models with appropriate quantization.

## Relationships

- DERIVED FROM: src-turboquant-122b-macbook
- RELATES TO: AICP
- RELATES TO: LightRAG

## Backlinks

[[src-turboquant-122b-macbook]]
[[AICP]]
[[LightRAG]]
