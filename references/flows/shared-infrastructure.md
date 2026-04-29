# 共享机制

本文件定义跨阶段共享的机制和规则。

---

## 黄金法则

1. **展示而非讲述** - 用动作和对话表现，不要直接陈述
2. **冲突驱动剧情** - 每章必须有冲突或转折
3. **悬念承上启下** - 每章结尾必须留下钩子
4. **黄金三章留住读者** - 前三章必须完成启示、转折、小高潮

---

## 用户偏好系统

### 存储文件

`user-preferences.json`（项目根目录，首次使用后自动创建）

### 数据结构

```json
{
  "version": 1,
  "updatedAt": "2026-04-12",
  "preferences": {
    "favoriteGenres": [],
    "preferredProtagonist": "",
    "preferredPerspective": "",
    "preferredTone": "",
    "typicalChapterCount": null,
    "styleReferences": [],
    "dislikes": [],
    "creationHistory": []
  }
}
```

### 偏好更新规则

| 时机 | 行为 |
|------|------|
| 每完成一层问答 | 静默将本层回答同步到偏好文件（追加/更新，不删除历史） |
| 用户说"记住我的偏好" | 保存当前所有配置到偏好 |
| 用户说"忘记XX偏好" | 清除指定维度的偏好 |
| 用户说"重置偏好" | 清空所有偏好数据 |
| 一部长篇创作完成 | 将作品信息追加到 `creationHistory` |

### 偏好如何影响交互

1. **启动欢迎语**：有偏好时显示"欢迎回来！" + 个性化提示
2. **选项排序**：Q1中将 `favoriteGenres` 匹配项排前面
3. **常用标记**：Q5/Q8中对应用⭐标记"你的常用"/"上次选择"
4. **需求报告**：结合偏好给个性化建议（如"你之前喜欢悬疑+第三人称限制，这次要不要试试多视角？"）
5. **随机生成**：优先从偏好范围内随机选取，保持一致性
6. **风格参考追问**：优先推荐 `styleReferences` 中的作者

### 错误恢复

- **回退修改**：用户随时可说"回到QX"、"修改XX"，AI 回退到指定问题重新询问
- **中途暂存**：通过 `02-写作计划.json` 实现自动暂存；下次触发SKILL时 Phase 0 自动检测未完成项目，询问"继续上次的《XXX》？"
- **偏好文件损坏**：JSON解析失败时忽略偏好，使用默认值，并在后台修复文件

---

## 标题传递机制

### 传递方式

标题通过**对话上下文**在阶段间传递，不单独持久化到文件。

**传递链路**：
1. Phase 1 Layer 3：用户选择/确认标题 → 标题存入对话上下文
2. Phase 2：从上下文读取标题 → 写入项目目录名、`02-写作计划.json`、`01-大纲.md`

### 中断恢复

若会话在 Layer 3 完成、Phase 2 开始前中断：
- Phase 0 不会找到已创建的项目目录（因为 Phase 2 尚未执行）
- 用户将重新进入 Layer 3 重新选择标题（标题选择耗时很短，重新选择成本可接受）

## 写作计划系统

### 存储文件

`02-写作计划.json`（项目文件夹内，Phase 2 创建）

### 作用

- **进度跟踪**：记录每章创作状态（pending/in_progress/completed/failed）
- **写作模式**：记录用户选择的写作模式（serial/subagent-parallel/agent-teams）
- **章节契约**：记录每章 `contractPath`，让写作和 QA 使用同一套验收标准
- **QA 闭环**：记录 `qaReportPath`、`qaStatus`、`qualityScore`、`blockingIssues`
- **文学质量**：记录 `antiAiStatus`、`literaryScore`、`aiTraceIssues`
- **黄金三章**：记录 `goldenThree` 和前三章 `goldenThreeRole`
- **中断续写**：Phase 0 读取 JSON 检测未完成项目，支持从断点继续
- **校验依据**：Phase 4 基于 JSON 校验章节闭环、字数、QA 和总体验收
- **并行协调**（可选）：多 Agent 并行写作时通过 owner、章节契约和状态避免冲突

### 与大纲的关系

- `01-大纲.md`：章节规划（核心事件、悬念钩子、承接上章、出场人物、场景列表）+ 章节摘要（连贯性参考）
- `chapter-contracts/第XX章.md`：从大纲派生的章节验收契约，是 Writer 和 Evaluator 的共同标准
- `02-写作计划.json`：章节状态、字数、QA、重试次数、写作模式（机器可读的进度跟踪）
- Phase 3 创作每章时必须读取章节契约、`01-大纲.md` 对应章节规划、`00-人物档案.md` 和上一章摘要
- 三者严格对应：JSON 中的 `chapterNumber`、`title`、`contractPath` 必须与大纲章节规划一致

### 推荐 JSON v2 字段

```json
{
  "version": 2,
  "harness": {
    "maxRevisionRounds": 3,
    "passScore": 85,
    "literaryPassScore": 80,
    "goldenThreeLiteraryPassScore": 85,
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
      "title": "章节标题",
      "filePath": "第01章-章节标题.md",
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
      "blockingIssues": [],
      "retryCount": 0
    }
  ]
}
```

### 状态流转

```text
pending -> in_progress -> in_qa -> completed
                         -> in_revision -> in_qa
                         -> failed -> in_revision
                         -> blocked
```

章节只有在以下条件同时满足时才能标记 `completed`：

- 章节文件存在
- 字数检查通过
- QA 报告存在
- `qaStatus == "pass"`
- `qualityScore >= 85`
- `antiAiStatus == "pass"`
- 普通章节 `literaryScore >= 80`
- 第1-3章 `literaryScore >= 85`
- `blockingIssues` 为空

### JSON 损坏处理

- JSON 解析失败时：提示用户，尝试从大纲的章节摘要区推断完成进度
- 章节状态丢失时：通过文件存在性和字数脚本重建状态

---

## 文学质量与反 AI 系统

参考：[literary-quality-gate.md](../guides/literary-quality-gate.md)

目标：

- 不依赖外部 AI 检测器
- 用文本证据判断 AI 痕迹
- 用文学质量评分约束最低可读性
- 用 A 类问题编号支持定向修复

核心字段：

| 字段 | 含义 |
|---|---|
| `antiAiStatus` | `pass` / `fail`，任一严重 AI 痕迹出现即 fail |
| `literaryScore` | 0-100，普通章节 >=80，第1-3章 >=85 |
| `aiTraceIssues` | A 类问题编号，如 `A-01`、`A-02` |

反 AI 一票否决项：

- 人物说话同质化
- 情绪全靠概括
- 空泛形容堆砌
- 四字套话过多
- 段落节奏模板化
- 解释替代表演
- 低级连续性错误
- 爽点或冲突缺席

章节只有 `antiAiStatus == "pass"` 且 `literaryScore` 达标时，才允许 `completed`。

---

## 黄金三章系统

存储位置：`03-黄金三章.md`

参考：[golden-three-chapters.md](../guides/golden-three-chapters.md)

作用：

- 在 Phase 1 收集主角共鸣特性
- 在 Phase 2 设计前三章的启示、转折、小高潮
- 在 Phase 3 对前三章写作和 QA 加专项门禁
- 在 Phase 4 做开篇留存总验收

前三章职责：

| 章节 | 角色 | 必须完成 |
|---|---|---|
| 第1章 | 启示 | 主角共鸣、当前生活、长钉子、未来展望 |
| 第2章 | 转折 | 引爆长钉子、重大损失、不得不行动 |
| 第3章 | 小高潮 | 主动出手、有限胜利、更大期待 |

第1-3章如果黄金三章专项失败，不得标记 `completed`。

---

## 章节契约与 QA 系统

### 章节契约

存储位置：`chapter-contracts/第XX章.md`

模板：[chapter-contract-template.md](../guides/chapter-contract-template.md)

用途：

- 把大纲规划转成可验收标准
- 约束 Chapter Writer 不偏离主线
- 约束 Evaluator 只按契约评分
- 支持失败项定向修复

### QA 报告

存储位置：`qa/第XX章.md`

模板：[qa-report-template.md](../guides/qa-report-template.md)

评分：

| 维度 | 分值 |
|---|---:|
| 字数与结构 | 10 |
| 大纲履约 | 20 |
| 承接与连贯 | 15 |
| 人物一致性 | 15 |
| 冲突与节奏 | 10 |
| 对话质量 | 10 |
| 结尾钩子 | 10 |
| 去 AI 味与文字质感 | 10 |

判定：

- `PASS`：总分 >= 85，且无阻塞项
- `PARTIAL`：总分 70-84，或存在非阻塞失败项
- `FAIL`：总分 < 70，或存在任一阻塞项

Evaluator 必须给出证据和修复建议，不能只输出主观评价。

---

## 进度收口系统

每章完成后刷新：

- `progress/latest.txt`：最近完成章节、QA 分数、阻塞项、下一章
- `progress/YYYY-MM.md`：月度追加记录

进度快照用于中断续写和并行写作交接。快照必须短，不替代章节摘要。

---

## 字数检查脚本

使用 `scripts/check_chapter_wordcount.py` 检查章节字数：

```bash
# 检查单个章节
python scripts/check_chapter_wordcount.py ./chinese-novelist/项目文件夹/第01章.md

# 检查所有章节
python scripts/check_chapter_wordcount.py --all ./chinese-novelist/项目文件夹/

# 自定义最小字数
python scripts/check_chapter_wordcount.py ./chinese-novelist/项目文件夹/第01章.md 3500
```

### 使用场景

| 阶段 | 用途 |
|------|------|
| Phase 3（逐章创作） | 撰写后检查单章字数，低于3000字必须扩充 |
| Phase 4（最终总验收） | 批量复查所有章节字数，发现问题回到章节 sprint |

低于3000字的章节必须使用 [content-expansion.md](../guides/content-expansion.md) 的扩充技巧进行扩充。

## 项目结构校验脚本

使用 `scripts/validate_novel_project.py` 检查轻量 Novel Harness 产物：

```bash
python scripts/validate_novel_project.py ./chinese-novelist/项目文件夹
python scripts/validate_novel_project.py ./chinese-novelist/项目文件夹 --json
```

检查内容：

- `02-写作计划.json` 是否存在且可解析
- 每章章节文件、章节契约、QA 报告、摘要路径是否符合状态
- 已完成章节是否字数达标、QA 通过、无阻塞项
- 项目目录是否包含 `chapter-contracts/`、`qa/`、`summaries/`、`continuity/`、`progress/`
