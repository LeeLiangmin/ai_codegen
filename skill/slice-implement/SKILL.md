---
name: slice-implement
description: Use when one slice is clearly defined and you need to implement only that slice, inside its allowed boundary, with the smallest necessary code and test changes
---

# slice-implement

## Overview

`slice-implement` 是核心闭环中的执行步。

它的职责被压缩为一句话：**只实现一个切片，不扩张范围，不顺手解决其他问题。**

与旧体系相比，本版本删除了大量额外治理要求：
- 不要求生成复杂实现说明文档
- 不默认生成偏差报告文件
- 不承担全局流程推进职责
- 不维护复杂切片总表

它关注的唯一目标是：让当前切片进入“可验证”状态。

---

## When to Use

在以下场景使用：

- 已存在一个清晰的切片定义
- 切片边界已明确
- 当前切片前置依赖已满足，或无依赖
- 准备进行最小实现并随后交给 [slice-verify/SKILL.md](../slice-verify/SKILL.md)

通常来源于 [design-to-slices/SKILL.md](../design-to-slices/SKILL.md) 输出的单切片文件。

---

## Input

| 输入项 | 必填 | 说明 |
|---|---|---|
| 切片定义 | 是 | 当前切片的目标、边界、依赖、验证方式 |
| 设计文档 | 建议 | 用于核对接口、数据结构、命名与约束 |
| 现有代码上下文 | 是 | 理解当前仓库结构与允许修改的文件 |
| 会话状态 | 否 | 用于确认当前切片与阻塞信息 |

---

## Procedure

1. **读取当前切片定义**
   先明确以下内容：
   - `objective`
   - `depends_on`
   - `allowed_changes`
   - `forbidden_changes`
   - `expected_outputs`
   - `verification`

2. **确认依赖是否满足**
   如果切片有直接依赖，只检查直接前置项：
   - 前置切片是否已完成并通过验证
   - 如果未满足，则停止，不进入实现

3. **确认修改边界**
   在编码前明确：
   - 哪些文件/目录允许修改
   - 哪些文件/目录明确禁止修改
   - 是否允许新增测试

4. **执行最小实现**
   只完成当前切片的目标：
   - 生成或修改业务代码
   - 补充当前切片所必需的测试
   - 如确有必要，更新最小范围配置

5. **避免范围扩张**
   实现过程中若发现以下情况，默认停止并记录为阻塞，而不是顺手继续：
   - 需要跨多个无关模块大改
   - 需要改变切片未授权的接口契约
   - 需要修复与当前切片无关的问题
   - 需要补做新的设计决策

6. **准备交付验证**
   完成后，确保当前切片已具备进入 [slice-verify/SKILL.md](../slice-verify/SKILL.md) 的最小条件：
   - 代码可读
   - 改动集中
   - 测试已补齐到必要程度
   - 未越界修改

7. **最小状态更新（如使用会话状态）**
   如存在 `state.md`，只更新必要信息，例如：
   - `current_slice`
   - `status` 保持 `active`
   - 不写复杂阶段迁移

---

## Output

### 必需输出

- 当前切片边界内的代码改动
- 当前切片所需的最小测试改动

### 可选输出

如果确实出现阻塞或必要说明，可在会话目录中增加轻量记录，例如：
- `.workflow/session/summary.md`
- `.workflow/session/slices/slice-<NNN>-notes.md`

但这些都不是默认要求。

---

## Quality Gate

- [ ] 只实现了一个切片
- [ ] 所有改动都落在允许范围内
- [ ] 未修改禁止修改区域
- [ ] 当前切片所需的最小测试已补充
- [ ] 未引入明显与当前切片无关的扩展功能
- [ ] 已具备进入 [slice-verify/SKILL.md](../slice-verify/SKILL.md) 的条件

---

## Failure Handling

| 场景 | 处理方式 |
|---|---|
| 前置依赖未满足 | 停止实现，等待依赖切片完成 |
| 需要跨边界修改 | 停止实现，回到切片定义重新拆分或调整边界 |
| 设计与代码现状冲突 | 记录冲突，优先保持切片边界，不擅自扩张任务 |
| 当前切片过大 | 暂停实现，回到 [design-to-slices/SKILL.md](../design-to-slices/SKILL.md) 继续拆小 |
| 实现中出现额外问题 | 仅记录，不自动顺手修复无关问题 |

---

## Non-Goals

以下内容不属于本 skill：

- 不验证切片是否通过
- 不运行全局集成验证
- 不生成复杂偏差文档
- 不维护全局流程状态机
- 不整理最终交付索引

当前切片实现完成后，下一步应进入 [slice-verify/SKILL.md](../slice-verify/SKILL.md)。
