# 第二阶段：规划 + 二次确认

> **前置条件**：本阶段使用 Phase 1 Layer 3 用户确认的小说标题。标题信息从对话上下文中获取，用于命名项目目录、写入大纲文件头和写作计划 JSON。

执行以下步骤：

1. **创建项目文件夹**：`./chinese-novelist/{YYYYMMDD-HHmmss}-{Layer 3 确认的标题}/`（相对当前工作目录，使用用户在 Layer 3 选定的小说标题）
2. **生成质量基准**：创建 `05-质量基准.md`，参考 [quality-baseline-guide.md](../guides/quality-baseline-guide.md)，明确目标读者、阅读场景、作品核心承诺、前三章留存理由、长期追读理由、质量红线、参考作品学习清单、质量评分优先级和读者流失雷区
3. **生成人物档案**：创建 `00-人物档案.md`，使用 [character-template.md](../guides/character-template.md) 模板，参考 [character-building.md](../guides/character-building.md) 创建主角、反派、配角档案。**人物档案必须详细**：每个角色的性格核心、致命缺陷、说话风格/口头禅、恐惧/弱项、背景故事都要具体到可以直接指导写作的程度
4. **生成大纲**：创建 `01-大纲.md`，使用 [outline-template.md](../guides/outline-template.md) 模板，参考 [quality-baseline-guide.md](../guides/quality-baseline-guide.md)、[plot-structures.md](../guides/plot-structures.md)、[web-novel-top-design.md](../guides/web-novel-top-design.md) 和 [golden-three-chapters.md](../guides/golden-three-chapters.md) 填入完整的章节规划。**大纲必须以人物驱动情节** 参照 `00-人物档案.md` 和 `05-质量基准.md`，确保情节服务于人物成长弧线和作品核心承诺
5. **生成黄金三章设计**：创建 `03-黄金三章.md`，明确：
   - 第1章“启示”：主角共鸣特性、当前生活、长钉子、未来展望
   - 第2章“转折”：长钉子如何引爆、主角可能失去什么、为什么不得不行动
   - 第3章“小高潮”：主角如何主动出手、获得什么有限胜利、留下什么更大期待
   - 前三章必须减少无关人物、明确风格路线、保持简洁明快、避免低级错误
6. **生成网文顶层设计**：创建 `04-网文顶层设计.md`，参考 [web-novel-top-design.md](../guides/web-novel-top-design.md)，明确：
   - 读者现实共鸣、情绪出口和代入锚点
   - 本书最离奇或反常识的设定，以及规则、证据、代价、旁人反应如何把它合理化
   - 主角熟悉领域、优势来源、金手指/能力/信息差/资源/身份/经验
   - Core Loop：主角反复进入什么问题、如何解决、获得什么收益、怎样升级、进入什么更难挑战
   - 系统流或非系统规则：触发条件、奖励边界、代价限制、升级路径、情节参与方式
   - 爽点阶梯：小爽点、阶段性大兑现、长期欲望升级
   - 挖坑填坑账本：主线坑、支线坑、每章必须兑现与升级的期待
7. **创建 Novel Harness 目录**：
   - `chapter-contracts/`：每章契约，使用 [chapter-contract-template.md](../guides/chapter-contract-template.md)
   - `scene-cards/`：每章场景卡，使用 [scene-card-template.md](../guides/scene-card-template.md)
   - `qa/`：章节 QA 报告，使用 [qa-report-template.md](../guides/qa-report-template.md)
   - `summaries/`：每章摘要，供后续章节承接
   - `continuity/`：时间线、伏笔表、人物弧线等全书级连续性材料
   - `progress/`：`latest.txt` 和月度进度日志
8. **生成章节契约**：为每一章创建 `chapter-contracts/第XX章.md`。契约必须从 `05-质量基准.md`、`01-大纲.md` 和 `04-网文顶层设计.md` 派生，包含核心事件、承接上章、出场人物、场景列表、章首引子类型、结尾策略、追读理由、质量基准对应承诺、读者流失雷区、代入锚点、合理化说明、Core Loop 步骤、系统/规则参与方式、伏笔要求、验收标准、自动修复复检规则和评分量表，并引用 [quality-baseline-guide.md](../guides/quality-baseline-guide.md)、[scene-card-template.md](../guides/scene-card-template.md)、[editor-gate.md](../guides/editor-gate.md)、[web-novel-top-design.md](../guides/web-novel-top-design.md)、[literary-quality-gate.md](../guides/literary-quality-gate.md)、[reader-hook-gate.md](../guides/reader-hook-gate.md)、[auto-repair-loop.md](../guides/auto-repair-loop.md)。第1-3章必须额外填充“黄金三章专项”。
9. **生成章节场景卡占位**：为每一章创建 `scene-cards/第XX章.md`，使用 [scene-card-template.md](../guides/scene-card-template.md)。规划阶段可先填章节目标和场景骨架，Phase 3 正文前必须补全并通过 `sceneCardStatus`。
10. **生成写作计划**：创建 `02-写作计划.json`，基于质量基准、大纲、网文顶层设计、场景卡和章节契约填充，结构如下：
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
     "qualityBaseline": {
       "enabled": true,
       "baselinePath": "05-质量基准.md",
       "corePromise": "[作品一句话核心承诺]",
       "targetReader": "[核心读者]",
       "openingRetentionHypothesis": "[前三章读者为什么留下]",
       "forbiddenPatterns": ["流水账", "空泛抒情", "低智反派", "机械钩子"]
     },
     "sceneCardPolicy": {
       "enabled": true,
       "directory": "scene-cards",
       "templatePath": "references/guides/scene-card-template.md",
       "requiredBeforeDraft": true
     },
     "editorGate": {
       "enabled": true,
       "guidePath": "references/guides/editor-gate.md",
       "passScore": 85,
       "readerLossRisksMustBeEmpty": true
     },
     "endingPolicy": {
       "avoidFormulaicEndings": true,
       "allowClosedChapterEndings": true,
       "maxConsecutiveStrongSuspenseEndings": 1,
       "strategyPool": [
         "payoff-close",
         "soft-question",
         "decision-point",
         "emotional-aftertaste",
         "resource-reveal",
         "relationship-shift",
         "threat-approach"
       ]
     },
     "webNovelDesign": {
       "enabled": true,
       "designPath": "04-网文顶层设计.md",
       "immersionEngine": {
         "readerResonance": "[读者能共鸣的现实压力、委屈、欲望或关系困境]",
         "emotionalOutlet": "[主角替读者完成的反击、选择或获得]",
         "unreasonablePremise": "[本书最夸张或反常识的设定]",
         "rationalizationRule": "用规则、证据、代价和旁人反应让不合理看似合理"
       },
       "coreLoop": {
         "loopName": "[核心循环名称]",
         "steps": ["进入问题/区域", "解决冲突", "获得收益", "升级", "进入更难问题/区域"],
         "rewardTypes": ["能力", "资源", "身份", "关系", "线索"]
       },
       "protagonistLogic": {
         "familiarDomain": "[主角熟悉领域或经验来源]",
         "advantageSource": "[金手指/能力/信息差/资源/身份/经验]",
         "avoidOutOfDomainYY": true
       },
       "systemLogic": {
         "exists": true,
         "rules": ["触发条件", "奖励边界", "代价限制", "升级路径", "情节参与方式"]
       },
       "expectationPolicy": {
         "pitFillLedger": true,
         "eachChapterMustPayoffAndUpgradeExpectation": true
       }
     },
     "shuangwenConfig": {
       "cadence": "每章至少一次有效情绪兑现，但不固定爽点数量",
       "protagonistAdvantage": "[金手指/能力/信息差/资源/身份/经验]",
       "payoffStyle": "[打脸|反击|升级|奖励|关系推进|真相揭示]",
       "antiRoutineRule": "爽点必须来自人物选择和代价，禁止清单式堆砌"
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
         "title": "[章节标题]",
         "filePath": "第01章-[章节标题].md",
         "contractPath": "chapter-contracts/第01章.md",
         "sceneCardPath": "scene-cards/第01章.md",
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
         "endingStrategy": "[payoff-close|soft-question|decision-point|emotional-aftertaste|resource-reveal|relationship-shift|threat-approach]",
         "immersionAnchor": "",
         "rationalizationNote": "",
         "coreLoopStep": "",
         "systemRuleUse": "",
         "expectationPayoff": "",
         "expectationNext": "",
         "satisfactionBeats": [],
         "formulaicIssues": [],
         "sceneCardStatus": null,
         "sceneCardIssues": [],
         "webNovelStatus": null,
         "webNovelIssues": [],
         "shuangwenStatus": null,
         "shuangwenIssues": [],
         "editorGateStatus": null,
         "editorGateScore": null,
         "readerLossRisks": [],
         "editorGateIssues": [],
         "revisionLevel": null,
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

11. **生成全书连续性占位文件**：
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
