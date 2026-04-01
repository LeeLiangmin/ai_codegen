---
name: design-intake
description: Use when a run exists and you need to validate a design Markdown document for structural completeness and produce an intake report before normalization
---

# design-intake

检查 `.workflow/docs/design/` 下设计稿是否够格进入 normalize；写 `stages/intake/intake-report.md`，更新 `state.md`（`current_stage: intake`）。

## 输入

设计 Markdown、`state.md`；可选补充材料、`run-brief.md`（任一节非「无」且有实质内容则作**本次约束**，与 design 冲突须写入报告）。

## 步骤

1. 读设计 + 可选 brief。  
2. 按下表「必备块」逐项标 ✅/⚠️/❌；记章节间矛盾、brief 与 design 矛盾。  
3. 写 `intake-report.md`：总结表、缺失、冲突、风险、结论二选一：`允许进入 normalize` | `需补充后重新 intake`。  
4. 更新 `state.md`：intake 行 `done`/`failed`，`updated_at`。

## 必备块（须有足够内容）

| 块 | 要点 |
| --- | --- |
| 元信息 | 名称、版本、状态 |
| 目标与范围 | 目标、非目标、In/Out |
| 术语与约束 | 术语、全局约束 |
| 流程 | 主流程 + 关键异常 |
| 模块 | 职责、边界、依赖 |
| 数据 | 实体/字段或等价说明 |
| 接口 | 签名或路径级约定 |
| 状态与规则 | 状态机/业务规则（若适用） |
| 验收 | 可测的完成标准 |
| 风险与待确认 | 已知风险、待决项 |
| AI 附录 | 切片建议、禁止事项（可简写） |

长文结构范例见旧版或团队模板；**本 skill 不强制 12 章标题**，但上表信息必须能在文档中定位。

## Gate

- [ ] 关键块充分：目标、模块、接口、数据、验收  
- [ ] 结论明确；报告已落盘；`state.md` 已更新

## 失败

关键缺、严重冲突 → 结论 `需补充后重新 intake`，intake 行 `failed`。
