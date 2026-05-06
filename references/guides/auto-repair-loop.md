# 自动修复复检循环

本指南定义 Novel Harness 在验收失败后的自动处理方式。任何章节或全书验收不通过，都不得停在“给出建议”；必须生成修复任务，完成修复，再重新发起检测。

## 核心规则

```text
验收失败 -> 生成失败项 -> 定向修复 -> 作废旧检测结论 -> 重新三轮检测 -> 通过后收口
```

硬约束：

- 任一门禁失败，章节不得标记 `completed`。
- 修复阶段只处理失败项，不改动已通过的核心事件、人物关系和结尾策略。
- 修复完成后，上一轮 QA 结论全部作废，不能沿用旧分数。
- 修复后必须重新执行至少 3 轮检测。
- 复检仍失败时，基于新的失败项继续修复。
- 同一章节最多自动修复 3 轮；超过后标记 `blocked`，写入最终报告。

## 失败项来源

失败项必须来自可定位的验收证据：

| 编号前缀 | 来源 |
|---|---|
| `B-XX` | 章节契约、字数、结构、人物、连贯等阻塞项 |
| `A-XX` | 反 AI 与文学质量门禁 |
| `R-XX` | 读者钩子、幽默、亮点、追读力门禁 |
| `M-XX` | 机械化结尾、同质强悬念、追读理由不成立 |
| `S-XX` | 爽文专项、情绪兑现、升级可见、打脸因果 |
| `G-XX` | 黄金三章专项 |
| `C-XX` | 连续性、时间线、伏笔、人物弧线 |

没有失败项编号的 QA 报告不得触发泛泛重写，Evaluator 必须先补齐失败项。

## 状态字段

`02-写作计划.json` 中每章必须维护：

| 字段 | 含义 |
|---|---|
| `repairRequired` | 当前是否仍有失败项需要修复 |
| `needsRecheck` | 修复已完成，是否等待重新三轮检测 |
| `lastFailureCodes` | 最近一次验收失败项编号 |
| `repairRound` | 已执行的自动修复轮次 |
| `repairHistory` | 每轮失败项、修复摘要、复检结果 |
| `lastRepairAt` | 最近一次修复完成时间 |

`repairRound` 与 legacy 字段 `retryCount` 应保持一致。

## 失败后写入

QA 或总验收失败时，State Keeper 写入：

```json
{
  "status": "failed",
  "repairRequired": true,
  "needsRecheck": false,
  "lastFailureCodes": ["A-02", "R-04", "M-01", "S-02", "B-01"],
  "blockingIssues": ["A-02", "R-04", "M-01", "S-02", "B-01"]
}
```

## 修复完成后写入

Fix Writer 完成定向修复后，不得直接写 `completed`。State Keeper 必须作废旧检测结论：

```json
{
  "status": "in_qa",
  "repairRequired": true,
  "needsRecheck": true,
  "qaStatus": null,
  "qualityScore": null,
  "antiAiStatus": null,
  "literaryScore": null,
  "readerHookStatus": null,
  "readerHookScore": null,
  "reviewRoundCount": 0,
  "lastRepairAt": "[ISO时间]"
}
```

`lastFailureCodes` 保留到复检通过，用于确认本轮修复确实覆盖了失败项。

## 复检通过后写入

重新三轮检测全部通过后，才允许清空修复状态：

```json
{
  "status": "completed",
  "repairRequired": false,
  "needsRecheck": false,
  "lastFailureCodes": [],
  "blockingIssues": [],
  "reviewRoundCount": 3
}
```

## 循环伪代码

```text
WHILE chapter is not completed:
    run QA for at least 3 independent rounds
    IF conservative aggregate passes:
        mark_pass
        BREAK

    write failure codes
    IF repairRound >= maxAutoRepairRounds:
        mark blocked
        BREAK

    repairRound += 1
    Fix Writer repairs only failure codes
    invalidate stale QA fields
    rerun QA for at least 3 independent rounds
```

## 禁止行为

- 禁止修复后复用旧 QA 分数。
- 禁止只补检测轮次，不重新阅读修复后的正文。
- 禁止以“已修复”替代复检。
- 禁止为了通过检测删除关键冲突、爽点或人物动机。
- 禁止把严重失败项降级成非阻塞项来绕过自动修复。
