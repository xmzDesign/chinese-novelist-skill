# 第二阶段：规划 + 二次确认

> **前置条件**：本阶段使用 Phase 1 Layer 3 用户确认的小说标题。标题信息从对话上下文中获取，用于命名项目目录、写入大纲文件头和写作计划 JSON。

执行以下步骤：

1. **创建项目文件夹**：`./chinese-novelist/{YYYYMMDD-HHmmss}-{Layer 3 确认的标题}/`（相对当前工作目录，使用用户在 Layer 3 选定的小说标题）
2. **生成人物档案**：创建 `00-人物档案.md`，使用 [character-template.md](../guides/character-template.md) 模板，参考 [character-building.md](../guides/character-building.md) 创建主角、反派、配角档案。**人物档案必须详细**：每个角色的性格核心、致命缺陷、说话风格/口头禅、恐惧/弱项、背景故事都要具体到可以直接指导写作的程度
3. **生成大纲**：创建 `01-大纲.md`，使用 [outline-template.md](../guides/outline-template.md) 模板，参考 [plot-structures.md](../guides/plot-structures.md) 和 [golden-three-chapters.md](../guides/golden-three-chapters.md) 填入完整的章节规划。**大纲必须以人物驱动情节** 参照 `00-人物档案.md`，确保情节服务于人物成长弧线
4. **生成黄金三章设计**：创建 `03-黄金三章.md`，明确：
   - 第1章“启示”：主角共鸣特性、当前生活、长钉子、未来展望
   - 第2章“转折”：长钉子如何引爆、主角可能失去什么、为什么不得不行动
   - 第3章“小高潮”：主角如何主动出手、获得什么有限胜利、留下什么更大期待
   - 前三章必须减少无关人物、明确风格路线、保持简洁明快、避免低级错误
5. **创建 Novel Harness 目录**：
   - `chapter-contracts/`：每章契约，使用 [chapter-contract-template.md](../guides/chapter-contract-template.md)
   - `qa/`：章节 QA 报告，使用 [qa-report-template.md](../guides/qa-report-template.md)
   - `summaries/`：每章摘要，供后续章节承接
   - `continuity/`：时间线、伏笔表、人物弧线等全书级连续性材料
   - `progress/`：`latest.txt` 和月度进度日志
6. **生成章节契约**：为每一章创建 `chapter-contracts/第XX章.md`。契约必须从 `01-大纲.md` 的章节规划派生，包含核心事件、承接上章、出场人物、场景列表、章首引子类型、结尾钩子、伏笔要求、验收标准、自动修复复检规则和评分量表，并引用 [literary-quality-gate.md](../guides/literary-quality-gate.md)、[reader-hook-gate.md](../guides/reader-hook-gate.md)、[auto-repair-loop.md](../guides/auto-repair-loop.md)。第1-3章必须额外填充“黄金三章专项”。
7. **生成写作计划**：创建 `02-写作计划.json`，基于大纲和章节契约填充，结构如下：
   ```json
   {
     "version": 2,
     "novelName": "[小说名称]",
     "projectPath": "./chinese-novelist/{timestamp}-[小说名称]",
     "totalChapters": [章节数],
     "minWordsPerChapter": 3000,
     "maxWordsPerChapter": 5000,
     "createdAt": "[ISO时间]",
     "updatedAt": "[ISO时间]",
     "status": "planning",
     "writingMode": "[serial|subagent-parallel|agent-teams]",
     "harness": {
       "maxRevisionRounds": 3,
       "qaReviewRounds": 3,
       "requiredReviewPasses": 3,
       "finalValidationRounds": 3,
       "autoRepairEnabled": true,
       "maxAutoRepairRounds": 3,
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
         "title": "[章节标题]",
         "filePath": "第01章-[章节标题].md",
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

8. **生成全书连续性占位文件**：
   - `continuity/timeline.md`：记录日期、地点、事件顺序
   - `continuity/foreshadowing-ledger.md`：记录伏笔的埋设、推进、回收
   - `continuity/character-arcs.md`：记录主要人物的阶段性变化
   - `progress/latest.txt`：记录最近完成章节、QA 状态、下一步

完成后，执行以下两步：

**1. 展示规划摘要并请求确认**

向用户展示规划摘要（小说名称、总章数、目标字数、主要人物）并请求确认。

**2. 写作模式选择**（用户确认规划后）

使用 `AskUserQuestion` 询问：

```
Question: 选择写作模式
Options:
- 逐章串行（主 Agent 自己逐章写，全程无中断，适合短中篇）
- 子Agent并行（按故事弧派生子 Agent 并行写作，章节契约驱动连贯性，适合中长篇）
- Agent Teams（Claude Code 多 Agent 协作模式，Agent 间可通讯，需手动开启）
```

用户选择后：
- 更新 `02-写作计划.json` 的 `writingMode` 字段
- 更新 `status` 为 `"in_progress"`
- 确认所有章节均存在 `contractPath`
- 进入第三阶段：Novel Harness 章节创作 → 详见 [phase3-writing.md](phase3-writing.md)
