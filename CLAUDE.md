# Novel Harness Claude Contract

Claude must follow Novel Harness for all novel creation work in this repository.

## Non-Negotiable Rule

Do not rely on memory or prose instructions alone. Use the configured hooks and scripts.

## Flow

```text
read task -> contract -> draft -> humanize -> post-draft hook -> QA -> fix -> recheck -> pre-mark-pass hook -> mark_pass -> session-close hook
```

Final completion requires:

```bash
python scripts/novel_hook_guard.py stop <project-dir>
```

## Hook Files

Claude hooks are configured in:

- `.claude/settings.json`
- `.claude/hooks/context-injector.py`
- `.claude/hooks/novel-flow-post-tool.py`
- `.claude/hooks/novel-flow-stop.py`

Codex hooks are configured in:

- `.codex/config.toml`
- `.codex/hooks.json`
- `.codex/hooks/context-injector.py`
- `.codex/hooks/novel-flow-post-tool.py`
- `.codex/hooks/novel-flow-stop.py`

The hook wrappers call [novel_runtime_hook.py](scripts/novel_runtime_hook.py), which then invokes [novel_hook_guard.py](scripts/novel_hook_guard.py).

## Completion Gate

Never mark a chapter or whole novel complete while any of these are true:

- QA report is missing
- `reviewRoundCount < 3`
- `antiAiStatus != "pass"`
- `readerHookStatus != "pass"`
- `endingStrategy` is missing or invalid
- `formulaicIssues` is not empty
- `satisfactionBeats` is empty
- `shuangwenStatus != "pass"`
- `repairRequired == true`
- `needsRecheck == true`
- `lastFailureCodes` is not empty
- stop hook fails

When a hook blocks, continue with the hook's `Next action`.
