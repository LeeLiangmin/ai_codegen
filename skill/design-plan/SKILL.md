---
name: design-plan
description: Use when the design is complex enough that you need an overall structural understanding — module boundaries, main flow, key interfaces, dependencies — before deriving safe slices
---

# design-plan

## Overview

`design-plan` 是核心流程中的一个**条件性**步骤，位于 `design-check` 之后、`design-to-slices` 之前。

它的职责非常单一：**建立整体执行结构认知，为后续切片提供稳定的结构基础**。

它不是旧体系中的 implementation plan。它不做：
- 不生成大而全的实施计划
- 不生成 backlog 或任务分解文档
- 不维护阶段状态
- 不写代码
- 不执行验证

它只回答以下问题：

1. 系统整体形态是什么（模块、组件、层次）
2. 主执行流是什么
3. 关键模块边界在哪里
4. 模块之间的关键依赖是什么
5. 切片应沿什么边界去切

---

## When to Use

在以下场景使用：

- `design-check` 结论为 `ready-for-slicing` 或 `ready-with-risks`，且复杂度判断为 `complex`
- 任务涉及跨模块改动，需要先理解模块间关系
- 任务涉及主流程重构或新系统构建
- 存在明显的前后依赖，需要先建立结构图再切片
- 目标明确，但落点复杂

### 可以跳过的场景

- 单文件修改
- 单接口修复
- 明确的小功能补丁
- 用户已给出非常清楚的执行边界
- `design-check` 复杂度判断为 `simple`

---

## Input

| 输入项 | 必填 | 说明 |
|---|---|---|
| 设计文档 | 是 | 原始设计文档或用户直接提供的结构化描述 |
| design-check 结果 | 建议 | 用于继承目标、范围、约束、风险、缺失项 |
| 现有代码上下文 | 否 | 用于识别已有模块结构与可修改边界 |
| 用户附加约束 | 否 | 例如仅做 MVP、只动 API 层、不改数据库等 |

---

## Procedure

1. **读取设计目标与约束**
   从设计文档和 `design-check` 结果中提取：
   - 总体目标
   - 当前范围与非目标
   - 技术约束
   - 风险与缺失项

2. **识别系统整体形态**
   回答：系统由哪些主要部分组成？
   - 列出主要模块 / 组件 / 层次
   - 每个模块的核心职责（一句话）
   - 模块之间的边界在哪里

3. **梳理主执行流**
   回答：主要业务流程或数据流是怎么走的？
   - 从输入到输出的主路径
   - 关键分支点
   - 不在本次范围内的流程分支

4. **标记关键接口与依赖**
   回答：模块之间怎么连接？
   - 模块间的关键接口（输入/输出）
   - 哪些模块之间存在强依赖
   - 哪些模块可以独立推进

5. **给出切片策略建议**
   回答：后续切片应沿什么边界去切？
   - 建议的切片维度（按模块、按流程、按层次、按功能点）
   - 建议的切片顺序原则
   - 已知的切片约束（哪些必须先做、哪些不能拆开）

6. **按需写入轻量文件**
   如果会话目录存在，可写入：
   - `.workflow/session/design-plan.md`

   如果没有显式会话目录，也可以直接在对话中输出，不强制落盘。

---

## Output

### 最小输出

无论是否落盘，都应产生以下结构化结果：

- `system_shape_summary`
- `main_flow`
- `module_boundaries`
- `key_interfaces`
- `dependency_notes`
- `slice_strategy`

### 可选文件输出

- `.workflow/session/design-plan.md`

建议格式：

```markdown
# Design Plan

## System Shape
- module-a: 职责描述
- module-b: 职责描述
- module-c: 职责描述

## Main Flow
1. 输入 → module-a 处理
2. module-a → module-b 转换
3. module-b → 输出

## Module Boundaries
- module-a: 负责 X，不负责 Y
- module-b: 负责 Y，不负责 Z

## Key Interfaces
- module-a → module-b: 接口描述（输入/输出）
- module-b → module-c: 接口描述（输入/输出）

## Dependencies
- module-b 依赖 module-a 的输出
- module-c 可独立推进

## Slice Strategy
- 建议沿模块边界切片
- 先实现 module-a（无依赖），再实现 module-b
- module-c 可并行
```

---

## Quality Gate

只有满足以下条件，才算完成一次有效的 `design-plan`：

- [ ] 已识别主要模块 / 组件
- [ ] 已梳理主执行流
- [ ] 已标记模块边界
- [ ] 已识别关键接口与依赖
- [ ] 已给出切片策略建议
- [ ] 输出足够轻量，不超出结构认知范围

---

## Failure Handling

| 场景 | 处理方式 |
|---|---|
| 设计信息不足以识别模块结构 | 返回 `design-check`，要求补充结构相关信息 |
| 模块边界模糊 | 标记为风险，给出最佳猜测并显式注明不确定性 |
| 依赖关系复杂 | 只记录直接依赖，不构造完整依赖图 |
| 系统过于简单不需要 plan | 直接跳过，进入 `design-to-slices` |

---

## Non-Goals

以下内容不属于本 skill：

- 不生成大而全的 implementation plan
- 不生成 backlog 或任务分解文档
- 不生成甘特式阶段规划
- 不直接拆切片（这是 `design-to-slices` 的职责）
- 不编写代码
- 不执行验证命令
- 不维护复杂全局阶段状态

完成后，下一步应进入 [design-to-slices/SKILL.md](../design-to-slices/SKILL.md)。
