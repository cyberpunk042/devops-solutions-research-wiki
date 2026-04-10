---
title: "Quality Standards — What Good Failure Prevention Looks Like"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: seed
created: 2026-04-10
updated: 2026-04-10
sources:
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
tags: [quality, standards, failure-prevention, gold-standard, anti-patterns, enforcement, stage-gates, depth-verification]
---

# Quality Standards — What Good Failure Prevention Looks Like

## Summary

This page defines the quality bar for FAILURE PREVENTION. Where [[Model: Quality and Failure Prevention]] defines the system (three-layer defense, six lessons, enforcement hierarchy), this page shows what GOOD quality enforcement looks like in practice — and what it looks like when it fails. ==Every gold standard on this page is a real incident from this ecosystem.== The failures are real. The fixes are real. The enforcement mechanisms are running in production.

## Key Insights

- **Good quality enforcement is invisible.** You don't notice it working — you notice when it's absent. The sync service that deploys reproducibly is invisible infrastructure. The agent that tries to `cat >` a systemd file is a visible failure.

- **The standard is NOT zero failures.** The standard is that every failure produces a codified lesson, a concrete enforcement mechanism, and a measurable threshold. A project with 7 bugs and 7 enforcement rules is healthier than a project with 0 documented bugs and unknown failure modes.

- **Enforcement that the agent can reason around is not enforcement.** A CLAUDE.md instruction that says "don't do X" is a suggestion. A hook that blocks X is enforcement. The quality bar for enforcement is: can the agent bypass it through reasoning? If yes, it's teaching, not enforcement.

- **Depth verification is pass/fail, not a spectrum.** Did you read the thing itself, or only a description? There is no partial credit. Layer 0 (description) → reject. Layer 1 (instance) → accept. The 0.25 ratio is the measurable proxy.

## Deep Analysis

### Gold Standard: Failure Lesson Codification

What a properly codified failure looks like — from incident to enforcement.

> [!info] **The gold standard lifecycle of a failure**
> | Stage | What happens | Artifact |
> |-------|-------------|----------|
> | 1. Incident | Something goes wrong during real operation | Raw observation |
> | 2. Root cause | WHY it happened, not just WHAT happened | Understanding |
> | 3. Lesson page | L4 wiki page with Context, Insight, Evidence, Applicability | `wiki/lessons/` entry |
> | 4. Enforcement mechanism | CLAUDE.md rule, hook, validation gate, or skill update | Operational change |
> | 5. Verification | Test that the enforcement prevents recurrence | Evidence it works |

> [!success] **Gold standard: "Never Synthesize from Descriptions Alone"**
> 1. **Incident:** Agent ingested awesome-design-md (a curated list of 58 DESIGN.md files), synthesized a page about the DESIGN.md pattern, never opened a single actual DESIGN.md file. The user challenged: "prove me... to me it just feels like you stayed on surface."
> 2. **Root cause:** The agent treated a CATALOG (Layer 0) as equivalent to the THING (Layer 1). Reading about DESIGN.md files ≠ reading a DESIGN.md file.
> 3. **Lesson page:** [[Never Synthesize from Descriptions Alone]] — 95 lines with the Layer 0/1/2 model, the 0.25 ratio rule, and 3 enforcement mechanisms.
> 4. **Enforcement:** CLAUDE.md quality gates section now requires source provenance. Wiki-agent skill encodes depth verification. Memory carries the directive cross-session. CLAUDE.md Agent Methodology section says "ALWAYS verify depth."
> 5. **Verification:** The context-mode source was later ingested correctly — 1,057 lines read in full, 254-line synthesis page produced (0.24 ratio). The first attempt had been 60 lines from the first chunk. The rule caught it.

> [!bug]- **Anti-pattern: lesson without enforcement**
> An agent fails, someone writes a post-mortem, the post-mortem lives in a doc, nobody reads the doc again. The failure recurs. This is the "documentation theater" pattern — the appearance of learning without operational change.
>
> **The test:** Can you point to the specific enforcement mechanism (CLAUDE.md line, hook, validation rule) that prevents this failure from recurring? If not, the lesson isn't codified — it's just written down.

---

### Gold Standard: Three-Layer Defense in Practice

What the three layers look like when all three are operating.

> [!success] **Gold standard: this wiki's ingestion quality system**
>
> **Layer 1 — Structural Prevention:**
> - `pipeline post` runs 6 deterministic steps — validation errors block (exit code 1)
> - Schema validation requires: frontmatter fields present, title matches heading, Summary ≥30 words, ≥1 relationship, source provenance
> - These CANNOT be bypassed. An invalid page will not pass `pipeline post` regardless of the agent's confidence.
>
> **Layer 2 — Teaching:**
> - CLAUDE.md defines quality gates, ingestion modes, the 0.25 ratio rule
> - Wiki-agent skill teaches depth verification, three ingestion modes, post-chain requirements
> - Memory carries cross-session directives: "never synthesize from descriptions alone"
>
> **Layer 3 — Review:**
> - Smart ingestion mode escalates to human on: new domains, contradictions, ambiguity, expert-level complexity
> - Maturity promotion (seed → growing) requires human confirmation
> - Model pages reviewed against model-builder skill quality bar
>
> **How they interact:** Teaching says "always read the full source." If the agent doesn't (teaching failure, ~40% of the time), the validation gate catches it — a 60-line page from a 1,000-line source fails the 0.25 ratio check. If validation somehow passes (edge case), human review catches it — "this page is thin, where's the depth?"

> [!bug]- **Anti-pattern: single-layer quality**
> A project that relies ONLY on CLAUDE.md instructions for quality. No validation tooling, no post-chain, no human review gates. The agent follows instructions ~60% of the time. 40% of quality violations pass silently.
>
> **Why it fails:** Teaching alone has ~60% compliance. Structural prevention alone produces correct-but-misaligned work. Review alone exhausts humans. The minimum viable quality system needs ALL THREE layers — even if each layer is thin.

---

### Gold Standard: Depth Verification

What proper depth verification looks like during ingestion.

> [!success] **Gold standard: ingesting the context-mode repo**
>
> **First attempt (FAILED):** Read the first chunk of the 1,057-line README. Produced a 60-line surface synthesis. The source described 12 platforms, FTS5/BM25 knowledge base, session continuity, benchmarks — the synthesis mentioned almost none of this.
>
> **After depth verification:** Read ALL 1,057 lines via multiple offset reads. Produced a 254-line synthesis covering: sandbox tools, FTS5/BM25 knowledge base, session continuity, 12-platform comparison matrix, benchmarks (315KB → 5.4KB, 98% reduction), Think in Code paradigm, routing enforcement gap, security model, OpenClaw integration, two-layer optimization, privacy.
>
> **The ratio:** 254/1,057 = 0.24 — just at the 0.25 threshold. The first attempt: 60/1,057 = 0.06 — would have failed the ratio check if it existed at that point.

> [!warning] **The diagnostic question for depth**
> "Can a reader of this synthesis DECIDE whether to use this tool/pattern/technique without reading the original source?" If they need to read the original, the synthesis failed. The synthesis should be a SUBSTITUTE for reading the source, not an advertisement for it.

> [!bug]- **Anti-pattern: the confident surface**
> A synthesis page that reads well, uses proper formatting, passes validation, but contains only what was visible in the first 60 lines. The rest of the source — the implementation details, the edge cases, the benchmarks, the limitations — is invisible.
>
> **Why it's dangerous:** The page PASSES all structural quality gates (frontmatter valid, summary ≥30 words, relationships present). Only a human reviewer or a ratio check would catch it. This is the failure mode that the 0.25 ratio rule exists to prevent.

---

### Gold Standard: Stage-Gate Enforcement

What properly enforced stage boundaries look like.

> [!success] **Gold standard: the backlog system scaffold stage**
> The scaffold stage for the backlog system produced ONLY: 4 new types in wiki-schema.yaml, 7 new statuses, 5 new enums, directory structure (wiki/backlog/epics/, modules/, tasks/), methodology.yaml (253 lines).
>
> ==Zero Python logic in the diff.== Zero business rules. Zero functions. The methodology.yaml defines stages — it does not implement them. This is what "scaffold means structure only" looks like when enforced.

> [!bug]- **Anti-pattern: OpenArms Bug 5 — scaffold with business logic**
> The scaffold stage produced a 135-line environment reader with full parsing, validation, and default handling. The stage had no FORBIDDEN list — nothing said "business logic is not allowed here."
>
> **Why it happened:** Stage NAMES don't prevent violations. "Scaffold" sounds like "structure only" to humans, but without an explicit FORBIDDEN list, the agent's definition of "structure" expanded to include everything.
>
> **The fix:** Explicit ALLOWED/FORBIDDEN lists per stage in methodology.yaml. Gate requires: diff inspection confirms no FORBIDDEN artifacts. This became methodology v4.

> [!bug]- **Anti-pattern: OpenArms Bug 6 — orphaned implementation**
> 2,073 lines of production code — network rules, cost tracking, hook events. None imported by any runtime file. Tests passed. Feature didn't work.
>
> **Why it happened:** "Code exists" was treated as "code works." No integration requirement at the implement stage.
>
> **The fix:** Implement stage MUST wire into runtime. "Done When" must name the specific consumer file that imports the new code. Tests pass ≠ feature works.

---

### Gold Standard: Enforcement Level Migration

What it looks like when a project migrates quality rules upward through the enforcement hierarchy.

> [!info] **The wiki's enforcement migration history**
> | Rule | Started at | Currently at | Target |
> |------|-----------|-------------|--------|
> | "Don't skip stages" | Level 0 (CLAUDE.md instruction) | Level 0 + Level 1 (skill + memory) | Level 2 (hook blocks Write to src/ during document stage) |
> | "Run pipeline post" | Level 0 (CLAUDE.md instruction) | Level 1 (post-chain in pipeline.py, exit code blocks) | Level 1 (already structural via exit codes) |
> | "No fabricated data" | Level 0 (CLAUDE.md instruction) | Level 0 + memory | Level 2 (hook flags unattributed quantitative claims) |
> | "Depth verification" | Level 0 (CLAUDE.md instruction) | Level 0 + Level 1 (wiki-agent skill + memory) | Level 2 (hook checks ratio before page write) |
> | "Block sudo/force-push" | Not implemented | Not implemented | Level 2 (R01-R04 from claude-code-harness) |

> [!tip] **The migration principle**
> Start at Level 0 (instructions). When a rule is violated despite instructions, migrate to Level 1 (skills + validation). When it's violated despite skills, migrate to Level 2 (hooks). Each violation is evidence that the current enforcement level is insufficient.
>
> Not every rule needs Level 2. Some rules are rarely violated — teaching is sufficient. The enforcement level should match the violation frequency and consequence severity.

---

### Anti-Pattern Summary

| Anti-pattern | What goes wrong | Gold standard contrast |
|-------------|----------------|----------------------|
| **Lesson without enforcement** | Failure documented, never prevented | Each lesson → CLAUDE.md rule + enforcement mechanism |
| **Single-layer quality** | ~60% compliance, 40% silent violations | Three layers: structural + teaching + review |
| **Confident surface** | Passes validation but hollow content | 0.25 ratio rule catches shallow synthesis |
| **Scaffold with logic** | Stage boundaries violated | Explicit ALLOWED/FORBIDDEN per stage |
| **Orphaned implementation** | Code exists but isn't imported | Implement MUST wire into runtime |
| **Hope-based enforcement** | Rules in docs the agent may not read | Rules in CLAUDE.md, hooks at execution time |
| **Documentation theater** | Post-mortems written, never operationalized | Lesson → enforcement mechanism → verification |

---

### The Quality Prevention Checklist

> [!tip] **Run this for any project using the quality system**
> - [ ] Three-layer defense is implemented (structural prevention + teaching + review)
> - [ ] Every known failure has a codified lesson page (Context, Insight, Evidence, Applicability)
> - [ ] Every lesson maps to a concrete enforcement mechanism (CLAUDE.md rule, hook, validation gate)
> - [ ] Validation tooling blocks on errors (exit code enforcement, not advisory warnings)
> - [ ] Depth verification is in the ingestion methodology (Layer 0/1/2 rule + 0.25 ratio)
> - [ ] Stage gates define ALLOWED and FORBIDDEN per stage (not just stage names)
> - [ ] Post-chain runs automatically after every change batch
> - [ ] Enforcement level is tracked per rule (Level 0-3) with migration targets identified
> - [ ] Unverified claims are explicitly flagged (no fabricated data points)

## Open Questions

> [!question] **Should there be a "quality health score" per project?**
> A composite metric: % of rules at Level 2+, % of failures with codified lessons, ratio check pass rate, stage gate violation rate. Would this drive improvement or become a vanity metric? (Requires: implementing and tracking across 3+ projects)

> [!question] **What's the minimum three-layer defense for a small project?**
> A solo developer with a 10-page wiki doesn't need 24 immune system rules. What's the minimum: CLAUDE.md + `pipeline post` + one human review gate? (Requires: testing with a minimal setup)

> [!question] **Can enforcement migration be automated?**
> When a rule is violated N times at Level 0, automatically suggest migrating to Level 1 (skill) or Level 2 (hook). This closes the loop between violation detection and enforcement improvement. (Requires: violation tracking infrastructure)

## Relationships

- BUILDS ON: [[Model: Quality and Failure Prevention]]
- RELATES TO: [[LLM Wiki Standards — What Good Looks Like]]
- RELATES TO: [[Methodology Standards — What Good Execution Looks Like]]
- RELATES TO: [[Claude Code Standards — What Good Agent Configuration Looks Like]]
- RELATES TO: [[Wiki Design Standards — What Good Styling Looks Like]]
- RELATES TO: [[Never Synthesize from Descriptions Alone]]
- RELATES TO: [[The Agent Must Practice What It Documents]]

## Backlinks

[[Model: Quality and Failure Prevention]]
[[LLM Wiki Standards — What Good Looks Like]]
[[Methodology Standards — What Good Execution Looks Like]]
[[Claude Code Standards — What Good Agent Configuration Looks Like]]
[[Wiki Design Standards — What Good Styling Looks Like]]
[[Never Synthesize from Descriptions Alone]]
[[The Agent Must Practice What It Documents]]
