# Finder 风险清单（examples-finder-001）

来源：`.workflow/docs/design/finder.normalized.md` §11.1、实现计划推演、当前仓库状态（`examples/finder` 尚无代码，属绿field）。

| 风险 | 类别 | 影响 | 缓解 / 应对 | 状态 |
| --- | --- | --- | --- | --- |
| 大文件或超长行导致内存压力 | 技术 | OOM 或卡顿 | 流式读行 + 单行长度上限常数（§6.3）；测试中可含中等长度行 | 开放 |
| 非 UTF-8 编码文件 | 技术 | 漏检、乱码、跳过不一致 | README + 实现固定一种编码失败策略（§3.1、§6.3） | 开放 |
| Windows 大小写、路径分隔符、`:` 与输出格式 | 兼容 | 测试失败或用户困惑 | README 明确；Output 可选转义策略；针对性 fixture | 开放 |
| 双路径设计稿（`examples/finder/DESIGN.md` vs `finder.md`）不同步 | 流程 | 实现偏离权威意图 | 修改以 `DESIGN.md` 为准并同步镜像（§11.1） | 持续注意 |
| uv / Python 版本与 CI 镜像不一致 | 工程 | CI 失败 | `pyproject` 钉 `requires-python`；文档写明本地命令 | 开放 |
| `finder path` 与 `finder text` 共享 Walker 时职责耦合 | 设计 | 重构成本 | 先完成 slice-001 Walker API，再挂 PathSearch/ContentSearch | 缓解中（计划内） |
| SIGINT 在 Windows 上非 130 | 平台 | 与 §8.4 Unix 承诺混淆 | README 写明实际行为；不在 Windows 上断言 130 | 可接受偏差 |

**与 run-brief 冲突**：当前 brief 无实质内容；若后续追加硬约束，须对比本表与设计并更新 backlog/计划。

**循环依赖**：模块依赖为有向无环（Walker → PathSearch/ContentSearch；CLI 聚合全部），无需打破循环的额外切片。

**技术栈**：已确定为 Python 3.10+ + uv；无「未选定栈」项。
