# 第四阶段：最终总验收

**目标**：确认全书已完成章节级闭环，并检查全书级连贯性。全程无需用户介入。

Phase 4 不再把所有问题都留到最后补救。章节级字数、人物一致性、承接、结尾钩子和去 AI 味应在 Phase 3 的章节 sprint 内完成。本阶段负责总验收和风险汇总。

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

如果发现章节未完成闭环：

- `retryCount < 3`：回到 Phase 3 对该章执行 fix loop
- `retryCount >= 3`：标记 `blocked`，写入最终报告

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

对总验收发现的问题：

| 问题类型 | 动作 |
|---|---|
| 缺章节文件、缺契约、缺 QA 报告 | 回到 Phase 3 补齐 |
| 字数不足 | 回到 Phase 3 定向扩写 |
| QA 未通过且 retry < 3 | 回到 Phase 3 fix loop |
| 反 AI 门禁失败 | 回到 Phase 3 按 A 类失败项定向修复 |
| 文学质量分不足 | 回到 Phase 3 修复低分维度 |
| 时间线/伏笔/人物弧线轻微矛盾 | 修订对应章节摘要和 continuity 文件；必要时定向修章节 |
| 关键人物或主线严重矛盾 | 标记 blocked，最终报告说明风险和建议 |
| 黄金三章专项失败 | 第1-3章必须回到 Phase 3 修复，超过 3 轮才可标记风险 |

循环规则：

- 最多执行 3 轮总验收-修复循环
- 超过 3 轮仍未解决的问题不阻塞报告生成，但必须明确标注

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
反 AI 门禁：全部通过 / 存在风险

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
