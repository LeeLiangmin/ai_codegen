---
name: run-status
description: Use when you need to interpret .workflow/runs/<run-id>/state.md for a design-driven run, summarize progress, and get the recommended next skill invocation for resume (read-only; does not advance the pipeline)
---

# run-status

**只读**：读 `state.md`（+ optional `run-brief`），输出摘要与**建议下一个** `skill/<name>/SKILL.md`；默认不写文件（可选写 `stages/plan/run-status.md`）。

## 输入

`state.md` 路径，或 `run_id`，或仅项目根（则列出 runs 供选）。

## 输出结构

```markdown
## Run 状态摘要
- run_id / status / current_stage / current_slice
- design_doc；brief 要点（若启用）
- 阶段表摘要；未完成切片；§5 阻塞

## 续跑建议
- 下一步：`skill/<name>/SKILL.md`
- 示例调用句；若已完成则说明无需续跑
```

## 路由（简表）

| 阶段/表观 | 下一步 |
| --- | --- |
| intake 未完成或失败 | design-intake |
| normalize 未完成 | design-normalize |
| plan 未完成 | design-to-plan |
| 无切片或 slice 行未完成 | plan-to-slices |
| 有 implemented 待验 | slice-verify |
| 有 pending 且依赖满足 | slice-implement |
| 全片 verified，集成未过 | integration-verify |
| 集成过，未归档 | result-curate |
| close 且 completed | 无 |

细则：以 §3 + §4 为准；矛盾时提示人工核对。

## Gate

- [ ] 不臆造字段；建议的 skill 路径在仓库中存在
