---
name: design-check
description: Use when you need the smallest possible design understanding step before coding: extract objective, scope, constraints, risks, and decide whether the design is sufficient to define at least one safe slice
---

# design-check

## Overview

`design-check` 是新体系中的第一个核心 skill。

它的职责非常单一：**判断当前设计材料是否足以开始切片执行**。

它不再承担旧体系中以下重负：
- 不做完整 intake 报告
- 不做 normalized 文档重写
- 不做 implementation plan 文档生成
- 不维护复杂阶段迁移

它只回答五个问题：

1. 目标是什么
2. 范围是什么
3. 约束是什么
4. 主要风险和缺失项是什么
5. 是否足以定义至少一个安全、可验证的切片

---

## When to Use

在以下场景使用：

- 刚拿到用户设计文档，需要开始实现前先做一次轻量理解
- 当前设计来源混杂，需要抽取核心事实
- 不确定是否可以直接开始切片
- 续跑时，需要重新确认任务目标与约束

它通常发生在 [run-init/SKILL.md](../run-init/SKILL.md) 之后，但如果不需要显式会话目录，也可以直接执行。

---

## Input

| 输入项 | 必填 | 说明 |
|---|---|---|
| 设计文档 | 是 | Markdown 设计文档，或用户直接提供的结构化描述 |
| 现有代码上下文 | 否 | 用于识别实现边界与兼容性约束 |
| 会话状态 | 否 | 若已初始化，可读取当前 [`state.md`](../run-init/SKILL.md#template) 或等价状态文件 |
| 用户补充约束 | 否 | 例如本次只做 MVP、禁止改数据库、仅做后端等 |

---

## Procedure

1. **读取设计材料**
   - 提取任务目标
   - 提取功能范围
   - 提取非目标（如果明确给出）
   - 提取技术约束、质量约束、兼容性约束

2. **识别实现所需的关键元素是否存在**
   最少检查以下五类信息是否达到“足以切片”的程度：
   - 目标
   - 业务流程或主要行为
   - 模块 / 组件边界
   - 接口或输入输出预期
   - 验收方式或成功标准

3. **标记缺失项与风险**
   对缺失或模糊内容进行分类：
   - `missing-critical`：缺失后无法安全定义任何切片
   - `missing-non-critical`：缺失但仍可开始局部切片
   - `risk`：存在冲突、不确定性、复杂依赖或环境风险

4. **判断是否可进入切片阶段**
   只做以下三种结论之一：
   - `ready-for-slicing`：可以直接进入 [design-to-slices/SKILL.md](../design-to-slices/SKILL.md)
   - `ready-with-risks`：可以切片，但必须显式携带风险与约束
   - `blocked-by-design`：设计信息不足，不能安全切片

5. **输出轻量结果**
   输出内容只保留：
   - 目标摘要
   - 范围摘要
   - 关键约束
   - 缺失项
   - 风险项
   - 结论

6. **按需写入轻量文件**
   如果会话目录存在，可写入：
   - `.workflow/session/design-check.md`

   如果没有显式会话目录，也可以直接在对话中输出，不强制落盘。

---

## Output

### 最小输出

无论是否落盘，都应产生以下结构化结果：

- `objective_summary`
- `scope_summary`
- `constraints`
- `missing_items`
- `risks`
- `decision`

### 可选文件输出

- `.workflow/session/design-check.md`

建议格式：

```markdown
# Design Check

## Objective
n/a

## Scope
n/a

## Constraints
- ...

## Missing Items
- [critical] ...
- [non-critical] ...

## Risks
- ...

## Decision
ready-for-slicing | ready-with-risks | blocked-by-design
```

---

## Quality Gate

只有满足以下条件，才算完成一次有效的 `design-check`：

- [ ] 已明确任务目标
- [ ] 已明确范围或至少明确当前不做什么
- [ ] 已识别关键约束
- [ ] 已区分关键缺失项与非关键缺失项
- [ ] 已给出唯一明确结论：`ready-for-slicing` / `ready-with-risks` / `blocked-by-design`

---

## Failure Handling

| 场景 | 处理方式 |
|---|---|
| 设计描述高度模糊 | 输出 `blocked-by-design`，列出最小补充清单 |
| 设计不完整但可局部推进 | 输出 `ready-with-risks`，只允许后续定义低风险切片 |
| 设计与现有代码冲突 | 记录为 `risk`，由后续切片显式限制修改边界 |
| 用户目标与约束互相矛盾 | 停止并列出冲突点，不擅自裁定 |

---

## Non-Goals

以下内容不属于本 skill：

- 不生成标准化设计文档
- 不生成 implementation plan
- 不直接拆切片
- 不编写代码
- 不执行验证命令

如果设计已足够开始执行，下一步应进入 [design-to-slices/SKILL.md](../design-to-slices/SKILL.md)。