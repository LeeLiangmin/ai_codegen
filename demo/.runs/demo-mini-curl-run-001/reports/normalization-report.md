# Normalization Report：demo-mini-curl-run-001

## 1. 基本信息

- skill：[`design-normalize`](.skills/design-normalize.md)
- 原始设计：[`demo/docs/design/mini-curl-design.md`](demo/docs/design/mini-curl-design.md)
- intake 报告：[`demo/.runs/demo-mini-curl-run-001/reports/intake-report.md`](demo/.runs/demo-mini-curl-run-001/reports/intake-report.md)
- 输出设计稿：[`demo/docs/design/mini-curl-design.normalized.md`](demo/docs/design/mini-curl-design.normalized.md)
- 执行时间：2026-03-30

## 2. 执行摘要

结论：**normalize 完成，允许进入 plan 阶段**

本次 normalize 主要完成了以下工作：

1. 收敛了 intake 报告中列出的 6 项待确认决策
2. 标准化了章节结构，补齐了表格化描述
3. 明确了错误输出格式、退出码策略和 method 推断规则
4. 补充了 Cargo.toml 依赖建议
5. 细化了异常流程处理表

## 3. 收敛决策清单

以下为 intake 报告中标记的待确认项及其收敛结果：

| # | 待确认项 | 收敛决策 | 理由 |
| --- | --- | --- | --- |
| 1 | HTTP 客户端选型 | reqwest（异步） | Rust 生态最成熟的 HTTP 客户端，文档完善 |
| 2 | CLI 参数解析选型 | clap（derive 模式） | 社区最广泛使用，derive 模式与结构体天然映射 |
| 3 | 集成测试机制 | wiremock（本地 mock server） | 无需外部网络依赖，测试稳定可重复 |
| 4 | method 白名单 | 仅 GET/POST | 与 In Scope 一致 |
| 5 | 错误输出格式 | `mini-curl: error: <描述>` 输出到 stderr | 统一格式，便于验证 |
| 6 | clippy 判定口径 | `cargo clippy -- -D warnings` 零警告 | 明确可执行标准 |

## 4. 章节变更摘要

| 章节 | 变更类型 | 说明 |
| --- | --- | --- |
| 4.1 术语定义 | 结构化 | 从列表改为表格，补充 method、timeout 定义 |
| 4.3 技术选型决策 | 新增 | 整理所有收敛决策为独立章节 |
| 5.2 异常流程 | 细化 | 从列表改为表格，补充退出码映射 |
| 6.x 模块设计 | 细化 | 补充具体类型签名、错误变体映射 |
| 6.5 error 模块 | 细化 | 新增错误变体表、Display 格式要求、exit_code 方法 |
| 7.1 核心实体 | 结构化 | 从嵌套列表改为表格 |
| 7.3 Method 推断规则 | 新增 | 明确所有 method/body 组合的行为 |
| 8.1 命令行接口 | 结构化 | 改为参数表格 |
| 8.2 输出格式 | 新增 | 明确 stdout 输出格式示例 |
| 8.3 退出码 | 新增 | 独立退出码表 |
| 10.x 验收标准 | 细化 | 补充验证方式和通过标准 |
| 11.2 已知限制 | 新增 | 明确首版接受的限制 |
| 12.3 Cargo.toml | 新增 | 依赖建议 |
| 12.4 禁止事项 | 补充 | 新增 unwrap 禁止、main 逻辑禁止 |

## 5. 补充信息来源

本次 normalize 未引入外部 PDF 或补充说明。所有补充内容均基于：

- intake 报告中的风险分析
- Rust 生态最佳实践
- curl 命令行行为惯例

## 6. 门禁检查

根据 [`.skills/design-normalize.md`](.skills/design-normalize.md) 的门禁要求，输出文档必须满足模板要求：

| 模板章节 | 是否覆盖 | 备注 |
| --- | --- | --- |
| 文档元信息 | ✅ | |
| 背景与目标 | ✅ | |
| 范围 | ✅ | |
| 术语与约束 | ✅ | 新增技术选型决策 |
| 业务流程 | ✅ | 异常流程已表格化 |
| 模块设计 | ✅ | 5 个模块均已细化 |
| 数据设计 | ✅ | 新增数据流图和推断规则表 |
| 接口设计 | ✅ | 新增输出格式和退出码 |
| 状态与规则 | ✅ | |
| 验收标准 | ✅ | 补充验证方式 |
| 风险与待确认项 | ✅ | 待确认项已全部收敛 |
| AI 实施附录 | ✅ | 新增依赖建议 |

门禁结论：**通过，允许进入 plan 阶段**
