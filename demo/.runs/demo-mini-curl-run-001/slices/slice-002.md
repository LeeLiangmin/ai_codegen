# Slice-002：CLI 参数解析与 AppConfig

## 1. 基本信息

- run_id: demo-mini-curl-run-001
- slice_id: slice-002
- title: CLI 参数解析与 AppConfig
- priority: P0
- owner: AI
- status: pending

## 2. 切片目标

使用 clap derive 模式实现 CLI 参数解析，生成 `AppConfig` 结构体，实现 method 推断规则。

## 3. 输入依据

- 设计章节：[`normalized § 6.1 cli 模块`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 7.1 AppConfig`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 7.3 Method 推断规则`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 8.1 命令行接口`](demo/docs/design/mini-curl-design.normalized.md)
- 关联模块：cli
- 关联接口：`parse_args()`
- 关联数据结构：`AppConfig`
- 前置依赖：slice-001

## 4. 实现边界

### 4.1 允许修改范围

- `demo/mini-curl/src/cli.rs`：完整实现
- `demo/mini-curl/src/main.rs`：可能需要调整模块引用

### 4.2 禁止修改范围

- 不得修改 `error.rs` 中已有的 `AppError` 定义（除非需要新增变体）
- 不得在 cli 模块中发送 HTTP 请求

## 5. 预期产出

- `demo/mini-curl/src/cli.rs`：clap derive 结构体 + `parse_args()` 函数 + method 推断逻辑 + 单元测试

## 6. 验证要求

- `cargo build` 通过
- `cargo test` 通过
- method 推断规则表 6 种组合全覆盖：
  - 无 method 无 body → GET
  - 无 method 有 body → POST
  - GET 无 body → GET
  - GET 有 body → 报错
  - POST 无 body → POST
  - POST 有 body → POST
- header 可重复解析测试通过
- timeout 非法值报错测试通过

## 7. 偏差与升级策略

### 7.1 允许记录偏差的条件

无预期偏差。

### 7.2 必须升级人工处理的条件

- clap derive 模式无法表达所需参数组合

## 8. 完成定义

- [x] `AppConfig` 结构体已定义
- [x] `parse_args()` 函数已实现
- [x] method 推断规则已实现
- [x] 6 种推断组合单元测试通过
- [x] `cargo build` 通过
- [x] `cargo test` 通过
