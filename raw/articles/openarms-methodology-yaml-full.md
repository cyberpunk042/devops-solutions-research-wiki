# OpenArms Methodology YAML + Agent Directive — Full Reference

Source: User-shared content from conversation, 2026-04-09
Type: documentation (primary source from ecosystem project)

---

## methodology.yaml

### Stages

5 stages in order, each with required artifacts and injected protocol:

1. **document** (readiness 0-25%): Understand the problem. Read existing code. Write wiki documentation.
   - Required: wiki page documenting concept/feature, mapping of existing infrastructure, gap analysis
   - Protocol: Do NOT write implementation code. Do NOT create new source files. MAY create wiki pages and docs.

2. **design** (readiness 25-50%): Make decisions. Write design docs. Define config shape.
   - Required: design decision document, target config shape, interface/type sketches
   - Protocol: Do NOT write implementation code. MAY write type sketches in documentation.

3. **scaffold** (readiness 50-80%): Create the skeleton. Types, examples, .env entries, empty test files.
   - Required: type definitions, .env.example entries, example config snippets, empty test files with describe blocks
   - Protocol: Do NOT implement business logic. Do NOT fill in test implementations. Types and scaffolding only.

4. **implement** (readiness 80-95%): Write the code. Fill in the logic. Make it work.
   - Required: implementation code, passing type checks, passing lint
   - Protocol: Build on the scaffold. Follow the design document. Keep changes additive.

5. **test** (readiness 95-100%): Write tests. Verify behavior. Ensure nothing broken.
   - Required: test implementations, passing test suite, verification existing tests still pass
   - Protocol: Fill in scaffolded test files. Fix failures before marking complete.

### Task Types — Per-Type Stage Requirements

| task_type | Required stages |
|-----------|----------------|
| epic | document, design, scaffold, implement, test |
| module | document, design, scaffold, implement, test |
| task | scaffold, implement, test |
| bug | document, implement, test |
| spike | document, design (research only, no code) |
| docs | document (documentation only) |
| refactor | document, scaffold, implement, test |

### Item Hierarchy: EPIC → MODULE → TASK

Rules:
1. An EPIC is a container. NEVER done by itself. Done ONLY when ALL children done AND acceptance criteria met.
2. A MODULE is a scoped deliverable within an epic. Same rule.
3. A TASK is the atomic work unit. Tasks go through stages. Done when all required stages complete.
4. READINESS flows UPWARD. Epic readiness = AVERAGE of children's readiness. Never set manually.
5. STATUS flows UPWARD: any child in-progress → parent in-progress. ALL children done → parent moves to review (not done). Parent done ONLY after human review confirms.
6. You WORK ON TASKS, not epics. To advance an epic, pick a task and complete the next stage.
7. An epic may stay in-progress for weeks. Normal.
8. When an epic has no tasks left but isn't at 100%, CREATE NEW TASKS to cover the gap.

### Execution Modes

| Mode | Description | Stop | Human Review | End Condition |
|------|-------------|------|-------------|---------------|
| autonomous | Default. Works through all stages, picks next task | null | false | backlog-empty |
| full-autonomous | Skips document stage on tasks (not epics/modules) | null | false | backlog-empty |
| semi-autonomous | Stops after each task for human review | null | true | backlog-empty |
| document-only | Runs document stage only | document | false | backlog-empty |
| design-only | Runs through design stage | design | false | backlog-empty |
| scaffold-only | Runs through scaffold | scaffold | false | backlog-empty |
| plan | Alias for design-only | design | false | backlog-empty |
| custom | Ephemeral, per-run config | null | false | null |

### End Conditions

- backlog-empty: all tasks done or archived
- stage-reached: current task has reached specified stage
- time-limit: N hours
- cost-limit: $N on API calls
- task-count: N tasks completed

### Defaults

- Mode: autonomous
- End condition: backlog-empty
- Priority order: P0, P1, P2, P3
- Max stage retries: 2
- Commit style: conventional

## Agent Directive

### Sacrosanct Operator Directives

Operator's founding directives are supreme source of truth. Live in wiki/log/. Never paraphrased, diluted, or overridden.

### The Work Loop (14 steps)

1. Read wiki/backlog/tasks/_index.md — find highest priority undone task
2. Read task file — check task_type, current_stage, stages_completed, readiness
3. Determine NEXT required stage from methodology.yaml
4. Read stage protocol
5. Execute ONLY that stage — produce ONLY artifacts for that stage
6. Update task frontmatter (current_stage, stages_completed, readiness, artifacts, status)
7. Git: stage and commit ALL changed files
8. VERIFY: re-read task file, confirm frontmatter correct
9. If more stages remain, go to step 3
10. When all stages complete: status=done, readiness=100
11. Update _index.md (move to Completed table)
12. Report: write completion note to wiki/log/
13. Check end condition — if not met, go to step 1
14. Final: commit remaining changes, print summary

### Stage Enforcement

- MUST NOT skip stages
- MUST NOT advance until: artifacts produced, committed, frontmatter updated, gate passes
- MUST NOT mark done unless: ALL stages in stages_completed, ALL Done When items verified, readiness=100

### Task Frontmatter Fields (Required)

```yaml
status: in-progress  # draft | active | in-progress | review | done
task_type: task       # docs | spike | task | bug | refactor
current_stage: scaffold
readiness: 50
stages_completed: [scaffold]
artifacts:
  - path/to/file.ts
```

### Git Management

- ONE COMMIT PER STAGE (not per task)
- COMMIT IMMEDIATELY after creating files
- NEVER destructive git commands without git status first
- Conventional commit messages: feat(wiki): T0XX stage-name — description

### Quality Gates Per Stage

- Document: wiki page exists with Summary + gap analysis
- Design: decision doc exists, config shape defined, types sketched IN DOCS
- Scaffold: types compile, .env entries added, empty test files exist
- Implement: code compiles, lint passes
- Test: scoped tests pass, no regressions

### What You Must Never Do

- Paraphrase operator directives
- Break upstream compatibility
- Skip stages
- Mark task done when stages incomplete
- Mark epic/module done (max "review")
- Set epic readiness manually
- Commit code that doesn't compile
- Leave files uncommitted
- Run destructive git commands without checking status
- Create files without reading existing code first
