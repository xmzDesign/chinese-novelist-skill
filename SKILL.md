---
name: chinese-novelist
description: |
  分章节创作引人入胜的中文小说。支持各种题材（悬疑/言情/奇幻/科幻/历史等），支持10-50章长篇创作，每章3000-5000字，结尾设置悬念钩子。强调深度润色去除AI痕迹，验收失败自动修复并复检，确保文字自然流畅。
  当用户要求：写小说、创作故事、分章节写作、连续剧情、章节悬念、长篇小说时使用。
metadata:
  trigger: 创作中文小说、分章节故事、长篇小说创作
  source: 基于小说创作最佳实践设计
---

# Chinese Novelist: 中文小说创作助手

## 四大黄金法则

1. **展示而非讲述** - 用动作和对话表现，不要直接陈述
2. **冲突驱动剧情** - 每章必须有冲突或转折
3. **悬念承上启下** - 每章结尾必须留下钩子
4. **黄金三章留住读者** - 前三章必须完成启示、转折、小高潮

## 特性说明

- **黄金三章专项**：开篇三章按“启示 → 转折 → 小高潮”设计和验收
- **文学质量门禁**：反 AI 一票否决，章节必须达到最低文学质量分
- **追读力门禁**：每章必须有亮点、幽默/反差调味和明确追读钩子
- **三轮检测**：所有 QA 检测至少重复 3 轮，最终按保守聚合放行
- **中断续写**：自动检测未完成项目，从断点继续创作
- **Novel Harness 章节闭环**：每章执行 read task → contract → draft → QA → fix → recheck → mark_pass → session_close
- **Novel Hook 机制**：写完、放行、停止和收口前用 hook 拦截跳过 QA/优化/复检的问题
- **运行时初始化**：提供 `scripts/init_novel_harness.py`，生成 `AGENTS.md`、`CLAUDE.md`、`.claude/`、`.codex/`
- **自动修复复检**：验收失败自动定向修复，修复后作废旧结论并重新三轮检测
- **自动校验**：每章写完立即生成 QA 报告，最终再做全书验收
- **并行写作**（可选）：支持子Agent按故事弧并行写作，通过章节契约和 `02-写作计划.json` 协调状态

## Novel Harness 核心原则

1. **先契约后写作**：每章写作前必须存在 `chapter-contracts/第XX章.md`
2. **先 QA 后完成**：章节只有在 `qaStatus == "pass"` 且无阻塞项时，才能标记 `completed`
3. **先反 AI 后评分**：`antiAiStatus == "pass"` 且 `literaryScore` 达标后，才允许通过
4. **先追读后放行**：`readerHookStatus == "pass"`，有 `memorableMoment` 和 `chapterTurnPageHook`
5. **至少三轮检测**：`reviewRoundCount >= 3`，任一轮阻塞失败都不得通过
6. **修复后必须复检**：`repairRequired == false`、`needsRecheck == false`、`lastFailureCodes` 为空后才可收口
7. **Hook 失败即阻断**：`post-draft`、`pre-mark-pass`、`stop`、`session-close` 任一失败时，按 Next action 继续执行
8. **全局状态集中写入**：并行 Agent 不直接改 `01-大纲.md` 和 `02-写作计划.json`，由 Orchestrator/State Keeper 合并
9. **失败项定向修复**：修复阶段只处理 QA 报告中的失败项，最多 3 轮

## 核心流程

进入每个阶段时，先阅读对应的流程文档以获取详细执行指令。

### 第0步：初始化与偏好加载

读取用户偏好，检测未完成项目（中断续写），展示个性化欢迎。 → 详见 [phase0-initialization.md](references/flows/phase0-initialization.md)

### 第一阶段：三层递进式问答

通过递进式问答收集创作需求，确定小说定位与标题：

- **核心定位**（必答，Q1-Q3）：题材创意、主角设定、核心冲突 → 详见 [phase1-layer1-core.md](references/flows/phase1-layer1-core.md)
- **深度定制与规格**（Q4-Q8）：世界观、视角基调、核心主题、读者定位、章节数量、配置确认 → 详见 [phase1-layer2-customize.md](references/flows/phase1-layer2-customize.md)
- **标题生成**：AI 基于创意元素生成候选标题，用户选择或自定义 → 详见 [phase1-layer3-title.md](references/flows/phase1-layer3-title.md)

### 第二阶段：规划 + 二次确认

创建项目文件夹（`./chinese-novelist/{timestamp}-{小说名称}/`），生成大纲、人物档案、黄金三章设计、章节契约和写作计划 JSON，等待用户确认。 → 详见 [phase2-planning.md](references/flows/phase2-planning.md)

### 第2.5步：写作模式选择

规划确认后，选择写作模式：
- **逐章串行**（`serial`）：主 Agent 自己逐章写，全程无中断
- **子Agent并行**（`subagent-parallel`）：将章节分成批次，派生子 Agent 并行写作
- **Agent Teams**（`agent-teams`）：Claude Code 多 Agent 协作模式，Agent 间可通讯（需手动开启）

→ 详见 [phase3-writing.md](references/flows/phase3-writing.md)

### 第三阶段：Novel Harness 创作（无需用户确认）
> 切记，一旦进入这个阶段，所有过程都禁止向用户确认。用户就是你的读者，你必须把完整的小说创作完成才能与用户报告

根据用户选择的写作模式（串行/并行/Teams）逐章执行 Novel Harness 章节 sprint。每章创作前必须读取章节契约、`01-大纲.md` 对应规划、`00-人物档案.md` 和上一章摘要；写完后必须运行 hook、QA、失败自动定向修复，修复后重新三轮检测。支持中断续写。 → 详见 [phase3-writing.md](references/flows/phase3-writing.md)

### 第四阶段：最终总验收（无需用户确认）

全程无需用户介入，汇总章节 QA、字数、状态、伏笔、时间线和人物弧线；未通过章节回到第三阶段最多修复 3 轮，并在每轮修复后重新发起检测。汇报完成前必须运行 stop hook。 → 详见 [phase4-validation.md](references/flows/phase4-validation.md)

## 共享机制

偏好系统、写作计划系统、黄金三章、章节契约、文学质量门禁、追读力门禁、三轮检测、自动修复复检、Novel Hook、QA 评分、进度收口、黄金法则、字数检查脚本和 flow smoke test 等跨阶段共享机制。 → 详见 [shared-infrastructure.md](references/flows/shared-infrastructure.md)

### 运行时初始化

如果目标仓库尚未配置 Claude/Codex hooks，先运行：

```bash
python scripts/init_novel_harness.py --target-dir .
```

该命令会初始化 `AGENTS.md`、`CLAUDE.md`、`.claude/settings.json`、`.codex/hooks.json` 和 hook 脚本。初始化后即使模型没有主动阅读流程文档，Stop hook 也会在汇报完成前拦截未 QA、未修复、未复检的项目。
