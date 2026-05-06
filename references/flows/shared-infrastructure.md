# 共享机制

本文件定义跨阶段共享的机制和规则。

---

## 黄金法则

1. **展示而非讲述** - 用动作和对话表现，不要直接陈述
2. **冲突驱动剧情** - 每章必须有冲突或转折
3. **期待承上启下** - 每章必须有追读理由，但结尾不必每章硬悬念
4. **黄金三章留住读者** - 前三章必须完成启示、转折、小高潮
5. **失败自动复检** - 验收失败必须定向修复，修复后重新三轮检测
6. **Hook 拦截偷懒** - 写完、放行、停止、收口都必须运行 Novel Hook
7. **爽文节拍可验收** - 所有小说都看情绪兑现和升级可见，不按固定爽点数量打卡

---

## 用户偏好系统

### 存储文件

`user-preferences.json`（项目根目录，首次使用后自动创建）

### 数据结构

```json
{
  "version": 1,
  "updatedAt": "2026-04-12",
  "preferences": {
    "favoriteGenres": [],
    "preferredProtagonist": "",
    "preferredPerspective": "",
    "preferredTone": "",
    "typicalChapterCount": null,
    "styleReferences": [],
    "dislikes": [],
    "creationHistory": []
  }
}
```

### 偏好更新规则

| 时机 | 行为 |
|------|------|
| 每完成一层问答 | 静默将本层回答同步到偏好文件（追加/更新，不删除历史） |
| 用户说"记住我的偏好" | 保存当前所有配置到偏好 |
| 用户说"忘记XX偏好" | 清除指定维度的偏好 |
| 用户说"重置偏好" | 清空所有偏好数据 |
| 一部长篇创作完成 | 将作品信息追加到 `creationHistory` |

### 偏好如何影响交互

1. **启动欢迎语**：有偏好时显示"欢迎回来！" + 个性化提示
2. **选项排序**：Q1中将 `favoriteGenres` 匹配项排前面
3. **常用标记**：Q5/Q8中对应用⭐标记"你的常用"/"上次选择"
4. **需求报告**：结合偏好给个性化建议（如"你之前喜欢悬疑+第三人称限制，这次要不要试试多视角？"）
5. **随机生成**：优先从偏好范围内随机选取，保持一致性
6. **风格参考追问**：优先推荐 `styleReferences` 中的作者

### 错误恢复

- **回退修改**：用户随时可说"回到QX"、"修改XX"，AI 回退到指定问题重新询问
- **中途暂存**：通过 `02-写作计划.json` 实现自动暂存；下次触发SKILL时 Phase 0 自动检测未完成项目，询问"继续上次的《XXX》？"
- **偏好文件损坏**：JSON解析失败时忽略偏好，使用默认值，并在后台修复文件

---

## 标题传递机制

### 传递方式

标题通过**对话上下文**在阶段间传递，不单独持久化到文件。

**传递链路**：
1. Phase 1 Layer 3：用户选择/确认标题 → 标题存入对话上下文
2. Phase 2：从上下文读取标题 → 写入项目目录名、`02-写作计划.json`、`01-大纲.md`

### 中断恢复

若会话在 Layer 3 完成、Phase 2 开始前中断：
- Phase 0 不会找到已创建的项目目录（因为 Phase 2 尚未执行）
- 用户将重新进入 Layer 3 重新选择标题（标题选择耗时很短，重新选择成本可接受）

## 写作计划系统

### 存储文件

`02-写作计划.json`（项目文件夹内，Phase 2 创建）

### 作用

- **进度跟踪**：记录每章创作状态（pending/in_progress/completed/failed）
- **写作模式**：记录用户选择的写作模式（serial/subagent-parallel/agent-teams）
- **章节契约**：记录每章 `contractPath`，让写作和 QA 使用同一套验收标准
- **QA 闭环**：记录 `qaReportPath`、`qaStatus`、`qualityScore`、`blockingIssues`
- **文学质量**：记录 `antiAiStatus`、`literaryScore`、`aiTraceIssues`
- **追读力**：记录 `readerHookStatus`、`readerHookScore`、`memorableMoment`、`chapterTurnPageHook`、`highlightIssues`
- **期待管理**：记录 `endingStrategy`、`expectationPayoff`、`expectationNext`、`formulaicIssues`
- **爽文专项**：记录 `satisfactionBeats`、`shuangwenStatus`、`shuangwenIssues`
- **三轮检测**：记录 `reviewRoundCount` 和 `requiredReviewPasses`
- **自动修复复检**：记录 `repairRequired`、`needsRecheck`、`lastFailureCodes`、`repairRound`、`repairHistory`
- **Hook 门禁**：记录 `hooksEnabled` 和 `hookGuardScript`，让写完、放行、停止、收口都有脚本拦截
- **黄金三章**：记录 `goldenThree` 和前三章 `goldenThreeRole`
- **中断续写**：Phase 0 读取 JSON 检测未完成项目，支持从断点继续
- **校验依据**：Phase 4 基于 JSON 校验章节闭环、字数、QA 和总体验收
- **并行协调**（可选）：多 Agent 并行写作时通过 owner、章节契约和状态避免冲突

### 与大纲的关系

- `01-大纲.md`：章节规划（核心事件、悬念钩子、承接上章、出场人物、场景列表）+ 章节摘要（连贯性参考）
- `chapter-contracts/第XX章.md`：从大纲派生的章节验收契约，是 Writer 和 Evaluator 的共同标准
- `02-写作计划.json`：章节状态、字数、QA、重试次数、写作模式（机器可读的进度跟踪）
- Phase 3 创作每章时必须读取章节契约、`01-大纲.md` 对应章节规划、`00-人物档案.md` 和上一章摘要
- 三者严格对应：JSON 中的 `chapterNumber`、`title`、`contractPath` 必须与大纲章节规划一致

### 推荐 JSON v2 字段

```json
{
  "version": 2,
  "writingMode": "serial",
  "endingPolicy": {
    "avoidFormulaicEndings": true,
    "allowClosedChapterEndings": true,
    "maxConsecutiveStrongSuspenseEndings": 1
  },
  "shuangwenConfig": {
    "enabledWhenContentModeIsShuangwen": true,
    "cadence": "每章至少一次有效情绪兑现，但不固定爽点数量"
  },
  "harness": {
    "maxRevisionRounds": 3,
    "qaReviewRounds": 3,
    "requiredReviewPasses": 3,
    "finalValidationRounds": 3,
    "autoRepairEnabled": true,
    "maxAutoRepairRounds": 3,
    "hooksEnabled": true,
    "hookGuardScript": "scripts/novel_hook_guard.py",
    "passScore": 85,
    "literaryPassScore": 80,
    "goldenThreeLiteraryPassScore": 85,
    "readerHookPassScore": 80,
    "goldenThreeReaderHookPassScore": 85,
    "stateWriter": "orchestrator"
  },
  "goldenThree": {
    "enabled": true,
    "designPath": "03-黄金三章.md",
    "chapters": [1, 2, 3]
  },
  "chapters": [
    {
      "chapterNumber": 1,
      "title": "章节标题",
      "filePath": "第01章-章节标题.md",
      "contractPath": "chapter-contracts/第01章.md",
      "qaReportPath": "qa/第01章.md",
      "summaryPath": "summaries/第01章.md",
      "continuityReportPath": "continuity/第01章.md",
      "goldenThreeRole": "启示",
      "status": "pending",
      "owner": null,
      "wordCount": null,
      "wordCountPass": null,
      "qaStatus": null,
      "qualityScore": null,
      "antiAiStatus": null,
      "literaryScore": null,
      "aiTraceIssues": [],
      "readerHookStatus": null,
      "readerHookScore": null,
      "memorableMoment": "",
      "chapterTurnPageHook": "",
      "endingStrategy": "resource-reveal",
      "expectationPayoff": "",
      "expectationNext": "",
      "satisfactionBeats": [],
      "formulaicIssues": [],
      "shuangwenStatus": null,
      "shuangwenIssues": [],
      "humorBeat": "",
      "highlightIssues": [],
      "reviewRoundCount": 0,
      "requiredReviewPasses": 3,
      "blockingIssues": [],
      "repairRequired": false,
      "needsRecheck": false,
      "lastFailureCodes": [],
      "repairRound": 0,
      "repairHistory": [],
      "lastRepairAt": null,
      "retryCount": 0
    }
  ]
}
```

### 状态流转

```text
pending -> in_progress -> in_qa -> completed
                         -> in_revision -> in_qa
                         -> failed -> in_revision
                         -> blocked
```

章节只有在以下条件同时满足时才能标记 `completed`：

- 章节文件存在
- 字数检查通过
- QA 报告存在
- `qaStatus == "pass"`
- `qualityScore >= 85`
- `antiAiStatus == "pass"`
- 普通章节 `literaryScore >= 80`
- 第1-3章 `literaryScore >= 85`
- `readerHookStatus == "pass"`
- 普通章节 `readerHookScore >= 80`
- 第1-3章 `readerHookScore >= 85`
- `memorableMoment` 非空
- `chapterTurnPageHook` 非空
- `endingStrategy` 合法
- `formulaicIssues` 为空
- `satisfactionBeats` 非空、`shuangwenStatus == "pass"`、`shuangwenIssues` 为空
- `highlightIssues` 为空
- `reviewRoundCount >= 3`
- `blockingIssues` 为空
- `repairRequired == false`
- `needsRecheck == false`
- `lastFailureCodes` 为空

### JSON 损坏处理

- JSON 解析失败时：提示用户，尝试从大纲的章节摘要区推断完成进度
- 章节状态丢失时：通过文件存在性和字数脚本重建状态

---

## 文学质量与反 AI 系统

参考：[literary-quality-gate.md](../guides/literary-quality-gate.md)

目标：

- 不依赖外部 AI 检测器
- 用文本证据判断 AI 痕迹
- 用文学质量评分约束最低可读性
- 用 A 类问题编号支持定向修复

核心字段：

| 字段 | 含义 |
|---|---|
| `antiAiStatus` | `pass` / `fail`，任一严重 AI 痕迹出现即 fail |
| `literaryScore` | 0-100，普通章节 >=80，第1-3章 >=85 |
| `aiTraceIssues` | A 类问题编号，如 `A-01`、`A-02` |

反 AI 一票否决项：

- 人物说话同质化
- 情绪全靠概括
- 空泛形容堆砌
- 四字套话过多
- 段落节奏模板化
- 解释替代表演
- 低级连续性错误
- 爽点或冲突缺席

章节只有 `antiAiStatus == "pass"` 且 `literaryScore` 达标时，才允许 `completed`。

---

## 追读理由与爽文系统

参考：[reader-hook-gate.md](../guides/reader-hook-gate.md)

目标：

- 每章都有能被读者记住的亮点
- 在题材允许范围内加入幽默、反差或轻松调味
- 每章至少有一次可感知的亮点或局部兑现
- 结尾有明确追读理由，但不强制每章都制造硬悬念
- 爽文专项强调憋屈释放、局部胜利、升级可见和下一步奖励

核心字段：

| 字段 | 含义 |
|---|---|
| `readerHookStatus` | `pass` / `fail` |
| `readerHookScore` | 0-100，普通章节 >=80，第1-3章 >=85 |
| `memorableMoment` | 本章最值得记住的桥段、台词、反转或爽点 |
| `chapterTurnPageHook` | 本章结尾驱动读者继续看的具体理由，不等于硬悬念 |
| `endingStrategy` | 结尾策略：兑现收束、软问题、选择点、情绪余味、资源揭示、关系变化、危险逼近等 |
| `expectationPayoff` | 本章已经兑现的期待 |
| `expectationNext` | 下一章承接的期待 |
| `satisfactionBeats` | 有效情绪兑现列表 |
| `formulaicIssues` | M 类机械化结尾问题 |
| `shuangwenStatus` | `pass` / `fail` / `null` |
| `shuangwenIssues` | S 类爽文专项问题 |
| `humorBeat` | 本章幽默、反差、尴尬、嘴损或轻松调味 |
| `highlightIssues` | R 类问题编号，如 `R-01`、`R-02` |

章节只有 `readerHookStatus == "pass"`、`readerHookScore` 达标、存在 `memorableMoment` 和 `chapterTurnPageHook`，且不存在机械化结尾问题并通过爽文专项时，才允许 `completed`。

---

## 三轮检测系统

为降低不同模型、不同轮次的主观差异，所有章节 QA 检测至少重复 3 轮。

规则：

- 每轮都必须独立检查：章节契约、反 AI、文学质量、追读理由、反套路结尾、爽文专项（如适用）、黄金三章（如适用）
- 最终结论采用保守聚合
- 任一轮出现阻塞失败，最终不得 `PASS`
- 文学质量分和追读力分采用三轮最低分
- `reviewRoundCount < 3` 的章节不得标记 `completed`
- Phase 4 的全书总验收也至少重复 3 轮，并采用保守聚合

---

## 自动修复复检系统

参考：[auto-repair-loop.md](../guides/auto-repair-loop.md)

目标：

- 验收失败后自动生成可执行修复任务
- 修复后作废旧检测结论，避免沿用旧分数
- 修复完成后重新执行至少 3 轮检测
- 多轮失败时保留失败项和修复历史，便于最终报告解释风险

核心字段：

| 字段 | 含义 |
|---|---|
| `repairRequired` | 当前是否仍有失败项需要修复 |
| `needsRecheck` | 修复已完成，是否等待重新三轮检测 |
| `lastFailureCodes` | 最近一次失败项编号，如 `B-01`、`A-02`、`R-04`、`G-01`、`C-03` |
| `repairRound` | 已执行的自动修复轮次 |
| `repairHistory` | 每轮失败项、修复摘要、复检结果 |
| `lastRepairAt` | 最近一次修复完成时间 |

循环规则：

1. 任一验收失败时，章节进入 `failed` 或 `in_revision`，写入 `repairRequired: true` 和 `lastFailureCodes`。
2. Fix Writer 只按 `lastFailureCodes` 修复，修复后进入 `in_qa`，写入 `needsRecheck: true`。
3. State Keeper 必须将旧的 `qaStatus`、`qualityScore`、`antiAiStatus`、`literaryScore`、`readerHookStatus`、`readerHookScore`、`reviewRoundCount` 置空或归零。
4. Evaluator 重新读取修复后的正文，重新执行至少 3 轮检测。
5. 复检通过后，清空 `repairRequired`、`needsRecheck`、`lastFailureCodes` 和 `blockingIssues`，才允许 `completed`。
6. `repairRound >= maxAutoRepairRounds` 且仍失败时，章节标记 `blocked`。

---

## Novel Hook 系统

参考：[novel-hooks.md](../guides/novel-hooks.md)、[hook-lifecycle.md](hook-lifecycle.md)

目标：

- 防止模型写完正文后跳过 QA
- 防止模型未三轮检测就标记 completed
- 防止修复后不复检
- 防止最终汇报时遗漏未完成章节
- 防止会话断点丢失

脚本：

```bash
python scripts/novel_hook_guard.py post-draft ./chinese-novelist/项目文件夹 --chapter 1
python scripts/novel_hook_guard.py pre-mark-pass ./chinese-novelist/项目文件夹 --chapter 1
python scripts/novel_hook_guard.py stop ./chinese-novelist/项目文件夹
python scripts/novel_hook_guard.py session-close ./chinese-novelist/项目文件夹 --note "第1章 completed"
```

硬规则：

- Step 3 draft 后必须运行 `post-draft`。
- Step 7 mark_pass 前必须运行 `pre-mark-pass`。
- Phase 4 汇报完成前必须运行 `stop`。
- 每章完成或会话暂停前必须运行 `session-close`。
- hook 失败时，按输出的 `Next action` 自动回到对应步骤，不向用户确认。

---

## 黄金三章系统

存储位置：`03-黄金三章.md`

参考：[golden-three-chapters.md](../guides/golden-three-chapters.md)

作用：

- 在 Phase 1 收集主角共鸣特性
- 在 Phase 2 设计前三章的启示、转折、小高潮
- 在 Phase 3 对前三章写作和 QA 加专项门禁
- 在 Phase 4 做开篇留存总验收

前三章职责：

| 章节 | 角色 | 必须完成 |
|---|---|---|
| 第1章 | 启示 | 主角共鸣、当前生活、长钉子、未来展望 |
| 第2章 | 转折 | 引爆长钉子、重大损失、不得不行动 |
| 第3章 | 小高潮 | 主动出手、有限胜利、更大期待 |

第1-3章如果黄金三章专项失败，不得标记 `completed`。

---

## 章节契约与 QA 系统

### 章节契约

存储位置：`chapter-contracts/第XX章.md`

模板：[chapter-contract-template.md](../guides/chapter-contract-template.md)

用途：

- 把大纲规划转成可验收标准
- 约束 Chapter Writer 不偏离主线
- 约束 Evaluator 只按契约评分
- 支持失败项定向修复

### QA 报告

存储位置：`qa/第XX章.md`

模板：[qa-report-template.md](../guides/qa-report-template.md)

评分：

| 维度 | 分值 |
|---|---:|
| 字数与结构 | 10 |
| 大纲履约 | 20 |
| 承接与连贯 | 15 |
| 人物一致性 | 15 |
| 冲突与节奏 | 10 |
| 对话质量 | 10 |
| 结尾策略与追读理由 | 10 |
| 去 AI 味与文字质感 | 10 |

判定：

- `PASS`：总分 >= 85，且无阻塞项
- `PARTIAL`：总分 70-84，或存在非阻塞失败项
- `FAIL`：总分 < 70，或存在任一阻塞项

Evaluator 必须给出证据和修复建议，不能只输出主观评价。

QA 未通过时，报告必须生成“修复指令”和失败项编号。修复完成后，必须按 [auto-repair-loop.md](../guides/auto-repair-loop.md) 重新检测，不允许只更新报告结论。

---

## 进度收口系统

每章完成后刷新：

- `progress/latest.txt`：最近完成章节、QA 分数、阻塞项、下一章
- `progress/YYYY-MM.md`：月度追加记录

进度快照用于中断续写和并行写作交接。快照必须短，不替代章节摘要。

---

## 字数检查脚本

使用 `scripts/check_chapter_wordcount.py` 检查章节字数：

```bash
# 检查单个章节
python scripts/check_chapter_wordcount.py ./chinese-novelist/项目文件夹/第01章.md

# 检查所有章节
python scripts/check_chapter_wordcount.py --all ./chinese-novelist/项目文件夹/

# 自定义最小字数
python scripts/check_chapter_wordcount.py ./chinese-novelist/项目文件夹/第01章.md 3500
```

### 使用场景

| 阶段 | 用途 |
|------|------|
| Phase 3（逐章创作） | 撰写后检查单章字数，低于3000字必须扩充 |
| Phase 4（最终总验收） | 批量复查所有章节字数，发现问题回到章节 sprint |

低于3000字的章节必须使用 [content-expansion.md](../guides/content-expansion.md) 的扩充技巧进行扩充。

## 项目结构校验脚本

使用 `scripts/validate_novel_project.py` 检查轻量 Novel Harness 产物：

```bash
python scripts/validate_novel_project.py ./chinese-novelist/项目文件夹
python scripts/validate_novel_project.py ./chinese-novelist/项目文件夹 --json
```

检查内容：

- `02-写作计划.json` 是否存在且可解析
- 每章章节文件、章节契约、QA 报告、摘要路径是否符合状态
- 已完成章节是否字数达标、QA 通过、无阻塞项、无待修复或待复检状态
- 项目目录是否包含 `chapter-contracts/`、`qa/`、`summaries/`、`continuity/`、`progress/`

## Hook Guard 脚本

使用 `scripts/novel_hook_guard.py` 检查章节和项目的关键执行节点：

```bash
python scripts/novel_hook_guard.py post-draft ./chinese-novelist/项目文件夹 --chapter 1
python scripts/novel_hook_guard.py pre-mark-pass ./chinese-novelist/项目文件夹 --chapter 1
python scripts/novel_hook_guard.py stop ./chinese-novelist/项目文件夹
python scripts/novel_hook_guard.py session-close ./chinese-novelist/项目文件夹 --note "保存断点"
```

Hook guard 会输出 `PASS/FAIL` 和 `Next action`。失败时必须继续执行下一步，不得直接对用户汇报完成。

## Novel Harness Runtime 初始化

使用 `scripts/init_novel_harness.py` 将入口契约和 Claude/Codex hook 配置安装到目标仓库：

```bash
python scripts/init_novel_harness.py --target-dir .
```

初始化内容：

- `AGENTS.md`：Codex 执行入口
- `CLAUDE.md`：Claude 执行入口
- `.claude/settings.json`：Claude hook 注册
- `.claude/hooks/*.py`：Claude hook wrapper
- `.codex/config.toml`：Codex hook 开关
- `.codex/hooks.json`：Codex hook 注册
- `.codex/hooks/*.py`：Codex hook wrapper
- `scripts/novel_runtime_hook.py`：Claude/Codex 共用 hook runtime

初始化后，模型即使没有主动读取流程文档，也会在 UserPromptSubmit、PostToolUse 和 Stop 阶段收到或触发 Novel Harness 约束。Stop hook 失败时会阻断“完成”汇报。

## Flow Smoke Test

使用 `scripts/smoke_novel_flow.py` 一键验证整体 flow 能否正常拦截漏检、漏修和漏复检：

```bash
python scripts/smoke_novel_flow.py
```

覆盖场景：

- 完整通过项目：`pre-mark-pass`、`stop`、`validate` 必须通过
- 缺 QA 报告：`pre-mark-pass` 必须失败
- 修复后未复检：`stop` 必须失败
- 分数不足：`pre-mark-pass` 必须失败
- blocked 风险章节：允许进入 `completed_with_risks`

修改 hook、QA 字段、状态流转或校验脚本后，必须运行 smoke test。
