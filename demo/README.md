# Demo 使用说明：Rust mini curl

当前 demo 已准备好第一批“开始流程的输入”，核心入口如下：

- 设计输入文档：[`demo/docs/design/mini-curl-design.md`](demo/docs/design/mini-curl-design.md)
- run 状态文件：[`demo/.runs/demo-mini-curl-run-001/state.md`](demo/.runs/demo-mini-curl-run-001/state.md)

## 建议你接下来这样做

### 第 1 步：执行 intake

目标：验证设计文档是否足够驱动实现。

你需要做的事：

1. 对照 [` .skills/design-intake.md`](.skills/design-intake.md) 检查 [`demo/docs/design/mini-curl-design.md`](demo/docs/design/mini-curl-design.md)
2. 重点看以下项是否完整：
   - 目标与非目标
   - 模块设计
   - 数据设计
   - CLI 接口设计
   - 验收标准
   - AI 禁止事项
3. 输出建议文件：
   - [`demo/.runs/demo-mini-curl-run-001/reports/intake-report.md`](demo/.runs/demo-mini-curl-run-001/reports/intake-report.md)

如果 intake 结论是“设计足够完整”，就把 [`demo/.runs/demo-mini-curl-run-001/state.md`](demo/.runs/demo-mini-curl-run-001/state.md) 里的 [`intake`](demo/.runs/demo-mini-curl-run-001/state.md) 阶段状态改为 passed 或 completed。

### 第 2 步：执行 normalize

目标：把设计收敛成最终执行版本。

在这个 demo 中，当前设计文档已经比较结构化，所以 normalize 主要做三件事：

1. 明确技术选型，例如：
   - CLI 参数库是否使用 [`clap`](demo/docs/design/mini-curl-design.md)
   - HTTP 客户端是否使用 [`reqwest`](demo/docs/design/mini-curl-design.md)
   - 测试是否使用本地 mock server
2. 把“待确认项”转成明确决策
3. 生成规范化版本设计稿或直接在原设计上冻结一个 v0.2

建议输出：

- [`demo/docs/design/mini-curl-design.normalized.md`](demo/docs/design/mini-curl-design.normalized.md)
- [`demo/.runs/demo-mini-curl-run-001/reports/normalization-report.md`](demo/.runs/demo-mini-curl-run-001/reports/normalization-report.md)

### 第 3 步：执行 design-to-plan

目标：把设计转成真正可实现的 backlog。

建议直接基于现有设计生成：

- [`demo/docs/implementation-plan/mini-curl-implementation-plan.md`](demo/docs/implementation-plan/mini-curl-implementation-plan.md)

内容至少包括：

- 模块拆分
- crate 依赖建议
- 切片顺序
- 验证方式
- 风险与偏差策略

### 第 4 步：执行切片规划

目标：把 backlog 拆成可逐步实现的小任务。

建议先创建：

- [`demo/.runs/demo-mini-curl-run-001/slices/slice-001.md`](demo/.runs/demo-mini-curl-run-001/slices/slice-001.md)
- [`demo/.runs/demo-mini-curl-run-001/slices/slice-002.md`](demo/.runs/demo-mini-curl-run-001/slices/slice-002.md)
- ……

其中首个切片建议是：

- `slice-001`：初始化 Rust crate、定义错误类型、搭建模块骨架

### 第 5 步：再进入真正编码

只有在切片文档明确后，才开始在 [`demo/`](demo/) 下创建 Rust 工程并编码。

推荐执行顺序：

1. 先实现 `slice-001`
2. 完成后执行局部验证
3. 更新 run 状态
4. 再进入下一个切片

## 当前最合理的下一动作

最合理的下一动作不是立刻写 Rust 代码，而是先补齐 intake 报告与 normalized 设计稿，这样后续实现更稳定、也更符合这套方法论。
