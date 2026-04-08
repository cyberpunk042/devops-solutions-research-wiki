# How I Run 122B Parameter LLMs on a MacBook

Source: https://medium.com/data-science-collective/how-i-run-122b-parameter-llms-on-a-macbook-outperforming-mxfp4-and-standard-quantization-on-apple-0552ee3da1f7
Ingested: 2026-04-08
Type: article

---

Article by Manjunath Janardhan on extending TurboQuant to Mixture-of-Experts (MoE) models for Apple Silicon.

## Key Details

- Model: 122B parameter MoE (Mixture-of-Experts) architecture
- Hardware: MacBook M4 Max with 64GB RAM
- Performance: 44 tokens/second on M4 Max
- Framework: MLX (Apple's ML framework for Apple Silicon)
- Method: TurboQuant — Google's quantization technique adapted for Apple Silicon, extended to MoE models
- Previous work: TurboQuant-MLX on dense models (1B-7B parameters)

## Claims

- Outperforms MXFP4 (Apple's native mixed-precision format)
- Outperforms standard affine quantization across multiple bit-widths
- Supports MoE architectures: Mixtral, Qwen-MoE, OpenAI GPT-OSS family

## Significance

Running 122B parameter models on consumer hardware (MacBook) with 44 tok/s is significant for local-first AI. This is directly relevant to AICP's LocalAI independence mission — if consumer hardware can run 122B MoE models efficiently, the case for cloud inference weakens further.

Note: Full article behind Medium paywall. Key details extracted from preview + web search.
