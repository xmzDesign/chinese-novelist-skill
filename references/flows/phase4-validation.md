# 第四阶段：最终总验收

**目标**：确认全书已完成章节级闭环，并检查全书级连贯性。全程无需用户介入。

Phase 4 不再把所有问题都留到最后补救。章节级字数、人物一致性、承接、追读理由、结尾反套路、爽文专项和去 AI 味应在 Phase 3 的章节 sprint 内完成。本阶段负责总验收和风险汇总。

汇报全稿完成前必须执行 stop hook。hook 失败时，不得向用户汇报完成，必须回到 hook 输出的 `Next action`。

---

## 1. 初始化总验收

1. 读取 `02-写作计划.json`
2. 将项目 `status` 更新为 `"validating"`
3. 运行项目结构检查：
   ```bash
   python scripts/validate_novel_project.py ./chinese-novelist/项目文件夹
   ```
4. 对所有章节补跑字数检查：
   ```bash
   python scripts/check_chapter_wordcount.py --all ./chinese-novelist/项目文件夹
   ```

---

## 2. 章节闭环检查

对每一章检查：

1. `filePath` 指向的章节文件存在
2. `contractPath` 指向的章节契约存在
3. `qaReportPath` 指向的 QA 报告存在
4. `summaryPath` 指向的章节摘要存在
5. `wordCountPass == true`
6. `qaStatus == "pass"` 或章节已标记 `blocked`
7. `status == "completed"` 的章节必须没有阻塞项
8. `antiAiStatus == "pass"`，否则不得 completed
9. 普通章节 `literaryScore >= 80`，第1-3章 `literaryScore >= 85`
10. `readerHookStatus == "pass"`，否则不得 completed
11. 普通章节 `readerHookScore >= 80`，第1-3章 `readerHookScore >= 85`
12. `memorableMoment` 和 `chapterTurnPageHook` 非空
13. `endingStrategy` 合法，`formulaicIssues` 为空
14. `satisfactionBeats` 非空、`shuangwenStatus == "pass"`、`shuangwenIssues` 为空
15. `reviewRoundCount >= 3`
16. `repairRequired == false`
17. `needsRecheck == false`
18. `lastFailureCodes` 为空

如果发现章节未完成闭环：

- `repairRound < maxAutoRepairRounds`：回到 Phase 3 对该章执行自动修复复检循环
- `repairRound >= maxAutoRepairRounds`：标记 `blocked`，写入最终报告

---

## 3. 全书连续性检查

读取以下文件：

- `00-人物档案.md`
- `01-大纲.md`
- `03-黄金三章.md`
- `summaries/*.md`
- `continuity/*.md`
- `qa/*.md`

检查维度：

| 维度 | 检查目标 |
|---|---|
| 时间线 | 日期、地点、事件先后不冲突 |
| 伏笔闭环 | 关键伏笔有埋设、推进、回收或保留说明 |
| 人物弧线 | 主角和关键配角变化有阶段性铺垫 |
| 关系变化 | 关系转折前有行为或事件支撑 |
| 主线推进 | 连续章节没有偏离核心冲突 |
| 节奏曲线 | 不连续多章低冲突或重复同类事件 |
| 主题回应 | 结局或阶段性收束回应核心主题 |
| 黄金三章 | 前三章完成启示、转折、小高潮，并引出后续期待 |
| 文学质量 | 全书没有系统性 AI 腔、台词同质、空泛抒情和模板化节奏 |
| 追读力 | 每章有亮点、局部兑现、追读理由和合适的幽默/反差 |
| 结尾反套路 | 全书结尾策略有变化，连续章节不重复强悬念套路 |
| 爽文专项 | 每章有有效情绪兑现、升级可见和下一步期待 |

总验收检测规则：

1. 全书连续性、黄金三章、文学质量、追读力、结尾反套路和爽文专项总评至少重复 3 轮
2. 每轮必须独立给出问题清单和风险等级
3. 最终报告采用保守聚合：任一轮发现阻塞级问题，最终状态不得为纯 `"completed"`
4. 三轮意见不一致时，按风险更高的一轮处理，并在 `qa/final-report.md` 标注分歧

产物：

- `qa/final-report.md`
- `continuity/timeline.md`
- `continuity/foreshadowing-ledger.md`
- `continuity/character-arcs.md`

黄金三章总验收必须写入 `qa/final-report.md`：

| 章节 | 验收重点 | 失败时处理 |
|---|---|---|
| 第1章 | 主角共鸣、现状、长钉子、未来展望、风格路线 | 回到 Phase 3 定向重写或补强 |
| 第2章 | 长钉子引爆、重大损失、不得不行动 | 回到 Phase 3 强化转折 |
| 第3章 | 主动出手、小高潮、有限胜利、更大期待 | 回到 Phase 3 补小高潮 |

---

## 4. 自动修复规则

参考：[auto-repair-loop.md](../guides/auto-repair-loop.md)

对总验收发现的问题：

| 问题类型 | 动作 |
|---|---|
| 缺章节文件、缺契约、缺 QA 报告 | 回到 Phase 3 补齐 |
| 字数不足 | 回到 Phase 3 定向扩写 |
| QA 未通过且 repairRound < maxAutoRepairRounds | 回到 Phase 3 自动修复复检循环 |
| 反 AI 门禁失败 | 回到 Phase 3 按 A 类失败项定向修复 |
| 文学质量分不足 | 回到 Phase 3 修复低分维度 |
| 追读门禁失败 | 回到 Phase 3 按 R 类失败项定向修复 |
| 机械化结尾失败 | 回到 Phase 3 按 M 类失败项定向修复 |
| 爽文专项失败 | 回到 Phase 3 按 S 类失败项定向修复 |
| 检测轮次不足 3 轮 | 回到 Phase 3 重新读取正文并补足 QA 检测轮次 |
| `repairRequired == true` | 回到 Phase 3 按 `lastFailureCodes` 修复 |
| `needsRecheck == true` | 回到 Phase 3 直接重新三轮检测 |
| `lastFailureCodes` 非空但章节 completed | 撤销 completed，回到 Phase 3 复检 |
| 时间线/伏笔/人物弧线轻微矛盾 | 修订对应章节摘要和 continuity 文件；必要时定向修章节 |
| 关键人物或主线严重矛盾 | 标记 blocked，最终报告说明风险和建议 |
| 黄金三章专项失败 | 第1-3章必须回到 Phase 3 修复，超过 3 轮才可标记风险 |

循环规则：

- 最多执行 3 轮总验收-修复循环
- 每轮修复后必须重新执行章节 QA 的 3 轮检测，再重新执行全书总验收
- 章节复检通过后，必须清空 `repairRequired`、`needsRecheck`、`lastFailureCodes` 和 `blockingIssues`
- 超过 3 轮仍未解决的问题不阻塞报告生成，但必须明确标注

总验收-修复循环伪代码：

```text
validationRound = 0

WHILE 总验收未通过 AND validationRound < finalValidationRounds:
    validationRound += 1
    汇总失败项，写入 qa/final-report.md

    FOR each failed chapter:
        IF chapter.repairRound >= maxAutoRepairRounds:
            chapter.status = "blocked"
            CONTINUE

        chapter.status = "in_revision"
        chapter.repairRequired = true
        chapter.lastFailureCodes = failure codes
        回到 Phase 3 自动修复
        修复后重新执行章节 QA 至少 3 轮

    重新运行 validate_novel_project.py
    重新执行全书连续性、黄金三章、文学质量、追读力、反套路结尾和爽文专项 3 轮总验收
```

完成总验收后，运行 stop hook：

```bash
python scripts/novel_hook_guard.py stop ./chinese-novelist/项目文件夹
```

stop hook 失败时，回到输出的 `Next action`，不得进入完成报告。

---

## 5. 完成报告

全部检查结束后，将项目 `status` 更新为：

- `"completed"`：所有章节 completed，且无总验收阻塞项
- `"completed_with_risks"`：存在 blocked 章节或未解决风险

向用户展示：

```text
《[小说名称]》创作完成

总章数：[X] 章
已通过：[X] 章
存在风险：[X] 章
总字数：[X] 字
平均 QA 分：[X]
平均文学质量分：[X]
平均追读力分：[X]
反 AI 门禁：全部通过 / 存在风险
追读门禁：全部通过 / 存在风险
结尾反套路：全部通过 / 存在风险
爽文专项：通过 / 存在风险
自动修复复检：已完成 / 存在待复检风险

关键产物：
- 项目文件夹：./chinese-novelist/[timestamp]-[小说名称]/
- 最终报告：qa/final-report.md
- 时间线：continuity/timeline.md
- 伏笔表：continuity/foreshadowing-ledger.md
- 人物弧线：continuity/character-arcs.md
```

章节状态示例：

```text
PASS 第01章：[标题]（3421字，QA 89）
PASS 第02章：[标题]（3670字，QA 91）
RISK 第08章：[标题]（2980字，已重试3次，字数不足）
```
