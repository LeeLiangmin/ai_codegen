# Slice-003：请求构造 request_builder

## 1. 基本信息

- run_id: demo-mini-curl-run-001
- slice_id: slice-003
- title: 请求构造 request_builder
- priority: P1
- owner: AI
- status: pending

## 2. 切片目标

实现 `request_builder` 模块，将 `AppConfig` 转换为 `reqwest::RequestBuilder`，校验 method/body/header 组合约束。

## 3. 输入依据

- 设计章节：[`normalized § 6.2 request_builder 模块`](demo/docs/design/mini-curl-design.normalized.md)
- 关联模块：request_builder
- 关联接口：`build_request()`
- 关联数据结构：`AppConfig` → `reqwest::RequestBuilder`
- 前置依赖：slice-002

## 4. 实现边界

### 4.1 允许修改范围

- `demo/mini-curl/src/request_builder.rs`：完整实现

### 4.2 禁止修改范围

- 不得修改 `cli.rs` 已有逻辑
- 不得在 request_builder 中发送请求或格式化输出

## 5. 预期产出

- `demo/mini-curl/src/request_builder.rs`：`build_request()` 函数 + header 解析 + 单元测试

## 6. 验证要求

- `cargo build` 通过
- `cargo test` 通过
- header 格式校验（必须含 `:`）测试通过
- method 白名单校验测试通过
- URL 设置正确
- body 设置正确

## 7. 偏差与升级策略

### 7.1 允许记录偏差的条件

- header 值中包含 `:` 时仅按首个 `:` 分割（记录偏差）

### 7.2 必须升级人工处理的条件

- reqwest API 变更导致无法构造 RequestBuilder

## 8. 完成定义

- [x] `build_request()` 函数已实现
- [x] header 解析与校验已实现
- [x] 单元测试通过
- [x] `cargo build` 通过
- [x] `cargo test` 通过
