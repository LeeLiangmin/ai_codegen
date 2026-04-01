---
name: result-curate
description: Use when integration verification passed and you need traceability matrix, deviations summary, delivery index, and next-iteration context for archival
---

# result-curate

## Overview

将本次 run 的全部过程结果整理为长期可复用资产，包括设计实现追踪矩阵、偏差汇总、最终交付索引和下一轮迭代上下文，支持后续 AI 或人工继续增量迭代。

## When to Use

集成验证通过后，进入收尾整理阶段。

**前置条件：**
- `integration-verify` 已通过（`passed`），或所有切片已通过 `slice-verify`
- 无处于 `blocked` 状态的关键切片

## Input

| 输入项 | 路径 / 来源 | 说明 |
| --- | --- | --- |
| 规范化设计稿 | `.workflow/docs/design/<name>.normalized.md` | 设计项提取来源 |
| 实现计划 | `.workflow/docs/implementation-plan/<name>-implementation-plan.md` | 计划与实际对照 |
| 切片定义和结果 | `.workflow/runs/<run-id>/slices/` | 所有切片的定义及状态 |
| 验证报告 | `.workflow/runs/<run-id>/stages/implement-verify/` | 所有验证阶段产出的报告 |
| 偏差记录 | `.workflow/runs/<run-id>/stages/implement-verify/slice-*-deviation.md` | 所有 deviation 文件 |
| 运行状态 | `.workflow/runs/<run-id>/state.md` | 当前 run 的全局状态 |

## Procedure

1. **收集实现结果**：遍历所有切片，收集每个切片的实现结果（status、verify_status）和关联的验证报告。
2. **建立设计实现追踪矩阵**：
   - 从规范化设计稿中提取所有设计项（模块、接口、数据结构）
   - 将每个设计项映射到实际代码路径和测试路径
   - 标注每项的实现状态（`completed` / `partial` / `missing`）
   - 记录偏差信息（`none` / `accepted` / `unresolved`）
   - 使用追踪矩阵模板（见 § Template A）
3. **汇总偏差记录**：收集所有 deviation 文件，按类别（设计偏差、实现偏差、范围偏差）分类整理。
4. **汇总未解决项**：收集所有标记为 unresolved 的问题，包括未解决的集成问题、待人工确认的偏差等。
5. **统计验证结果**：计算通过率、失败项数量、偏差项数量，形成量化摘要。
6. **生成最终交付索引**：使用交付索引模板（见 § Template B），填写 run 概览、交付摘要、覆盖情况、验证结果、偏差与风险。
7. **生成下一轮迭代上下文**：
   - 推荐下一步行动
   - 列出待确认项（需人工决策）
   - 标注不建议自动推进的区域（风险高或信息不足）
8. **归档所有报告**：确认各阶段产出已按约定分布在 `.workflow/runs/<run-id>/stages/` 下（`intake/`、`normalize/`、`implement-verify/`、`integrate/` 等）。
9. **更新 state.md**：将 **`current_stage`** 更新为 `close`（完成沉淀后）；若在归档过程中需要区分，中间可设为 `curate`。视需要更新顶层 **`status`**（如 `completed`）。

## Output

| 输出项 | 路径 | 条件 |
| --- | --- | --- |
| 追踪矩阵 | `.workflow/runs/<run-id>/stages/curate/traceability-matrix.md` | 始终产出 |
| 偏差汇总 | `.workflow/runs/<run-id>/stages/curate/deviations-summary.md` | 始终产出 |
| 最终交付索引 | `.workflow/runs/<run-id>/stages/curate/final-index.md` | 始终产出 |
| 下一轮迭代上下文 | `.workflow/runs/<run-id>/stages/curate/next-iteration-context.md` | 始终产出 |
| 更新后状态 | `.workflow/runs/<run-id>/state.md` | 始终更新 |

## Quality Gate

- [ ] 追踪矩阵覆盖设计稿中所有模块和接口
- [ ] 所有偏差都已记录且有原因说明
- [ ] 交付索引完整（代码、测试、文档路径都已列出且可访问）
- [ ] 下一轮迭代上下文内容充分，可供新 AI 会话直接使用
- [ ] `state.md` 已更新：`current_stage` 为 `close`（或流程中的 `curate`），顶层 `status` 已与 run 收尾约定一致

## Failure Handling

| 失败场景 | 处理方式 |
| --- | --- |
| **追踪矩阵存在大量 missing 项** | 标记为未完成 run，不将 `current_stage` 设为 `close`（可保持 `curate` 或回退至 `implement`），建议继续实现 |
| **关键偏差未记录** | 补充偏差记录后重新执行 curate |
| **产物路径不存在** | 标记为异常，在交付索引中注明路径缺失，不阻塞整体 curate 流程 |
| **验证报告不完整** | 记录缺失的报告，在交付索引中标注，建议补充验证 |

## Template

### 模板 A — 设计实现追踪矩阵

```markdown
### 设计实现追踪矩阵

| design_id | design_section | module | interface | code_path | test_path | status | deviation | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | planned / completed / partial / missing | none / accepted / unresolved | |
```

**字段说明：**
- `design_id`：设计稿中的章节编号或标识
- `design_section`：设计章节名称
- `module`：对应的代码模块
- `interface`：接口或关键函数名
- `code_path`：实际代码文件路径
- `test_path`：对应测试文件路径
- `status`：实现状态（`planned` 仅计划 / `completed` 已完成 / `partial` 部分完成 / `missing` 缺失）
- `deviation`：偏差状态（`none` 无偏差 / `accepted` 已接受偏差 / `unresolved` 未解决偏差）
- `notes`：补充说明

### 模板 B — 最终交付索引

```markdown
### 最终交付索引

#### 1. run 概览

- run_id: <填入>
- objective: <填入>
- design_doc: <填入>
- final_status: <填入>
- completed_at: <填入>

#### 2. 交付摘要

##### 2.1 代码交付
列出主要代码产出路径。

##### 2.2 测试交付
列出主要测试产出路径与测试范围。

##### 2.3 文档交付
列出设计、计划、验证、沉淀相关文档。

#### 3. 设计实现覆盖情况
说明哪些设计项已完成、部分完成、未完成。

#### 4. 验证结果摘要

- 设计一致性检查：
- 格式检查：
- 静态检查：
- 类型检查：
- 单元测试：
- 集成验证：

#### 5. 偏差与风险

##### 5.1 偏差摘要
列出关键偏差及原因。

##### 5.2 剩余风险
列出尚未完全解决的风险。

#### 6. 下一轮迭代上下文

- 推荐下一步：
- 待确认项：
- 不建议自动推进的区域：
```
