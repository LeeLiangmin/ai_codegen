---
name: design-to-plan
description: Use when normalized design exists and you need an executable implementation plan, backlog, and risks under `.workflow/docs/implementation-plan/`
---

# design-to-plan

从 `*.normalized.md` 生成实现计划、backlog、risks；更新 `state.md`（`current_stage: plan`）。

## 输入

`.workflow/docs/design/<name>.normalized.md`、仓库上下文、`state.md`；可选 `run-brief`（对齐优先级与非目标）。

## 步骤

1. 提取模块、接口、数据、跨模块约束与依赖顺序。  
2. 写三份文件：  
   - `<name>-implementation-plan.md`（目标、模块表、接口表、数据变更、**切片草案表**、质量门禁摘要）  
   - `backlog.md`（可执行条目 + 优先级）  
   - `risks.md`（风险、模糊点、与设计/brief 冲突）  
3. `state.md` §6 可填 `implementation_plan` 路径；`updated_at`。

## Gate

- [ ] 设计中的模块/主要接口出现在计划中；切片草案各有验证标准；无静默忽略 brief

## 失败

模糊边界、循环依赖 → 记入 risks，必要时回 normalize。

## 计划文档最小骨架

```markdown
### 基本信息
- run_id / design_doc / run_brief（路径或「未启用」）/ generated_at

### 模块分解
| 模块 | 职责 | 依赖 | 风险 | 优先级 |

### 接口清单
| 接口 | 模块 | 输入输出 | 验收点 |

### 切片计划（草案）
| slice_id | 目标 | 依赖 | 验证标准 |
```
