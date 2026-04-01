---
name: plan-to-slices
description: Use when an implementation plan and backlog exist and you need minimal verifiable slice definitions and `slice-NNN.md` files under the run
---

# plan-to-slices

把计划拆成 `slices/slice-<NNN>.md` + `slices/index.md`，更新 `state.md` 切片表（`current_stage: slice`）。

## 前置

实现计划与 backlog 已就绪；`plan` 阶段完成。

## 输入

`implementation-plan`、`backlog`、`*.normalized.md`、`state.md`；可选 `run-brief`（不得包含 brief 非目标）。

## 步骤

1. 按依赖排序：先基础后业务；无环；首个切片无依赖。  
2. 每切片必须含：目标、`input_refs`、**允许/禁止修改范围**、预期文件、**验证命令/标准**、`depends_on`。  
3. 写 `index.md`（切片一览 + 依赖）。  
4. 填 `state.md` §4。

## 并行（可选）

无相互依赖的切片可并行实现；各切片仍 `slice-implement` → `slice-verify`；集成前均 `verified`。

## Gate

- [ ] backlog 项有归属切片；每片有验证标准；依赖无环、范围不重叠

## 失败

无法拆分 → 记入风险或合并切片；循环依赖 → 合并或抽象接口。

## Slice 文件最小骨架

```markdown
### 基本信息
- slice_id / title / status: pending / depends_on

### 目标
（一句话可验交付）

### 输入依据
- 设计章节 / 模块 / 接口

### 允许修改 / 禁止修改
（路径或 glob）

### 验证
- 设计一致性要点；fmt/lint/test 命令（按仓库）

### 完成定义
- [ ] 代码 + 测试 + 检查通过
```
