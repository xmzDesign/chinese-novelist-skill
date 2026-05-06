# Hook 生命周期

本文件定义 Novel Hook 在创作流程中的触发顺序。Hook 不是建议项，而是章节状态流转的硬门禁。

## 生命周期图

```text
draft
  -> post-draft hook
  -> humanize
  -> qa（三轮检测）
  -> fail ? fix -> recheck（三轮检测）
  -> pre-mark-pass hook
  -> mark_pass
  -> session-close hook
  -> next chapter
  -> Phase 4
  -> stop hook
```

## 章节级触发点

### 1. Draft 后

正文写完并完成基础字数检查后，运行：

```bash
python scripts/novel_hook_guard.py post-draft ./chinese-novelist/项目文件夹 --chapter <章节号>
```

失败时不得进入下一章，不得声称章节完成。

### 2. Completed 前

准备将章节写入 `status: "completed"` 前，运行：

```bash
python scripts/novel_hook_guard.py pre-mark-pass ./chinese-novelist/项目文件夹 --chapter <章节号>
```

失败时根据输出回到：

- QA 三轮检测
- 自动修复复检
- 反 AI 润色
- 追读力补强
- 黄金三章专项修复

### 3. 每章收口

章节通过 `pre-mark-pass` 并完成摘要、continuity 后，运行：

```bash
python scripts/novel_hook_guard.py session-close ./chinese-novelist/项目文件夹 --note "第<章节号>章 completed"
```

该 hook 会刷新断点，不替代 QA。

## 全书级触发点

Phase 4 最终总验收结束、准备向用户汇报完成前，运行：

```bash
python scripts/novel_hook_guard.py stop ./chinese-novelist/项目文件夹
```

失败时不得汇报“全稿完成”，必须回到 hook 输出的 `Next action`。

## 并行模式要求

子 Agent 并行写作时：

- 子 Agent 必须在自己负责章节内运行 `post-draft`。
- 子 Agent 不得自行运行 `pre-mark-pass` 后写全局 `completed`；它只能在最终报告中说明 hook 结果。
- 主 Agent 或 State Keeper 合并全局状态前，必须统一运行 `pre-mark-pass`。
- 主 Agent 汇报全稿前，必须统一运行 `stop`。

## Stop Hook 阻断条件

出现以下任一情况时，stop hook 必须失败：

- 有章节仍为 `pending`、`in_progress`、`in_qa`、`in_revision` 或 `failed`
- 有章节 `qaStatus != "pass"` 且未 `blocked`
- 有章节检测轮次不足 3
- 有章节仍需修复或复检
- 项目结构校验存在 error

blocked 章节允许进入 `completed_with_risks`，但最终报告必须明确风险。
