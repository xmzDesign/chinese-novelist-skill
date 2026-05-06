<div align="center">

# 🎭 chinese-novelist skill

### 让 AI 为你写一部完整的中文小说

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/PenglongHuang/chinese-novelist-skill/releases/tag/v2.0)
[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blue)](https://claude.com/claude-code)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **🎉 v2.0 重构发布**：引入三层递进式问答、偏好记忆系统、中断续写、三种写作模式和自动校验修复复检！
>
> 查看 [v1.0 → v2.0 升级说明](https://github.com/PenglongHuang/chinese-novelist-skill/pull/10) 了解详情。

</div>


## ✨ 为什么用这个？

写小说最难的是**坚持写完**。这个 Skill 专为解决这个痛点而生：

- **智能问答** - 三层递进式问答，支持快速跳过和随机生成
- **黄金三章** - 开篇三章按“启示 / 转折 / 小高潮”设计和验收
- **文学质量门禁** - 反 AI 一票否决 + 文学评分 + 证据化修复
- **追读力门禁** - 每章有亮点、幽默/反差调味和明确追读理由
- **爽文专项** - 所有小说都检查爽点节拍、情绪兑现和升级可见
- **反套路结尾** - 用结尾策略轮换拦截每章同质硬钩子
- **三轮检测** - 所有 QA 至少重复 3 轮，按保守结果放行
- **自动修复复检** - 验收失败自动修，修完重新三轮检测
- **Novel Hook** - 写完、放行、停止和收口前强制拦截漏检漏修
- **运行时初始化** - 一键生成 `AGENTS.md`、`CLAUDE.md`、Claude/Codex hook 配置
- **偏好记忆** - 跨会话学习你的喜好，下次创作更贴心
- **中断续写** - 意外中断？自动检测并从断点继续
- **多种写作模式** - 串行 / 子Agent并行 / Agent Teams，按需选择
- **Novel Harness** - 每章按契约写作、hook、QA、修复、复检、收口，避免长篇越写越散
- **自动校验** - 每章生成 QA 报告，完成后做全书连续性验收，失败自动回修
- **节拍有爽感** - 开头抓人、过程有兑现、结尾有追读理由

## 🚀 快速开始

安装skill：`npx skills add PenglongHuang/chinese-novelist-skill`

输入指令：`使用 chinese-novelist 帮我写一部小说`

可选：在目标仓库初始化 Novel Harness 运行时入口和 hooks：

```bash
python scripts/init_novel_harness.py --target-dir .
```

## 🖼️ 使用过程

<table>
  <tr>
    <td align="center"><b>Phase 1 — 交互问答</b></td>
    <td align="center"><b>Phase 2 — 规划确认</b></td>
  </tr>
  <tr>
    <td><img src="assets/phase1-qa.png" width="400"/></td>
    <td><img src="assets/phase2-plan.png" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><b>Phase 3 — Novel Harness 创作</b></td>
    <td align="center"><b>Phase 4 — 完稿输出</b></td>
  </tr>
  <tr>
    <td><img src="assets/phase3-writing.png" width="400"/></td>
    <td><img src="assets/phase4-done.png" width="400"/></td>
  </tr>
</table>


## 🧠 创作记忆

每次创作后，Skill 会自动学习你的偏好：喜欢的题材类型、叙事风格、章节数量倾向、文字密度等。下次使用时，直接应用你的习惯，省去重复问答。

<p align="center">
  <img src="assets/memory-demo.png" width="600"/>
</p>


## 📊 创作流程

```
用户 → ┌─────────────┐    ┌──────────────────────┐    ┌──────────────┐
       │ Phase 0     │ →  │ Phase 1              │ →  │ Phase 2      │
       │ 初始化      │    │ 三层递进式问答        │    │ 规划 + 确认  │
       │ ·加载偏好   │    │ L1: 核心定位 (必答)   │    │ ·大纲        │
       │ ·检测中断   │    │ L2: 深度定制 (可选)   │    │ ·人物档案    │
       └─────────────┘    └──────────────────────┘    │ ·写作计划JSON│
                                                     └──────┬───────┘
                                                            ↓
                                            ┌───────────────────────────┐
                                            │ Phase 2.5 写作模式选择     │
                                            │ 串行 / 子Agent并行 / Teams │
                                            └─────────┬─────────────────┘
                                                      ↓
       ┌──────────────────────────────────────────────────────────────┐
       │ Phase 3 Novel Harness 创作（全自动，无需确认）                │
       │ 逐章：契约 → 初稿 → Hook → QA → 修复 → 复检 → Hook → 收口    │
       └──────────────────────────────────────────────────────────────┘
                            ↓
       ┌──────────────────────────────────────────────────────────────┐
       │ Phase 4 最终总验收（全自动）                                  │
       │ 章节闭环检查 → 全书连续性检查 → 风险汇总                     │
       └──────────────────────────────────────────────────────────────┘
                            ↓
                       ✅ 全稿完成
```

### Phase 0：初始化

自动加载用户偏好（`user-preferences.json`），检测是否有未完成的项目可续写，展示个性化欢迎。

### Phase 1：三层递进式问答

**Layer 1 — 核心定位（必答，3问）**：题材创意、主角设定、核心冲突

**Layer 2 — 深度定制（可选，5问）**：世界观、叙事视角、核心主题、读者定位、章节数量

> 每个问题都支持🎲随机生成，也可以直接说"跳过"或"都用默认"。

```
📝 Q1：题材与创意
   ○ 悬疑推理   ○ 现代言情   ○ 奇幻玄幻   ○ 科幻未来
   ○ 武侠仙侠   ○ 历史架空   ○ 都市现实   ○ 🎲 随机生成

📝 Q2：主角设定
   ○ 男性主角   ○ 女性主角   ○ 双主角     ○ 群像戏

📝 Q3：核心冲突
   ○ 生死存亡   ○ 查明真相   ○ 复仇雪恨   ○ 成长突破
   ○ 爱情阻碍   ○ 权力争夺   ○ 守护保护

   ... Layer 2 可继续定制，也可直接跳到规划 ...
```

### Phase 2：规划 + 确认

AI 自动生成大纲（7列章节规划）、人物档案、写作计划 JSON，展示给你确认：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
规划完成！请确认：

基本信息
  题材：悬疑推理  |  主角：男性侦探  |  冲突：查明真相
  章节数：20章    |  视角：第一人称  |  基调：紧张冷峻

章节规划（前5章）
  第1章：午夜凶铃 - 接到神秘电话...
  第2章：第一具尸体 - 发现密室杀人案...
  ...

主要角色
  主角：李明 - 资深刑警，冷静智慧
  反派：张华 - 高智商罪犯
  配角：王芳 - 法医专家

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
回复"确认" → 选择写作模式 → 立即开始
```

### Phase 2.5：写作模式选择

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **串行** | 主 Agent 逐章写，稳定可靠 | 默认推荐 |
| **子Agent并行** | 多个子 Agent 分批并行写 | 追求速度 |
| **Agent Teams** | Claude Code 多 Agent 协作 | 大型长篇 |

### Phase 3：Novel Harness 创作

确认后进入全自动创作模式，无需再次确认。你可以离开工作台，等待完成。

每章严格执行：读取章节任务 → 检查章节契约 → 撰写(3000-5000字) → 去AI味润色 → post-draft hook → QA评分 → 失败项定向修复 → 修复后重新三轮检测 → pre-mark-pass hook → 标记通过 → session-close hook。

```
✅ 第1章完成（3247字，QA 89）
✅ 第2章完成（3582字，QA 91）
✅ 第3章完成（3412字，QA 87）
...
```

### Phase 4：最终总验收

全稿完成后自动检查：章节文件、章节契约、QA 报告、摘要、字数、时间线、伏笔闭环、人物弧线。未闭环章节回到 Phase 3 修复，修复后重新发起检测，最多3轮。最终汇报前运行 stop hook。

---

## 📖 输出样例

```
chinese-novelist/
├── user-preferences.json              # 用户偏好（跨项目共享）
└── 20260412-143000-午夜列车/
    ├── 01-大纲.md                      # 故事概述、章节规划（7列模板）
    ├── 00-人物档案.md                  # 主角、反派、配角档案
    ├── 02-写作计划.json                # 机器可读的写作计划（v2）
    ├── 03-黄金三章.md                  # 开篇三章设计
    ├── chapter-contracts/              # 每章契约
    ├── qa/                             # 章节 QA 与最终报告
    ├── summaries/                      # 每章摘要
    ├── continuity/                     # 时间线、伏笔表、人物弧线
    ├── progress/                       # 中断续写快照
    ├── 第01章-最后一班列车.md
    ├── 第02章-消失的乘客.md
    └── ...
```

---

## 🎯 核心法则

| 法则 | 说明 |
|-----|------|
| **展示而非讲述** | 用动作和对话表现，不要直接陈述 |
| **冲突驱动剧情** | 每章必须有冲突或转折 |
| **期待承上启下** | 每章必须有追读理由，但不强制硬悬念 |
| **开头即高潮** | 前 20% 必须极其吸引人 |
| **黄金三章** | 前三章完成启示、转折、小高潮 |
| **反 AI 门禁** | 严重 AI 痕迹一票否决，必须定向修复 |
| **追读力门禁** | 每章必须有记忆点、局部兑现和追读理由 |
| **爽文专项** | 所有小说必须有有效爽点节拍、情绪兑现和升级可见 |
| **反套路结尾** | 连续章节不得重复同质强悬念钩子 |
| **三轮检测** | 所有检测至少 3 轮，任一轮阻塞失败不得通过 |
| **自动修复复检** | 验收失败自动修复，修复后旧结论作废并重新检测 |
| **Novel Hook** | post-draft、pre-mark-pass、stop、session-close 拦截漏检 |

---

## 🛠️ 安装

将此目录放入 Claude Code 的 skills 目录：

```
~/.claude/skills/chinese-novelist/
```

或通过 Claude Code 技能管理界面安装。

---

## 📚 内置参考资料

### 流程文档（`references/flows/`）

| 文件 | 内容 |
|------|------|
| `phase0-initialization.md` | Phase 0：初始化与偏好加载 |
| `phase1-layer1-core.md` | Phase 1 Layer 1：核心定位问答（Q1-Q3） |
| `phase1-layer2-customize.md` | Phase 1 Layer 2：深度定制问答（Q4-Q8） |
| `phase2-planning.md` | Phase 2：规划与写作计划生成 |
| `phase3-writing.md` | Phase 3：Novel Harness 章节创作（三种写作模式） |
| `phase4-validation.md` | Phase 4：最终总验收 |
| `shared-infrastructure.md` | 共享机制（偏好系统、章节契约、文学质量、追读力、三轮检测、Hook、QA、进度收口、字数脚本） |
| `hook-lifecycle.md` | Hook 生命周期与触发点 |

### Agent 角色（`references/agents/`）

| 文件 | 内容 |
|------|------|
| `novel-harness-agents.md` | Novel Harness 多 Agent 角色边界与写入权限 |

### 写作指南（`references/guides/`）

| 文件 | 内容 |
|------|------|
| `chapter-guide.md` | 章节写作指南（含开头技巧、中文文学技法、连贯性保证、质量检查） |
| `hook-techniques.md` | 悬念和追读理由技巧（含结尾策略参考） |
| `character-building.md` | 人物塑造技法（侧重写作过程中的塑造技巧） |
| `dialogue-writing.md` | 对话写作规范（含节奏进阶、权力博弈） |
| `plot-structures.md` | 情节结构模板 |
| `content-expansion.md` | 内容扩充技巧（含分题材策略、实例对比） |
| `golden-three-chapters.md` | 黄金三章指南（启示、转折、小高潮） |
| `literary-quality-gate.md` | 文学质量与反 AI 门禁 |
| `reader-hook-gate.md` | 追读理由、幽默、亮点、爽文专项与反套路门禁 |
| `auto-repair-loop.md` | 验收失败后的自动修复与复检循环 |
| `novel-hooks.md` | post-draft、pre-mark-pass、stop、session-close hook 规则 |
| `outline-template.md` | 大纲模板（7列章节规划） |
| `character-template.md` | 人物档案模板 |
| `chapter-template.md` | 章节文件模板 |
| `chapter-contract-template.md` | 章节契约模板 |
| `qa-report-template.md` | QA 报告模板 |

### 脚本（`scripts/`）

| 文件 | 内容 |
|------|------|
| `check_chapter_wordcount.py` | 自动检查章节字数是否达标 |
| `validate_novel_project.py` | 校验 Novel Harness 项目结构和章节闭环 |
| `novel_hook_guard.py` | 执行 post-draft、pre-mark-pass、stop、session-close hook |
| `novel_runtime_hook.py` | Claude/Codex hook 的统一运行时入口 |
| `init_novel_harness.py` | 初始化 `AGENTS.md`、`CLAUDE.md`、`.claude/` 和 `.codex/` |
| `smoke_novel_flow.py` | 一键验证整体 flow 的通过和失败路径 |

---

## 🔄 版本更新

### v2.0 → v1.0 重大升级

**核心架构重构**
- ✅ 从单一 5 问流程升级为**三层递进式问答**（Layer 1 必答 + Layer 2 可选深度定制）
- ✅ 新增 **Phase 0 初始化**：用户偏好跨会话记忆、中断续写检测
- ✅ 新增 **写作模式选择**：串行/子Agent并行/Agent Teams 三种模式
- ✅ 新增 **Phase 4 自动校验**：字数与连贯性自动检查，不合格自动修复并复检
- ✅ 流程文档化：将详细执行指令从 SKILL.md 拆分到 `references/flows/` 独立维护

**新增功能**
- 🧠 **偏好记忆系统**：自动学习用户创作偏好（题材类型、叙事风格、章节数量倾向等）
- ⏸️ **中断续写**：自动检测未完成项目，支持从断点继续创作
- 📋 **写作计划 JSON**：机器可读的写作状态文件，支持并行写作协调
- 🧷 **Claude/Codex Hooks**：初始化后自动拦截漏检、漏修和未复检收口
- 🔢 **字数检查脚本**：`scripts/check_chapter_wordcount.py` 自动验证每章 3000-5000 字要求
- 🧪 **Flow Smoke Test**：`scripts/smoke_novel_flow.py` 一键验证 hook 与状态流转

**文档重组**
- 📁 `references/flows/`：新增 7 个流程文档（phase0-4 + shared-infrastructure）
- 📁 `references/guides/`：重组写作指南文档，新增质量门禁、追读门禁和自动修复复检规则

**查看完整变更**：[v2.0 提交记录](https://github.com/PenglongHuang/chinese-novelist-skill/commits/v2.0/)

---

## ⚖️ 许可

MIT
