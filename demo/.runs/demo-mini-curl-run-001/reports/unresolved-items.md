# Unresolved Items：demo-mini-curl-run-001（normalize 阶段）

## 1. 概述

经过 normalize 阶段处理后，所有 intake 报告中标记的待确认项已全部收敛为明确决策。

**当前无未决项。**

## 2. 已解决项回顾

| # | 原始待确认项 | 解决方式 | 解决位置 |
| --- | --- | --- | --- |
| 1 | 同步/异步模型选择 | 决策为异步（tokio + reqwest） | [`mini-curl-design.normalized.md § 4.3`](demo/docs/design/mini-curl-design.normalized.md) |
| 2 | CLI 库选型 | 决策为 clap derive 模式 | [`mini-curl-design.normalized.md § 4.3`](demo/docs/design/mini-curl-design.normalized.md) |
| 3 | HTTP 客户端库选型 | 决策为 reqwest | [`mini-curl-design.normalized.md § 4.3`](demo/docs/design/mini-curl-design.normalized.md) |
| 4 | 集成测试方案 | 决策为 wiremock | [`mini-curl-design.normalized.md § 4.3`](demo/docs/design/mini-curl-design.normalized.md) |
| 5 | body 自动推断规则 | 保留自动推断为 POST | [`mini-curl-design.normalized.md § 7.3`](demo/docs/design/mini-curl-design.normalized.md) |
| 6 | method 白名单 | 仅 GET/POST | [`mini-curl-design.normalized.md § 4.3`](demo/docs/design/mini-curl-design.normalized.md) |
| 7 | clippy 判定口径 | `cargo clippy -- -D warnings` | [`mini-curl-design.normalized.md § 10.2`](demo/docs/design/mini-curl-design.normalized.md) |
| 8 | 错误输出格式 | `mini-curl: error: <描述>` | [`mini-curl-design.normalized.md § 5.2`](demo/docs/design/mini-curl-design.normalized.md) |
| 9 | 退出码策略 | 0/1/2 三级 | [`mini-curl-design.normalized.md § 8.3`](demo/docs/design/mini-curl-design.normalized.md) |

## 3. 已知限制（非未决项，首版接受）

以下为首版有意接受的限制，不视为未决项：

- 响应体完全加载到内存
- 不支持 HTTPS 证书自定义
- 不支持重定向跟随控制（使用 reqwest 默认行为）
