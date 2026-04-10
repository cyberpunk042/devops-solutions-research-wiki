---
title: "Test OpenAI backend with LocalAI"
type: task
domain: backlog
status: blocked
priority: P1
epic: E001
task_type: task
current_stage: scaffold
readiness: 0
stages_completed: []
artifacts: []
depends_on: []
confidence: high
created: 2026-04-09
updated: 2026-04-09
estimate: M
sources: []
tags: [local-inference, openai-backend, testing, blocked]
---

# Test OpenAI backend with LocalAI

## Summary

Run `pipeline evolve --auto --backend openai --top 1` against a running LocalAI instance to validate the local model evolution backend. Verify the generated page passes validation and content quality gates. Requires 19GB VRAM hardware upgrade (pending). This is the first end-to-end test of the $0 target evolution path — local inference generating wiki pages without Claude API calls.

## Done When

- [ ] LocalAI running with a 30B+ model
- [ ] `pipeline evolve --auto --backend openai --top 1` completes without error
- [ ] Generated page passes `pipeline post` validation
- [ ] Token count and generation time documented
