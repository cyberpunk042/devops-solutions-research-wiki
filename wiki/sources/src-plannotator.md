---
title: "Plannotator — Interactive Plan & Code Review for AI Agents"
type: source-synthesis
layer: 1
maturity: growing
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: src-plannotator
    type: github-repo
    url: https://github.com/backnotprop/plannotator
    file: raw/articles/backnotpropplannotator.md
tags: [plannotator, plan-annotation, code-review, implementation-plans, claude-code-plugin, pm]
---

# Plannotator — Interactive Plan & Code Review for AI Agents

## Summary

Plannotator is an open-source tool that injects a human-in-the-loop UI between an AI agent's planning phase and its execution phase. It intercepts agent-generated plans via a built-in hook, opens a browser-based annotation interface, and returns structured feedback — either approving the plan to proceed or sending revision instructions back into the agent loop. Supported agents include Claude Code, Copilot CLI, Gemini CLI, OpenCode, Pi, and Codex.

## Key Insights

- **Hook-based interception**: Plannotator registers as a plan-mode hook in the agent runtime. When the agent finishes planning, the hook fires before execution, opening the UI. This is non-invasive — the agent loop is paused, not replaced. The feedback message fed back is structured, not freeform.

- **Four interaction modes beyond plan approval**:
  - `/plannotator-review` — code review of git diffs or remote GitHub PRs, with inline annotation and AI Q&A
  - `/plannotator-annotate` — annotate any markdown file and push feedback to the agent
  - `/plannotator-last` — annotate the agent's last message directly
  - Plan diff view — automatically shows what changed between plan revisions, enabling targeted feedback

- **Cross-agent coverage**: Installation is consistent (single `install.sh` / `install.ps1`) but agent integration differs per platform — Claude Code uses a plugin marketplace, Gemini CLI auto-configures from `~/.gemini` detection, OpenCode uses `opencode.json`, Codex uses `!plannotator` prefixed commands. This reflects the fractured plugin ecosystem across current AI CLI agents.

- **Zero-knowledge sharing**: Small plans encode entirely in URL hash (no server). Large plans use AES-256-GCM client-side encryption before upload; the server stores only ciphertext; the decryption key lives only in the shared URL. Auto-delete after 7 days. Self-hostable. This is a strong privacy model for sharing sensitive implementation plans with colleagues.

- **SLSA provenance from v0.17.2**: Released binaries ship with SHA256 sidecars and support SLSA supply chain verification — a meaningful signal that the project treats security as a first-class concern for enterprise adoption.

- **Plan review as a forcing function**: By making plan approval a required gate before execution, Plannotator operationalizes the "always plan before executing" lesson. It externalizes the review step that many teams skip because it has no tooling friction without it.

- **Structured feedback vs. natural language**: Annotations (delete, insert, replace, comment) are structured operations, not free text. This means feedback is machine-parseable and more precisely actionable by the agent than a prose correction would be.

- **Dual licensing (MIT + Apache 2.0)**: Permissive dual license signals intent for broad ecosystem adoption including commercial use. The self-hosting path reinforces enterprise suitability.

## Open Questions

- How does Plannotator handle agent re-planning cycles? If an agent re-plans after receiving feedback, does the hook fire again?
- What is the latency impact of the browser UI step on automated pipelines where human review is fast but the round-trip adds friction?
- Is there a headless/CI mode for non-interactive environments (e.g., async review queues)?
- Does the annotation schema map to a standard format (e.g., GitHub review comments, RFC diff formats) or is it proprietary?
- How does the SFIF (Speculate-Feedback-Iterate-Finalize) pattern map to Plannotator's annotation → feedback → re-plan loop?

## Relationships

- IMPLEMENTS: [[Plan Execute Review Cycle]] (provides the tooling layer that makes plan-gate-review a concrete workflow)
- EXTENDS: [[Agent Orchestration Patterns]] (adds structured human oversight as a first-class hook in multi-step agent flows)
- RELATES TO: [[Scaffold → Foundation → Infrastructure → Features]] (operationalizes the speculate → feedback → iterate loop with UI tooling)
- RELATES TO: [[Claude Code Best Practices]] (plan-mode review is a best practice; Plannotator makes it frictionless)
- RELATES TO: [[Claude Code Skills]] (integrates as a Claude Code plugin, complements slash-command patterns)
- FEEDS INTO: [[Always Plan Before Executing]] (provides tooling that enforces the planning gate lesson)

## Backlinks

[[[[Plan Execute Review Cycle]] (provides the tooling layer that makes plan-gate-review a concrete workflow)]]
[[[[Agent Orchestration Patterns]] (adds structured human oversight as a first-class hook in multi-step agent flows)]]
[[[[Scaffold → Foundation → Infrastructure → Features]] (operationalizes the speculate → feedback → iterate loop with UI tooling)]]
[[[[Claude Code Best Practices]] (plan-mode review is a best practice; Plannotator makes it frictionless)]]
[[[[Claude Code Skills]] (integrates as a Claude Code plugin, complements slash-command patterns)]]
[[[[Always Plan Before Executing]] (provides tooling that enforces the planning gate lesson)]]
[[Hooks Lifecycle Architecture]]
[[Model: Skills, Commands, and Hooks]]
[[Per-Role Command Architecture]]
