#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Install Novel Harness runtime files into a target repository.

This mirrors by-harness style initialization: root contracts plus Claude/Codex hooks.
"""

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


SOURCE_ROOT = Path(__file__).resolve().parents[1]

RUNTIME_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    ".claude/hooks/context-injector.py",
    ".claude/hooks/novel-flow-post-tool.py",
    ".claude/hooks/novel-flow-stop.py",
    ".codex/config.toml",
    ".codex/hooks/context-injector.py",
    ".codex/hooks/novel-flow-post-tool.py",
    ".codex/hooks/novel-flow-stop.py",
    "scripts/check_chapter_wordcount.py",
    "scripts/validate_novel_project.py",
    "scripts/novel_hook_guard.py",
    "scripts/novel_runtime_hook.py",
    "scripts/smoke_novel_flow.py",
]

JSON_RUNTIME_FILES = [
    ".claude/settings.json",
    ".codex/hooks.json",
]


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object, returning an empty object if missing."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, ValueError):
        return {}


def hook_group_signature(group: dict[str, Any]) -> str:
    """Return a stable signature for hook group de-duplication."""
    matcher = str(group.get("matcher", ""))
    hooks = group.get("hooks", [])
    commands = []
    if isinstance(hooks, list):
        for hook in hooks:
            if isinstance(hook, dict):
                commands.append(str(hook.get("command", "")))
    return matcher + "::" + "||".join(commands)


def merge_json_file(src: Path, dst: Path) -> str:
    """Merge settings/hooks JSON while preserving existing entries."""
    incoming = load_json(src)
    existing = load_json(dst)

    if "permissions" in incoming:
        existing.setdefault("permissions", {})
        for key in ("allow", "deny"):
            values = incoming.get("permissions", {}).get(key, [])
            if not isinstance(values, list):
                continue
            current = existing["permissions"].setdefault(key, [])
            if not isinstance(current, list):
                current = []
                existing["permissions"][key] = current
            for value in values:
                if value not in current:
                    current.append(value)

    incoming_hooks = incoming.get("hooks", {})
    if isinstance(incoming_hooks, dict):
        existing.setdefault("hooks", {})
        if not isinstance(existing["hooks"], dict):
            existing["hooks"] = {}
        for event_name, groups in incoming_hooks.items():
            if not isinstance(groups, list):
                continue
            current_groups = existing["hooks"].setdefault(event_name, [])
            if not isinstance(current_groups, list):
                current_groups = []
                existing["hooks"][event_name] = current_groups
            signatures = {
                hook_group_signature(group)
                for group in current_groups
                if isinstance(group, dict)
            }
            for group in groups:
                if not isinstance(group, dict):
                    continue
                signature = hook_group_signature(group)
                if signature not in signatures:
                    current_groups.append(group)
                    signatures.add(signature)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return "merged"


def copy_file(src: Path, dst: Path, force: bool) -> str:
    """Copy a runtime file, respecting force."""
    if dst.exists() and not force:
        return "skipped"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return "copied" if not dst.exists() else "updated"


def install(target_dir: Path, force: bool) -> list[tuple[str, str]]:
    """Install runtime files into target_dir."""
    results: list[tuple[str, str]] = []
    target_dir = target_dir.resolve()

    for rel in RUNTIME_FILES:
        src = SOURCE_ROOT / rel
        dst = target_dir / rel
        if not src.exists():
            results.append((rel, "missing-source"))
            continue
        results.append((rel, copy_file(src, dst, force)))

    for rel in JSON_RUNTIME_FILES:
        src = SOURCE_ROOT / rel
        dst = target_dir / rel
        if not src.exists():
            results.append((rel, "missing-source"))
            continue
        results.append((rel, merge_json_file(src, dst)))

    for rel in [
        ".claude/hooks/context-injector.py",
        ".claude/hooks/novel-flow-post-tool.py",
        ".claude/hooks/novel-flow-stop.py",
        ".codex/hooks/context-injector.py",
        ".codex/hooks/novel-flow-post-tool.py",
        ".codex/hooks/novel-flow-stop.py",
        "scripts/check_chapter_wordcount.py",
        "scripts/validate_novel_project.py",
        "scripts/novel_hook_guard.py",
        "scripts/novel_runtime_hook.py",
        "scripts/smoke_novel_flow.py",
    ]:
        path = target_dir / rel
        if path.exists():
            path.chmod(path.stat().st_mode | 0o755)

    return results


def main() -> int:
    """CLI entry."""
    parser = argparse.ArgumentParser(description="初始化 Novel Harness Claude/Codex hook runtime")
    parser.add_argument("--target-dir", default=".", help="目标仓库目录")
    parser.add_argument("--force", action="store_true", help="覆盖普通文件；JSON hook 配置仍采用合并")
    args = parser.parse_args()

    results = install(Path(args.target_dir), args.force)
    print("Novel Harness runtime initialized:")
    for rel, status in results:
        print(f"- {status}: {rel}")
    print("\nNext:")
    print("1. Read AGENTS.md / CLAUDE.md")
    print("2. Run: python scripts/smoke_novel_flow.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
