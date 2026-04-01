---
name: slice-verify
description: Use when a slice is implemented and you need design-consistency checks, lint, typecheck, tests, and a written verification report with pass or fail
---

# slice-verify

## Overview

对单个切片执行设计一致性检查和自动化验证，确保实现质量达标。验证范围涵盖设计一致性、代码格式、静态分析、类型检查和单元测试。

## When to Use

切片实现完成后，进入验证阶段。

**前置条件：**
- 切片 status 为 `implemented`
- 切片对应的代码改动和测试改动已就绪

## Input

| 输入项 | 路径 / 来源 | 说明 |
| --- | --- | --- |
| 切片定义 | `.workflow/runs/<run-id>/slices/slice-<NNN>.md` | 切片目标、边界和验收标准 |
| 代码改动 | git diff 或文件列表 | 切片实现产生的所有变更 |
| 测试改动 | 对应测试文件 | 切片新增或修改的测试 |
| 规范化设计稿 | `.workflow/docs/design/<name>.normalized.md` | 设计一致性检查参考 |
| 运行状态 | `.workflow/runs/<run-id>/state.md` | 当前 run 的全局状态 |

## Procedure

1. **读取切片定义和关联设计章节**：明确该切片的目标、接口定义、数据结构和验收标准。
2. **收集代码改动**：通过 git diff 或文件比对，获取切片实现的所有代码改动清单。
3. **设计一致性检查**：
   - 实现是否覆盖切片定义中的所有目标
   - 接口签名是否与设计一致（函数名、参数类型、返回值类型）
   - 数据结构是否与设计一致（字段名、类型、约束）
   - 是否存在未授权的功能扩展（超出切片 scope 的新增功能）
   - 命名是否符合设计约定和项目风格
4. **格式检查**：执行项目的格式化工具验证代码风格一致性。
   - 示例：`cargo fmt --check`、`prettier --check`、`gofmt -l`、`black --check` 等
5. **静态检查**：执行 linter 检查潜在问题。
   - 示例：`cargo clippy`、`eslint`、`golint`、`pylint` 等
6. **类型检查**：执行编译或类型检查确保类型安全。
   - 示例：`cargo build`、`tsc --noEmit`、`mypy` 等
7. **单元测试**：执行与切片相关的测试，确保功能正确。
   - 优先运行切片直接关联的测试；若无法精确定位则运行全量测试
8. **契约测试**（如适用）：验证接口契约是否满足上下游约定。
9. **汇总检查结果**：收集以上所有检查步骤的输出，分类记录通过项和失败项。
10. **生成验证报告**：将检查结果写入结构化的验证报告（见 § Template）。
11. **判定结果**：根据质量门禁标准判定 `passed` 或 `failed`。
12. **更新状态**：更新切片 status（`verified` 或 `failed`）和 `state.md`。

## Output

| 输出项 | 路径 | 条件 |
| --- | --- | --- |
| 验证报告 | `.workflow/runs/<run-id>/stages/implement-verify/slice-<NNN>-verification-report.md` | 始终产出 |
| 失败检查清单 | `.workflow/runs/<run-id>/stages/implement-verify/slice-<NNN>-failed-checks.md` | 存在失败项时产出 |
| 修复建议 | `.workflow/runs/<run-id>/stages/implement-verify/slice-<NNN>-remediation-suggestions.md` | 存在失败项时产出 |
| 更新后状态 | `.workflow/runs/<run-id>/state.md` | 始终更新 |

## Quality Gate

| 检查项 | 通过标准 | 备注 |
| --- | --- | --- |
| 设计一致性检查 | 所有必要项通过 | 接口、数据结构、命名均与设计一致 |
| 格式检查 | 通过 | 无格式违规 |
| 静态检查 | 无 error | warning 可接受但需记录 |
| 类型检查 / 编译 | 通过 | 无编译错误 |
| 单元测试 | 全部通过 | 包括新增和既有测试 |

**判定标准：** 以上所有项通过 → `verified`；任一项失败 → `failed`。

## Failure Handling

| 失败场景 | 处理方式 |
| --- | --- |
| **格式 / 静态检查失败** | 尝试自动修复（如 `cargo fmt`、`prettier --write`），修复后重新验证，最多自动重试 2 次 |
| **类型检查 / 编译失败** | 回到 `slice-implement` 修复类型错误或编译错误 |
| **单元测试失败** | 分析失败原因（实现缺陷 vs 测试问题），回到 `slice-implement` 修复 |
| **设计一致性失败** | 记录偏差详情，判断是否可接受：可接受则标记为 `accepted deviation` 并通过；不可接受则回到 `slice-implement` |
| **反复失败（≥ 3 次）** | 升级为人工处理，在报告中标注 `escalated`，停止自动重试 |

## Template

验证报告写入 `.workflow/runs/<run-id>/stages/implement-verify/slice-<NNN>-verification-report.md`。

报告结构：
- 切片标识与验证时间
- 设计一致性检查结果
- 自动化检查结果（格式 / lint / 类型 / 测试）
- 总体结论（pass / fail）
- 失败项明细与修复建议（如有）
