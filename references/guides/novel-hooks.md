# Novel Hook 机制

Novel Hook 用来解决模型写完章节后跳过检查、优化、复检的问题。它借鉴 by-harness 的 stop hook 和 pre-completion hook，但保持轻量，只围绕小说章节闭环生效。

## Hook 列表

| Hook | 触发时机 | 目标 |
|---|---|---|
| `post-draft` | 章节正文写完后 | 阻止无正文、无契约、字数不足的章节进入 QA |
| `pre-mark-pass` | 章节标记 `completed` 前 | 阻止未 QA、未三轮检测、未修复复检的章节通过 |
| `stop` | 汇报全稿完成前 | 阻止模型跳过章节 QA、Phase 4 或总验收 |
| `session-close` | 每次会话结束或暂停前 | 刷新进度快照，确保下次能从正确断点继续 |

## 命令

```bash
python scripts/novel_hook_guard.py post-draft ./chinese-novelist/项目文件夹 --chapter 1
python scripts/novel_hook_guard.py pre-mark-pass ./chinese-novelist/项目文件夹 --chapter 1
python scripts/novel_hook_guard.py stop ./chinese-novelist/项目文件夹
python scripts/novel_hook_guard.py session-close ./chinese-novelist/项目文件夹 --note "第1章 QA 后待修复"
```

所有 hook 均支持 JSON 输出：

```bash
python scripts/novel_hook_guard.py pre-mark-pass ./chinese-novelist/项目文件夹 --chapter 1 --json
```

## post-draft Hook

章节写完正文后立即运行。

必须通过：

- `contractPath` 指向的章节契约存在
- `filePath` 指向的章节正文存在
- 章节字数达到 `minWordsPerChapter`

失败时动作：

- 字数不足：回到 draft 或 humanize 扩写
- 缺章节契约：回到 Phase 2 或 contract check 补齐
- 缺正文：回到 draft

## pre-mark-pass Hook

任何章节写入 `status: "completed"` 前必须运行。

必须通过：

- QA 报告存在
- `qaStatus == "pass"`
- `qualityScore >= passScore`
- `antiAiStatus == "pass"`
- `literaryScore` 达标
- `readerHookStatus == "pass"`
- `readerHookScore` 达标
- `memorableMoment` 非空
- `chapterTurnPageHook` 非空
- `reviewRoundCount >= requiredReviewPasses`
- `blockingIssues` 为空
- `aiTraceIssues` 为空
- `highlightIssues` 为空
- `repairRequired == false`
- `needsRecheck == false`
- `lastFailureCodes` 为空

失败时动作：

- 不是 pass：回到 QA 或 fix
- 检测轮次不足：重新三轮检测
- 待修复：执行自动修复复检循环
- 待复检：直接重新三轮检测

## stop Hook

模型准备对用户汇报“全稿完成”“已经写好”“全部结束”之前必须运行。

必须通过：

- `validate_novel_project.py` 无 error
- 所有章节状态为 `completed` 或 `blocked`
- 没有章节 `repairRequired == true`
- 没有章节 `needsRecheck == true`

失败时动作：

- 不得向用户汇报完成
- 根据 hook 输出的 `Next action` 回到对应章节继续

## session-close Hook

每章完成后、会话暂停前、上下文即将耗尽前运行。

作用：

- 刷新 `progress/latest.txt`
- 追加 `progress/YYYY-MM.md`
- 写清当前完成进度、风险和下一步

session-close hook 不代表章节通过，只负责断点保存。

## 硬约束

- 写完正文后，未运行 `post-draft` 不得进入下一章。
- 标记 `completed` 前，未运行 `pre-mark-pass` 不得收口。
- 汇报全稿完成前，未运行 `stop` 不得结束。
- hook 失败时，必须按 `Next action` 继续执行，不向用户请求确认。

## 回归验证

修改 hook 或状态字段后，运行：

```bash
python scripts/smoke_novel_flow.py
```

该脚本会生成临时 fixture 项目，验证通过项目、缺 QA、待复检、低分和 blocked 风险章节等关键路径。
