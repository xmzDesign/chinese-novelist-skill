#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Novel Harness Flow Smoke Test

用临时 fixture 项目验证 hook guard 和项目校验脚本能拦住漏检、漏修、漏复检。
"""

import json
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HOOK_SCRIPT = ROOT / "scripts" / "novel_hook_guard.py"
VALIDATE_SCRIPT = ROOT / "scripts" / "validate_novel_project.py"


def chapter_text() -> str:
    """生成达到 smoke test 最低字数的章节正文。"""
    return "# 第01章 烟火\n\n" + "少年推开门，看见街口灯火忽明忽暗。朋友笑着骂他来晚了，他却盯住墙上的新刀痕，忽然明白今晚没人能安稳回家。"


def base_plan() -> dict[str, Any]:
    """返回一个最小可通过的写作计划。"""
    return {
        "version": 2,
        "novelName": "Smoke Novel",
        "projectPath": "",
        "totalChapters": 1,
        "minWordsPerChapter": 20,
        "maxWordsPerChapter": 5000,
        "status": "completed",
        "writingMode": "serial",
        "endingPolicy": {
            "avoidFormulaicEndings": True,
            "allowClosedChapterEndings": True,
        },
        "shuangwenConfig": {
            "cadence": "每章至少一次有效情绪兑现",
            "protagonistAdvantage": "有限优势",
        },
        "harness": {
            "maxRevisionRounds": 3,
            "qaReviewRounds": 3,
            "requiredReviewPasses": 3,
            "finalValidationRounds": 3,
            "autoRepairEnabled": True,
            "maxAutoRepairRounds": 3,
            "hooksEnabled": True,
            "hookGuardScript": "scripts/novel_hook_guard.py",
            "passScore": 85,
            "literaryPassScore": 80,
            "goldenThreeLiteraryPassScore": 85,
            "readerHookPassScore": 80,
            "goldenThreeReaderHookPassScore": 85,
            "stateWriter": "orchestrator",
        },
        "goldenThree": {
            "enabled": True,
            "designPath": "03-黄金三章.md",
            "chapters": [1, 2, 3],
        },
        "chapters": [
            {
                "chapterNumber": 1,
                "title": "烟火",
                "filePath": "第01章-烟火.md",
                "contractPath": "chapter-contracts/第01章.md",
                "qaReportPath": "qa/第01章.md",
                "summaryPath": "summaries/第01章.md",
                "continuityReportPath": "continuity/第01章.md",
                "goldenThreeRole": "启示",
                "status": "completed",
                "owner": None,
                "wordCount": 48,
                "wordCountPass": True,
                "qaStatus": "pass",
                "qualityScore": 90,
                "antiAiStatus": "pass",
                "literaryScore": 86,
                "aiTraceIssues": [],
                "readerHookStatus": "pass",
                "readerHookScore": 88,
                "memorableMoment": "主角从墙上刀痕意识到今晚的危机",
                "chapterTurnPageHook": "墙上的刀痕是谁留下的",
                "endingStrategy": "resource-reveal",
                "expectationPayoff": "兑现主角发现异常的观察力",
                "expectationNext": "刀痕背后的袭击者仍未现身",
                "satisfactionBeats": ["主角用刀痕反推袭击方向，让误判他的朋友当场闭嘴"],
                "formulaicIssues": [],
                "shuangwenStatus": "pass",
                "shuangwenIssues": [],
                "humorBeat": "朋友嘴损地骂主角来晚",
                "highlightIssues": [],
                "reviewRoundCount": 3,
                "requiredReviewPasses": 3,
                "blockingIssues": [],
                "repairRequired": False,
                "needsRecheck": False,
                "lastFailureCodes": [],
                "repairRound": 0,
                "repairHistory": [],
                "lastRepairAt": None,
                "retryCount": 0,
            }
        ],
    }


def write_project(project_dir: Path, plan: dict[str, Any], *, omit_qa: bool = False) -> None:
    """把写作计划和相关文件写入临时项目。"""
    for dirname in ["chapter-contracts", "qa", "summaries", "continuity", "progress"]:
        (project_dir / dirname).mkdir(parents=True, exist_ok=True)

    (project_dir / "00-人物档案.md").write_text("# 人物档案\n\n主角：少年，有锋芒。", encoding="utf-8")
    (project_dir / "01-大纲.md").write_text("# 大纲\n\n第1章：烟火。", encoding="utf-8")
    (project_dir / "03-黄金三章.md").write_text("# 黄金三章\n\n第1章启示。", encoding="utf-8")
    for chapter in plan["chapters"]:
        number = chapter["chapterNumber"]
        title = chapter["title"]
        chapter_no = f"第{number:02d}章"
        (project_dir / "chapter-contracts" / f"{chapter_no}.md").write_text(f"# {chapter_no}章节契约\n\n验收标准齐全。", encoding="utf-8")
        if not (omit_qa and number == 1):
            (project_dir / "qa" / f"{chapter_no}.md").write_text(f"# {chapter_no} QA 报告\n\nPASS。", encoding="utf-8")
        (project_dir / "summaries" / f"{chapter_no}.md").write_text(f"# {chapter_no}摘要\n\n主角发现刀痕。", encoding="utf-8")
        (project_dir / "continuity" / f"{chapter_no}.md").write_text(f"# {chapter_no}连续性\n\n刀痕伏笔。", encoding="utf-8")
        (project_dir / chapter["filePath"]).write_text(chapter_text().replace("第01章 烟火", f"{chapter_no} {title}"), encoding="utf-8")

    plan = deepcopy(plan)
    plan["projectPath"] = str(project_dir)
    (project_dir / "02-写作计划.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    """运行命令并返回结果。"""
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def assert_result(name: str, result: subprocess.CompletedProcess[str], should_pass: bool, expected_text: str | None = None) -> None:
    """断言命令结果符合预期。"""
    passed = result.returncode == 0
    if passed != should_pass:
        status = "PASS" if should_pass else "FAIL"
        raise AssertionError(
            f"{name}: expected {status}, got rc={result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    if expected_text and expected_text not in result.stdout:
        raise AssertionError(f"{name}: expected text {expected_text!r}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")


def make_blocked_plan() -> dict[str, Any]:
    """生成包含 blocked 章节的计划，stop hook 应允许 completed_with_risks。"""
    plan = base_plan()
    blocked_chapter = deepcopy(plan["chapters"][0])
    blocked_chapter.update(
        {
            "chapterNumber": 2,
            "title": "堵点",
            "filePath": "第02章-堵点.md",
            "contractPath": "chapter-contracts/第02章.md",
            "qaReportPath": "qa/第02章.md",
            "summaryPath": "summaries/第02章.md",
            "continuityReportPath": "continuity/第02章.md",
            "goldenThreeRole": "转折",
            "status": "blocked",
            "qaStatus": "fail",
            "qualityScore": 62,
            "blockingIssues": ["B-01"],
            "repairRequired": True,
            "lastFailureCodes": ["B-01"],
            "repairRound": 3,
            "retryCount": 3,
        }
    )
    plan["totalChapters"] = 2
    plan["status"] = "completed_with_risks"
    plan["chapters"].append(blocked_chapter)
    return plan


def make_formulaic_plan() -> dict[str, Any]:
    """生成连续强悬念结尾的计划，validate/stop 应拦截。"""
    plan = base_plan()
    second = deepcopy(plan["chapters"][0])
    second.update(
        {
            "chapterNumber": 2,
            "title": "回声",
            "filePath": "第02章-回声.md",
            "contractPath": "chapter-contracts/第02章.md",
            "qaReportPath": "qa/第02章.md",
            "summaryPath": "summaries/第02章.md",
            "continuityReportPath": "continuity/第02章.md",
            "goldenThreeRole": "转折",
            "endingStrategy": "threat-approach",
        }
    )
    plan["chapters"][0]["endingStrategy"] = "threat-approach"
    plan["totalChapters"] = 2
    plan["chapters"].append(second)
    return plan


def run_smoke_tests() -> None:
    """执行所有 smoke test case。"""
    with tempfile.TemporaryDirectory(prefix="novel-flow-smoke-") as tmp:
        tmp_root = Path(tmp)

        pass_dir = tmp_root / "fixture-pass"
        pass_dir.mkdir()
        write_project(pass_dir, base_plan())
        assert_result(
            "pass/pre-mark-pass",
            run_command([str(HOOK_SCRIPT), "pre-mark-pass", str(pass_dir), "--chapter", "1"]),
            True,
        )
        assert_result("pass/stop", run_command([str(HOOK_SCRIPT), "stop", str(pass_dir)]), True)
        assert_result("pass/validate", run_command([str(VALIDATE_SCRIPT), str(pass_dir)]), True)

        no_qa_dir = tmp_root / "fixture-no-qa"
        no_qa_dir.mkdir()
        no_qa_plan = base_plan()
        no_qa_plan["chapters"][0]["status"] = "in_qa"
        no_qa_plan["chapters"][0]["qaStatus"] = None
        write_project(no_qa_dir, no_qa_plan, omit_qa=True)
        assert_result(
            "no-qa/pre-mark-pass",
            run_command([str(HOOK_SCRIPT), "pre-mark-pass", str(no_qa_dir), "--chapter", "1"]),
            False,
            "missing-qaReportPath-file",
        )

        needs_recheck_dir = tmp_root / "fixture-needs-recheck"
        needs_recheck_dir.mkdir()
        needs_recheck_plan = base_plan()
        needs_recheck_plan["chapters"][0]["needsRecheck"] = True
        needs_recheck_plan["chapters"][0]["reviewRoundCount"] = 0
        write_project(needs_recheck_dir, needs_recheck_plan)
        assert_result(
            "needs-recheck/stop",
            run_command([str(HOOK_SCRIPT), "stop", str(needs_recheck_dir)]),
            False,
            "chapter-needs-recheck",
        )

        low_score_dir = tmp_root / "fixture-low-score"
        low_score_dir.mkdir()
        low_score_plan = base_plan()
        low_score_plan["chapters"][0]["qualityScore"] = 70
        low_score_plan["chapters"][0]["literaryScore"] = 70
        write_project(low_score_dir, low_score_plan)
        assert_result(
            "low-score/pre-mark-pass",
            run_command([str(HOOK_SCRIPT), "pre-mark-pass", str(low_score_dir), "--chapter", "1"]),
            False,
            "quality-score-low",
        )

        blocked_dir = tmp_root / "fixture-blocked"
        blocked_dir.mkdir()
        write_project(blocked_dir, make_blocked_plan())
        assert_result("blocked/stop", run_command([str(HOOK_SCRIPT), "stop", str(blocked_dir)]), True)

        satisfaction_missing_dir = tmp_root / "fixture-satisfaction-missing"
        satisfaction_missing_dir.mkdir()
        satisfaction_missing_plan = base_plan()
        satisfaction_missing_plan["chapters"][0]["satisfactionBeats"] = []
        write_project(satisfaction_missing_dir, satisfaction_missing_plan)
        assert_result(
            "satisfaction-missing/pre-mark-pass",
            run_command([str(HOOK_SCRIPT), "pre-mark-pass", str(satisfaction_missing_dir), "--chapter", "1"]),
            False,
            "missing-satisfaction-beats",
        )

        formulaic_dir = tmp_root / "fixture-formulaic"
        formulaic_dir.mkdir()
        write_project(formulaic_dir, make_formulaic_plan())
        assert_result(
            "formulaic/validate",
            run_command([str(VALIDATE_SCRIPT), str(formulaic_dir)]),
            False,
            "formulaic-strong-ending-repeat",
        )


def main() -> int:
    """命令行入口。"""
    try:
        run_smoke_tests()
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        return 1

    print("OK: Novel flow smoke tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
