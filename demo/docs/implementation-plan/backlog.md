# Backlog：mini-curl

## 1. 基本信息

- run_id: demo-mini-curl-run-001
- generated_from: [`mini-curl-implementation-plan.md`](demo/docs/implementation-plan/mini-curl-implementation-plan.md)
- generated_at: 2026-03-30

## 2. Backlog 条目

### BL-001：创建 Rust crate 骨架

- 优先级：P0
- 切片：slice-001
- 设计来源：[`normalized § 6.5`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 7`](demo/docs/design/mini-curl-design.normalized.md)
- 描述：初始化 `demo/mini-curl/` Cargo 项目，创建 `Cargo.toml`（含 clap/reqwest/tokio/wiremock 依赖），建立 `src/main.rs`、`src/error.rs`、`src/cli.rs`、`src/request_builder.rs`、`src/http_client.rs`、`src/output.rs` 模块文件
- 验收：`cargo build` 通过

### BL-002：实现 AppError 枚举

- 优先级：P0
- 切片：slice-001
- 设计来源：[`normalized § 6.5`](demo/docs/design/mini-curl-design.normalized.md)
- 描述：定义 `AppError` 枚举（InvalidArgs、Timeout、DnsError、ConnectionError、RequestError、OutputError），实现 `Display` trait（格式 `mini-curl: error: <描述>`），实现 `exit_code()` 方法
- 验收：单元测试覆盖所有变体的 Display 和 exit_code

### BL-003：实现 CLI 参数解析

- 优先级：P0
- 切片：slice-002
- 设计来源：[`normalized § 6.1`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 8.1`](demo/docs/design/mini-curl-design.normalized.md)
- 描述：使用 clap derive 模式定义 CLI 结构体，解析 URL、method、header、data、timeout、include、show-status 参数，生成 `AppConfig`
- 验收：参数解析单元测试通过

### BL-004：实现 method 推断规则

- 优先级：P0
- 切片：slice-002
- 设计来源：[`normalized § 7.3`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 9.2`](demo/docs/design/mini-curl-design.normalized.md)
- 描述：实现 method 推断逻辑：无 method 无 body → GET；无 method 有 body → POST；GET + body → 报错；POST ± body → POST
- 验收：推断规则表 6 种组合全覆盖测试通过

### BL-005：实现请求构造

- 优先级：P1
- 切片：slice-003
- 设计来源：[`normalized § 6.2`](demo/docs/design/mini-curl-design.normalized.md)
- 描述：将 `AppConfig` 转换为 `reqwest::RequestBuilder`，设置 method、URL、headers、body
- 验收：构造结果正确，header 格式校验生效

### BL-006：实现 HTTP 请求发送

- 优先级：P1
- 切片：slice-004
- 设计来源：[`normalized § 6.3`](demo/docs/design/mini-curl-design.normalized.md)
- 描述：发送 reqwest 请求，设置超时，将响应转换为 `HttpResult`，将错误分类为对应 `AppError` 变体
- 验收：`cargo build` 通过，错误分类逻辑正确

### BL-007：实现输出格式化

- 优先级：P2
- 切片：slice-005
- 设计来源：[`normalized § 6.4`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 8.2`](demo/docs/design/mini-curl-design.normalized.md)
- 描述：根据 `show_status`/`show_headers` 标志输出状态码、响应头、响应体到 stdout
- 验收：输出格式与设计一致

### BL-008：实现 main 编排

- 优先级：P2
- 切片：slice-005
- 设计来源：[`normalized § 10.3`](demo/docs/design/mini-curl-design.normalized.md)
- 描述：`main()` 仅调用 `parse_args()` → `build_request()` → `send_request()` → `print_response()`，处理错误输出和退出码
- 验收：`main()` 无业务逻辑，仅编排

### BL-009：补齐集成测试

- 优先级：P2
- 切片：slice-006
- 设计来源：[`normalized § 10.1`](demo/docs/design/mini-curl-design.normalized.md)
- 描述：使用 wiremock 编写集成测试，覆盖 GET 请求、POST 请求、超时、自定义 header、状态码输出、响应头输出
- 验收：`cargo test` 全部通过

### BL-010：全量质量验证

- 优先级：P2
- 切片：slice-006
- 设计来源：[`normalized § 10.2`](demo/docs/design/mini-curl-design.normalized.md)
- 描述：运行 `cargo fmt --check`、`cargo clippy -- -D warnings`、`cargo test`，确保全部通过
- 验收：三项检查零错误零警告
