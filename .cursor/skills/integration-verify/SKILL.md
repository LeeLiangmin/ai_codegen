---
name: integration-verify
description: Use when all slices are verified and you need cross-slice integration checks, E2E flows, and regression before closing the run
---

# integration-verify

## Overview

对多个已验证切片的组合结果执行集成验证，确保模块间协作正确、数据流通畅、关键业务流程端到端闭环。

## When to Use

所有切片（或一组相关切片）都已通过 slice-verify，准备进行集成级别的验证。

**前置条件：**
- 相关切片的 `verify_status` 均为 `passed`
- 无处于 `blocked` 或 `failed` 状态的前置切片

## Input

| 输入项 | 路径 / 来源 | 说明 |
| --- | --- | --- |
| 已验证切片列表 | `.workflow/runs/<run-id>/slices/` | 所有 status 为 `verified` 的切片 |
| 集成场景定义 | 从设计文档业务流程章节提取 | 关键业务流程和模块间交互 |
| 规范化设计稿 | `.workflow/docs/design/<name>.normalized.md` | 模块接口和数据流参考 |
| 运行状态 | `.workflow/runs/<run-id>/state.md` | 当前 run 的全局状态 |

## Procedure

1. **确认切片验证状态**：逐一检查所有相关切片的验证状态，确保均为 `verified`。如有未通过的切片，停止集成验证并报告。
2. **提取集成场景**：从规范化设计稿中提取业务流程章节，识别关键的集成场景和模块间交互路径。
3. **检查模块间接口一致性**：
   - 验证模块间调用的输入/输出类型是否匹配
   - 检查参数名称、顺序和类型是否一致
   - 检查返回值类型和错误类型是否对齐
4. **检查数据流传递**：
   - 验证数据在模块间的传递路径是否正确
   - 检查数据转换和映射逻辑是否完整
   - 确认无数据丢失或类型不匹配
5. **执行集成测试**：运行项目中已有的集成测试套件，验证模块协作的正确性。
6. **验证关键业务流程**：逐一验证设计稿中定义的关键业务流程是否可端到端跑通。
7. **检查错误处理链**：
   - 验证错误在模块间的传播是否正确
   - 检查回滚逻辑是否完整
   - 确认异常场景下系统行为符合预期
8. **执行回归测试**：运行先前已通过的测试套件，确保新实现未破坏既有功能。
9. **汇总集成验证结果**：收集以上所有检查和测试的输出，分类记录。
10. **生成报告**：生成集成报告、回归报告和未解决问题清单（见 § Template）。
11. **更新 state.md**：根据验证结果更新 run 的全局状态。

## Output

| 输出项 | 路径 | 条件 |
| --- | --- | --- |
| 集成报告 | `.workflow/runs/<run-id>/stages/integrate/integration-report.md` | 始终产出 |
| 回归报告 | `.workflow/runs/<run-id>/stages/integrate/regression-report.md` | 始终产出 |
| 未解决问题清单 | `.workflow/runs/<run-id>/stages/integrate/unresolved-integration-issues.md` | 存在未解决问题时产出 |
| 更新后状态 | `.workflow/runs/<run-id>/state.md` | 始终更新 |

## Quality Gate

| 检查项 | 通过标准 | 备注 |
| --- | --- | --- |
| 关键业务流程 | 端到端可跑通 | 所有关键链路必须通过 |
| 模块间接口类型 | 一致 | 输入/输出/错误类型完全匹配 |
| 集成测试 | 通过 | 所有集成测试用例通过 |
| 回归测试 | 通过 | 无既有功能被破坏 |

**判定标准：** 所有关键链路通过 → `passed`；任一关键链路失败 → `failed`。

## Failure Handling

| 失败场景 | 处理方式 |
| --- | --- |
| **接口不一致** | 定位到具体切片和模块，回到 `slice-implement` 修复接口定义，修复后重新走 `slice-verify` → `integration-verify` |
| **集成测试失败** | 分析根因，确定影响的切片范围，回到对应 `slice-implement` 修复后重新验证 |
| **关键链路失败** | 不允许进入 close 阶段，必须修复后重新验证。记录失败详情到 `unresolved-integration-issues.md` |
| **非关键链路失败** | 记录为 `accepted deviation`，可继续进入下一阶段，但须在最终报告中注明 |
| **回归测试失败** | 定位引起回归的切片，回到 `slice-implement` 修复，确保既有功能不受影响 |

## Template

集成验证报告写入 `.workflow/runs/<run-id>/stages/integrate/integration-report.md`。

报告结构：
- 验证范围（参与集成的切片列表）
- 接口一致性检查结果
- 数据流验证结果
- 端到端业务流程验证结果
- 回归测试结果
- 总体结论（pass / fail）
- 失败项明细与修复建议（如有）
