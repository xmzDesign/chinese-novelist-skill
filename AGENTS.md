# Novel Harness Agent Contract

This repository is governed by Novel Harness. Codex must follow this file before writing or reporting novel work.

## Hard Flow

Use this order for every chapter:

```text
read task -> contract -> draft -> humanize -> post-draft hook -> QA -> fix -> recheck -> pre-mark-pass hook -> mark_pass -> session-close hook
```

Before claiming the whole novel is complete, run the stop hook.

## Required Commands

After drafting or revising a chapter:

```bash
python scripts/novel_hook_guard.py post-draft <project-dir> --chapter <chapter-number>
```

Before writing `status: "completed"`:

```bash
python scripts/novel_hook_guard.py pre-mark-pass <project-dir> --chapter <chapter-number>
```

Before final completion:

```bash
python scripts/novel_hook_guard.py stop <project-dir>
```

Before pausing or ending a session:

```bash
python scripts/novel_hook_guard.py session-close <project-dir> --note "<short note>"
```

## Completion Gate

A chapter is not complete unless all are true:

- chapter file exists and reaches the word count threshold
- QA report exists
- `qaStatus == "pass"`
- `antiAiStatus == "pass"`
- literary score reaches the configured threshold
- `readerHookStatus == "pass"`
- reader hook score reaches the configured threshold
- `endingStrategy` is valid
- `formulaicIssues` is empty
- `satisfactionBeats` is non-empty and `shuangwenStatus == "pass"`
- `reviewRoundCount >= requiredReviewPasses`
- `repairRequired == false`
- `needsRecheck == false`
- `lastFailureCodes` is empty
- `pre-mark-pass` hook passes

The whole novel is not complete unless:

- every chapter is `completed` or `blocked`
- project validation has no error
- stop hook passes
- blocked chapters are explicitly reported as risks

## If A Hook Fails

Do not ask the user whether to continue. Follow the hook's `Next action` and continue the flow.

## References

- [SKILL.md](SKILL.md)
- [phase3-writing.md](references/flows/phase3-writing.md)
- [phase4-validation.md](references/flows/phase4-validation.md)
- [hook-lifecycle.md](references/flows/hook-lifecycle.md)
- [novel-hooks.md](references/guides/novel-hooks.md)
