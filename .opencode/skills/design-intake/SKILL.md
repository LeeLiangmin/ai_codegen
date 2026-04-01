---
name: design-intake
description: Use when a run exists and you need to validate a design Markdown document for structural completeness and produce an intake report before normalization
---

# design-intake

## Overview

验证输入设计文档是否满足 AI 可执行的结构化要求，输出 intake 报告。

## When to Use

run 初始化完成后执行第一次 intake，或 intake 失败后重试。

前置条件：
- run 已通过 `run-init` 初始化
- `state.md` 中 **`status`** 可为 `created`（或失败重试时仍为可继续的 run 状态）；**`current_stage`** 为 `init`（首次）或 `intake`（重试）
- 设计文档已放入 `.workflow/docs/design/` 目录

## Input

| 参数 | 必填 | 说明 |
|------|------|------|
| 设计文档路径 | 是 | `.workflow/docs/design/` 下的 Markdown 文件 |
| 补充参考资料 | 否 | PDF、口头说明等辅助材料 |
| `state.md` 路径 | 是 | `.workflow/runs/<run-id>/state.md` |
| `run-brief.md` | 否 | `.workflow/runs/<run-id>/run-brief.md`；由 `run-init` 创建。各节仅为「无」或空则视为**未启用**本次额外约束 |

## Procedure

1. **读取设计文档**：加载 `.workflow/docs/design/` 下的目标 Markdown 文件及可选补充资料。
2. **读取 run-brief（可选）**：若存在 `.workflow/runs/<run-id>/run-brief.md`（或 `state.md` §6 所列路径），且除模板说明外**含有实质内容**（任一节非空且非仅「无」），则加载并在后续检查中作为**本次 run 约束**；否则跳过，不改变既有 intake 规则。
3. **逐项对照模板检查**：按 § 8 中的设计文档结构参考，检查以下必要章节是否存在且内容充分：
   - 文档元信息
   - 背景与目标（含非目标）
   - 范围（In Scope / Out of Scope）
   - 术语与约束
   - 业务流程（主流程 + 异常流程）
   - 模块设计
   - 数据设计
   - 接口设计
   - 状态与规则
   - 验收标准
   - 风险与待确认项
   - AI 实施附录
4. **评估每个章节**：对每个章节标注评估结果：
   - ✅ 存在且充分
   - ⚠️ 存在但不完整（附说明）
   - ❌ 缺失
5. **识别设计冲突与模糊表述**：检查章节间是否存在矛盾、模糊定义或无法落地的描述。若已加载有效 run-brief，另设「**brief 与设计一致性**」：brief 中硬约束/非目标/范围是否与设计章节明显冲突；若有，写入冲突项清单，结论倾向 `需补充后重新 intake` 或至少在风险项中要求人工裁定（**不**在 intake 中静默忽略 brief）。
6. **生成 intake 报告**：按以下结构输出 `.workflow/runs/<run-id>/stages/intake/intake-report.md`：
   - 检查总结表（章节 × 评估结果）
   - 缺失项清单
   - 冲突项清单（含 design 内部矛盾，及 **run-brief 与设计** 的矛盾，若适用）
   - 风险项清单
   - 结论：`允许进入 normalize` 或 `需补充后重新 intake`
7. **更新状态文件**：更新 `.workflow/runs/<run-id>/state.md`：
   - `current_stage` → `intake`
   - intake 行的 `status` → `done` 或 `failed`
   - `updated_at` → 当前时间

## Output

- `.workflow/runs/<run-id>/stages/intake/intake-report.md` — intake 检查报告
- 更新 `.workflow/runs/<run-id>/state.md` — 阶段状态更新

## Quality Gate

- [ ] 所有**关键章节**必须存在且充分：目标、模块设计、接口设计、数据设计、验收标准
- [ ] 无关键冲突（章节间无矛盾）
- [ ] 结论明确：`允许进入 normalize` 或 `需补充后重新 intake`
- [ ] 报告已写入 `.workflow/runs/<run-id>/stages/intake/intake-report.md`
- [ ] `state.md` 已更新

## Failure Handling

- **关键章节缺失**：在报告中列出全部缺失项，结论设为 `需补充后重新 intake`，给出每项的补充建议。`state.md` intake 状态设为 `failed`。
- **存在设计冲突**：在报告中列出冲突点，建议人工确认后重新提交。
- **补充资料无法解析**：记录在报告中，标记为风险项，不阻塞流程。

## Template

### 设计文档结构参考

以下为设计文档应遵循的标准结构，intake 检查将对照此结构进行：

#### 1. 文档元信息

- 项目名称
- 文档标题
- 版本
- 作者
- 日期
- 状态：草稿 / 评审中 / 已确认
- 关联需求
- 关联 run

#### 2. 背景与目标

##### 2.1 业务背景
说明业务上下文与问题来源。

##### 2.2 目标
明确本次设计要解决的问题与目标范围。

##### 2.3 非目标
明确本次设计不解决的问题，避免实现范围蔓延。

#### 3. 范围

##### 3.1 In Scope
列出本次需要实现的功能点。

##### 3.2 Out of Scope
列出本次不在实现范围内的内容。

#### 4. 术语与约束

##### 4.1 术语定义
列出关键术语与统一命名。

##### 4.2 全局约束
包括但不限于：技术栈约束、安全约束、性能约束、合规约束、部署约束。

#### 5. 业务流程

##### 5.1 主流程
以步骤形式描述核心业务流程。

##### 5.2 异常流程
列出关键异常、失败、回滚、补偿场景。

#### 6. 模块设计

对每个模块描述：
- 模块职责
- 输入
- 输出
- 依赖
- 边界
- 错误处理
- 安全要求

#### 7. 数据设计

##### 7.1 核心实体
按实体说明：实体名、字段、类型、是否必填、约束、备注。

##### 7.2 数据关系
说明实体关系与一致性要求。

##### 7.3 数据迁移需求
说明是否涉及表结构、索引、历史数据修复。

#### 8. 接口设计

对每个接口描述：
- 目的、方法、路径
- 请求参数、响应结构
- 错误码、幂等要求
- 权限要求、限流要求

#### 9. 状态与规则

##### 9.1 状态机
描述对象状态变化规则。

##### 9.2 核心业务规则
按规则逐条列出。

#### 10. 验收标准

##### 10.1 功能验收
列出必须满足的功能点。

##### 10.2 质量验收
测试覆盖要求、性能指标、稳定性要求、兼容性要求。

##### 10.3 设计一致性要求
列出实现不得偏离的关键设计约束。

#### 11. 风险与待确认项

##### 11.1 风险
列出已识别风险。

##### 11.2 待确认项
列出需要人工或上游确认的问题。

#### 12. AI 实施附录

##### 12.1 实现切片建议
##### 12.2 推荐测试点
##### 12.3 禁止事项
