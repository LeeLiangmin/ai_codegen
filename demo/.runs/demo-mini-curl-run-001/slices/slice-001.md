# Slice-001：Rust crate 骨架与 AppError 枚举

## 1. 基本信息

- run_id: demo-mini-curl-run-001
- slice_id: slice-001
- title: Rust crate 骨架与 AppError 枚举
- priority: P0
- owner: AI
- status: pending

## 2. 切片目标

初始化 `demo/mini-curl/` Cargo 项目，建立模块文件结构，定义 `AppError` 枚举及其 `Display` 和 `exit_code()` 实现。

## 3. 输入依据

- 设计章节：[`normalized § 6.5 error 模块`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 7`](demo/docs/design/mini-curl-design.normalized.md)
- 关联模块：error
- 关联接口：`AppError::fmt()`、`AppError::exit_code()`
- 关联数据结构：`AppError` 枚举
- 前置依赖：无

## 4. 实现边界

### 4.1 允许修改范围

- 创建 `demo/mini-curl/Cargo.toml`
- 创建 `demo/mini-curl/src/main.rs`
- 创建 `demo/mini-curl/src/error.rs`
- 创建 `demo/mini-curl/src/cli.rs`（空模块声明）
- 创建 `demo/mini-curl/src/request_builder.rs`（空模块声明）
- 创建 `demo/mini-curl/src/http_client.rs`（空模块声明）
- 创建 `demo/mini-curl/src/output.rs`（空模块声明）

### 4.2 禁止修改范围

- 不得修改 `demo/` 下除 `mini-curl/` 以外的任何文件
- 不得在空模块中添加业务逻辑

## 5. 预期产出

- `demo/mini-curl/Cargo.toml`：含 clap、reqwest、tokio、wiremock 依赖
- `demo/mini-curl/src/main.rs`：模块声明 + 占位 main
- `demo/mini-curl/src/error.rs`：完整 `AppError` 枚举 + Display + exit_code
- `demo/mini-curl/src/cli.rs`：空模块
- `demo/mini-curl/src/request_builder.rs`：空模块
- `demo/mini-curl/src/http_client.rs`：空模块
- `demo/mini-curl/src/output.rs`：空模块

## 6. 验证要求

- `cargo build` 通过
- `cargo fmt --check` 通过
- `cargo clippy -- -D warnings` 通过
- `AppError` 所有变体的 Display 输出格式为 `mini-curl: error: <描述>`
- `AppError` 所有变体的 exit_code 返回 1 或 2

## 7. 偏差与升级策略

### 7.1 允许记录偏差的条件

无预期偏差。

### 7.2 必须升级人工处理的条件

- 依赖版本冲突导致 `cargo build` 失败
- Rust toolchain 不可用

## 8. 完成定义

- [x] Cargo 项目已创建
- [x] 所有模块文件已建立
- [x] `AppError` 枚举已定义并实现 Display 和 exit_code
- [x] `cargo build` 通过
- [x] `cargo fmt --check` 通过
- [x] `cargo clippy -- -D warnings` 通过
