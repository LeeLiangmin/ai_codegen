---
name: run-init
description: Use when starting a new implementation session and you need only the minimal session layout and minimal recoverable state before using the core slice loop
---

# run-init

## Overview

`run-init` 在新体系中不再负责初始化复杂阶段机，也不再生成大量模板与阶段目录。

它只做一件事：**创建最小会话目录与最小恢复状态**，让后续核心闭环可以开始运行。

新体系下，`run-init` 是基础设施 skill，而不是重流程入口。

---

## When to Use

在以下场景使用：

- 准备开始一个新的实现会话
- 希望把目标、设计文档和当前进度以最小形式落盘
- 希望后续可以通过 [run-status/SKILL.md](../run-status/SKILL.md) 恢复

如果任务非常简单，也可以不执行 `run-init`，直接进入 [design-check/SKILL.md](../design-check/SKILL.md)。

---

## Input

| 参数 | 必填 | 说明 |
|---|---|---|
| `session_id` | 否 | 会话标识；未提供时可使用默认 `session` |
| `design_doc` | 是 | 设计文档路径，或其逻辑引用 |
| `objective` | 是 | 当前实现目标 |
| `context_notes` | 否 | 会话附加上下文，例如范围裁剪、人工约束 |

---

## Procedure

1. **校验输入**
   - 确认 `design_doc` 已给出
   - 确认 `objective` 已给出
   - 若提供 `session_id`，确认其可作为目录名

2. **确定会话目录**
   推荐使用以下其中一种：

   - 单会话模式：`.workflow/session/`
   - 多会话模式：`.workflow/sessions/<session-id>/`

   默认可采用单会话模式，避免目录层级过深。

3. **创建最小目录结构**
   创建以下目录：

   ```text
   .workflow/session/
   .workflow/session/slices/
   .workflow/session/verify/
   ```

4. **创建最小状态文件**
   在会话目录中创建 `state.md`，只包含恢复所必需的信息。

5. **按需创建上下文文件**
   如果存在 `context_notes` 或需要记录人工约束，可创建：
   - `context.md`

6. **结束初始化**
   初始化完成后，不更新复杂阶段状态，只将系统置于可进入 [design-check/SKILL.md](../design-check/SKILL.md) 的状态。

---

## Output

### 必需输出

- `.workflow/session/state.md`

### 建议输出

- `.workflow/session/context.md`
- `.workflow/session/slices/`
- `.workflow/session/verify/`

### 最小目录结构

```text
.workflow/
└── session/
    ├── state.md
    ├── context.md
    ├── slices/
    └── verify/
```

---

## Quality Gate

- [ ] 会话目录已创建
- [ ] `state.md` 已创建
- [ ] `state.md` 中已写入 `objective`
- [ ] `state.md` 中已写入 `design_doc`
- [ ] `status` 初始值为 `active`
- [ ] 后续可直接进入 [design-check/SKILL.md](../design-check/SKILL.md)

---

## Failure Handling

| 场景 | 处理方式 |
|---|---|
| 会话目录已存在 | 若可复用则保留；若需要新会话，则更换 `session_id` |
| `design_doc` 未提供 | 停止初始化，要求补充 |
| `objective` 未提供 | 停止初始化，要求补充 |
| 目录结构部分存在 | 保留已有最小结构，只补缺失项 |

---

## Template

### `state.md` 模板

```markdown
# Session State

- objective: <填入>
- design_doc: <填入>
- status: active
- current_slice: —
- last_completed_slice: —
- last_verify_result: none
- blocked: no
- block_reason: —
```

### `context.md` 模板（可选）

```markdown
# Session Context

## Notes
- <可选补充说明>

## Constraints
- <可选约束>

## Non-Goals
- <可选非目标>
```

---

## Non-Goals

以下内容不属于本 skill：

- 不创建复杂阶段目录
- 不生成 run-brief
- 不初始化阶段表或切片总表
- 不生成计划文档
- 不生成验证报告

初始化完成后，通常下一步应进入 [design-check/SKILL.md](../design-check/SKILL.md)。
