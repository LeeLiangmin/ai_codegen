---
name: slice-implement
description: Use when a slice definition exists, dependencies are satisfied, and you need code and tests strictly within the slice's allowed modification scope
---

# slice-implement

在 `slice-<NNN>.md` 范围内改代码与测试；不越界；依赖切片须已 `verified`。

## 输入

`slices/slice-<NNN>.md`、`*.normalized.md`、`state.md`；可选 `run-brief`。

## 步骤

1. 确认 `depends_on` 已满足；读 brief（若有）不违反非目标。  
2. 读设计对应章节与允许修改路径；实现 + 单测。  
3. 有决策/偏差可写 `stages/implement-verify/slice-<NNN>-implementation-notes.md` / `-deviation.md`。  
4. 切片 `implemented`；`state.md` 同步。

## 产出

代码 + 测试；可选 notes/deviation；更新 `state.md`。

## Gate

- [ ] 改动仅在允许范围；有测；与接口/数据约定一致；可编译

## 失败

设计冲突、依赖缺、越界 → `blocked` 并记录原因。
