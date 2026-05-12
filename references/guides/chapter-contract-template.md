# 第[XX]章章节契约

## 元信息

- **章节编号**：第[XX]章
- **章节标题**：[标题]
- **章节文件**：`第XX章-[标题].md`
- **大纲来源**：`01-大纲.md` 第[XX]章规划
- **上一章摘要**：`summaries/第[XX-1]章.md`（第1章填“无”）
- **场景卡**：`scene-cards/第XX章.md`
- **QA 报告**：`qa/第XX章.md`
- **最大修复轮次**：3
- **最低检测轮次**：3
- **文学质量门槛**：普通章节 `literaryScore >= 80`；第1-3章 `literaryScore >= 85`
- **追读力门槛**：普通章节 `readerHookScore >= 80`；第1-3章 `readerHookScore >= 85`
- **自动修复复检**：验收失败时按 [auto-repair-loop.md](auto-repair-loop.md) 定向修复；修复后旧检测结论作废，必须重新三轮检测

## 输入上下文

- **核心事件**：[本章必须发生的事件]
- **质量基准对应承诺**：[本章兑现 `05-质量基准.md` 中哪条读者承诺]
- **读者流失雷区**：[本章最容易在哪个位置让读者弃书，如何避免]
- **承接上章**：[必须回应的上一章悬念或情绪]
- **出场人物**：[人物列表]
- **场景列表**：[场景1；场景2；场景3]
- **章首引子类型**：[从 hook-techniques.md 选择]
- **结尾策略 endingStrategy**：payoff-close / soft-question / decision-point / emotional-aftertaste / resource-reveal / relationship-shift / threat-approach
- **代入锚点 immersionAnchor**：[本章让读者共鸣的现实压力、委屈、欲望、关系或职业处境]
- **合理化说明 rationalizationNote**：[本章如何通过规则、证据、代价或旁人反应让离奇设定看似合理]
- **Core Loop 步骤 coreLoopStep**：[本章处在“进入问题/解决冲突/获得收益/升级/进入更难挑战”的哪一步]
- **系统/规则参与 systemRuleUse**：[系统、金手指、职业流程、能力体系、社会规则或案件逻辑如何推动本章]
- **本章兑现 expectationPayoff**：[本章必须让读者得到什么情绪、信息、爽点或关系推进]
- **下章期待 expectationNext**：[读者继续读的具体理由，不等于硬悬念]
- **爽点节拍 satisfactionBeats**：[必填；按“压迫/误判 -> 主角行动 -> 可见收益 -> 旁人或局势反应 -> 下一步期待”写清本章有效情绪兑现]
- **伏笔要求**：[本章必须埋下、推进或回收的伏笔]
- **用户特殊要求**：[必须包含或禁止出现的内容]

## 黄金三章专项（仅第1-3章必填）

> 参考 [golden-three-chapters.md](golden-three-chapters.md)。第4章以后填“不适用”。

- **黄金角色**：第1章启示 / 第2章转折 / 第3章小高潮 / 不适用
- **主角共鸣特性**：[从九特性中选择1-2个]
- **第1章长钉子**：[第1章埋下、第2章引爆的问题/秘密/关系/危险]
- **未来展望**：[主角愿望或亲友期待]
- **重大损失风险**：[第2章主角可能失去什么]
- **第三章有限胜利**：[第3章兑现什么，但保留什么]
- **后续大期待**：[第三章结尾画出的更大饼]

## 范围

### 范围内

- 严格完成本章核心事件。
- 让出场人物的行为和说话方式符合 `00-人物档案.md`。
- 执行 `05-质量基准.md` 中的目标读者、核心承诺和质量红线。
- 按 `scene-cards/第XX章.md` 完成每个场景的目的、冲突、信息释放、情绪兑现和局面变化。
- 回应上一章摘要中的关键悬念。
- 执行 `04-网文顶层设计.md` 中的代入感、核心循环、系统/规则和挖坑填坑要求。
- 为下一章留下可承接的追读理由；结尾可以收束、兑现、留余味，也可以制造悬念。

### 范围外

- 不提前解决后续章节的终极谜题。
- 不改写其他章节既定事实。
- 不新增会破坏全书主线的设定。

## 验收标准

| # | 标准 | 验证方式 | 阻塞 |
|---|---|---|---|
| 1 | 正文字数不少于 3000 个汉字，建议不超过 5000 个汉字 | script | 是 |
| 2 | 场景卡通过：`sceneCardStatus == "pass"` 且 `sceneCardIssues` 为空 | evaluator/state | 是 |
| 3 | 本章核心事件完整发生，不能只铺垫不兑现 | evaluator | 是 |
| 4 | 明确回应上一章至少 1 个悬念、情绪或行动后果 | evaluator | 是 |
| 5 | 主要人物行为、动机、语气符合人物档案 | evaluator | 是 |
| 6 | 全章至少有 2 个张力波峰，且中段不连续空转 | evaluator | 否 |
| 7 | 对话推动情节或暴露人物关系，避免同质化闲聊 | evaluator | 否 |
| 8 | 至少出现 1 个读者预期外的信息、行动或反转 | evaluator | 否 |
| 9 | 结尾策略清晰，追读理由成立，并能被下一章规划承接 | evaluator | 是 |
| 10 | 没有明显 AI 味：空泛抒情、套话、堆砌形容词、四字格律过密 | evaluator | 否 |
| 11 | 伏笔记录完整：新增、推进、回收都写入摘要或伏笔表 | evaluator | 否 |
| 12 | 第1-3章满足黄金三章专项门禁 | evaluator | 是 |
| 13 | 反 AI 门禁通过：`antiAiStatus == "pass"` | evaluator | 是 |
| 14 | 文学质量达标：普通章节 `literaryScore >= 80`，第1-3章 `>= 85` | evaluator | 是 |
| 15 | 追读门禁通过：有亮点、有追读理由，`readerHookStatus == "pass"` | evaluator | 是 |
| 16 | 所有检测至少完成 3 轮，且三轮均无阻塞失败 | evaluator | 是 |
| 17 | 若曾验收失败，修复后已重新三轮检测，且 `repairRequired == false`、`needsRecheck == false`、`lastFailureCodes` 为空 | evaluator/state | 是 |
| 18 | 无机械化结尾问题：`formulaicIssues` 为空，连续章节不重复强悬念策略 | evaluator/state | 是 |
| 19 | 网文顶层设计通过：`webNovelStatus == "pass"`，`webNovelIssues` 为空，代入锚点、合理化说明、Core Loop 步骤和系统/规则参与均非空 | evaluator | 是 |
| 20 | 爽文专项通过：`shuangwenStatus == "pass"` 且 `satisfactionBeats` 非空 | evaluator | 是 |
| 21 | Editor Gate 通过：`editorGateStatus == "pass"`、`editorGateScore` 达标、无读者流失风险 | editor | 是 |

## 评分量表

| 维度 | 分值 |
|---|---:|
| 字数与结构 | 10 |
| 场景卡履约 | 10 |
| 大纲履约 | 10 |
| 承接与连贯 | 10 |
| 人物一致性 | 10 |
| 冲突与节奏 | 10 |
| 对话质量 | 10 |
| 结尾策略与追读理由 | 10 |
| 网文顶层设计履约 | 10 |
| 去 AI 味与文字质感 | 10 |

## 文学质量评分

> 参考 [literary-quality-gate.md](literary-quality-gate.md)。该评分独立于上方章节 QA 总分。

| 维度 | 分值 |
|---|---:|
| 画面具体性 | 15 |
| 人物声音 | 15 |
| 情绪可信度 | 15 |
| 冲突密度 | 15 |
| 节奏变化 | 10 |
| 语言自然度 | 15 |
| 类型爽点 | 10 |
| 余味与追读理由 | 5 |

## 追读力评分

> 参考 [reader-hook-gate.md](reader-hook-gate.md)。该评分独立于章节 QA 总分和文学质量分。

| 维度 | 分值 |
|---|---:|
| 开场抓力 | 15 |
| 章节亮点 | 20 |
| 幽默与反差 | 10 |
| 主角魅力 | 15 |
| 爽点兑现 | 15 |
| 期待升级 | 15 |
| 阅读顺滑 | 10 |

通过标准：
- `PASS`：总分 >= 85，且无阻塞项失败。
- `PARTIAL`：总分 70-84，或存在非阻塞失败项。
- `FAIL`：总分 < 70，或存在任一阻塞项失败。
- `antiAiStatus` 必须为 `pass`。
- `literaryScore` 必须达到门槛。
- `readerHookStatus` 必须为 `pass`。
- `readerHookScore` 必须达到门槛。
- `memorableMoment` 和 `chapterTurnPageHook` 必须非空。
- `endingStrategy` 必须属于允许策略之一。
- `formulaicIssues` 必须为空。
- 启用 `sceneCardPolicy` 时，`sceneCardStatus` 必须为 `pass`，`sceneCardIssues` 必须为空。
- 启用 `webNovelDesign` 时，`immersionAnchor`、`rationalizationNote`、`coreLoopStep`、`systemRuleUse` 必须非空，`webNovelStatus` 必须为 `pass`，`webNovelIssues` 必须为空。
- `satisfactionBeats` 必须非空，`shuangwenStatus` 必须为 `pass`，`shuangwenIssues` 必须为空。
- 启用 `editorGate` 时，`editorGateStatus` 必须为 `pass`，`editorGateScore` 必须达标，`readerLossRisks` 和 `editorGateIssues` 必须为空，`revisionLevel` 必须为 `none`。
- 每章至少完成 3 轮检测；任一轮发现阻塞项时，最终不得 `PASS`。
- 修复后的章节必须重新完成 3 轮检测；不得沿用修复前的 QA 分数或结论。
- `repairRequired`、`needsRecheck` 必须为 `false`，`lastFailureCodes` 必须为空。

第1-3章补充规则：
- 黄金三章专项未通过时，不得标记 `PASS`。
- 第1章必须有主角共鸣特性、当前生活、长钉子和未来展望。
- 第2章必须引爆第1章长钉子，并让主角面临重大损失。
- 第3章必须形成小高潮，给有限胜利和更大期待。
