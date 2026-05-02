# 第[XX]章 QA 报告

## 结论

- **状态**：PASS / PARTIAL / FAIL
- **分数**：[0-100]
- **反 AI 门禁**：pass / fail
- **文学质量分**：[0-100]
- **读者钩子门禁**：pass / fail
- **追读力分**：[0-100]
- **检测轮次**：[至少3]
- **是否可标记 completed**：是 / 否
- **修复轮次**：[0-3]
- **是否需要修复**：是 / 否
- **是否等待复检**：是 / 否
- **最近失败项**：[A-XX/R-XX/B-XX/G-XX/C-XX，若无写“无”]
- **检查时间**：[ISO时间]

## 输入文件

- 章节契约：`chapter-contracts/第XX章.md`
- 章节正文：`第XX章-[标题].md`
- 人物档案：`00-人物档案.md`
- 大纲：`01-大纲.md`
- 上一章摘要：`summaries/第[XX-1]章.md`

## 验收结果

| # | 项目 | 状态 | 分数 | 证据 |
|---|---|---|---:|---|
| 1 | 字数与结构 | PASS/PARTIAL/FAIL | /10 | |
| 2 | 大纲履约 | PASS/PARTIAL/FAIL | /20 | |
| 3 | 承接与连贯 | PASS/PARTIAL/FAIL | /15 | |
| 4 | 人物一致性 | PASS/PARTIAL/FAIL | /15 | |
| 5 | 冲突与节奏 | PASS/PARTIAL/FAIL | /10 | |
| 6 | 对话质量 | PASS/PARTIAL/FAIL | /10 | |
| 7 | 结尾钩子 | PASS/PARTIAL/FAIL | /10 | |
| 8 | 去 AI 味与文字质感 | PASS/PARTIAL/FAIL | /10 | |

## 反 AI 门禁

> 参考 [literary-quality-gate.md](literary-quality-gate.md)。任一严重 AI 痕迹出现时，`antiAiStatus` 必须为 `fail`。

| 编号 | 类型 | 状态 | 位置或证据 | 为什么像 AI | 修复建议 |
|---|---|---|---|---|---|
| A-01 | 抽象情绪替代表演 | PASS/FAIL | | | |
| A-02 | 角色台词同质化 | PASS/FAIL | | | |
| A-03 | 空泛形容和四字套话堆积 | PASS/FAIL | | | |
| A-04 | 段落节奏过于工整 | PASS/FAIL | | | |
| A-05 | 设定解释压过剧情 | PASS/FAIL | | | |
| A-06 | 作者替人物总结主题 | PASS/FAIL | | | |
| A-07 | 低级连续性错误 | PASS/FAIL | | | |
| A-08 | 冲突或爽点缺席 | PASS/FAIL | | | |

antiAiStatus：pass / fail

## 文学质量评分

| 维度 | 分数 | 证据 |
|---|---:|---|
| 画面具体性 | /15 | |
| 人物声音 | /15 | |
| 情绪可信度 | /15 | |
| 冲突密度 | /15 | |
| 节奏变化 | /10 | |
| 语言自然度 | /15 | |
| 类型爽点 | /10 | |
| 余味与钩子 | /5 | |

literaryScore：[0-100]

## 读者钩子门禁

> 参考 [reader-hook-gate.md](reader-hook-gate.md)。任一严重追读问题出现时，`readerHookStatus` 必须为 `fail`。

| 编号 | 类型 | 状态 | 位置或证据 | 为什么不吸引人 | 修复建议 |
|---|---|---|---|---|---|
| R-01 | 开场抓力不足 | PASS/FAIL | | | |
| R-02 | 本章没有可记忆亮点 | PASS/FAIL | | | |
| R-03 | 幽默缺席或幽默破坏基调 | PASS/FAIL | | | |
| R-04 | 主角魅力没有展示出来 | PASS/FAIL | | | |
| R-05 | 爽点只铺垫没有兑现 | PASS/FAIL | | | |
| R-06 | 结尾追读钩子不成立 | PASS/FAIL | | | |
| R-07 | 章节中段停滞 | PASS/FAIL | | | |
| R-08 | 反转或冲突太常规 | PASS/FAIL | | | |

readerHookStatus：pass / fail

## 追读力评分

| 维度 | 分数 | 证据 |
|---|---:|---|
| 开场抓力 | /15 | |
| 章节亮点 | /20 | |
| 幽默与反差 | /10 | |
| 主角魅力 | /15 | |
| 爽点兑现 | /15 | |
| 期待升级 | /15 | |
| 阅读顺滑 | /10 | |

readerHookScore：[0-100]

## 章节记忆点

- **memorableMoment**：[本章最值得读者记住的桥段/台词/反转/爽点]
- **chapterTurnPageHook**：[读者读完本章后想继续看的具体原因]
- **humorBeat**：[本章幽默或反差点；严肃题材可写“低频/克制”，但必须说明调味方式]

## 黄金三章专项（第1-3章必填）

> 第4章以后写“不适用”。

| 项目 | 状态 | 证据 |
|---|---|---|
| 主角共鸣特性清晰 | PASS/PARTIAL/FAIL/不适用 | |
| 第1章长钉子已埋下或已引爆 | PASS/PARTIAL/FAIL/不适用 | |
| 未来展望或期待感明确 | PASS/PARTIAL/FAIL/不适用 | |
| 第2章重大转折足够强 | PASS/PARTIAL/FAIL/不适用 | |
| 第3章小高潮成立 | PASS/PARTIAL/FAIL/不适用 | |
| 有限胜利和更大期待并存 | PASS/PARTIAL/FAIL/不适用 | |

黄金三章专项结论：PASS / FAIL / 不适用

## 三轮检测记录

> 为降低模型差异，所有检测至少重复 3 轮。每轮必须独立给出结论；最终结论采用保守聚合：任一轮出现阻塞失败，最终不得 PASS；分数采用三轮最低分。

| 轮次 | QA状态 | antiAiStatus | literaryScore | readerHookStatus | readerHookScore | 黄金三章 | 阻塞项 |
|---|---|---|---:|---|---:|---|---|
| 1 | PASS/PARTIAL/FAIL | pass/fail | | pass/fail | | PASS/FAIL/不适用 | |
| 2 | PASS/PARTIAL/FAIL | pass/fail | | pass/fail | | PASS/FAIL/不适用 | |
| 3 | PASS/PARTIAL/FAIL | pass/fail | | pass/fail | | PASS/FAIL/不适用 | |

最终聚合：
- **reviewRoundCount**：3
- **requiredReviewPasses**：3
- **lowestLiteraryScore**：[三轮最低文学质量分]
- **lowestReaderHookScore**：[三轮最低追读力分]
- **consensusStatus**：pass / fail

## 自动修复复检状态

> 参考 [auto-repair-loop.md](auto-repair-loop.md)。只要本报告不是 PASS，就必须生成失败项和修复指令。修复完成后，本报告结论不得被直接改成 PASS，必须重新三轮检测。

```json
{
  "repairRequired": true,
  "needsRecheck": false,
  "repairRound": 0,
  "lastFailureCodes": ["A-XX", "R-XX", "B-XX"]
}
```

状态写入规则：

- 初次 QA 失败：`repairRequired: true`，`needsRecheck: false`，写入 `lastFailureCodes`。
- 修复完成：`repairRequired: true`，`needsRecheck: true`，旧检测分数作废，`reviewRoundCount: 0`。
- 复检通过：`repairRequired: false`，`needsRecheck: false`，`lastFailureCodes: []`。
- 复检失败：保留新的失败项，继续下一轮修复，直到达到最大修复轮次。

## 阻塞项

> 没有阻塞项时写“无”。

### B-[编号]：[问题标题]

- **对应标准**：[编号]
- **位置或证据**：[章节中的位置、短摘录或事件说明]
- **预期**：[来自章节契约]
- **实际**：[实际表现]
- **修复建议**：[具体改法]

## 非阻塞问题

### N-[编号]：[问题标题]

- **对应标准**：[编号]
- **位置或证据**：
- **影响**：
- **修复建议**：

## 修复指令

只修复以下失败项，不改动已通过的核心事件、人物关系和结尾钩子：

1. [失败项编号]：[具体修复目标]
2. [失败项编号]：[具体修复目标]

修复后动作：

1. 将旧 QA 结论作废，不得沿用旧分数。
2. 将 `needsRecheck` 设为 `true`。
3. 重新读取修复后的章节正文。
4. 重新执行至少 3 轮检测。

## 复评记录

| 修复轮次 | 修复摘要 | 重新检测轮次 | 最低文学分 | 最低追读分 | 结果 |
|---|---|---:|---:|---:|---|
| 1 | | 3 | | | PASS/FAIL |
