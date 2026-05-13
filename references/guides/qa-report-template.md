# 第[XX]章 QA 报告

## 结论

- **状态**：PASS / PARTIAL / FAIL
- **分数**：[0-100]
- **反 AI 门禁**：pass / fail
- **文学质量分**：[0-100]
- **追读理由门禁**：pass / fail
- **追读力分**：[0-100]
- **结尾策略**：[endingStrategy]
- **场景卡**：pass / fail
- **网文顶层设计**：pass / fail
- **爽文专项**：pass / fail
- **Editor Gate**：pass / fail
- **编辑审稿分**：[0-100]
- **检测轮次**：[至少3]
- **是否可标记 completed**：是 / 否
- **修复轮次**：[0-3]
- **是否需要修复**：是 / 否
- **是否等待复检**：是 / 否
- **最近失败项**：[SC-XX/A-XX/R-XX/M-XX/W-XX/S-XX/E-XX/B-XX/G-XX/C-XX，若无写“无”]
- **检查时间**：[ISO时间]

## 输入文件

- 章节契约：`chapter-contracts/第XX章.md`
- 场景卡：`scene-cards/第XX章.md`
- 章节正文：`第XX章-[标题].md`
- 质量基准：`05-质量基准.md`
- 人物档案：`00-人物档案.md`
- 大纲：`01-大纲.md`
- 网文顶层设计：`04-网文顶层设计.md`
- 上一章摘要：`summaries/第[XX-1]章.md`

## 验收结果

| # | 项目 | 状态 | 分数 | 证据 |
|---|---|---|---:|---|
| 1 | 字数与结构 | PASS/PARTIAL/FAIL | /10 | |
| 2 | 场景卡履约 | PASS/PARTIAL/FAIL | /10 | |
| 3 | 大纲履约 | PASS/PARTIAL/FAIL | /10 | |
| 4 | 承接与连贯 | PASS/PARTIAL/FAIL | /10 | |
| 5 | 人物一致性 | PASS/PARTIAL/FAIL | /10 | |
| 6 | 冲突与节奏 | PASS/PARTIAL/FAIL | /10 | |
| 7 | 对话质量 | PASS/PARTIAL/FAIL | /10 | |
| 8 | 结尾策略与追读理由 | PASS/PARTIAL/FAIL | /10 | |
| 9 | 网文顶层设计履约 | PASS/PARTIAL/FAIL | /10 | |
| 10 | 去 AI 味与文字质感 | PASS/PARTIAL/FAIL | /10 | |

## 场景卡门禁

> 参考 [scene-card-template.md](scene-card-template.md)。场景卡不通过时，正文不得 PASS。

| 编号 | 类型 | 状态 | 位置或证据 | 为什么会水或空转 | 修复建议 |
|---|---|---|---|---|---|
| SC-01 | 场景目的不清，删掉也不影响章节 | PASS/FAIL | | | |
| SC-02 | 场景没有冲突双方 | PASS/FAIL | | | |
| SC-03 | 场景没有新信息、新选择、新阻力或新收益 | PASS/FAIL | | | |
| SC-04 | 中段连续空转 | PASS/FAIL | | | |
| SC-05 | 爽点或情绪兑现只写结果，没有过程 | PASS/FAIL | | | |
| SC-06 | 读者流失风险未预判 | PASS/FAIL | | | |
| SC-07 | 结尾没有兑现或下一步期待 | PASS/FAIL | | | |

sceneCardStatus：pass / fail
sceneCardIssues：[]

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
| A-09 | 格言式总结句替代事件 | PASS/FAIL | | | |
| A-10 | 主角分析器化，人的反应不足 | PASS/FAIL | | | |

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
| 余味与追读理由 | /5 | |

literaryScore：[0-100]

## 网文顶层设计门禁

> 参考 [web-novel-top-design.md](web-novel-top-design.md)。任一阻塞级 W 类问题出现时，`webNovelStatus` 必须为 `fail`。

| 编号 | 类型 | 状态 | 位置或证据 | 为什么破坏代入/爽点/期待 | 修复建议 |
|---|---|---|---|---|---|
| W-01 | 不合理设定缺少规则、证据或代价 | PASS/FAIL | | | |
| W-02 | 主角行动脱离熟悉领域或能力来源 | PASS/FAIL | | | |
| W-03 | 本章与核心循环脱节，像随机事件 | PASS/FAIL | | | |
| W-04 | 欲望升级不可见，读者不知道主角获得了什么 | PASS/FAIL | | | |
| W-05 | 只挖坑不填坑，或只收束不制造下一步期待 | PASS/FAIL | | | |
| W-06 | 系统/金手指/能力规则随意，像作者临时开挂 | PASS/FAIL | | | |
| W-07 | 前三章没有快速抛出核心梗、优势来源和初始冲突 | PASS/FAIL/不适用 | | | |
| W-08 | 对手低智或世界无反应，导致爽感廉价 | PASS/FAIL | | | |
| W-09 | 真实细节只作说明，没有转化为压力、选择或风险 | PASS/FAIL | | | |

webNovelStatus：pass / fail
immersionAnchor：[本章代入锚点]
rationalizationNote：[本章合理化说明]
coreLoopStep：[本章 Core Loop 步骤]
systemRuleUse：[系统、金手指、职业流程、能力体系或案件逻辑如何参与]
webNovelIssues：[]

## 追读理由门禁

> 参考 [reader-hook-gate.md](reader-hook-gate.md)。任一严重追读问题出现时，`readerHookStatus` 必须为 `fail`。

| 编号 | 类型 | 状态 | 位置或证据 | 为什么不吸引人 | 修复建议 |
|---|---|---|---|---|---|
| R-01 | 开场抓力不足 | PASS/FAIL | | | |
| R-02 | 本章没有可记忆亮点 | PASS/FAIL | | | |
| R-03 | 幽默缺席或幽默破坏基调 | PASS/FAIL | | | |
| R-04 | 主角魅力没有展示出来 | PASS/FAIL | | | |
| R-05 | 爽点只铺垫没有兑现 | PASS/FAIL | | | |
| R-06 | 结尾追读理由不成立 | PASS/FAIL | | | |
| R-07 | 章节中段停滞 | PASS/FAIL | | | |
| R-08 | 反转或冲突太常规 | PASS/FAIL | | | |

readerHookStatus：pass / fail

## 结尾反套路门禁

| 编号 | 类型 | 状态 | 位置或证据 | 为什么机械化 | 修复建议 |
|---|---|---|---|---|---|
| M-01 | 连续强悬念结尾 | PASS/FAIL | | | |
| M-02 | 惯用物件钩子重复 | PASS/FAIL | | | |
| M-03 | 只铺垫不兑现 | PASS/FAIL | | | |
| M-04 | 结尾和本章核心事件无因果 | PASS/FAIL | | | |
| M-05 | 追读理由只靠“下一章会发生事” | PASS/FAIL | | | |

formulaicIssues：[]

## 爽文专项（所有章节必填）

| 编号 | 类型 | 状态 | 位置或证据 | 为什么不爽 | 修复建议 |
|---|---|---|---|---|---|
| S-01 | 爽点无铺垫 | PASS/FAIL | | | |
| S-02 | 本章无有效爽点节拍 | PASS/FAIL | | | |
| S-03 | 只憋屈不释放 | PASS/FAIL | | | |
| S-04 | 主角升级不可见 | PASS/FAIL | | | |
| S-05 | 打脸没有因果 | PASS/FAIL | | | |
| S-06 | 爽点靠旁白宣布 | PASS/FAIL | | | |
| S-07 | 金手指、信息差或规则优势没有参与情节 | PASS/FAIL | | | |

shuangwenStatus：pass / fail
satisfactionBeats：
- [本章有效爽点节拍，必须具体到铺垫、行动、兑现和后续期待]
shuangwenIssues：[]

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

## Editor Gate

> 参考 [editor-gate.md](editor-gate.md)。Editor Gate 是 QA 后的商业可读性审稿；它不替代 QA，但失败时章节不得 PASS。

| 编号 | 类型 | 修复级别 | 状态 | 位置或证据 | 读者为什么可能流失 | 修复建议 |
|---|---|---|---|---|---|---|
| E-01 | 前300字不抓人 | plot | PASS/FAIL | | | |
| E-02 | 1000字内主冲突未出现 | structure | PASS/FAIL | | | |
| E-03 | 中段空转，场景没有变化 | structure | PASS/FAIL | | | |
| E-04 | 主角没有主动选择或魅力展示 | character | PASS/FAIL | | | |
| E-05 | 本章没有可感知兑现 | plot | PASS/FAIL | | | |
| E-06 | 结尾只有硬钩子，没有本章价值 | plot | PASS/FAIL | | | |
| E-07 | 反派低智或世界无反应，爽感廉价 | character | PASS/FAIL | | | |
| E-08 | 文字能读但没有类型味道 | prose | PASS/FAIL | | | |
| E-09 | 配角只提供信息，不制造压迫 | character | PASS/FAIL | | | |
| E-10 | 首章核心梗后缺少外部风险 | plot | PASS/FAIL/不适用 | | | |

editorGateStatus：pass / fail
editorGateScore：[0-100]
readerLossRisks：[]
editorGateIssues：[]
revisionLevel：none / prose / character / plot / structure

## 章节记忆点

- **memorableMoment**：[本章最值得读者记住的桥段/台词/反转/爽点]
- **chapterTurnPageHook**：[读者读完本章后想继续看的具体原因；不是硬悬念模板]
- **endingStrategy**：payoff-close / soft-question / decision-point / emotional-aftertaste / resource-reveal / relationship-shift / threat-approach
- **expectationPayoff**：[本章已经兑现给读者的东西]
- **expectationNext**：[下一章的具体期待]
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

| 轮次 | QA状态 | 场景卡 | antiAiStatus | literaryScore | readerHookStatus | readerHookScore | 网文顶层 | 反套路 | 爽文专项 | Editor Gate | editorGateScore | 黄金三章 | 阻塞项 |
|---|---|---|---|---:|---|---:|---|---|---|---|---:|---|---|
| 1 | PASS/PARTIAL/FAIL | PASS/FAIL | pass/fail | | pass/fail | | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | | PASS/FAIL/不适用 | |
| 2 | PASS/PARTIAL/FAIL | PASS/FAIL | pass/fail | | pass/fail | | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | | PASS/FAIL/不适用 | |
| 3 | PASS/PARTIAL/FAIL | PASS/FAIL | pass/fail | | pass/fail | | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | | PASS/FAIL/不适用 | |

最终聚合：
- **reviewRoundCount**：3
- **requiredReviewPasses**：3
- **lowestLiteraryScore**：[三轮最低文学质量分]
- **lowestReaderHookScore**：[三轮最低追读力分]
- **lowestEditorGateScore**：[三轮最低编辑审稿分]
- **consensusStatus**：pass / fail

## 自动修复复检状态

> 参考 [auto-repair-loop.md](auto-repair-loop.md)。只要本报告不是 PASS，就必须生成失败项和修复指令。修复完成后，本报告结论不得被直接改成 PASS，必须重新三轮检测。

```json
{
  "repairRequired": true,
  "needsRecheck": false,
  "repairRound": 0,
  "lastFailureCodes": ["SC-XX", "A-XX", "R-XX", "M-XX", "W-XX", "S-XX", "E-XX", "B-XX"]
}
```

状态写入规则：

- 初次 QA 失败：`repairRequired: true`，`needsRecheck: false`，写入 `lastFailureCodes`。
- 修复完成：`repairRequired: true`，`needsRecheck: true`，旧检测分数和 Editor Gate 结论作废，`reviewRoundCount: 0`。
- 结构级失败：同步作废 `sceneCardStatus`，回到场景卡或章节契约重做。
- 复检通过：`repairRequired: false`，`needsRecheck: false`，`lastFailureCodes: []`，`revisionLevel: "none"`。
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

只修复以下失败项，不改动已通过的核心事件、人物关系和结尾策略：

1. [失败项编号]：[具体修复目标]
2. [失败项编号]：[具体修复目标]

修复后动作：

1. 将旧 QA 结论作废，不得沿用旧分数。
2. 将 `needsRecheck` 设为 `true`。
3. 重新读取修复后的章节正文。
4. 重新执行至少 3 轮 QA 与 Editor Gate。

## 复评记录

| 修复轮次 | 修复摘要 | revisionLevel | 重新检测轮次 | 最低文学分 | 最低追读分 | 最低编辑分 | 结果 |
|---|---|---|---:|---:|---:|---:|---|
| 1 | | none/prose/character/plot/structure | 3 | | | | PASS/FAIL |
