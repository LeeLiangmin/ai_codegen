# 实现计划：mini-curl

## 1. 基本信息

- run_id: demo-mini-curl-run-001
- design_doc: [`demo/docs/design/mini-curl-design.normalized.md`](demo/docs/design/mini-curl-design.normalized.md)
- scope: Rust 小型 curl 命令行工具首版
- owner: AI Toolkit Demo
- generated_at: 2026-03-30

## 2. 总体实现目标

- 业务目标：实现一个可执行的 Rust CLI 工具，支持 GET/POST 请求、自定义 header、超时控制和格式化输出
- 技术目标：使用 clap + reqwest + tokio 构建异步 CLI 程序，模块边界清晰，可测试
- 交付目标：可通过 `cargo build`、`cargo test`、`cargo fmt --check`、`cargo clippy -- -D warnings` 的完整工程

## 3. 模块分解

| 模块 | 职责 | 依赖 | 风险 | 优先级 |
| --- | --- | --- | --- | --- |
| error | 统一错误枚举 `AppError`，含 Display 和 exit_code | 无外部依赖 | 低 | P0 |
| cli | clap derive 解析参数，生成 `AppConfig`，含 method 推断 | clap, error | 低 | P0 |
| request_builder | `AppConfig` → `reqwest::RequestBuilder`，校验 method/body/header | reqwest, error | 中（header 解析边界） | P1 |
| http_client | 发送请求，超时处理，错误分类为 `AppError` 变体 | reqwest, tokio, error | 中（异步+错误分类） | P1 |
| output | 格式化输出 status/headers/body 到 stdout | error | 低 | P2 |
| main | 编排入口，调用各模块，处理退出码 | 全部模块 | 低 | P2 |

## 4. 接口实现清单

| 接口 | 所属模块 | 输入 | 输出 | 权限/约束 | 验收点 |
| --- | --- | --- | --- | --- | --- |
| `parse_args()` | cli | `std::env::args()` | `Result<AppConfig, AppError>` | method 白名单 GET/POST | 参数解析正确，推断规则生效 |
| `build_request()` | request_builder | `&AppConfig` | `Result<reqwest::RequestBuilder, AppError>` | GET 不允许 body | 请求配置正确构造 |
| `send_request()` | http_client | `RequestBuilder`, timeout | `Result<HttpResult, AppError>` | 超时限制 | 请求发送成功，错误正确分类 |
| `print_response()` | output | `&HttpResult`, `&AppConfig` | `Result<(), AppError>` | 输出到 stdout | 格式符合设计 |
| `AppError::fmt()` | error | `&self` | `String` | 格式 `mini-curl: error: <描述>` | 所有变体格式正确 |
| `AppError::exit_code()` | error | `&self` | `i32` | 1 或 2 | 退出码与错误类型匹配 |

## 5. 数据变更清单

| 数据对象 | 变更类型 | 影响范围 | 风险 | 验证方式 |
| --- | --- | --- | --- | --- |
| `AppConfig` | 新建 struct | cli → request_builder, output | 低 | 单元测试 |
| `HttpResult` | 新建 struct | http_client → output | 低 | 单元测试 |
| `AppError` | 新建 enum | 全模块 | 低 | 单元测试 |

## 6. 切片计划

| slice_id | 目标 | 输入 | 产出 | 依赖 | 验证标准 |
| --- | --- | --- | --- | --- | --- |
| slice-001 | Rust crate 骨架 + `AppError` 枚举 + 模块文件结构 | normalized design § 6.5, § 7 | `Cargo.toml`, `src/main.rs`, `src/error.rs`, `src/cli.rs`(空), `src/request_builder.rs`(空), `src/http_client.rs`(空), `src/output.rs`(空) | 无 | `cargo build` 通过 |
| slice-002 | `cli` 模块：clap derive + `AppConfig` + method 推断 | normalized design § 6.1, § 7.1, § 7.3, § 8.1 | `src/cli.rs` 完整实现 + 单元测试 | slice-001 | 推断规则表全覆盖测试通过 |
| slice-003 | `request_builder` 模块：AppConfig → RequestBuilder | normalized design § 6.2 | `src/request_builder.rs` 完整实现 + 单元测试 | slice-002 | method/body/header 校验测试通过 |
| slice-004 | `http_client` 模块：发送请求 + 错误分类 | normalized design § 6.3 | `src/http_client.rs` 完整实现 | slice-003 | `cargo build` 通过 |
| slice-005 | `output` 模块：格式化输出 + `main()` 编排 | normalized design § 6.4, § 8.2 | `src/output.rs` + `src/main.rs` 完整实现 | slice-004 | 手动运行可输出响应 |
| slice-006 | wiremock 集成测试 + fmt/clippy/test 全量验证 | normalized design § 10 | `tests/` 目录 + 验证报告 | slice-005 | `cargo test` + `cargo fmt --check` + `cargo clippy -- -D warnings` 全部通过 |

## 7. 质量门禁

### 7.1 设计一致性检查

每个切片完成后必须检查：

- 模块边界是否与设计一致（5 个模块不得合并或拆分）
- `main()` 是否仅做编排
- 错误格式是否为 `mini-curl: error: <描述>`
- 退出码是否为 0/1/2
- method 推断规则是否与设计表一致

### 7.2 自动化检查

| 检查项 | 命令 | 首次执行切片 |
| --- | --- | --- |
| 格式检查 | `cargo fmt --check` | slice-001 起 |
| 静态检查 | `cargo clippy -- -D warnings` | slice-001 起 |
| 类型检查 | `cargo build` | slice-001 起 |
| 单元测试 | `cargo test` | slice-002 起 |
| 集成测试 | `cargo test --test '*'` | slice-006 |

## 8. 风险与偏差策略

### 8.1 风险项

| 风险 | 概率 | 影响 | 应对方式 |
| --- | --- | --- | --- |
| reqwest 异步模型增加 main 复杂度 | 高 | 低 | 使用 `#[tokio::main]` 宏 |
| header 解析边界情况多 | 中 | 中 | 首版仅校验包含 `:` 分隔符 |
| wiremock 版本兼容性 | 低 | 中 | 锁定具体版本 |
| 大响应体内存占用 | 低 | 低 | 首版接受，记录为已知限制 |

### 8.2 可接受偏差

| 偏差项 | 条件 | 记录要求 |
| --- | --- | --- |
| reqwest 默认重定向行为 | 不主动控制重定向 | 记录在 deviation.md |
| header 值中包含 `:` 的处理 | 仅按首个 `:` 分割 | 记录在 deviation.md |
| 响应体编码 | 使用 reqwest 默认 text() 解码 | 记录在 deviation.md |

## 9. 最终交付物

- 代码产出：`demo/mini-curl/` Rust crate（含 `src/` 下 6 个文件）
- 测试产出：`demo/mini-curl/tests/` 集成测试 + 各模块单元测试
- 文档产出：实现计划、切片文档、验证报告、追踪矩阵
- 报告产出：每个切片的验证报告 + 最终交付索引
