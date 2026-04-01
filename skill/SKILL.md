---
name: ai-design-toolkit
description: Use when orienting to this repo's design-to-code pipeline, choosing which stage skill to run, or invoking run-init through result-curate
---

# AI Design-Driven Implementation Toolkit

## 一句话

设计文档 → 计划与切片 → 逐切片实现/验证 → 集成 → 归档；权威指令在 `skill/<name>/SKILL.md`。**弱模型 / 小范围**先读 [`SKILL-LITE.md`](SKILL-LITE.md)。

## Skill 表

| # | Skill | 产出要点 |
|---|--------|----------|
| — | [run-status](run-status/SKILL.md) | 只读解读 `state.md`，建议下一步（不推进阶段） |
| 1 | [run-init](run-init/SKILL.md) | `.workflow/runs/<id>/`、`state.md`、`run-brief.md` |
| 2 | [design-intake](design-intake/SKILL.md) | `stages/intake/intake-report.md` |
| 3 | [design-normalize](design-normalize/SKILL.md) | `*.normalized.md`、normalize 报告 |
| 4 | [design-to-plan](design-to-plan/SKILL.md) | `implementation-plan/*`、backlog、risks |
| 5 | [plan-to-slices](plan-to-slices/SKILL.md) | `slices/slice-NNN.md`、`index.md` |
| 6 | [slice-implement](slice-implement/SKILL.md) | 代码 + 测试（在切片 scope 内） |
| 7 | [slice-verify](slice-verify/SKILL.md) | `slice-NNN-verification-report.md` |
| 8 | [integration-verify](integration-verify/SKILL.md) | `integrate/integration-report.md` 等 |
| 9 | [result-curate](result-curate/SKILL.md) | `curate/traceability-matrix.md`、`final-index.md` 等 |

## 顺序（ASCII）

`run-init → design-intake → design-normalize → design-to-plan → plan-to-slices → (slice-implement ↔ slice-verify)* → integration-verify → result-curate → close`

- intake/normalize 失败：补文档后重试同阶段。  
- verify 失败：回到 `slice-implement` 再验。  
- integration 失败：定位切片后回退修复。  
- 续跑不确定：先 `run-status`。

## OpenCode / Cursor

- 权威：`skill/<name>/SKILL.md`。镜像：`.opencode/skills/`、`.cursor/skills/` — 改后执行 `scripts/sync-ide-mirrors.ps1` 或 `sync-ide-mirrors.sh`。  
- 入口：根 [`AGENTS.md`](../AGENTS.md)、[`opencode.json`](../opencode.json)。Cursor：[`ai-design-toolkit.mdc`](../.cursor/rules/ai-design-toolkit.mdc)。

## 调用示例

```
请按照 skill/design-intake/SKILL.md 执行，输入为 .workflow/docs/design/my-feature-design.md
```

## 目录约定（精简）

```
.workflow/docs/design/{name}.md, {name}.normalized.md
.workflow/docs/implementation-plan/
.workflow/runs/<run-id>/state.md, run-brief.md, slices/, stages/{intake,normalize,plan,implement-verify,integrate,curate}/
```

细则见 [`docs/superpowers/specs/2026-04-01-workflow-layout-design.md`](../docs/superpowers/specs/2026-04-01-workflow-layout-design.md)。

## 状态

`state.md`：`status`（run 生命周期）≠ `current_stage`（推进阶段）。阶段名：`init` → `intake` → `normalize` → `plan` → `slice` → `implement` / `verify`（循环）→ `integrating` → `curate` → `close`。模板见 [run-init/SKILL.md](run-init/SKILL.md)。

## 质量与失败

- **L1** 对照设计；**L2** lint/类型/测试；**L3** 人工。  
- 失败类：设计缺陷 / 实现偏差 / 验证失败 / 环境 — 从当前阶段或上一可恢复点重试（见 [run-init §7](run-init/SKILL.md)）。
