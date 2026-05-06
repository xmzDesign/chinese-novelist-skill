# Novel Harness Agent Roles

本文件定义轻量 Novel Harness 的多 Agent 分工。执行时不要求一定派生真实子 Agent；在串行模式下，主 Agent 也必须按这些角色边界依次完成工作。

## Orchestrator

职责：
- 读取 `02-写作计划.json`，选择下一个可执行章节。
- 认领章节，更新 `owner`、`status`、`updatedAt`。
- 控制写作、QA、修复、收口的顺序。
- 如果验收失败，自动触发修复复检循环，不向用户确认。
- 在章节写完、标记通过、最终停止和会话收口前触发 Novel Hook。
- 在并行模式下只分配不重叠的故事弧或章节段。

只允许 Orchestrator 或 State Keeper 写入全局状态文件：
- `02-写作计划.json`
- `01-大纲.md` 的章节摘要区
- `progress/latest.txt`
- `progress/YYYY-MM.md`

## Story Planner

职责：
- 根据用户配置生成人物档案、大纲、故事弧分片。
- 为每章生成可验收的章节契约。
- 保证章节契约和 `02-写作计划.json` 的章节编号、标题、文件路径一致。

主要产物：
- `00-人物档案.md`
- `01-大纲.md`
- `chapter-contracts/第XX章.md`

## Chapter Writer

职责：
- 只写自己被分配的章节正文。
- 写作前读取章节契约、大纲对应行、人物档案、上一章摘要。
- 严格按契约完成核心事件、承接、冲突、人物行为和结尾钩子。

禁止：
- 禁止改写其他章节。
- 禁止直接修改全局状态文件。
- 禁止在未通过 QA 前自行标记 completed。

## Style Humanizer

职责：
- 对已完成初稿做去 AI 味修订。
- 删除空泛抒情、过度修饰、四字套话和模板化转折。
- 用动作、对话、具体感官细节替代抽象总结。

修订原则：
- 不改变章节契约中的核心事件和结尾钩子。
- 不牺牲人物一致性来追求漂亮句子。
- 不为了扩字数灌水。

## Continuity Editor

职责：
- 检查人物设定、时间线、地点、伏笔、关系变化。
- 对比上一章摘要和当前章节，确认承接成立。
- 对比下一章规划，确认结尾钩子可被承接。

主要产物：
- `continuity/第XX章.md`
- `continuity/timeline.md`（全书级）
- `continuity/foreshadowing-ledger.md`（全书级）
- `continuity/character-arcs.md`（全书级）

## Evaluator

职责：
- 只按章节契约、用户特殊要求和质量量表评分。
- 执行 [literary-quality-gate.md](../guides/literary-quality-gate.md) 的反 AI 门禁和文学质量评分。
- 执行 [reader-hook-gate.md](../guides/reader-hook-gate.md) 的追读力、幽默、亮点和章节钩子评分。
- 执行 [auto-repair-loop.md](../guides/auto-repair-loop.md) 的失败项编号和复检规则。
- 所有检测至少执行 3 轮，最终按保守聚合放行。
- 必须给出证据摘录或位置说明。
- 对失败项输出可执行修复指令。

禁止：
- 禁止按个人审美临时加标准。
- 禁止只写“文笔还可以”“节奏一般”这类不可修复评价。
- 禁止修改章节正文。

主要产物：
- `qa/第XX章.md`
- `qa/final-report.md`

## Fix Writer

职责：
- 只读取 QA 报告中的失败项并修复。
- 对 `A-XX` 反 AI 问题做定向修复，不做泛泛润色。
- 对 `R-XX` 追读力问题做定向修复，不靠硬塞段子补救。
- 保留已通过的核心事件、承接关系和结尾钩子。
- 每轮修复后交回 Evaluator 复评。
- 修复完成后不得自行标记通过，必须等待 Evaluator 重新三轮检测。

限制：
- 同一章节最多 3 轮修复。
- 阻塞项过多时可以整章重写，但必须记录原因。

## State Keeper

职责：
- 合并章节摘要草稿到 `summaries/` 和 `01-大纲.md`。
- 更新 `02-写作计划.json` 的 QA 字段、字数、状态和 retry 计数。
- QA 失败时写入 `repairRequired`、`lastFailureCodes`、`repairRound` 和 `repairHistory`。
- 修复完成后清空旧 QA 结论，写入 `needsRecheck: true`，并把 `reviewRoundCount` 重置为 0。
- 运行 `post-draft`、`pre-mark-pass`、`stop`、`session-close` hook，并按失败输出阻断状态流转。
- 写入 `progress/latest.txt` 和月度进度日志。

状态写入规则：
- `qaStatus == "pass"`、`antiAiStatus == "pass"`、`literaryScore` 达标、`readerHookStatus == "pass"`、`readerHookScore` 达标、`reviewRoundCount >= 3`、`repairRequired == false`、`needsRecheck == false`、`lastFailureCodes` 为空且无阻塞项时，才可将章节标记为 `completed`。
- `qaStatus == "fail"` 或存在阻塞项时，章节保持 `failed` 或 `in_revision`。
- 超过 3 轮仍失败时，记录为 `blocked`，进入最终报告。
