#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Novel runtime hook entrypoint.

Claude/Codex hook wrappers call this script so the actual gate logic stays in one place.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ACTIVE_PROJECT_STATUSES = {"planning", "in_progress", "validating", "completed_with_risks"}


def emit(payload: dict[str, Any]) -> None:
    """Emit hook JSON payload."""
    print(json.dumps(payload, ensure_ascii=False))


def read_payload() -> dict[str, Any]:
    """Read hook payload from stdin."""
    try:
        raw = sys.stdin.read() or "{}"
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, ValueError):
        return {}


def repo_root(cwd: Path) -> Path:
    """Find repository root, falling back to cwd."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
    except OSError:
        pass
    return cwd


def load_json(path: Path) -> dict[str, Any] | None:
    """Load JSON safely."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except (OSError, json.JSONDecodeError, ValueError):
        return None


def candidate_project_plans(root: Path) -> list[Path]:
    """Find candidate novel project plan files."""
    plans: list[Path] = []
    direct = root / "02-写作计划.json"
    if direct.exists():
        plans.append(direct)

    novel_root = root / "chinese-novelist"
    if novel_root.exists():
        plans.extend(novel_root.glob("*/02-写作计划.json"))

    deduped: list[Path] = []
    seen: set[str] = set()
    for plan in plans:
        key = str(plan.resolve())
        if key not in seen:
            seen.add(key)
            deduped.append(plan)
    return deduped


def find_active_project(root: Path) -> Path | None:
    """Pick the most relevant active novel project."""
    candidates: list[tuple[int, float, Path]] = []
    for plan_path in candidate_project_plans(root):
        plan = load_json(plan_path)
        if plan is None:
            continue
        status = str(plan.get("status", ""))
        priority = 0 if status in ACTIVE_PROJECT_STATUSES else 1
        try:
            mtime = plan_path.stat().st_mtime
        except OSError:
            mtime = 0
        candidates.append((priority, -mtime, plan_path.parent))

    if not candidates:
        return None
    candidates.sort()
    return candidates[0][2]


def run_guard(root: Path, project_dir: Path) -> dict[str, Any]:
    """Run novel_hook_guard stop and parse JSON output."""
    guard = root / "scripts" / "novel_hook_guard.py"
    if not guard.exists():
        return {
            "status": "fail",
            "issues": [
                {
                    "level": "error",
                    "code": "missing-hook-guard",
                    "message": f"缺少 hook guard 脚本: {guard}",
                }
            ],
            "nextAction": "恢复 scripts/novel_hook_guard.py 后重新执行 stop hook",
        }

    result = subprocess.run(
        [sys.executable, str(guard), "stop", str(project_dir), "--json"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    try:
        payload = json.loads(result.stdout)
        if isinstance(payload, dict):
            return payload
    except (json.JSONDecodeError, ValueError):
        pass

    return {
        "status": "fail",
        "issues": [
            {
                "level": "error",
                "code": "hook-guard-runtime-error",
                "message": result.stderr.strip() or result.stdout.strip() or "hook guard 执行失败",
            }
        ],
        "nextAction": "修复 hook guard 运行错误",
    }


def format_guard_failure(project_dir: Path, payload: dict[str, Any]) -> str:
    """Format guard result for a blocking hook reason."""
    lines = [
        "Novel Harness stop hook failed.",
        f"项目目录: {project_dir}",
        "",
        "发现以下阻塞项：",
    ]
    for issue in payload.get("issues", []):
        if not isinstance(issue, dict):
            continue
        if issue.get("level") != "error":
            continue
        lines.append(f"- {issue.get('code')}: {issue.get('message')}")
    next_action = payload.get("nextAction")
    if next_action:
        lines.extend(["", f"Next action: {next_action}"])
    lines.extend(["", "不得向用户汇报完成；请继续执行 Next action。"])
    return "\n".join(lines)


def handle_context(root: Path) -> None:
    """Inject lightweight execution context."""
    project_dir = find_active_project(root)
    lines = [
        "Novel Harness runtime active.",
        "Before novel work, read AGENTS.md/CLAUDE.md and follow read task -> draft -> hook -> QA -> fix -> recheck -> mark_pass.",
        "Never claim completion before the stop hook passes.",
    ]
    if project_dir is not None:
        lines.append(f"Active novel project: {project_dir}")
    emit({"systemMessage": "\n".join(lines)})


def handle_stop(root: Path, payload: dict[str, Any]) -> None:
    """Run final stop gate."""
    if bool(payload.get("stop_hook_active")):
        emit({})
        return

    project_dir = find_active_project(root)
    if project_dir is None:
        emit({})
        return

    guard_result = run_guard(root, project_dir)
    if guard_result.get("status") == "fail":
        emit({"decision": "block", "reason": format_guard_failure(project_dir, guard_result)})
        return

    emit({"systemMessage": f"Novel Harness stop hook passed for {project_dir}."})


def handle_post_tool(root: Path) -> None:
    """Inject reminder after writes; blocking is handled by stop hook."""
    project_dir = find_active_project(root)
    if project_dir is None:
        emit({})
        return
    emit(
        {
            "systemMessage": (
                f"Novel project detected: {project_dir}\n"
                "If a chapter was just written, run post-draft hook. "
                "Before completed, run pre-mark-pass hook. "
                "Before final answer, stop hook must pass."
            )
        }
    )


def main() -> int:
    """CLI entry."""
    parser = argparse.ArgumentParser(description="Novel Harness runtime hook")
    parser.add_argument("--mode", choices=["context", "post-tool", "stop"], required=True)
    args = parser.parse_args()

    payload = read_payload()
    root = repo_root(Path.cwd())

    if args.mode == "context":
        handle_context(root)
    elif args.mode == "post-tool":
        handle_post_tool(root)
    elif args.mode == "stop":
        handle_stop(root, payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
