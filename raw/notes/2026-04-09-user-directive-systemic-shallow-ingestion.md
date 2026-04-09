# User Directive — 2026-04-09 — Systemic Shallow Ingestion Issue

## Verbatim

> WTF happened in the first place... we have a systemic issue in our system

## Interpretation

The context-mode source page was created from only the first ~60 lines of a 1,057-line file. The subagent didn't read the full source before synthesizing. This is NOT a one-off — it's a systemic issue that likely affects all source-synthesis pages created by subagents.

### Root Cause
Subagents use the Read tool which has a default line limit. Large raw files (500+ lines) get truncated silently. The subagent doesn't know it's missing 90% of the content.

### Impact
All 20 source-synthesis pages may be shallow. Pages synthesized from long transcripts (12 YouTube transcripts, some 500+ lines) and detailed READMEs may only cover the introduction.

### Required Fix
1. Audit all source-synthesis pages for depth vs raw file length
2. Fix the methodology: subagent prompts must instruct to read the FULL file with multiple offset reads
3. Add to the evolve skill / wiki-agent skill: "always verify raw file length before synthesizing"
4. Consider adding a quality check to the pipeline: compare raw file length vs wiki page length