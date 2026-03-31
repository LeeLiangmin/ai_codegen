# Slice-004：HTTP 请求发送 http_client

## 1. 基本信息

- run_id: demo-mini-curl-run-001
- slice_id: slice-004
- title: HTTP 请求发送 http_client
- priority: P1
- owner: AI
- status: pending

## 2. 切片目标

实现 `http_client` 模块，发送 HTTP 请求，处理超时，将响应转换为 `HttpResult`，将错误分类为对应 `AppError` 变体。

## 3. 输入依据

- 设计章节：[`normalized § 6.3 http_client 模块`](demo/docs/design/mini-curl-design.normalized.md)
- 关联模块：http_client
- 关联接口：`send_request()`
- 关联数据结构：`HttpResult`
- 前置依赖：slice-003

## 4. 实现边界

### 4.1 允许修改范围

- `demo/mini-curl/src/http_client.rs`：完整实现
- 可能需要在 `error.rs` 中补充 `From<reqwest::Error>` 实现

### 4.2 禁止修改范围

- 不得修改 `cli.rs`、`request_builder.rs` 已有逻辑
- 不得在 http_client 中解析 CLI 参数或格式化输出

## 5. 预期产出

- `demo/mini-curl/src/http_client.rs`：`send_request()` 函数 + `HttpResult` 结构体 + 错误分类逻辑

## 6. 验证要求

- `cargo build` 通过
- `HttpResult` 结构体包含 status、headers、body 字段
- 错误分类覆盖：Timeout、DnsError、ConnectionError、RequestError

## 7. 偏差与升级策略

### 7.1 允许记录偏差的条件

- reqwest 错误分类粒度不足时，部分错误归入 `RequestError`（记录偏差）
- 响应体使用 `text()` 默认解码（记录偏差）

### 7.2 必须升级人工处理的条件

- tokio runtime 配置问题导致无法发送请求

## 8. 完成定义

- [x] `send_request()` 函数已实现
- [x] `HttpResult` 结构体已定义
- [x] 错误分类逻辑已实现
- [x] `cargo build` 通过
