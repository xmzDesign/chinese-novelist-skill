#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Novel Harness 项目结构校验脚本

检查小说项目是否具备章节契约、QA 报告、摘要、连续性材料和写作计划状态。
该脚本只检查质量基准、场景卡、网文顶层设计、文学质量、追读力、Editor Gate 和自动修复复检字段是否达标，不直接判断正文文学质量。
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from check_chapter_wordcount import check_chapter


REQUIRED_DIRS = [
    "chapter-contracts",
    "qa",
    "summaries",
    "continuity",
    "progress",
]

VALID_STATUSES = {
    "pending",
    "in_progress",
    "in_qa",
    "in_revision",
    "completed",
    "failed",
    "blocked",
}

VALID_ENDING_STRATEGIES = {
    "payoff-close",
    "soft-question",
    "decision-point",
    "emotional-aftertaste",
    "resource-reveal",
    "relationship-shift",
    "threat-approach",
}

STRONG_SUSPENSE_ENDINGS = {
    "soft-question",
    "decision-point",
    "threat-approach",
}

WEB_NOVEL_REQUIRED_FIELDS = {
    "immersionAnchor": "代入锚点",
    "rationalizationNote": "合理化说明",
    "coreLoopStep": "Core Loop 步骤",
    "systemRuleUse": "系统/规则参与方式",
}


def add_issue(issues: list[dict[str, str]], level: str, code: str, message: str) -> None:
    """追加一条结构化问题记录。"""
    issues.append({"level": level, "code": code, "message": message})


def is_web_novel_enabled(plan: dict[str, Any]) -> bool:
    """仅在写作计划显式包含 webNovelDesign 时启用新增网文顶层门禁。"""
    config = plan.get("webNovelDesign")
    return isinstance(config, dict) and config.get("enabled", True) is not False


def is_quality_baseline_enabled(plan: dict[str, Any]) -> bool:
    """仅在写作计划显式包含 qualityBaseline 时启用质量基准文件校验。"""
    config = plan.get("qualityBaseline")
    return isinstance(config, dict) and config.get("enabled", True) is not False


def is_scene_card_enabled(plan: dict[str, Any]) -> bool:
    """仅在写作计划显式包含 sceneCardPolicy 时启用场景卡门禁。"""
    config = plan.get("sceneCardPolicy")
    return isinstance(config, dict) and config.get("enabled", True) is not False


def is_editor_gate_enabled(plan: dict[str, Any]) -> bool:
    """仅在写作计划显式包含 editorGate 时启用编辑审稿门禁。"""
    config = plan.get("editorGate")
    return isinstance(config, dict) and config.get("enabled", True) is not False


def load_plan(project_dir: Path, issues: list[dict[str, str]]) -> dict[str, Any] | None:
    """读取并解析 02-写作计划.json。"""
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
    """将写作计划中的相对路径解析为项目目录下的绝对路径。"""
    if not value:
        return None

    path = Path(value)
    if path.is_absolute():
        return path
    return project_dir / path


def check_required_dirs(project_dir: Path, issues: list[dict[str, str]]) -> None:
    """检查 Novel Harness 所需目录。"""
    for dirname in REQUIRED_DIRS:
        path = project_dir / dirname
        if not path.exists():
            add_issue(issues, "error", "missing-dir", f"缺少目录: {path}")
        elif not path.is_dir():
            add_issue(issues, "error", "not-dir", f"路径不是目录: {path}")


def check_golden_three_design(
    project_dir: Path,
    plan: dict[str, Any],
    chapters: list[dict[str, Any]],
    issues: list[dict[str, str]],
) -> None:
    """检查黄金三章设计文件和前三章角色字段。"""
    golden_three = plan.get("goldenThree") or {}
    if golden_three.get("enabled") is False:
        return

    design_path = resolve_project_path(project_dir, golden_three.get("designPath", "03-黄金三章.md"))
    if design_path is None or not design_path.exists():
        add_issue(issues, "error", "missing-golden-three", f"缺少黄金三章设计: {design_path or project_dir / '03-黄金三章.md'}")

    role_by_chapter = {1: "启示", 2: "转折", 3: "小高潮"}
    chapter_map = {chapter.get("chapterNumber"): chapter for chapter in chapters if isinstance(chapter, dict)}
    for number, expected_role in role_by_chapter.items():
        chapter = chapter_map.get(number)
        if chapter is None:
            continue
        role = chapter.get("goldenThreeRole")
        if role != expected_role:
            add_issue(
                issues,
                "warn",
                "golden-three-role-mismatch",
                f"第{number}章 goldenThreeRole 应为 {expected_role}，当前为 {role}",
            )


def check_web_novel_design(project_dir: Path, plan: dict[str, Any], issues: list[dict[str, str]]) -> None:
    """检查网文顶层设计文件是否存在。"""
    if not is_web_novel_enabled(plan):
        return

    config = plan.get("webNovelDesign") or {}
    design_path = resolve_project_path(project_dir, config.get("designPath", "04-网文顶层设计.md"))
    if design_path is None or not design_path.exists():
        add_issue(issues, "error", "missing-web-novel-design", f"缺少网文顶层设计: {design_path or project_dir / '04-网文顶层设计.md'}")


def check_quality_baseline(project_dir: Path, plan: dict[str, Any], issues: list[dict[str, str]]) -> None:
    """检查质量基准文件是否存在。"""
    if not is_quality_baseline_enabled(plan):
        return

    config = plan.get("qualityBaseline") or {}
    baseline_path = resolve_project_path(project_dir, config.get("baselinePath", "05-质量基准.md"))
    if baseline_path is None or not baseline_path.exists():
        add_issue(issues, "error", "missing-quality-baseline", f"缺少质量基准: {baseline_path or project_dir / '05-质量基准.md'}")


def check_scene_card_directory(project_dir: Path, plan: dict[str, Any], issues: list[dict[str, str]]) -> None:
    """检查场景卡目录是否存在。"""
    if not is_scene_card_enabled(plan):
        return

    config = plan.get("sceneCardPolicy") or {}
    directory = config.get("directory", "scene-cards")
    path = project_dir / str(directory)
    if not path.exists():
        add_issue(issues, "error", "missing-scene-card-dir", f"缺少场景卡目录: {path}")
    elif not path.is_dir():
        add_issue(issues, "error", "scene-card-not-dir", f"场景卡路径不是目录: {path}")


def check_ending_distribution(chapters: list[dict[str, Any]], issues: list[dict[str, str]]) -> None:
    """检查连续章节结尾策略是否过度同质化。"""
    completed = [
        chapter
        for chapter in sorted(chapters, key=lambda item: item.get("chapterNumber") or 0)
        if chapter.get("status") == "completed"
    ]

    previous_strategy: str | None = None
    previous_number: Any = None
    repeat_count = 0
    for chapter in completed:
        strategy = chapter.get("endingStrategy")
        number = chapter.get("chapterNumber")
        if not strategy:
            previous_strategy = None
            previous_number = None
            repeat_count = 0
            continue

        if strategy == previous_strategy:
            repeat_count += 1
            if strategy in STRONG_SUSPENSE_ENDINGS:
                add_issue(
                    issues,
                    "error",
                    "formulaic-strong-ending-repeat",
                    f"第{previous_number}章和第{number}章连续使用强悬念结尾策略 {strategy}",
                )
            if repeat_count >= 3:
                add_issue(
                    issues,
                    "error",
                    "formulaic-ending-repeat",
                    f"截至第{number}章连续 {repeat_count} 章使用同一结尾策略 {strategy}",
                )
        else:
            repeat_count = 1

        previous_strategy = strategy
        previous_number = number


def check_chapter_record(
    project_dir: Path,
    chapter: dict[str, Any],
    min_words: int,
    pass_score: int,
    literary_pass_score: int,
    golden_three_literary_pass_score: int,
    reader_hook_pass_score: int,
    golden_three_reader_hook_pass_score: int,
    required_review_passes: int,
    max_auto_repair_rounds: int,
    web_novel_enabled: bool,
    scene_card_enabled: bool,
    editor_gate_enabled: bool,
    editor_gate_pass_score: int,
    reader_loss_risks_must_be_empty: bool,
    issues: list[dict[str, str]],
) -> dict[str, Any]:
    """检查单章记录与相关文件。"""
    number = chapter.get("chapterNumber")
    label = f"第{number}章" if number is not None else "未知章节"
    status = chapter.get("status")
    result: dict[str, Any] = {
        "chapterNumber": number,
        "title": chapter.get("title"),
        "status": status,
        "wordCount": None,
        "wordCountPass": None,
        "qaStatus": chapter.get("qaStatus"),
        "qualityScore": chapter.get("qualityScore"),
        "antiAiStatus": chapter.get("antiAiStatus"),
        "literaryScore": chapter.get("literaryScore"),
        "readerHookStatus": chapter.get("readerHookStatus"),
        "readerHookScore": chapter.get("readerHookScore"),
        "reviewRoundCount": chapter.get("reviewRoundCount"),
        "repairRequired": chapter.get("repairRequired"),
        "needsRecheck": chapter.get("needsRecheck"),
        "lastFailureCodes": chapter.get("lastFailureCodes"),
        "repairRound": chapter.get("repairRound", chapter.get("retryCount")),
        "endingStrategy": chapter.get("endingStrategy"),
        "sceneCardStatus": chapter.get("sceneCardStatus"),
        "webNovelStatus": chapter.get("webNovelStatus"),
        "shuangwenStatus": chapter.get("shuangwenStatus"),
        "editorGateStatus": chapter.get("editorGateStatus"),
        "editorGateScore": chapter.get("editorGateScore"),
    }

    if status not in VALID_STATUSES:
        add_issue(issues, "error", "invalid-status", f"{label} 状态非法: {status}")

    contract_path = resolve_project_path(project_dir, chapter.get("contractPath"))
    qa_path = resolve_project_path(project_dir, chapter.get("qaReportPath"))
    summary_path = resolve_project_path(project_dir, chapter.get("summaryPath"))
    file_path = resolve_project_path(project_dir, chapter.get("filePath"))
    scene_card_path = resolve_project_path(project_dir, chapter.get("sceneCardPath"))

    if contract_path is None:
        add_issue(issues, "error", "missing-contract-path", f"{label} 缺少 contractPath")
    elif not contract_path.exists():
        add_issue(issues, "error", "missing-contract", f"{label} 缺少章节契约: {contract_path}")

    if status in {"in_qa", "in_revision", "failed", "completed", "blocked"}:
        if file_path is None:
            add_issue(issues, "error", "missing-file-path", f"{label} 缺少 filePath")
        elif not file_path.exists():
            add_issue(issues, "error", "missing-chapter-file", f"{label} 缺少章节文件: {file_path}")

    if file_path is not None and file_path.exists():
        word_result = check_chapter(str(file_path), min_words)
        result["wordCount"] = word_result["word_count"]
        result["wordCountPass"] = word_result["status"] == "pass"
        planned_count = chapter.get("wordCount")
        if planned_count is not None and planned_count != word_result["word_count"]:
            add_issue(
                issues,
                "warn",
                "word-count-mismatch",
                f"{label} JSON 字数 {planned_count} 与脚本统计 {word_result['word_count']} 不一致",
            )

    if status in {"in_revision", "failed", "completed", "blocked"}:
        if qa_path is None:
            add_issue(issues, "error", "missing-qa-path", f"{label} 缺少 qaReportPath")
        elif not qa_path.exists():
            add_issue(issues, "error", "missing-qa-report", f"{label} 缺少 QA 报告: {qa_path}")

    if status in {"in_revision", "failed"}:
        failure_codes = chapter.get("lastFailureCodes") or []
        if chapter.get("repairRequired") is not True:
            add_issue(issues, "warn", "repair-required-not-set", f"{label} 处于 {status} 但 repairRequired 未设为 true")
        if not failure_codes:
            add_issue(issues, "warn", "missing-failure-codes", f"{label} 处于 {status} 但缺少 lastFailureCodes")

    if status == "completed":
        blocking_issues = chapter.get("blockingIssues") or []
        quality_score = chapter.get("qualityScore")
        qa_status = chapter.get("qaStatus")
        anti_ai_status = chapter.get("antiAiStatus")
        literary_score = chapter.get("literaryScore")
        literary_threshold = golden_three_literary_pass_score if number in {1, 2, 3} else literary_pass_score
        reader_hook_status = chapter.get("readerHookStatus")
        reader_hook_score = chapter.get("readerHookScore")
        reader_hook_threshold = golden_three_reader_hook_pass_score if number in {1, 2, 3} else reader_hook_pass_score
        review_round_count = chapter.get("reviewRoundCount")
        repair_required = chapter.get("repairRequired")
        needs_recheck = chapter.get("needsRecheck")
        last_failure_codes = chapter.get("lastFailureCodes") or []
        repair_round = chapter.get("repairRound", chapter.get("retryCount", 0))
        ending_strategy = chapter.get("endingStrategy")

        if file_path is None or not file_path.exists():
            add_issue(issues, "error", "completed-without-file", f"{label} 已 completed 但章节文件不存在")
        elif not result["wordCountPass"]:
            add_issue(issues, "error", "completed-word-count-fail", f"{label} 已 completed 但字数未达标")

        if qa_status != "pass":
            add_issue(issues, "error", "completed-qa-not-pass", f"{label} 已 completed 但 qaStatus 不是 pass")

        if not isinstance(quality_score, (int, float)) or quality_score < pass_score:
            add_issue(issues, "error", "completed-low-score", f"{label} 已 completed 但 qualityScore 低于 {pass_score}")

        if anti_ai_status != "pass":
            add_issue(issues, "error", "completed-anti-ai-not-pass", f"{label} 已 completed 但 antiAiStatus 不是 pass")

        if not isinstance(literary_score, (int, float)) or literary_score < literary_threshold:
            add_issue(
                issues,
                "error",
                "completed-literary-score-low",
                f"{label} 已 completed 但 literaryScore 低于 {literary_threshold}",
            )

        ai_trace_issues = chapter.get("aiTraceIssues") or []
        if ai_trace_issues:
            add_issue(issues, "error", "completed-with-ai-traces", f"{label} 已 completed 但仍有 AI 痕迹问题")

        if reader_hook_status != "pass":
            add_issue(issues, "error", "completed-reader-hook-not-pass", f"{label} 已 completed 但 readerHookStatus 不是 pass")

        if not isinstance(reader_hook_score, (int, float)) or reader_hook_score < reader_hook_threshold:
            add_issue(
                issues,
                "error",
                "completed-reader-hook-score-low",
                f"{label} 已 completed 但 readerHookScore 低于 {reader_hook_threshold}",
            )

        if not chapter.get("memorableMoment"):
            add_issue(issues, "error", "completed-missing-memorable-moment", f"{label} 已 completed 但缺少 memorableMoment")

        if not chapter.get("chapterTurnPageHook"):
            add_issue(issues, "error", "completed-missing-turn-page-hook", f"{label} 已 completed 但缺少 chapterTurnPageHook/追读理由")

        if ending_strategy not in VALID_ENDING_STRATEGIES:
            add_issue(issues, "error", "completed-invalid-ending-strategy", f"{label} endingStrategy 非法或缺失: {ending_strategy}")

        if chapter.get("formulaicIssues"):
            add_issue(issues, "error", "completed-with-formulaic-issues", f"{label} 仍存在机械化结尾问题")

        if scene_card_enabled:
            if scene_card_path is None:
                add_issue(issues, "error", "completed-missing-scene-card-path", f"{label} 缺少 sceneCardPath")
            elif not scene_card_path.exists():
                add_issue(issues, "error", "completed-missing-scene-card", f"{label} 缺少场景卡: {scene_card_path}")
            if chapter.get("sceneCardStatus") != "pass":
                add_issue(issues, "error", "completed-scene-card-not-pass", f"{label} sceneCardStatus 不是 pass")
            if chapter.get("sceneCardIssues"):
                add_issue(issues, "error", "completed-with-scene-card-issues", f"{label} 仍存在场景卡问题")

        if web_novel_enabled:
            for field, description in WEB_NOVEL_REQUIRED_FIELDS.items():
                if not chapter.get(field):
                    add_issue(issues, "error", f"completed-missing-{field}", f"{label} 缺少 {field}/{description}")
            if chapter.get("webNovelStatus") != "pass":
                add_issue(issues, "error", "completed-web-novel-not-pass", f"{label} 网文顶层设计 webNovelStatus 不是 pass")
            if chapter.get("webNovelIssues"):
                add_issue(issues, "error", "completed-with-web-novel-issues", f"{label} 仍存在网文顶层设计问题")

        satisfaction_beats = chapter.get("satisfactionBeats") or []
        if not satisfaction_beats:
            add_issue(issues, "error", "completed-missing-satisfaction-beats", f"{label} 缺少 satisfactionBeats")
        if chapter.get("shuangwenStatus") != "pass":
            add_issue(issues, "error", "completed-shuangwen-not-pass", f"{label} 爽文专项 shuangwenStatus 不是 pass")
        if chapter.get("shuangwenIssues"):
            add_issue(issues, "error", "completed-with-shuangwen-issues", f"{label} 仍存在爽文专项问题")

        if editor_gate_enabled:
            editor_gate_score = chapter.get("editorGateScore")
            if chapter.get("editorGateStatus") != "pass":
                add_issue(issues, "error", "completed-editor-gate-not-pass", f"{label} editorGateStatus 不是 pass")
            if not isinstance(editor_gate_score, (int, float)) or editor_gate_score < editor_gate_pass_score:
                add_issue(
                    issues,
                    "error",
                    "completed-editor-gate-score-low",
                    f"{label} editorGateScore 低于 {editor_gate_pass_score}",
                )
            if reader_loss_risks_must_be_empty and chapter.get("readerLossRisks"):
                add_issue(issues, "error", "completed-with-reader-loss-risks", f"{label} 仍存在读者流失风险")
            if chapter.get("editorGateIssues"):
                add_issue(issues, "error", "completed-with-editor-gate-issues", f"{label} 仍存在 Editor Gate 问题")
            if chapter.get("revisionLevel") != "none":
                add_issue(issues, "error", "completed-revision-level-not-none", f"{label} revisionLevel 不是 none")

        highlight_issues = chapter.get("highlightIssues") or []
        if highlight_issues:
            add_issue(issues, "error", "completed-with-highlight-issues", f"{label} 已 completed 但仍有追读力问题")

        if not isinstance(review_round_count, int) or review_round_count < required_review_passes:
            add_issue(
                issues,
                "error",
                "completed-review-rounds-insufficient",
                f"{label} 已 completed 但检测轮次少于 {required_review_passes}",
            )

        if blocking_issues:
            add_issue(issues, "error", "completed-with-blockers", f"{label} 已 completed 但仍有阻塞项")

        if repair_required:
            add_issue(issues, "error", "completed-repair-required", f"{label} 已 completed 但 repairRequired 仍为 true")

        if needs_recheck:
            add_issue(issues, "error", "completed-needs-recheck", f"{label} 已 completed 但 needsRecheck 仍为 true")

        if last_failure_codes:
            add_issue(issues, "error", "completed-with-failure-codes", f"{label} 已 completed 但 lastFailureCodes 未清空")

        if isinstance(repair_round, int) and repair_round > max_auto_repair_rounds:
            add_issue(
                issues,
                "error",
                "completed-repair-rounds-exceeded",
                f"{label} 已 completed 但 repairRound 超过 {max_auto_repair_rounds}",
            )

        if number in {1, 2, 3} and chapter.get("goldenThreeRole") not in {"启示", "转折", "小高潮"}:
            add_issue(issues, "error", "completed-missing-golden-role", f"{label} 已 completed 但缺少黄金三章角色")

        if summary_path is None:
            add_issue(issues, "error", "missing-summary-path", f"{label} 缺少 summaryPath")
        elif not summary_path.exists():
            add_issue(issues, "error", "missing-summary", f"{label} 已 completed 但缺少摘要: {summary_path}")

    return result


def validate_project(project_dir: Path) -> dict[str, Any]:
    """执行 Novel Harness 项目校验。"""
    issues: list[dict[str, str]] = []
    project_dir = project_dir.resolve()

    if not project_dir.exists():
        add_issue(issues, "error", "missing-project", f"项目目录不存在: {project_dir}")
        return {"projectDir": str(project_dir), "issues": issues, "chapters": []}

    check_required_dirs(project_dir, issues)
    plan = load_plan(project_dir, issues)
    if plan is None:
        return {"projectDir": str(project_dir), "issues": issues, "chapters": []}

    min_words = int(plan.get("minWordsPerChapter", 3000))
    harness = plan.get("harness") or {}
    pass_score = int(harness.get("passScore", 85))
    literary_pass_score = int(harness.get("literaryPassScore", 80))
    golden_three_literary_pass_score = int(harness.get("goldenThreeLiteraryPassScore", 85))
    reader_hook_pass_score = int(harness.get("readerHookPassScore", 80))
    golden_three_reader_hook_pass_score = int(harness.get("goldenThreeReaderHookPassScore", 85))
    required_review_passes = int(harness.get("requiredReviewPasses", 3))
    max_auto_repair_rounds = int(harness.get("maxAutoRepairRounds", harness.get("maxRevisionRounds", 3)))
    web_novel_enabled = is_web_novel_enabled(plan)
    scene_card_enabled = is_scene_card_enabled(plan)
    editor_gate_enabled = is_editor_gate_enabled(plan)
    editor_gate = plan.get("editorGate") or {}
    editor_gate_pass_score = int(editor_gate.get("passScore", 85))
    reader_loss_risks_must_be_empty = editor_gate.get("readerLossRisksMustBeEmpty", True) is not False
    chapters = plan.get("chapters")

    if not isinstance(chapters, list):
        add_issue(issues, "error", "invalid-chapters", "写作计划 chapters 不是数组")
        chapters = []

    check_golden_three_design(project_dir, plan, chapters, issues)
    check_quality_baseline(project_dir, plan, issues)
    check_scene_card_directory(project_dir, plan, issues)
    check_web_novel_design(project_dir, plan, issues)
    check_ending_distribution([chapter for chapter in chapters if isinstance(chapter, dict)], issues)

    chapter_results = [
        check_chapter_record(
            project_dir,
            chapter,
            min_words,
            pass_score,
            literary_pass_score,
            golden_three_literary_pass_score,
            reader_hook_pass_score,
            golden_three_reader_hook_pass_score,
            required_review_passes,
            max_auto_repair_rounds,
            web_novel_enabled,
            scene_card_enabled,
            editor_gate_enabled,
            editor_gate_pass_score,
            reader_loss_risks_must_be_empty,
            issues,
        )
        for chapter in chapters
        if isinstance(chapter, dict)
    ]

    total = len(chapter_results)
    completed = sum(1 for item in chapter_results if item.get("status") == "completed")
    blocked = sum(1 for item in chapter_results if item.get("status") == "blocked")
    errors = sum(1 for item in issues if item["level"] == "error")
    warnings = sum(1 for item in issues if item["level"] == "warn")

    return {
        "projectDir": str(project_dir),
        "novelName": plan.get("novelName"),
        "totalChapters": total,
        "completedChapters": completed,
        "blockedChapters": blocked,
        "errors": errors,
        "warnings": warnings,
        "issues": issues,
        "chapters": chapter_results,
    }


def print_report(report: dict[str, Any]) -> None:
    """打印人类可读校验报告。"""
    print("\n" + "=" * 60)
    print("Novel Harness 项目校验报告")
    print("=" * 60)
    print(f"项目目录: {report['projectDir']}")
    if report.get("novelName"):
        print(f"小说名称: {report['novelName']}")
    print(
        f"章节: {report.get('completedChapters', 0)}/{report.get('totalChapters', 0)} completed"
        f" | blocked: {report.get('blockedChapters', 0)}"
        f" | errors: {report.get('errors', 0)}"
        f" | warnings: {report.get('warnings', 0)}"
    )

    issues = report.get("issues", [])
    if not issues:
        print("\nOK: 未发现结构问题")
        return

    print("\n问题列表:")
    for issue in issues:
        icon = "ERROR" if issue["level"] == "error" else "WARN"
        print(f"- [{icon}] {issue['code']}: {issue['message']}")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="校验 Novel Harness 小说项目结构")
    parser.add_argument("project_dir", help="小说项目目录")
    parser.add_argument("--json", action="store_true", help="输出 JSON 报告")
    args = parser.parse_args()

    report = validate_project(Path(args.project_dir))

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)

    return 1 if report.get("errors", 0) else 0


if __name__ == "__main__":
    sys.exit(main())
