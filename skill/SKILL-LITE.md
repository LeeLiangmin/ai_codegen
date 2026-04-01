---
name: ai-design-toolkit-lite
description: Use when you need a minimal design-to-code loop for small scope or weaker models; merges full pipeline stages; full registry in skill/SKILL.md
---

# AI 设计驱动实现 — 轻量流程（Lite）

完整九阶段流水线见 [`SKILL.md`](SKILL.md)。**Lite 只做一件事：用最少步骤保留「设计 → 小步实现 → 验证 → 可恢复状态」四条底线。**

## 何时用 Lite

- 模型上下文/推理能力有限，跟不住长 procedure。
- 需求范围小、设计文档已经比较完整，不需要单独的 intake/normalize 报告链。
- 你愿意用**一份合并产出**代替多份阶段报告（需要审计或合规时再切回完整 skill）。

## 四条第一性原理（必须保留）

1. **单一事实源**：实现依据只能来自明确写下的设计/计划（口头不算）。
2. **小步交付**：每次只做一个切片；不跨切片大改。
3. **验证关门**：改完必须跑项目约定的检查（至少：能编译 + 相关测试）。
4. **状态可续**：只维护一个 `state.md`（或等价清单），写清「做到哪、哪失败」。

## 压缩后的五步（对应完整流水线）

| Lite 步 | 做什么 | 合并了哪些完整阶段 |
| --- | --- | --- |
| **L1 初始化** | 创建 `.workflow/runs/<run-id>/`，`state.md`，`run-brief.md`（可空），设计路径写进 state | `run-init` |
| **L2 规格包** | 读设计稿，**一次性**产出：① 仍缺的要点清单（若有）② 归一化设计或补丁 ③ 实现计划 + backlog（可一个文件里分节） | `design-intake` + `design-normalize` + `design-to-plan` |
| **L3 切片** | 把计划拆成 `slice-NNN.md`（目标、范围、依赖、验收） | `plan-to-slices` |
| **L4 实现与验证** | 每个切片：改代码 → 跑 lint/测试 → 简短通过/失败记录 | `slice-implement` + `slice-verify` |
| **L5 收尾** | 全部切片通过后：跑一次集成/回归（若项目有）；写一段「交付摘要 + 已知偏差」（可极短） | `integration-verify` + `result-curate`（可降级） |

**续跑**：不确定进度时读 `.workflow/runs/<run-id>/state.md` 与 `slices/`；仍可用 [`run-status/SKILL.md`](run-status/SKILL.md) 只读解读。

## 弱模型执行清单（按顺序打勾）

**L1**

- [ ] `run-init` 已执行，目录与 `state.md` 存在（可直接照 [`run-init/SKILL.md`](run-init/SKILL.md) 的模板，不必读长 procedure）。

**L2**

- [ ] 设计里已有：目标、范围、主要接口/数据、验收方式；缺的补在「规格包」里，不要静默假设。
- [ ] 产出路径与完整流水线兼容即可，例如：`.workflow/docs/design/<name>.normalized.md` + `.workflow/docs/implementation-plan/<name>-implementation-plan.md`（或合并为一个 `spec-lite.md` 再在 state §6 里登记）。

**L3**

- [ ] 每个切片可独立完成、可测试；依赖关系写清。

**L4**

- [ ] 只动切片允许的路径；做完跑验证命令（以仓库 README 或 `package.json`/`Cargo.toml` 等为准）。
- [ ] 失败则修到通过再下一切片；`state.md` 与切片表同步。

**L5**

- [ ] 至少一次「全量相关测试」或项目规定的检查；交付摘要 10～30 行可接受。

## 刻意省略的内容（换人工或切回完整 skill）

- 长篇 **intake / normalization 独立报告**（Lite 用清单 + 合并稿代替）。
- **追溯矩阵、完整偏差档案**（小项目可用 `deviations-summary` 一段话）。
- 复杂多团队/强合规场景：**不要用 Lite**，按 [`SKILL.md`](SKILL.md) 全阶段执行。

## 与 `skill/<name>/SKILL.md` 的关系

- 各阶段 skill 已压成短指令；Lite 仍可合并 L2/L5 的**文件个数**，需要审计时再拆报告。
