# 下一轮迭代上下文 — examples-finder-001

面向后续 AI 或人工会话：在 **不重读全量 skill** 的前提下可继续的工作包与禁区。

## 推荐下一步

1. **可选 — B-14**：若仓库引入 GitHub Actions（或其他 CI），增加 `examples/finder` 下 `uv run pytest`（或等价）任务，与根仓库风格对齐；完成后更新 `backlog.md` / 新 run 的切片或在本 run 追溯矩阵将 B-14 行改为 `completed`。
2. **可选 — 设计 vNext**：若需「仅统计文件数」、跟随 symlink 防环、或第三大类功能，须先升版 `examples/finder/DESIGN.md` → 同步 `finder.md` → 重新 normalize/plan（新 run 或同一 run 的变更流程）。
3. **维护**：双设计稿与 `finder.normalized.md` 保持同步策略见 `final-index.md` §5.2。

## 待确认项（需人工决策）

- **是否要为 ai_codegen 根仓库加 CI**：当前无 `.github/workflows`；加与不加均为合理产品决策。
- **是否在后续迭代中强制 Windows SIGINT 与 Unix 对齐**：当前实现符合设计「Windows 以实现为准」。

## 不建议自动推进的区域

- **未经设计升版** 的网络搜索、索引服务、GUI、或弱化路径逃逸 / 默认 symlink 策略 — 违反 `finder.normalized.md` §10.3 / §12.3。
- **在生产路径中硬编码** 机器相关绝对路径作为默认根 — 设计禁止项。

## 快速路径索引

| 目的 | 路径 |
| --- | --- |
| 规范化设计 | `.workflow/docs/design/finder.normalized.md` |
| 实现计划与 backlog | `.workflow/docs/implementation-plan/finder-implementation-plan.md`、`backlog.md` |
| Run 状态 | `.workflow/runs/examples-finder-001/state.md` |
| 集成与回归结论 | `stages/integrate/integration-report.md`、`regression-report.md` |
| 交付与追溯 | `stages/curate/final-index.md`、`traceability-matrix.md` |
| 源码 | `examples/finder/` |

## 恢复 run 时

- 若仅文档/CI 增量：可从 **close** 状态开新 run 或在本仓库直接改代码并补验证报告。
- 若设计变更：从 **design-intake** 或至少 **normalize** 重跑流水线；勿在旧 `normalized.md` 上直接堆叠矛盾需求。
