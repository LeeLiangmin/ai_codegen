---
name: design-to-plan
description: Use when normalized design exists and you need an executable implementation plan, backlog, and risks under `.workflow/docs/implementation-plan/`
---

# design-to-plan

## Overview

将规范化设计文档转换为可执行的实现计划，提取模块、接口、数据结构、依赖关系，形成有优先级的 backlog，并识别风险项与可接受偏差。

## When to Use

normalize 阶段完成后执行。

**前置条件：**
- 规范化设计稿 `.workflow/docs/design/<name>.normalized.md` 已生成
- `.workflow/runs/<run-id>/state.md` 中 **`current_stage`** 为 `normalize`（normalize 阶段已完成，准备进入 plan）

## Input

| 输入 | 说明 |
| --- | --- |
| `.workflow/docs/design/<name>.normalized.md` | 规范化设计稿 |
| 项目仓库现有代码上下文 | 如存在，用于评估影响范围 |
| `.workflow/runs/<run-id>/state.md` | 当前运行状态 |
| `.workflow/runs/<run-id>/run-brief.md` | 可选。有实质内容时：backlog、初步切片与 risks 须**显式对齐** brief；实现计划「基本信息」中引用该路径 |

## Procedure

1. **读取规范化设计稿**：加载 `.workflow/docs/design/<name>.normalized.md`，确认文档完整性。
2. **读取 run-brief（可选）**：若 `.workflow/runs/<run-id>/run-brief.md` 存在且含实质内容，加载并在提取模块、优先级与切片草案时作为约束；若与设计或代码现状冲突，写入 `risks.md`，不在计划中静默覆盖 brief。
3. **提取所有模块及其职责、依赖关系**：识别设计中定义的每个模块，记录职责描述和模块间依赖。
4. **提取所有接口定义，映射到所属模块**：列出所有 API / 函数接口，标注其归属模块、输入输出参数。
5. **提取所有数据结构及其关系**：识别数据模型、配置结构、状态对象，记录字段和关联关系。
6. **识别全局约束与规则**：提取性能要求、安全约束、兼容性规则等跨模块约束。
7. **分析依赖关系，确定实现优先级**：构建依赖图，按拓扑排序确定模块实现顺序，标注关键路径。
8. **生成模块分解表**：输出包含模块、职责、依赖、风险、优先级的结构化表格。
9. **生成接口实现清单**：输出包含接口、所属模块、输入、输出、约束、验收点的表格。
10. **生成数据变更清单**：输出包含数据对象、变更类型、影响范围、风险、验证方式的表格。
11. **生成初步切片计划**：按依赖顺序规划切片，每个切片包含 slice_id、目标、输入、产出、依赖、验证标准。
12. **识别风险项和可接受偏差**：标注技术风险、设计模糊点、外部依赖风险，记录可暂时接受的偏差。
13. **生成实现计划文档、backlog 和风险清单**：按模板输出三份文档。
14. **更新 state.md**：将 **`current_stage`** 更新为 `plan`，记录产出文件路径和时间戳。

## Output

| 输出 | 路径 |
| --- | --- |
| 实现计划 | `.workflow/docs/implementation-plan/<name>-implementation-plan.md` |
| 实现 backlog | `.workflow/docs/implementation-plan/backlog.md` |
| 风险清单 | `.workflow/docs/implementation-plan/risks.md` |
| 状态更新 | `.workflow/runs/<run-id>/state.md` |

## Quality Gate

- [ ] 设计中所有模块都已出现在计划中
- [ ] 所有接口都已映射到模块
- [ ] 每个模块都有明确的优先级
- [ ] 切片计划中每个切片都有验证标准
- [ ] 无遗漏的关键设计元素

## Failure Handling

| 场景 | 处理方式 |
| --- | --- |
| 设计中存在模糊模块边界 | 标记为风险项，建议回到 normalize 补充 |
| 循环依赖 | 在计划中明确标注，建议切片策略打破循环 |
| 技术栈未确定 | 在风险清单中记录，给出推荐选项 |

## Template

以下为实现计划文档模板，生成时按此结构填写：

```markdown
## 实现计划模板

### 1. 基本信息

- run_id: <填入>
- design_doc: <填入>
- run_brief: <`.workflow/runs/<run-id>/run-brief.md` 路径，或「未启用」>
- scope: <填入>
- owner: <填入>
- generated_at: <填入>

### 2. 总体实现目标

概述本次实现的业务目标、技术目标和交付目标。

### 3. 模块分解

| 模块 | 职责 | 依赖 | 风险 | 优先级 |
| --- | --- | --- | --- | --- |
| | | | | |

### 4. 接口实现清单

| 接口 | 所属模块 | 输入 | 输出 | 权限/约束 | 验收点 |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

### 5. 数据变更清单

| 数据对象 | 变更类型 | 影响范围 | 风险 | 验证方式 |
| --- | --- | --- | --- | --- |
| | | | | |

### 6. 切片计划

| slice_id | 目标 | 输入 | 产出 | 依赖 | 验证标准 |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

### 7. 质量门禁

#### 7.1 设计一致性检查

列出本次必须检查的一致性项。

#### 7.2 自动化检查

- 格式检查：
- 静态检查：
- 类型检查：
- 单元测试：
- 契约测试：

### 8. 风险与偏差策略

#### 8.1 风险项

列出关键风险与应对方式。

#### 8.2 可接受偏差

列出哪些偏差可暂时接受，以及记录要求。

### 9. 最终交付物

- 代码产出：
- 测试产出：
- 文档产出：
- 报告产出：
```
