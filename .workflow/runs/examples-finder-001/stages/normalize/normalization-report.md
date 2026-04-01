# 规范化报告 — examples-finder-001

## 输入

- **原始设计**：`.workflow/docs/design/finder.md`
- **Intake 报告**：`.workflow/runs/examples-finder-001/stages/intake/intake-report.md`
- **run-brief**：无实质内容，未并入本稿。

## 输出

- **规范化设计**：`.workflow/docs/design/finder.normalized.md`
- **待确认清单**：`.workflow/runs/examples-finder-001/stages/normalize/unresolved-items.md`

---

## 标准化与结构调整

| 动作 | 说明 |
| --- | --- |
| 章节对齐 | 按 design-intake 模板使用 §1–§12 及约定小节标题（如 ### 2.1 业务背景、### 5.1 主流程 / ### 5.2 异常流程）。 |
| §5 主流程合并 | 将原「5.1 文本 / 5.2 路径」并入 **§5.1 主流程**，分别以 #### 5.1.1 / 5.1.2 编号；原 **5.3 异常流程** 升格为 **§5.2 异常流程**。 |
| 元信息 | **作者**：由占位「—」改为「未署名（由仓库贡献记录为准）」；**版本**升为 0.2（规范化稿）；增加源文档/规范化稿路径字段。 |
| Intake ⚠️ 作者 | 已处理（见上），不虚构具体人名。 |
| Intake ⚠️ 退出码 | 新增 **§8.4 CLI 退出码约定**（0/1/2/3）；同步更新 §3.1、§5.2、§9.2、§10.1 中与退出码相关的描述。 |
| 模块 6.5 | **错误处理**由「—」改为明确：无独立错误码，由 CLI 映射 §8.4。 |
| 术语 | 「名称模式」与 **[待确认：名称模式]** 交叉引用；增加「规范化路径」简述。 |

---

## 内容补充（有依据的收敛）

| 项 | 依据 | 说明 |
| --- | --- | --- |
| 无匹配退出码 = 1 | 原 §9.2 建议与 grep 一致；intake 建议 normalize 收敛 | 写入 §8.4，并从 §11.2 开放项中移除该条。 |
| 用法错误 = 2、不可恢复 = 3 | 业界常见 CLI 惯例；与原「成功/无匹配/用户错误/运行时错误」四分法对应 | 表格式固定，减少实现歧义。 |
| 异常流程与码表一致 | 原表格 + 新 §8.4 | 根无效、正则失败映射为 3。 |

---

## 显式 [待确认] / 未决策项（不伪造）

以下不在正文中擅自选定，均以 **[待确认：…]** 标记，并列入 `unresolved-items.md`：

- 实现语言与包管理器
- `finder text` 默认匹配模式（`--regex` vs `--fixed-strings`）
- `finder path` 的 `--name` 语义（glob / fnmatch / 正则）
- SIGINT 具体退出码（仅要求非零）

---

## 与 intake 建议的对照

| Intake 建议 | 处理 |
| --- | --- |
| 关联 run → examples-finder-001 | 源 `finder.md` 已含；规范化稿 §1 保留。 |
| 退出码表 | 已补充 §8.4。 |
| 默认 regex/fixed、名称匹配语义 | 标记 [待确认]，收录 unresolved-items.md。 |
| 双路径同步风险 | 写入 §1 与 §11.1。 |

---

## Quality Gate（自检）

- [x] 12 个标准章节存在且顺序与模板一致
- [x] intake ⚠️/建议项已处理（补齐、收敛或 [待确认]）
- [x] `unresolved-items.md` 与正文占位一致
- [x] `state.md` 将更新为 normalize / done
