---
name: run-status
description: Use when you need a minimal, read-only summary of the current session: objective, current slice, latest verification result, blockers, and the single most appropriate next step
---

# run-status

## Overview

`run-status` 是新体系中的只读基础设施 skill。

它不推进流程，不修改会话状态，不生成复杂审计报告。它只做一件事：**把当前会话压缩成可恢复的最小摘要**。

它回答的核心问题是：

1. 当前目标是什么
2. 当前正在处理哪个切片
3. 上一次验证结果是什么
4. 当前是否阻塞
5. 下一步最合理的动作是什么

---

## When to Use

在以下场景使用：

- 会话中断后需要恢复
- 不确定当前应该进入哪个核心 skill
- 想快速了解当前会话状态
- 切换模型或切换会话时，需要一个短摘要

通常读取由 [run-init/SKILL.md](../run-init/SKILL.md) 创建的 `state.md`，以及相关切片与验证文件。

---

## Input

| 输入项 | 必填 | 说明 |
|---|---|---|
| `state.md` | 是 | 会话状态文件 |
| 切片目录 | 否 | 用于识别已存在的切片定义 |
| 验证目录 | 否 | 用于识别最新验证结果 |
| `context.md` | 否 | 用于补充人工约束与非目标 |

---

## Procedure

1. **读取会话状态**
   从 `state.md` 提取：
   - `objective`
   - `design_doc`
   - `status`
   - `current_slice`
   - `last_completed_slice`
   - `last_verify_result`
   - `blocked`
   - `block_reason`

2. **按需读取补充上下文**
   如果存在：
   - `context.md`
   - `slices/`
   - `verify/`

   则提取恢复下一步所必需的最小信息，不展开为长报告。

3. **判断当前会话位置**
   用最小规则推断当前所处位置：
   - 无切片且未阻塞：建议先执行 [design-check/SKILL.md](../design-check/SKILL.md) 或 [design-to-slices/SKILL.md](../design-to-slices/SKILL.md)
   - 已有切片但无当前实现：建议进入 [slice-implement/SKILL.md](../slice-implement/SKILL.md)
   - 最近验证失败：建议回到 [slice-implement/SKILL.md](../slice-implement/SKILL.md)
   - 当前切片已实现待验证：建议进入 [slice-verify/SKILL.md](../slice-verify/SKILL.md)
   - 全部核心切片已通过：建议结束核心闭环，或按需进入扩展层

4. **输出单一下一步建议**
   输出时只给出一个最优先的下一步，避免同时给多个分叉建议。

5. **保持只读**
   `run-status` 默认不修改任何文件。

---

## Output

### 最小输出

- `objective`
- `current_position`
- `current_slice`
- `last_verify_result`
- `blocked`
- `block_reason`
- `recommended_next_step`

### 建议输出格式

```markdown
# Run Status

- objective: <...>
- current_position: <...>
- current_slice: <...>
- last_verify_result: pass | fail | none
- blocked: yes | no
- block_reason: <...>
- recommended_next_step: <skill-name>
```

如果需要对话内更短摘要，可进一步压缩为 3 行：

```text
目标：...
当前：...
下一步：...
```

---

## Quality Gate

- [ ] 已成功读取 `state.md`
- [ ] 已给出当前目标摘要
- [ ] 已给出当前切片或说明尚无切片
- [ ] 已给出最近验证结果
- [ ] 已识别阻塞状态
- [ ] 已给出唯一明确的下一步建议

---

## Failure Handling

| 场景 | 处理方式 |
|---|---|
| `state.md` 缺失 | 提示先执行 [run-init/SKILL.md](../run-init/SKILL.md) 或确认会话目录 |
| `state.md` 信息不完整 | 输出可恢复部分，并明确缺失项 |
| 切片文件与状态不一致 | 优先报告不一致，不擅自修复 |
| 无法判断下一步 | 明确说明原因，并推荐回到 [design-check/SKILL.md](../design-check/SKILL.md) 重新建立最小上下文 |

---

## Non-Goals

以下内容不属于本 skill：

- 不更新 `state.md`
- 不修改切片状态
- 不写审计报告
- 不推进阶段
- 不执行实现或验证动作

`run-status` 的作用只是帮助会话恢复，而不是替代核心闭环。
