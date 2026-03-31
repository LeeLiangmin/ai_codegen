# Slice-005：输出格式化与 main 编排

## 1. 基本信息

- run_id: demo-mini-curl-run-001
- slice_id: slice-005
- title: 输出格式化与 main 编排
- priority: P2
- owner: AI
- status: pending

## 2. 切片目标

实现 `output` 模块的格式化输出，完成 `main()` 函数的编排逻辑，使程序可端到端运行。

## 3. 输入依据

- 设计章节：[`normalized § 6.4 output 模块`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 8.2 输出格式`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 8.3 退出码`](demo/docs/design/mini-curl-design.normalized.md)
- 关联模块：output, main
- 关联接口：`print_response()`
- 关联数据结构：`HttpResult`, `AppConfig`
- 前置依赖：slice-004

## 4. 实现边界

### 4.1 允许修改范围

- `demo/mini-curl/src/output.rs`：完整实现
- `demo/mini-curl/src/main.rs`：完成编排逻辑

### 4.2 禁止修改范围

- 不得修改其他模块已有逻辑
- `main()` 不得包含业务逻辑，仅做编排

## 5. 预期产出

- `demo/mini-curl/src/output.rs`：`print_response()` 函数 + 单元测试
- `demo/mini-curl/src/main.rs`：完整编排 parse_args → build_request → send_request → print_response

## 6. 验证要求

- `cargo build` 通过
- 输出格式符合设计：
  - `--show-status` 时输出 `HTTP <status_code>`
  - `--include` 时逐行输出 `<name>: <value>` + 空行
  - 始终输出 body
- 错误输出到 stderr，格式 `mini-curl: error: <描述>`
- 退出码正确：0/1/2
- 手动运行 `cargo run -- https://httpbin.org/get` 可输出响应

## 7. 偏差与升级策略

### 7.1 允许记录偏差的条件

无预期偏差。

### 7.2 必须升级人工处理的条件

- 编排逻辑无法正确串联各模块

## 8. 完成定义

- [x] `print_response()` 函数已实现
- [x] `main()` 编排已完成
- [x] 输出格式符合设计
- [x] 手动运行可正常工作
- [x] `cargo build` 通过
