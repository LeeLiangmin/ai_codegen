---
name: integration-verify
description: Use when all slices are verified and you need cross-slice integration checks, E2E flows, and regression before closing the session
---

# integration-verify

## Overview

对多个已验证切片的组合结果执行集成验证，确保模块间协作正确、数据流通畅、关键业务流程端到端闭环。

本 skill 属于 Extensions 层，不是默认主流程的阻塞步骤。只在需要时使用。

## When to Use

所有切片（或一组相关切片）都已通过 [slice-verify/SKILL.md](../slice-verify/SKILL.md)，准备进行集成级别的验证。

**前置条件：**
- 相关切片均已通过 `slice-verify`，结果为 `pass`
- 无处于 `blocked` 或 `fail` 状态的前置切片

## Input

| 输入项 | 来源 | 说明 |
|---|---|---|
| 已验证切片列表 | `.workflow/session/slices/` | 所有已通过验证的切片定义 |
| 验证结果 | `.workflow/session/verify/` | 各切片的验证结果文件 |
| 设计文档 | 原始设计文档 | 业务流程和模块间交互参考 |
| 会话状态 | `.workflow/session/state.md` | 当前会话状态（如存在） |

## Procedure

1. **确认切片验证状态**：逐一检查所有相关切片的验证状态，确保均为 `pass`。如有未通过的切片，停止集成验证并报告。
2. **提取集成场景**：从设计文档中提取业务流程章节，识别关键的集成场景和模块间交互路径。
3. **检查模块间接口一致性**：
   - 验证模块间调用的输入/输出类型是否匹配
   - 检查参数名称、顺序和类型是否一致
   - 检查返回值类型和错误类型是否对齐
4. **检查数据流传递**：
   - 验证数据在模块间的传递路径是否正确
   - 检查数据转换和映射逻辑是否完整
   - 确认无数据丢失或类型不匹配
5. **执行集成测试**：运行项目中已有的集成测试套件，验证模块协作的正确性。
6. **验证关键业务流程**：逐一验证设计中定义的关键业务流程是否可端到端跑通。
7. **检查错误处理链**：
   - 验证错误在模块间的传播是否正确
   - 检查回滚逻辑是否完整
   - 确认异常场景下系统行为符合预期
8. **执行回归测试**：运行先前已通过的测试套件，确保新实现未破坏既有功能。
9. **汇总为单一结论**：
   - `pass`：集成验证通过
   - `fail`：存在集成问题需要修复
10. **按需写入轻量结果**：如使用会话目录，可写入 `.workflow/session/integration-report.md`。

## Output

### 最小输出

- `verified_slices`
- `interface_check`
- `data_flow_check`
- `integration_tests`
- `regression_tests`
- `result`
- `next_step`

### 建议文件输出

- `.workflow/session/integration-report.md`

建议结构：

```markdown
# Integration Report

- verified_slices: [slice-001, slice-002, ...]
- interface_check: pass | fail
- data_flow_check: pass | fail
- integration_tests: pass | fail | partial
- regression_tests: pass | fail
- result: pass | fail
- next_step: <...>

## Details
- ...

## Issues
- ...
```

## Quality Gate

| 检查项 | 通过标准 |
|---|---|
| 关键业务流程 | 端到端可跑通 |
| 模块间接口类型 | 一致 |
| 集成测试 | 通过 |
| 回归测试 | 无既有功能被破坏 |

**判定标准：** 所有关键链路通过 → `pass`；任一关键链路失败 → `fail`。

## Failure Handling

| 失败场景 | 处理方式 |
|---|---|
| **接口不一致** | 定位到具体切片和模块，回到 [slice-implement/SKILL.md](../slice-implement/SKILL.md) 修复接口定义，修复后重新走 `slice-verify` → `integration-verify` |
| **集成测试失败** | 分析根因，确定影响的切片范围，回到对应 `slice-implement` 修复后重新验证 |
| **关键链路失败** | 必须修复后重新验证，不允许跳过 |
| **非关键链路失败** | 记录为已知问题，可继续进入下一阶段，但须在报告中注明 |
| **回归测试失败** | 定位引起回归的切片，回到 `slice-implement` 修复 |

## Non-Goals

以下内容不属于本 skill：

- 不替代单切片验证
- 不生成复杂追踪矩阵（由 `result-curate` 负责）
- 不维护复杂阶段状态机
- 不自动推进流程

集成验证通过后，如需归档沉淀，可进入 [result-curate/SKILL.md](../result-curate/SKILL.md)。
