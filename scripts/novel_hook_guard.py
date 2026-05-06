#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Novel Harness Hook Guard

为章节写作、标记完成、最终收口和会话收口提供轻量 hook 门禁。
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from check_chapter_wordcount import check_chapter
from validate_novel_project import validate_project


Issue = dict[str, str]


def add_issue(issues: list[Issue], level: str, code: str, message: str) -> None:
    """追加一条 hook 问题。"""
    issues.append({"level": level, "code": code, "message": message})


def load_plan(project_dir: Path, issues: list[Issue]) -> dict[str, Any] | None:
    """读取写作计划。"""
    plan_path = project_dir / "02-写作计划.json"
    if not plan_path.exists():
        add_issue(issues, "error", "missing-plan", f"缺少写作计划: {plan_path}")
        return None

    try:
        return json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_issue(issues, "error", "invalid-plan-json", f"写作计划 JSON 解析失败: {exc}")
        return None


def resolve_project_path(project_dir: Path, value: str | None) -> Path | None:
    """解析项目内相对路径。"""
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    return project_dir / path


def find_chapter(plan: dict[str, Any], chapter_number: int, issues: list[Issue]) -> dict[str, Any] | None:
    """按章节号定位章节记录。"""
    chapters = plan.get("chapters")
    if not isinstance(chapters, list):
        add_issue(issues, "error", "invalid-chapters", "写作计划 chapters 不是数组")
        return None

    for chapter in chapters:
        if isinstance(chapter, dict) and chapter.get("chapterNumber") == chapter_number:
            return chapter

    add_issue(issues, "error", "chapter-not-found", f"未找到第{chapter_number}章")
    return None


def harness_config(plan: dict[str, Any]) -> dict[str, int]:
    """读取门槛配置，并提供默认值。"""
    harness = plan.get("harness") or {}
    return {
        "minWords": int(plan.get("minWordsPerChapter", 3000)),
        "passScore": int(harness.get("passScore", 85)),
        "literaryPassScore": int(harness.get("literaryPassScore", 80)),
        "goldenThreeLiteraryPassScore": int(harness.get("goldenThreeLiteraryPassScore", 85)),
        "readerHookPassScore": int(harness.get("readerHookPassScore", 80)),
        "goldenThreeReaderHookPassScore": int(harness.get("goldenThreeReaderHookPassScore", 85)),
        "requiredReviewPasses": int(harness.get("requiredReviewPasses", 3)),
    }


def require_existing_path(
    project_dir: Path,
    chapter: dict[str, Any],
    field_name: str,
    label: str,
    issues: list[Issue],
) -> Path | None:
    """检查章节记录中的路径字段是否存在。"""
    path = resolve_project_path(project_dir, chapter.get(field_name))
    chapter_label = f"第{chapter.get('chapterNumber')}章"
    if path is None:
        add_issue(issues, "error", f"missing-{field_name}", f"{chapter_label} 缺少 {field_name}")
        return None
    if not path.exists():
        add_issue(issues, "error", f"missing-{field_name}-file", f"{chapter_label} 缺少{label}: {path}")
        return None
    return path


def check_word_count(project_dir: Path, chapter: dict[str, Any], min_words: int, issues: list[Issue]) -> None:
    """检查章节正文是否达到最低字数。"""
    file_path = require_existing_path(project_dir, chapter, "filePath", "章节文件", issues)
    if file_path is None:
        return

    result = check_chapter(str(file_path), min_words)
    if result["status"] != "pass":
        add_issue(
            issues,
            "error",
            "word-count-fail",
            f"第{chapter.get('chapterNumber')}章字数 {result['word_count']}，低于 {min_words}",
        )


def run_post_draft(project_dir: Path, plan: dict[str, Any], chapter: dict[str, Any]) -> list[Issue]:
    """章节初稿后门禁：正文和契约必须具备，字数必须达标。"""
    issues: list[Issue] = []
    cfg = harness_config(plan)
    require_existing_path(project_dir, chapter, "contractPath", "章节契约", issues)
    check_word_count(project_dir, chapter, cfg["minWords"], issues)

    if chapter.get("status") == "pending":
        add_issue(issues, "warn", "status-not-advanced", "章节已写初稿但 status 仍为 pending，应更新为 in_progress 或 in_qa")
    if chapter.get("status") == "completed":
        add_issue(issues, "warn", "already-completed", "章节已 completed，post-draft hook 通常不需要再次运行")
    return issues


def run_pre_mark_pass(project_dir: Path, plan: dict[str, Any], chapter: dict[str, Any]) -> list[Issue]:
    """标记 completed 前门禁：QA、反 AI、追读力、三轮检测和修复状态必须全部通过。"""
    issues: list[Issue] = []
    cfg = harness_config(plan)
    number = chapter.get("chapterNumber")
    label = f"第{number}章"
    literary_threshold = cfg["goldenThreeLiteraryPassScore"] if number in {1, 2, 3} else cfg["literaryPassScore"]
    reader_threshold = cfg["goldenThreeReaderHookPassScore"] if number in {1, 2, 3} else cfg["readerHookPassScore"]

    require_existing_path(project_dir, chapter, "contractPath", "章节契约", issues)
    require_existing_path(project_dir, chapter, "qaReportPath", "QA 报告", issues)
    check_word_count(project_dir, chapter, cfg["minWords"], issues)

    checks: list[tuple[bool, str, str]] = [
        (chapter.get("qaStatus") == "pass", "qa-not-pass", f"{label} qaStatus 不是 pass"),
        (
            isinstance(chapter.get("qualityScore"), (int, float)) and chapter["qualityScore"] >= cfg["passScore"],
            "quality-score-low",
            f"{label} qualityScore 低于 {cfg['passScore']}",
        ),
        (chapter.get("antiAiStatus") == "pass", "anti-ai-not-pass", f"{label} antiAiStatus 不是 pass"),
        (
            isinstance(chapter.get("literaryScore"), (int, float)) and chapter["literaryScore"] >= literary_threshold,
            "literary-score-low",
            f"{label} literaryScore 低于 {literary_threshold}",
        ),
        (not chapter.get("aiTraceIssues"), "ai-traces-exist", f"{label} 仍存在 AI 痕迹问题"),
        (chapter.get("readerHookStatus") == "pass", "reader-hook-not-pass", f"{label} readerHookStatus 不是 pass"),
        (
            isinstance(chapter.get("readerHookScore"), (int, float)) and chapter["readerHookScore"] >= reader_threshold,
            "reader-hook-score-low",
            f"{label} readerHookScore 低于 {reader_threshold}",
        ),
        (bool(chapter.get("memorableMoment")), "missing-memorable-moment", f"{label} 缺少 memorableMoment"),
        (bool(chapter.get("chapterTurnPageHook")), "missing-turn-page-hook", f"{label} 缺少 chapterTurnPageHook"),
        (not chapter.get("highlightIssues"), "highlight-issues-exist", f"{label} 仍存在追读力问题"),
        (
            isinstance(chapter.get("reviewRoundCount"), int)
            and chapter["reviewRoundCount"] >= cfg["requiredReviewPasses"],
            "review-rounds-insufficient",
            f"{label} 检测轮次少于 {cfg['requiredReviewPasses']}",
        ),
        (not chapter.get("blockingIssues"), "blocking-issues-exist", f"{label} 仍存在阻塞项"),
        (chapter.get("repairRequired") is False, "repair-required", f"{label} repairRequired 未清空"),
        (chapter.get("needsRecheck") is False, "needs-recheck", f"{label} needsRecheck 未清空"),
        (not chapter.get("lastFailureCodes"), "failure-codes-exist", f"{label} lastFailureCodes 未清空"),
    ]

    for passed, code, message in checks:
        if not passed:
            add_issue(issues, "error", code, message)

    if number in {1, 2, 3} and chapter.get("goldenThreeRole") not in {"启示", "转折", "小高潮"}:
        add_issue(issues, "error", "missing-golden-role", f"{label} 缺少黄金三章角色")

    return issues


def run_stop(project_dir: Path, plan: dict[str, Any]) -> list[Issue]:
    """最终停止门禁：阻止未检查、未优化、未复检的项目被汇报为完成。"""
    issues: list[Issue] = []
    report = validate_project(project_dir)
    for issue in report.get("issues", []):
        if issue["level"] == "error":
            issues.append(issue)

    chapters = plan.get("chapters") or []
    for chapter in chapters:
        if not isinstance(chapter, dict):
            continue
        status = chapter.get("status")
        number = chapter.get("chapterNumber")
        if status not in {"completed", "blocked"}:
            add_issue(issues, "error", "chapter-not-terminal", f"第{number}章状态为 {status}，不得汇报全稿完成")
        if status == "blocked":
            continue
        if chapter.get("needsRecheck"):
            add_issue(issues, "error", "chapter-needs-recheck", f"第{number}章修复后尚未复检")
        if chapter.get("repairRequired"):
            add_issue(issues, "error", "chapter-repair-required", f"第{number}章仍需修复")

    return issues


def next_action(plan: dict[str, Any]) -> str:
    """根据写作计划推断下一步动作。"""
    chapters = plan.get("chapters") or []
    for chapter in chapters:
        if not isinstance(chapter, dict):
            continue
        number = chapter.get("chapterNumber")
        status = chapter.get("status")
        if status == "blocked":
            continue
        if chapter.get("needsRecheck"):
            return f"第{number}章 needsRecheck=true，重新执行三轮 QA"
        if chapter.get("repairRequired"):
            return f"第{number}章 repairRequired=true，按 lastFailureCodes 定向修复"
        if status in {"failed", "in_revision"}:
            return f"第{number}章处于 {status}，进入 fix -> recheck"
        if status == "in_qa":
            return f"第{number}章处于 in_qa，执行 QA 三轮检测"
        if status in {"pending", "in_progress"}:
            return f"继续第{number}章 sprint"
    return "所有章节已进入 completed/blocked，可执行 Phase 4 总验收或最终报告"


def run_session_close(project_dir: Path, plan: dict[str, Any], note: str | None) -> list[Issue]:
    """刷新 progress/latest.txt 和月度进度日志。"""
    issues: list[Issue] = []
    progress_dir = project_dir / "progress"
    progress_dir.mkdir(parents=True, exist_ok=True)

    chapters = [chapter for chapter in plan.get("chapters", []) if isinstance(chapter, dict)]
    completed = sum(1 for chapter in chapters if chapter.get("status") == "completed")
    blocked = sum(1 for chapter in chapters if chapter.get("status") == "blocked")
    now = datetime.now().isoformat(timespec="seconds")
    action = next_action(plan)
    latest = progress_dir / "latest.txt"
    content = [
        "# Novel Harness Latest Progress",
        "",
        f"updatedAt: {now}",
        f"novelName: {plan.get('novelName', '')}",
        f"projectStatus: {plan.get('status', '')}",
        f"completed: {completed}/{len(chapters)}",
        f"blocked: {blocked}",
        f"nextAction: {action}",
    ]
    if note:
        content.append(f"note: {note}")
    content.append("")
    latest.write_text("\n".join(content), encoding="utf-8")

    monthly = progress_dir / f"{datetime.now().strftime('%Y-%m')}.md"
    line = f"- {now} | completed {completed}/{len(chapters)} | blocked {blocked} | next: {action}"
    if note:
        line += f" | note: {note}"
    with monthly.open("a", encoding="utf-8") as file:
        file.write(line + "\n")

    add_issue(issues, "info", "session-close-written", f"已刷新 {latest}")
    return issues


def print_report(hook: str, issues: list[Issue], action: str | None, as_json: bool) -> None:
    """输出 hook 结果。"""
    errors = [issue for issue in issues if issue["level"] == "error"]
    payload = {
        "hook": hook,
        "status": "fail" if errors else "pass",
        "errors": len(errors),
        "issues": issues,
        "nextAction": action,
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(f"Novel Hook Guard [{hook}]: {payload['status'].upper()}")
    if action:
        print(f"Next action: {action}")
    for issue in issues:
        label = issue["level"].upper()
        print(f"- [{label}] {issue['code']}: {issue['message']}")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="执行 Novel Harness hook 门禁")
    parser.add_argument("hook", choices=["post-draft", "pre-mark-pass", "stop", "session-close"], help="hook 类型")
    parser.add_argument("project_dir", help="小说项目目录")
    parser.add_argument("--chapter", type=int, help="章节号，post-draft/pre-mark-pass 必填")
    parser.add_argument("--note", help="session-close 记录备注")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    issues: list[Issue] = []
    plan = load_plan(project_dir, issues)
    if plan is None:
        print_report(args.hook, issues, None, args.json)
        return 1

    if args.hook in {"post-draft", "pre-mark-pass"} and args.chapter is None:
        add_issue(issues, "error", "missing-chapter-arg", f"{args.hook} 必须传 --chapter")
        print_report(args.hook, issues, next_action(plan), args.json)
        return 1

    if args.hook == "post-draft":
        chapter = find_chapter(plan, args.chapter, issues)
        if chapter is not None:
            issues.extend(run_post_draft(project_dir, plan, chapter))
    elif args.hook == "pre-mark-pass":
        chapter = find_chapter(plan, args.chapter, issues)
        if chapter is not None:
            issues.extend(run_pre_mark_pass(project_dir, plan, chapter))
    elif args.hook == "stop":
        issues.extend(run_stop(project_dir, plan))
    elif args.hook == "session-close":
        issues.extend(run_session_close(project_dir, plan, args.note))

    print_report(args.hook, issues, next_action(plan), args.json)
    return 1 if any(issue["level"] == "error" for issue in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
