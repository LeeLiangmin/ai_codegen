# AI 设计驱动实现 Toolkit 使用说明

## 1. 使用目标

本说明用于指导如何在单仓库内使用 [`docs/ai-design-implementation-toolkit.md`](docs/ai-design-implementation-toolkit.md) 中定义的方案、[` .skills/`](.skills/) 中的 skill 说明，以及 [` .templates/`](.templates/) 中的模板，组织一次完整的 AI 设计驱动实现 run。

## 2. 推荐流程

### 步骤 1：准备输入设计

1. 依据 [` .templates/design-doc-template.md`](.templates/design-doc-template.md) 编写或整理设计文档。
2. 若原始资料包含 PDF，仅作为参考，最终收敛到 Markdown 版本。
3. 将设计文档放入建议目录，例如 [`docs/design/`](docs/design/)。

### 步骤 2：执行 intake

1. 使用 [` .skills/design-intake.md`](.skills/design-intake.md) 检查设计完整性。
2. 输出 intake 报告，确认是否允许进入 normalize 阶段。

### 步骤 3：执行 normalize

1. 使用 [` .skills/design-normalize.md`](.skills/design-normalize.md) 规范化设计文档。
2. 输出标准设计稿与待确认项列表。

### 步骤 4：生成实现计划

1. 使用 [` .skills/design-to-plan.md`](.skills/design-to-plan.md) 生成实现计划。
2. 参考 [` .templates/implementation-plan-template.md`](.templates/implementation-plan-template.md) 形成计划文档。

### 步骤 5：切分任务

1. 使用 [` .skills/plan-to-slices.md`](.skills/plan-to-slices.md) 生成切片任务。
2. 参考 [` .templates/slice-template.md`](.templates/slice-template.md) 为每个切片生成定义文档。

### 步骤 6：逐切片实现与验证

1. 使用 [` .skills/slice-implement.md`](.skills/slice-implement.md) 执行单切片实现。
2. 使用 [` .skills/slice-verify.md`](.skills/slice-verify.md) 执行单切片验证。
3. 多切片完成后，使用 [` .skills/integration-verify.md`](.skills/integration-verify.md) 执行集成验证。

### 步骤 7：结果沉淀

1. 使用 [` .skills/result-curate.md`](.skills/result-curate.md) 汇总结果。
2. 参考 [` .templates/traceability-matrix-template.md`](.templates/traceability-matrix-template.md) 和 [` .templates/final-index-template.md`](.templates/final-index-template.md) 生成交付资产。

## 3. 运行时状态管理

每次 run 建议都创建独立状态文件，参考 [` .templates/run-state-template.md`](.templates/run-state-template.md)。

建议目录结构：

```text
.runs/<run-id>/
  state.md
  slices/
  reports/
```

状态文件用于支持：

- 断点恢复
- 失败重试
- 人工接管
- 结果追踪

## 4. 最小落地顺序

建议按以下顺序开始真正实现该 toolkit：

1. 固化模板与规范
2. 建立 run 目录约定
3. 先手工跑通一轮完整流程
4. 再把各阶段逐步脚本化/自动化
5. 最后实现统一编排入口

## 5. 成功标准

若满足以下条件，可认为首版 toolkit 具备可用性：

- 设计文档可以被规范化
- 实现计划可以从设计中稳定提取
- 切片可以独立执行与验证
- 质量门禁可以阻止明显偏差进入后续阶段
- 最终结果可以被追踪、归档和复用
