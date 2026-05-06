# 第三阶段：Novel Harness 章节创作

**重要：全程无需再次向用户确认，必须逐章推进直到全稿完成。**

进入本阶段后，所有章节都按轻量 Novel Harness 闭环执行：

```text
read task -> contract -> draft -> humanize -> qa -> fix -> recheck -> mark_pass -> session_close
```

多 Agent 角色边界详见 [novel-harness-agents.md](../agents/novel-harness-agents.md)。
Hook 生命周期详见 [hook-lifecycle.md](hook-lifecycle.md)，章节写完、标记通过和会话收口都必须运行 hook。

---

## 0. 启动检测与模式读取

开始创作前：

1. 读取 `02-写作计划.json`
2. 读取 `writingMode` 字段，进入对应模式流程
3. 检查每章是否有 `contractPath`、`qaReportPath`、`summaryPath`
4. 如果存在 `status: "in_progress"` 或 `"in_revision"` 的章节，从该章节继续
5. 如果存在 `status: "failed"`、`repairRequired: true` 且 `repairRound < maxAutoRepairRounds` 的章节，优先修复
6. 如果所有章节 `status: "pending"`，从第 1 章开始

状态含义：

| 状态 | 含义 |
|---|---|
| `pending` | 尚未开始 |
| `in_progress` | 正在写初稿或润色 |
| `in_qa` | 已写完，等待 QA |
| `in_revision` | QA 未通过，正在定向修复 |
| `completed` | QA 通过，可进入后续章节 |
| `failed` | 本轮 QA 失败，等待修复 |
| `blocked` | 超过 3 轮仍未通过，留待最终报告 |

---

## 1. 章节 Sprint（通用，所有模式共用）

每章必须执行完整 sprint。章节未通过 QA 前，不得标记 `completed`。

如果章节 `repairRequired == true` 且 `lastFailureCodes` 非空，说明已有明确失败项。此时跳过 draft 和 humanize，直接进入 Step 6 做定向修复。

如果章节 `needsRecheck == true`，说明修复已完成但尚未复检。此时跳过 draft 和 humanize，直接进入 Step 5，对当前章节正文重新执行三轮 QA。

### Step 1：read task

1. 读取 `02-写作计划.json`，确定待处理章节
2. 读取该章 `contractPath`
3. 读取 `01-大纲.md` 中对应章节规划
4. 读取 `00-人物档案.md` 中本章出场人物设定
5. 读取上一章 `summaryPath`（第 1 章除外）
6. 读取下一章规划，确认本章结尾钩子要能承接
7. 如果当前章节为第 1-3 章，读取 `03-黄金三章.md` 和 [golden-three-chapters.md](../guides/golden-three-chapters.md)
8. 读取 [literary-quality-gate.md](../guides/literary-quality-gate.md)
9. 读取 [reader-hook-gate.md](../guides/reader-hook-gate.md)
10. 读取 [auto-repair-loop.md](../guides/auto-repair-loop.md)
11. 读取 [novel-hooks.md](../guides/novel-hooks.md)
12. 更新 `02-写作计划.json`：普通写作将本章 `status` 设为 `"in_progress"` 并填入 `owner`；若 `needsRecheck == true`，保持 `status: "in_qa"`，直接进入 Step 5

### Step 2：contract check

写作前自检章节契约：

- 核心事件是否清晰
- 承接上章是否明确
- 出场人物和场景列表是否完整
- 结尾钩子是否能连接下一章
- 用户特殊要求是否已写入契约
- 第1-3章的黄金三章专项是否完整
- 文学质量门槛是否写入契约：普通章节 `literaryScore >= 80`，第1-3章 `>= 85`
- 追读力门槛是否写入契约：普通章节 `readerHookScore >= 80`，第1-3章 `>= 85`
- 最低检测轮次是否写入契约：`reviewRoundCount >= 3`
- 自动修复复检规则是否写入契约：修复后必须作废旧结论并重新三轮检测

如契约缺失关键信息，主 Agent 直接从大纲和人物档案补齐契约，不向用户确认。

第1-3章额外检查：

| 章节 | 黄金角色 | 写作前必须确认 |
|---|---|---|
| 第1章 | 启示 | 主角共鸣特性、当前生活、长钉子、未来展望 |
| 第2章 | 转折 | 第1章长钉子如何引爆、重大损失风险、不得不行动的理由 |
| 第3章 | 小高潮 | 主角主动出手、有限胜利、心理打脸或局部兑现、更大期待 |

### Step 3：draft

创建章节文件，文件名使用 `02-写作计划.json` 的 `filePath`。

写作要求：

- 使用 [chapter-template.md](../guides/chapter-template.md) 结构
- 按契约中的章首引子类型写 50-150 字引子
- 正文第一段使用 [chapter-guide.md](../guides/chapter-guide.md) 十种开头技巧之一
- 严格完成契约中的核心事件和场景列表
- 每章必须达到 3000-5000 个汉字
- 全章至少 2 个张力波峰
- 每章至少 1 个读者预期外的信息、行动或反转
- 对话必须推进情节、暴露关系或制造冲突
- 人物行为和语气必须符合 `00-人物档案.md`
- 结尾必须按契约设置悬念钩子
- 每章必须设计至少 1 个 `memorableMoment`
- 每章必须设计明确的 `chapterTurnPageHook`
- 题材允许时加入幽默、反差、嘴损、误会、尴尬或荒诞感；严肃题材也要有克制的可读性调味

前三章专项要求：

- 第1章必须聚焦主角，减少无关人物，明确故事风格和路线
- 第1章必须埋下能在第2章引爆的长钉子
- 第2章必须让转折足够大，大到主角可能失去重要之物
- 第2章必须强化主角行动理由，不能只让主角被动挨打
- 第3章必须引发第一个小高潮，让主角主动出手
- 第3章只能给有限胜利，不能直接解决主线或让主角无敌
- 前三章必须避免低级错误：人名、时间、视角、设定、动机不能混乱

写完后运行字数检查：

```bash
python scripts/check_chapter_wordcount.py <章节文件路径>
```

字数不足时，参考 [content-expansion.md](../guides/content-expansion.md) 扩写；禁止用空泛抒情灌水。

### Step 4：humanize

按 [literary-quality-gate.md](../guides/literary-quality-gate.md) 做反 AI 润色：

- 删除过度修饰的形容词和抽象抒情
- 用动作、对话、物件、场景细节替代总结性判断
- 打散过密的四字词和工整排比
- 调整句长节奏，避免每段同样长度
- 让人物对话带有个人习惯和潜台词
- 检查不同角色台词是否同质化
- 检查是否用解释替代表演
- 检查是否有低级连续性错误
- 检查是否缺少本题材爽点或有效冲突

润色不得改变契约中的核心事件、人物动机、伏笔和结尾钩子。

润色后再次运行字数检查。

润色和字数检查通过后，必须运行 post-draft hook：

```bash
python scripts/novel_hook_guard.py post-draft ./chinese-novelist/项目文件夹 --chapter <章节号>
```

post-draft hook 失败时，不得进入下一章，不得声称章节完成；必须按输出的 `Next action` 修复。

### Step 5：qa

将本章 `status` 更新为 `"in_qa"`，按 [qa-report-template.md](../guides/qa-report-template.md) 生成 `qaReportPath`。

Evaluator 只读取：

1. 当前章节契约
2. 当前章节正文
3. `00-人物档案.md`
4. `01-大纲.md` 对应章节规划
5. 上一章摘要
6. 下一章规划
7. 用户特殊要求和偏好中的 `dislikes`
8. 第1-3章还必须读取 `03-黄金三章.md`
9. [literary-quality-gate.md](../guides/literary-quality-gate.md)
10. [reader-hook-gate.md](../guides/reader-hook-gate.md)
11. [auto-repair-loop.md](../guides/auto-repair-loop.md)
12. [novel-hooks.md](../guides/novel-hooks.md)

评分规则来自章节契约：

- `PASS`：总分 >= 85，且无阻塞项
- `PARTIAL`：总分 70-84，或存在非阻塞失败项
- `FAIL`：总分 < 70，或存在任一阻塞项

Evaluator 必须提供证据和可执行修复建议；禁止只写主观感受。

反 AI 与文学质量规则：

- `antiAiStatus == "fail"` 时，不得 `PASS`
- 普通章节 `literaryScore < 80` 时，不得 `PASS`
- 第1-3章 `literaryScore < 85` 时，不得 `PASS`
- 每个 AI 痕迹问题必须使用 `A-XX` 编号，并写清位置、为什么像 AI、修复建议

读者钩子规则：

- `readerHookStatus == "fail"` 时，不得 `PASS`
- 普通章节 `readerHookScore < 80` 时，不得 `PASS`
- 第1-3章 `readerHookScore < 85` 时，不得 `PASS`
- `memorableMoment` 为空时，不得 `PASS`
- `chapterTurnPageHook` 为空时，不得 `PASS`
- 每个追读问题必须使用 `R-XX` 编号，并写清位置、为什么不吸引人、流失风险、修复建议

三轮检测规则：

1. Evaluator 必须连续执行至少 3 轮独立检测
2. 每轮都检查章节契约、反 AI、文学质量、读者钩子、黄金三章（如适用）
3. 最终结论采用保守聚合：任一轮出现阻塞失败，最终不得 `PASS`
4. `literaryScore` 与 `readerHookScore` 使用三轮最低分写入 JSON
5. `reviewRoundCount` 必须写入实际轮次，且不得低于 3
6. 如果本章刚经过修复，必须重新读取修复后的正文，三轮检测从第 1 轮重新开始

第1-3章如果黄金三章专项未通过，即使总分达到 85，也必须判定为 `FAIL` 或 `PARTIAL`，不得 `PASS`。

### Step 6：fix

如果 QA 未通过：

如果是从 `failed` 或 `in_revision` 断点恢复，且 `lastFailureCodes` 已存在，沿用现有失败项，不重复生成 QA 报告；直接从第 4 步开始。

1. 将章节 `status` 设为 `"in_revision"`
2. 从 QA 报告提取所有失败项编号，写入 `lastFailureCodes` 和 `blockingIssues`
3. 写入 `repairRequired: true`、`needsRecheck: false`
4. 如果 `repairRound >= maxAutoRepairRounds`，直接标记 `blocked`
5. 否则 `retryCount += 1`，`repairRound += 1`
6. Fix Writer 只读取 QA 报告中的失败项
7. 只修失败项，不改动已通过的核心事件、人物关系和结尾钩子
8. 修复完成后，将章节 `status` 设为 `"in_qa"`，写入 `needsRecheck: true` 和 `lastRepairAt`
9. 作废旧检测结论：`qaStatus`、`qualityScore`、`antiAiStatus`、`literaryScore`、`readerHookStatus`、`readerHookScore` 置为 `null`，`reviewRoundCount` 置为 `0`
10. 回到 Step 5，对修复后的正文重新执行至少 3 轮检测

A 类反 AI 问题修复要求：

- 空泛心理改成动作、物件、身体反应、短句台词
- AI 套话直接删除或换成具体事实，不做同义词替换
- 对话同质时，为角色区分句长、词汇、回避方式和攻击方式
- 设定解释过重时，拆进冲突、误会、道具、任务失败或人物争执
- 节奏太平时，增加选择、代价、误判或时间压力
- 爽点不足时，让主角赢一点，但付出代价或留下更大坑

R 类追读问题修复要求：

- 开场弱时，前 300 字加入行动、异常、冲突或强信息差
- 没亮点时，增加可复述桥段：反击、误会、反转、名台词
- 幽默弱时，从人物性格里生笑点，不插无关段子
- 主角不吸引时，让主角做一个有锋芒、有反差或有代价的选择
- 爽点不足时，给局部兑现，保留更大问题
- 结尾弱时，让危险更具体、奖励更近、秘密更反常

最多修复 3 轮。超过 3 轮仍不通过：

- 将章节 `status` 设为 `"blocked"`
- 在 QA 报告和 `progress/latest.txt` 写明原因
- 继续后续章节，最终报告中标注风险

自动修复循环伪代码：

```text
WHILE QA 未通过:
    写入失败项编号和修复指令
    IF repairRound >= maxAutoRepairRounds:
        status = "blocked"
        BREAK

    repairRound += 1
    Fix Writer 定向修复 lastFailureCodes
    作废旧 QA 字段
    reviewRoundCount = 0
    重新执行 Step 5 三轮检测
```

### Step 7：mark_pass

QA 通过后：

标记 `completed` 前必须先运行 pre-mark-pass hook：

```bash
python scripts/novel_hook_guard.py pre-mark-pass ./chinese-novelist/项目文件夹 --chapter <章节号>
```

pre-mark-pass hook 失败时，不得写入 `status: "completed"`，必须回到 QA、fix 或 recheck。

1. 写入 `summaries/第XX章.md`，摘要 300-500 字，包含核心事件、人物变化、伏笔、结尾钩子
2. 将摘要追加到 `01-大纲.md` 的“章节摘要”区
3. 更新 `02-写作计划.json`：
   - `status: "completed"`
   - `wordCount`
   - `wordCountPass`
   - `qaStatus: "pass"`
   - `qualityScore`
   - `antiAiStatus: "pass"`
   - `literaryScore`
   - `aiTraceIssues: []`
   - `readerHookStatus: "pass"`
   - `readerHookScore`
   - `memorableMoment`
   - `chapterTurnPageHook`
   - `humorBeat`
   - `highlightIssues: []`
   - `reviewRoundCount`
   - `requiredReviewPasses: 3`
   - `blockingIssues: []`
   - `repairRequired: false`
   - `needsRecheck: false`
   - `lastFailureCodes: []`
   - `repairRound`
   - `repairHistory`
   - `updatedAt`
4. 更新 `continuity/第XX章.md`，记录本章时间线、伏笔、人物关系变化

### Step 8：session_close

每章完成后，刷新：

- `progress/latest.txt`：最近完成章节、分数、下一章、未解决风险
- `progress/YYYY-MM.md`：追加本章完成记录

必须运行 session-close hook：

```bash
python scripts/novel_hook_guard.py session-close ./chinese-novelist/项目文件夹 --note "第<章节号>章 completed"
```

完成后立即读取 `02-写作计划.json`，认领下一章，不向用户确认。

---

## 2. 串行模式（writingMode: "serial"）

主 Agent 自己按章节顺序执行完整 sprint。

```text
WHILE 存在 status 非 completed/blocked 的章节:
    选择第一个 failed/in_revision/pending 章节；如果 needsRecheck == true，优先直接复检
    执行章节 sprint
所有章节完成或 blocked -> 进入第四阶段
```

串行模式也必须生成章节契约、QA 报告、摘要和进度快照。

---

## 3. 子Agent并行模式（writingMode: "subagent-parallel"）

核心机制：按故事弧分片，而不是机械按固定章节数切块。

### 主 Agent 流程

1. 从 `01-大纲.md` 识别故事弧：
   - 开端/设局
   - 对抗/升级
   - 中点反转
   - 高潮/真相逼近
   - 收束/终局
2. 将章节分配给不重叠的弧段，每段尽量连续
3. 为每段派生一个子 Agent，子 Agent 在自己弧段内串行执行章节 sprint
4. 子 Agent 只写自己的章节、QA 报告草稿、摘要草稿和连续性报告
5. 主 Agent 或 State Keeper 统一合并全局状态文件
6. 每个弧段完成后生成 `summaries/arc-[编号].md`
7. 后续弧段启动前必须读取前序弧段摘要

### 子 Agent prompt 模板

```text
你是 Novel Harness 的 Chapter Writer，负责第 {start} 章到第 {end} 章。

项目路径：{projectPath}
负责范围：第 {start} 章到第 {end} 章

工作方式：
1. 逐章读取章节契约、人物档案、大纲对应规划、上一章摘要和下一章规划。
2. 按章节 sprint 执行 draft -> humanize -> qa -> fix -> recheck。
3. 只创建或修改你负责的章节文件、qa/第XX章.md、summaries/第XX章.md、continuity/第XX章.md。
4. 不直接修改 02-写作计划.json。
5. 不直接修改 01-大纲.md 的章节摘要区。
6. 每章 QA 通过后，在最终报告中列出章节编号、字数、QA 分数、阻塞项。
7. 每章正文写完后运行 post-draft hook；提交通过结果前运行 pre-mark-pass hook。
8. 所有章节完成后生成本弧段摘要。

重要约束：
- 不要使用 AskUserQuestion，不要向用户确认任何事。
- 每章必须达到 3000 字以上。
- QA 失败时最多修复 3 轮；每次修复后必须重新三轮检测。
- Hook 失败时按 Next action 继续处理，不要绕过。
- 不要改写其他 Agent 负责的章节。
```

### 并发安全

- 子 Agent 写入范围必须不重叠。
- 全局状态只由主 Agent/State Keeper 合并。
- 如果某章依赖前序弧段的结果，但前序弧段尚未完成，当前弧段应等待或使用前序弧段摘要。

---

## 4. Agent Teams 模式（writingMode: "agent-teams"）

Agent Teams 模式仍遵守 Novel Harness 闭环，但可使用团队任务系统协调所有权。

### 主 Agent 流程

1. 使用 TeamCreate 创建写作团队
2. 创建角色：Story Planner、Chapter Writer、Evaluator、Continuity Editor、State Keeper
3. 使用 TaskCreate 为每章创建任务，任务内容包含 `contractPath`
4. 团队成员通过 TaskUpdate 认领章节
5. Chapter Writer 完成 draft/humanize
6. Evaluator 生成 QA 报告
7. Fix Writer 根据失败项修复
8. Evaluator 对修复后的章节重新三轮检测
9. State Keeper 运行 post-draft/pre-mark-pass/session-close hook 并合并摘要和状态
10. 所有章节完成后进入第四阶段

### 团队约束

- Task owner 是章节唯一写作者。
- Evaluator 不修改章节正文。
- State Keeper 是全局状态唯一写入者。
- 所有角色必须按 [novel-harness-agents.md](../agents/novel-harness-agents.md) 的边界执行。
