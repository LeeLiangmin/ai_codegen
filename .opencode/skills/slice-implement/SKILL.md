---
name: slice-implement
description: Use when a slice definition exists, dependencies are satisfied, and you need code and tests strictly within the slice's allowed modification scope
---

# slice-implement

## Overview

针对单个切片，在受控范围内完成代码实现，包括业务代码、测试代码和配置文件。确保实现严格遵循切片定义的边界，不越界修改，不扩展未授权功能。

## When to Use

切片定义文档已生成，准备进入编码实现阶段。

**前置条件：**
- 切片 status 为 `pending` 或 `blocked` 已解除
- 所有前置依赖切片（`depends_on` 中列出的切片）已完成（status 为 `verified`）
- 规范化设计稿和实现计划可访问

## Input

| 输入项 | 路径 / 来源 | 说明 |
| --- | --- | --- |
| 当前切片定义 | `.workflow/runs/<run-id>/slices/slice-<NNN>.md` | 包含目标、边界、允许修改范围 |
| 规范化设计稿 | `.workflow/docs/design/<name>.normalized.md` | 关联设计章节参考 |
| 仓库现有代码 | 项目代码库 | 理解当前代码结构和上下文 |
| 运行状态 | `.workflow/runs/<run-id>/state.md` | 当前 run 的全局状态 |
| run-brief | `.workflow/runs/<run-id>/run-brief.md` | 可选。有实质内容时与切片边界一起作为硬约束，不得扩展至 brief 非目标 |

## Procedure

1. **读取切片定义文档**：确认切片目标（`objective`）、输入依据（`input_refs`）和实现边界（`scope`，包括允许修改范围和禁止修改范围）。
2. **读取 run-brief（可选）**：若存在且含实质内容，确认本切片未违反其硬约束与非目标；若有疑问，标记 `blocked` 并记录原因。
3. **检查前置依赖**：验证 `depends_on` 中列出的所有前置切片 status 均为 `verified`。若不满足，标记为 `blocked` 并停止。
4. **阅读关联设计章节**：从规范化设计稿中定位切片引用的设计章节，理解设计意图、接口定义和数据结构。
5. **阅读现有代码上下文**：浏览切片允许修改范围涉及的文件和目录，理解当前代码结构、命名风格和依赖关系。
6. **确认修改范围**：明确列出允许修改的文件/模块和禁止修改的文件/模块，作为实现过程中的硬约束。
7. **实现业务代码**：按设计要求生成或修改业务代码。严格遵循设计稿中的接口签名、数据结构和命名约定。
8. **补齐单元测试**：为新增或修改的代码编写对应的单元测试，覆盖正常路径和关键异常路径。
9. **更新配置文件**：如切片涉及配置变更（依赖声明、环境配置等），同步更新相关配置文件。
10. **记录实现决策**：将实现过程中的重要决策写入 `implementation-notes`（如：为何选择某种实现方式、性能考量等）。
11. **记录偏差**：如发现实际实现与设计存在不一致之处，写入 `deviation` 记录，说明偏差内容和原因。
12. **处理阻塞情况**：如遇设计冲突、依赖缺失或边界外问题，立即停止实现，标记切片为 `blocked`，记录阻塞原因。
13. **更新切片状态**：将切片 status 从 `running` 更新为 `implemented`。
14. **更新 state.md**：同步更新 run 的全局状态文件，反映当前切片进展。

## Output

| 输出项 | 路径 | 条件 |
| --- | --- | --- |
| 代码改动 | 切片允许范围内的文件 | 始终产出 |
| 测试改动 | 对应测试文件 | 始终产出 |
| 实现决策记录 | `.workflow/runs/<run-id>/stages/implement-verify/slice-<NNN>-implementation-notes.md` | 如有决策记录 |
| 偏差记录 | `.workflow/runs/<run-id>/stages/implement-verify/slice-<NNN>-deviation.md` | 如有偏差 |
| 更新后状态 | `.workflow/runs/<run-id>/state.md` | 始终更新 |

## Quality Gate

- [ ] 所有代码改动都在切片定义的允许修改范围内
- [ ] 不存在超出切片边界的修改
- [ ] 新增代码有对应的单元测试
- [ ] 代码可编译 / 可解析（基本语法正确）
- [ ] 实现与设计章节描述一致（接口签名、数据结构、命名）
- [ ] 切片 status 已正确更新为 `implemented`

## Failure Handling

| 失败场景 | 处理方式 |
| --- | --- |
| **设计冲突** | 停止实现，在 `deviation` 中记录冲突详情，标记切片为 `blocked`，建议人工决策 |
| **依赖不满足** | 检查前置切片完成状态，标记为 `blocked`，记录具体缺失的依赖切片 |
| **改动越界** | 回退越界改动，重新审视切片边界；如边界定义不合理，建议拆分为子切片 |
| **实现复杂度超预期** | 记录在 `implementation-notes`，评估是否需要拆分当前切片为更细粒度的子切片 |

## Template

本 Skill 不生成文档模板，产出物为代码文件。

切片任务定义模板请参考 [plan-to-slices § Template](../plan-to-slices/SKILL.md#template)。
