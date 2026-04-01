# AI 设计驱动实现 Toolkit

本套 skill **主要面向 [OpenCode](https://open-code.ai/)**：仓库根目录 [`AGENTS.md`](../AGENTS.md) 为项目规则入口，[`opencode.json`](../opencode.json) 通过 `instructions` 合并 [`SKILL.md`](SKILL.md) 索引。

> 快速参考: [SKILL.md](SKILL.md) — Skill 索引与命令速查。权威定义为 `skill/<name>/SKILL.md`（YAML frontmatter），目录形状与 [superpowers/skills](https://github.com/obra/superpowers/tree/main/skills) 一致。**镜像**：OpenCode 使用 `.opencode/skills/`（见 [`.opencode/README.md`](../.opencode/README.md)）；Cursor 使用 `.cursor/skills/`（见 [`.cursor/README.md`](../.cursor/README.md)）。修改 `skill/` 后运行 **`scripts/sync-ide-mirrors.ps1`** 或 **`sync-ide-mirrors.sh`** 一次更新两侧，或分别运行 `sync-opencode-skills` / `sync-cursor-skills`。

## 1. Overview

本 Toolkit 用于在**单仓库、单服务**场景下，建立一套"根据结构化设计文档驱动 AI 持续完成代码实现"的 skill 体系。

Toolkit 重点解决三个核心问题：

1. **持续代码生成** — 将实现过程拆分为可独立执行的最小切片，支持连续运行与断点恢复
2. **质量保证** — 在每个切片完成后内建验证关卡，防止偏差积累
3. **结果沉淀** — 将关键决策、偏差、验证结果和交付索引转化为可复用资产

设计文档输入以 Markdown 为主；PDF 可作为参考材料，但最终必须收敛为结构化 Markdown。

---

## 2. Design Principles

| # | 原则 | 说明 |
|---|------|------|
| 1 | **文档先行** | AI 不基于零散描述编码，而是基于结构化设计文档进行实现 |
| 2 | **切片执行** | 以可独立验证的最小切片推进，避免一次性生成大批代码而失控 |
| 3 | **状态可恢复** | 每个阶段有显式状态记录，支持失败重试、断点续跑与人工接管 |
| 4 | **验证内建** | 质量检查嵌入在每个切片完成后的必经关卡，而非收尾动作 |
| 5 | **结果沉淀** | 所有关键决策、偏差、验证结果和交付索引都形成可复用资产 |

---

## 3. Architecture

Toolkit 分为六层：

| 层 | 名称 | 职责 |
|----|------|------|
| 1 | **文档规范层** | 定义设计文档格式与模板，使设计既适合人工评审，也适合 AI 理解与执行 |
| 2 | **文档建模层** | 将设计文档解析为统一实现模型，提取模块、接口、数据结构、约束、风险点与测试点 |
| 3 | **编排执行层** | 将设计实现流程拆分为可连续运行的阶段任务，提供状态机、切片调度、失败重试与断点恢复 |
| 4 | **代码生成层** | 按切片完成代码实现，输出业务代码、测试代码、配置文件与辅助文档 |
| 5 | **质量保障层** | 对每个切片和整体结果进行自动验证，包括设计一致性检查、静态分析与测试执行 |
| 6 | **沉淀控制层** | 将执行过程和结果转化为长期资产，包括追踪矩阵、偏差说明、运行报告与交付索引 |

---

## 4. Skill System

Toolkit 组织为 **9 个流水线 skill** 与 **1 个工具 skill**（`run-status`，不推进阶段顺序）：

| Skill | 文件 | 说明 |
|-------|------|------|
| `run-status` | [`run-status/SKILL.md`](run-status/SKILL.md) | 解读 `state.md`，输出续跑建议（只读，可选写 `stages/plan/run-status.md`） |
| `run-init` | [`run-init/SKILL.md`](run-init/SKILL.md) | 初始化 run 目录结构与状态文件 |
| `design-intake` | [`design-intake/SKILL.md`](design-intake/SKILL.md) | 验证设计文档完整性 |
| `design-normalize` | [`design-normalize/SKILL.md`](design-normalize/SKILL.md) | 规范化设计文档 |
| `design-to-plan` | [`design-to-plan/SKILL.md`](design-to-plan/SKILL.md) | 设计转实现计划 |
| `plan-to-slices` | [`plan-to-slices/SKILL.md`](plan-to-slices/SKILL.md) | 实现计划拆切片 |
| `slice-implement` | [`slice-implement/SKILL.md`](slice-implement/SKILL.md) | 单切片代码实现 |
| `slice-verify` | [`slice-verify/SKILL.md`](slice-verify/SKILL.md) | 单切片验证 |
| `integration-verify` | [`integration-verify/SKILL.md`](integration-verify/SKILL.md) | 多切片集成验证 |
| `result-curate` | [`result-curate/SKILL.md`](result-curate/SKILL.md) | 结果沉淀与归档 |

---

## 5. Pipeline Flow

流程图、状态机图与调用示例见根目录 [SKILL.md](SKILL.md)（Pipeline Flow、State Machine）。

核心流程：`run-init → design-intake → design-normalize → design-to-plan → plan-to-slices → [slice-implement → slice-verify]* → integration-verify → result-curate → close`

**续跑**：不确定进度时先按 [`run-status/SKILL.md`](run-status/SKILL.md) 读取 `.workflow/runs/<run-id>/state.md`，再执行其推荐的下一阶段 skill。

失败恢复规则：
- **design-intake / design-normalize 失败**：修复文档后重试当前阶段
- **slice-verify 失败**：修复实现后重新执行 `slice-implement → slice-verify`
- **integration-verify 失败**：定位问题切片，回退到对应切片重新实现

---

## 6. Usage

### 步骤 1：准备设计文档

编写或整理结构化设计文档（Markdown 格式），放入 `.workflow/docs/design/` 目录。PDF 资料仅作参考，最终收敛到 Markdown。

### 步骤 2：初始化 run（`run-init`）

使用 [`run-init/SKILL.md`](run-init/SKILL.md) 创建本次运行的目录结构与状态文件。

**产出**：`.workflow/runs/<run-id>/state.md` 及目录骨架（含 `stages/*/` 子目录）。

**`run-brief.md`（可插拔）**：`run-init` 会同时创建 `.workflow/runs/<run-id>/run-brief.md`。除说明外各节填「无」即**不启用**本次额外约束；需要为单次 run 附加范围裁剪、硬约束或非目标时，在 intake 之前或之后编辑该文件即可，**无需**新增流水线阶段。详见 [`run-init/SKILL.md`](run-init/SKILL.md)。

### 步骤 3：执行 intake（`design-intake`）

使用 [`design-intake/SKILL.md`](design-intake/SKILL.md) 检查设计文档完整性，识别缺失章节与不完整信息。

**产出**：intake 报告，确认是否允许进入下一阶段。

### 步骤 4：规范化（`design-normalize`）

使用 [`design-normalize/SKILL.md`](design-normalize/SKILL.md) 将补充说明、PDF 参考内容合并，生成规范化设计文档。

**产出**：`*.normalized.md` 标准设计稿与待确认项列表。

### 步骤 5：生成计划（`design-to-plan`）

使用 [`design-to-plan/SKILL.md`](design-to-plan/SKILL.md) 将设计转为实现计划，提取模块、接口、数据结构与依赖关系。

**产出**：实现计划文档（含 backlog、优先级与验收点）。

### 步骤 6：切片（`plan-to-slices`）

使用 [`plan-to-slices/SKILL.md`](plan-to-slices/SKILL.md) 将实现计划拆成最小可验证切片。

**产出**：切片列表，每个切片包含输入、产出、验证标准与依赖关系。

### 步骤 7：逐切片实现与验证（`slice-implement` + `slice-verify`）

1. 使用 [`slice-implement/SKILL.md`](slice-implement/SKILL.md) 按切片生成代码、测试与配置
2. 使用 [`slice-verify/SKILL.md`](slice-verify/SKILL.md) 执行验证，检查设计一致性与自动化测试
3. 验证通过则进入下一切片；失败则修复后重试

**产出**：业务代码、测试代码、切片验证报告。

### 步骤 8：集成验证（`integration-verify`）

使用 [`integration-verify/SKILL.md`](integration-verify/SKILL.md) 对所有切片的组合结果执行集成验证。

**产出**：集成验证报告。

### 步骤 9：结果沉淀（`result-curate`）

使用 [`result-curate/SKILL.md`](result-curate/SKILL.md) 汇总归档过程证据与结果报告，生成追踪矩阵与交付索引。

**产出**：追踪矩阵、偏差说明、最终交付索引。

---

## 7. Runtime Directory Structure

```text
<project>/
  .workflow/
    docs/
      design/                    # 设计文档（含 *.normalized.md）
      implementation-plan/       # 实现计划、backlog、risks
    runs/
      <run-id>/
        state.md                 # 运行状态文件
        run-brief.md             # 本次 run 专用约束（可插拔，默认「无」）
        slices/                  # 切片定义（含 index.md、slice-NNN.md）
        stages/                  # 按阶段分目录的产出（见各 stage skill）
          intake/
          normalize/
          plan/                  # 可选，如 run-status 审计落盘
          implement-verify/      # 切片实现说明、验证报告、偏差等
          integrate/
          curate/                # traceability-matrix、final-index 等
  skill/
    <name>/SKILL.md              # 各阶段 SKILL.md + YAML frontmatter
```

细目见 [`docs/superpowers/specs/2026-04-01-workflow-layout-design.md`](../docs/superpowers/specs/2026-04-01-workflow-layout-design.md)。

- `state.md` — 记录当前 run 的阶段、进度与失败信息，支持断点恢复（§3 阶段表为权威阶段名）；§6 含 `run_brief` 路径
- `run-brief.md` — 与 evergreen 设计文档分离的本次约束；空/「无」则各阶段等同未启用
- `.workflow/docs/implementation-plan/` — 由 `design-to-plan` 产出
- `slices/` — 每个切片的定义文档与实现状态
- `stages/` — 过程与归档报告按阶段分目录；具体文件名以各 `skill/<name>/SKILL.md` 为准

---

## 8. State Machine

**字段约定**：`state.md` 中 **`status`** 表示 run 级生命周期（如 `run-init` 后为 `created`，失败可为 `failed`，收尾可为 `completed`）；**`current_stage`** 表示当前推进阶段，与 §3 阶段表行名一致。二者不要混用。

**权威阶段名**（与 [run-init/SKILL.md](run-init/SKILL.md) 模板 §3 一致）：`init` → `intake` → `normalize` → `plan` → `slice` → `implement` / `verify`（多轮）→ **`integrating`**（`integration-verify` 进行中）→ `curate` → `close`。其中 `integrating` 在 §3 中可不单独占行，由执行者在集成验证期间将 `current_stage` 设为 `integrating` 或在 `verify` 行备注即可，但须与根目录 [SKILL.md](SKILL.md) 状态图一致。

```text
init → intake → normalize → plan → slice → (implement ↔ verify)* → integrating → curate → close
```

状态转换规则（`current_stage` 视角）：

| 当前阶段 | 成功后 | 失败处理 |
|----------|--------|----------|
| `init` | → `intake`（开始 `design-intake`） | — |
| `intake` | → `normalize` | 修复文档后重试 intake |
| `normalize` | → `plan` | 补充文档后重试 normalize |
| `plan` | → `slice` | 调整计划后重试 plan |
| `slice` | → `implement`（进入第一个或下一个待实现切片） | 重新切分则回到 `plan-to-slices` |
| `implement` | → `verify`（`slice-verify`） | 修复实现后仍从 `implement` 进入 `verify` |
| `verify` | 仍有未完成切片 → `implement`；全部单切片验证完成 → `integrating` | 验证失败 → `implement`（修复后重试） |
| `integrating` | → `curate`（`integration-verify` 通过） | 定位问题切片 → `implement` |
| `curate` | → `close`（`result-curate` 完成） | 补充沉淀后重试 curate |

失败状态标记：任何阶段失败时，状态文件记录 `status: failed`（若采用该约定）、失败原因与恢复建议。必要时可人工标记为 `accepted-deviation`。

---

## 9. Quality Assurance

质量保证分为三个层级：

### 一级：设计一致性检查

- 是否覆盖设计中定义的模块与接口
- 是否实现设计规定的关键约束
- 是否产生未授权功能扩展
- 是否违反命名、边界或依赖约束

### 二级：自动化技术检查

- 格式检查 / Lint / 静态分析
- 类型检查
- 单元测试
- 核心契约测试

### 三级：人工补充评审

适用于自动修复反复失败、架构偏差较大、高风险模块改动、设计文档存在明显歧义等情形。

---

## 10. Failure Classification & Recovery

### 失败分类

| 类型 | 示例 | 常见原因 |
|------|------|----------|
| **文档问题** | 设计缺失、定义冲突、约束不明确 | 设计文档不完整或存在歧义 |
| **实现问题** | 生成代码错误、依赖不满足、改动越界 | 切片定义不清晰或上下文不足 |
| **验证问题** | 测试失败、契约不满足、与设计不一致 | 实现偏差或验证标准定义不当 |

### 恢复策略

1. **同阶段重试** — 修复问题后在当前阶段重新执行
2. **切片隔离** — 切片失败不阻断其他无依赖切片的执行；无依赖切片可并行实现，约定见 [plan-to-slices/SKILL.md](plan-to-slices/SKILL.md)「并行切片执行（可选）」
3. **偏差接受** — 必要时可人工标记为 `accepted-deviation`，记录原因与风险
4. **全程记录** — 所有恢复动作都必须记录原因和结果
