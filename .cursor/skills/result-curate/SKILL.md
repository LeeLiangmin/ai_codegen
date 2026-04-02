---
name: result-curate
description: Use when the session is complete and you need traceability, deviations summary, delivery index, and next-iteration context for archival
---

# result-curate

## Overview

将本次会话的全部过程结果整理为长期可复用资产，包括设计实现追踪矩阵、偏差汇总、最终交付索引和下一轮迭代上下文，支持后续 AI 或人工继续增量迭代。

本 skill 属于 Extensions 层，不是默认主流程的阻塞步骤。只在需要时使用。

## When to Use

会话核心闭环完成后，进入收尾整理阶段。

**前置条件：**
- 所有切片已通过 [slice-verify/SKILL.md](../slice-verify/SKILL.md)
- 如已执行 `integration-verify`，其结果为 `pass`
- 无处于 `blocked` 状态的关键切片

## Input

| 输入项 | 来源 | 说明 |
|---|---|---|
| 设计文档 | 原始设计文档 | 设计项提取来源 |
| 切片定义 | `.workflow/session/slices/` | 所有切片的定义 |
| 验证结果 | `.workflow/session/verify/` | 所有切片的验证结果 |
| 集成报告 | `.workflow/session/integration-report.md` | 如已执行集成验证 |
| 会话状态 | `.workflow/session/state.md` | 当前会话状态 |

## Procedure

1. **收集实现结果**：遍历所有切片，收集每个切片的实现结果和验证结果。
2. **建立设计实现追踪矩阵**：
   - 从设计文档中提取所有设计项（模块、接口、数据结构）
   - 将每个设计项映射到实际代码路径和测试路径
   - 标注每项的实现状态（`completed` / `partial` / `missing`）
   - 记录偏差信息（`none` / `accepted` / `unresolved`）
3. **汇总偏差记录**：收集所有偏差，按类别（设计偏差、实现偏差、范围偏差）分类整理。
4. **汇总未解决项**：收集所有标记为 unresolved 的问题。
5. **统计验证结果**：计算通过率、失败项数量、偏差项数量，形成量化摘要。
6. **生成最终交付索引**：填写会话概览、交付摘要、覆盖情况、验证结果、偏差与风险。
7. **生成下一轮迭代上下文**：
   - 推荐下一步行动
   - 列出待确认项（需人工决策）
   - 标注不建议自动推进的区域
8. **按需更新会话状态**：如存在 `state.md`，将 `status` 更新为 `completed`。

## Output

### 建议文件输出

如使用会话目录，建议写入：

- `.workflow/session/traceability-matrix.md`
- `.workflow/session/deviations-summary.md`
- `.workflow/session/final-index.md`
- `.workflow/session/next-iteration-context.md`

如果不使用会话目录，也可以直接在对话中输出，不强制落盘。

## Quality Gate

- [ ] 追踪矩阵覆盖设计文档中所有主要模块和接口
- [ ] 所有偏差都已记录且有原因说明
- [ ] 交付索引完整（代码、测试、文档路径都已列出）
- [ ] 下一轮迭代上下文内容充分，可供新会话直接使用

## Failure Handling

| 失败场景 | 处理方式 |
|---|---|
| **追踪矩阵存在大量 missing 项** | 标记为未完成会话，建议继续实现 |
| **关键偏差未记录** | 补充偏差记录后重新执行 curate |
| **产物路径不存在** | 标记为异常，在交付索引中注明路径缺失 |
| **验证结果不完整** | 记录缺失的结果，在交付索引中标注 |

## Template

### 模板 A — 设计实现追踪矩阵

```markdown
# Traceability Matrix

| design_item | module | interface | code_path | test_path | status | deviation | notes |
|---|---|---|---|---|---|---|---|
| | | | | | completed / partial / missing | none / accepted / unresolved | |
```

### 模板 B — 最终交付索引

```markdown
# Final Index

## 1. Session Overview

- objective: <填入>
- design_doc: <填入>
- final_status: <填入>
- completed_at: <填入>

## 2. Delivery Summary

### 2.1 Code
列出主要代码产出路径。

### 2.2 Tests
列出主要测试产出路径与测试范围。

### 2.3 Documentation
列出设计、验证相关文档。

## 3. Coverage
说明哪些设计项已完成、部分完成、未完成。

## 4. Verification Summary

- boundary_checks: pass | fail
- design_alignment: pass | fail
- automated_checks: pass | fail
- integration: pass | fail | not_run

## 5. Deviations & Risks

### 5.1 Deviations
列出关键偏差及原因。

### 5.2 Remaining Risks
列出尚未完全解决的风险。

## 6. Next Iteration Context

- recommended_next_steps:
- pending_decisions:
- areas_not_safe_to_auto_advance:
```

## Non-Goals

以下内容不属于本 skill：

- 不执行验证动作
- 不推进流程
- 不编写代码
- 不替代人工产品验收

`result-curate` 的作用是将会话结果沉淀为可复用资产，而不是替代核心闭环。
