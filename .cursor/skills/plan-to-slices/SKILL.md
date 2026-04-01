---
name: plan-to-slices
description: Use when an implementation plan and backlog exist and you need minimal verifiable slice definitions and `slice-NNN.md` files under the run
---

# plan-to-slices

## Overview

将实现计划拆分为可独立执行和验证的最小切片任务，每个切片可在一次实现-验证闭环中完成。切片是后续自动化执行的基本单元。

## When to Use

实现计划生成完成后执行。

**前置条件：**
- `.workflow/docs/implementation-plan/<name>-implementation-plan.md` 和 `.workflow/docs/implementation-plan/backlog.md` 已生成
- `.workflow/runs/<run-id>/state.md` 中 **`current_stage`** 为 `plan`（plan 文档已就绪）

## Input

| 输入 | 说明 |
| --- | --- |
| `.workflow/docs/implementation-plan/<name>-implementation-plan.md` | 实现计划 |
| `.workflow/docs/implementation-plan/backlog.md` | 实现 backlog |
| `.workflow/docs/design/<name>.normalized.md` | 规范化设计稿（作为参考） |
| `.workflow/runs/<run-id>/state.md` | 当前运行状态 |
| `.workflow/runs/<run-id>/run-brief.md` | 可选。有实质内容时：切片粒度与「完成定义」须符合 brief 的范围、硬约束与非目标 |

## Procedure

1. **读取实现计划和 backlog**：加载实现计划文档和 backlog，确认内容完整性。若 `run-brief.md` 存在且含实质内容，一并加载；拆分切片时不得包含 brief 中声明为非目标的工作，除非在 `state.md` / risks 中已有人工接受记录。
2. **分析模块依赖关系图**：根据模块分解表构建依赖图，识别关键路径和并行分支。
3. **确定切片顺序原则**：
   - 先基础模块后业务模块
   - 先数据后逻辑
   - 先核心后扩展
   - 无依赖项优先
4. **按模块边界和依赖关系拆分切片**：沿模块边界划分，确保每个切片聚焦单一模块或紧密关联的最小模块集合。
5. **为每个切片定义完整属性**：
   - **目标**：最小可验证的交付目标
   - **输入依据**：关联的设计章节、模块、接口
   - **实现边界**：允许修改和禁止修改的范围
   - **预期产出**：代码文件、测试文件、配置文件
   - **验证要求**：具体检查项（静态检查、类型检查、测试等）
   - **偏差与升级策略**：允许偏差的条件和必须升级的条件
   - **完成定义**：checklist 形式的完成标准
6. **标注切片间的依赖关系和并行性**：明确哪些切片必须串行执行，哪些可以并行。
7. **生成切片索引文件**：创建 `index.md`，包含所有切片的概览表和依赖关系图。
8. **为每个切片生成独立定义文档**：按模板为每个切片生成 `slice-<NNN>.md`。
9. **更新 state.md**：将 **`current_stage`** 更新为 `slice`，写入切片状态表。

## Output

| 输出 | 路径 |
| --- | --- |
| 切片索引 | `.workflow/runs/<run-id>/slices/index.md` |
| 切片定义文档 | `.workflow/runs/<run-id>/slices/slice-<NNN>.md`（每个切片一份） |
| 状态更新 | `.workflow/runs/<run-id>/state.md` |

## Quality Gate

- [ ] 实现计划中所有 backlog 项都已分配到切片
- [ ] 每个切片都有明确的验证标准
- [ ] 切片间依赖关系无循环
- [ ] 每个切片的修改范围不重叠
- [ ] 首个切片无前置依赖

## Failure Handling

| 场景 | 处理方式 |
| --- | --- |
| 无法拆出足够小的切片 | 标注为高风险切片，建议人工评审 |
| 存在循环依赖 | 建议合并为一个切片或引入接口抽象打破循环 |
| backlog 项无法映射到切片 | 记录为遗漏项，更新风险清单 |

## 并行切片执行（可选）

当切片依赖图中存在**无相互依赖**的切片时，允许多个切片并行实现。约定：

- 在 `state.md` 的切片状态表中为每个切片单独维护一行；并行进行时可将多个切片的 `status` 设为 `running`（或项目约定的等价状态）。
- `current_stage` 可保持为 `implement`，或在备注中标明并行切片 id 列表。
- 每个切片仍须独立完成 `slice-implement` → `slice-verify`；集成验证前，相关切片应均已 `verified`。
- 报告与笔记仍写入 `.workflow/runs/<run-id>/stages/implement-verify/`，按 `slice-<NNN>-*` 文件名区分，避免覆盖。

## Template

以下为切片任务定义模板，为每个切片生成时按此结构填写：

```markdown
## 切片任务模板

### 1. 基本信息

- run_id: <填入>
- slice_id: <填入>
- title: <填入>
- priority: <填入>
- owner: <填入>
- status: pending / running / blocked / verified / curated

### 2. 切片目标

描述该切片要完成的最小可验证目标。

### 3. 输入依据

- 设计章节：
- 关联模块：
- 关联接口：
- 关联数据结构：
- 前置依赖：

### 4. 实现边界

#### 4.1 允许修改范围

列出可修改目录、模块、文件类型。

#### 4.2 禁止修改范围

列出不得修改的部分。

### 5. 预期产出

- 代码文件：
- 测试文件：
- 配置文件：
- 其他产物：

### 6. 验证要求

- 设计一致性检查：
- 静态检查：
- 类型检查：
- 单元测试：
- 契约测试：

### 7. 偏差与升级策略

#### 7.1 允许记录偏差的条件

说明何种情形可暂时偏离设计。

#### 7.2 必须升级人工处理的条件

说明何种情形必须停止自动推进。

### 8. 完成定义

满足以下条件方可标记完成：

- [ ] 代码已生成或修改
- [ ] 测试已补齐
- [ ] 自动检查通过
- [ ] 偏差已记录
- [ ] 结果已归档
```
