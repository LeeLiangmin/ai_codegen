# Demo：Rust 小型 curl 工具设计文档（规范化版）

> 本文档由 [`design-normalize`](.skills/design-normalize.md) 阶段基于 [`mini-curl-design.md`](demo/docs/design/mini-curl-design.md) 与 [`intake-report.md`](demo/.runs/demo-mini-curl-run-001/reports/intake-report.md) 生成。所有待确认项已收敛为明确决策。

## 1. 文档元信息

- 项目名称：mini-curl
- 文档标题：Rust 小型 curl 命令行工具设计（规范化版）
- 版本：v0.2-normalized
- 作者：AI Toolkit Demo
- 日期：2026-03-30
- 状态：已规范化
- 关联需求：在 demo 目录下验证设计驱动实现流程
- 关联 run：demo-mini-curl-run-001
- 基线文档：[`demo/docs/design/mini-curl-design.md`](demo/docs/design/mini-curl-design.md)

## 2. 背景与目标

### 2.1 业务背景

在 [`demo/`](demo/) 下构建一个体量较小、边界清晰的 Rust CLI 程序，模仿 curl 的最小子集，用于向 HTTP 服务发起请求并输出结果。该项目同时作为 AI 设计驱动实现流程的验证载体。

### 2.2 目标

实现一个可执行的 Rust 命令行工具，支持最小但完整的 HTTP 请求能力：

- 设计文档能驱动实现计划生成
- 实现能按切片逐步推进
- 自动化测试与结果沉淀能闭环

### 2.3 非目标

本项目首版不包含：

- HTTP/2、HTTP/3 支持
- 文件上传下载进度展示
- 代理支持
- Cookie jar 管理
- TLS 高级参数配置
- 重定向链详细控制
- 并发请求
- 配置文件支持

## 3. 范围

### 3.1 In Scope

- 通过命令行传入 URL
- 支持 GET 请求
- 支持 POST 请求
- 支持自定义请求头（可重复）
- 支持字符串请求体
- 支持输出响应状态码
- 支持输出响应头
- 支持输出响应体
- 支持请求超时时间设置
- 具备基本错误处理
- 具备单元测试与最小集成测试

### 3.2 Out of Scope

- PUT、DELETE、PATCH 等更多方法
- 文件上传
- 流式下载到文件
- 自动重定向控制
- 认证机制
- 重试机制
- 彩色输出
- 复杂格式化输出

## 4. 术语与约束

### 4.1 术语定义

| 术语 | 定义 |
| --- | --- |
| CLI | 命令行程序 |
| request | 一次 HTTP 请求 |
| response | 一次 HTTP 响应 |
| header | HTTP 请求头或响应头，格式为 `Name: Value` |
| body | HTTP 消息体 |
| method | HTTP 请求方法，首版仅支持 GET 和 POST |
| timeout | 请求超时时间，单位为秒 |

### 4.2 全局约束

- 编程语言：Rust（stable toolchain）
- 构建工具：Cargo
- 工程必须可通过 `cargo build`、`cargo test`、`cargo fmt --check`、`cargo clippy`
- CLI 参数解析逻辑必须与请求执行逻辑分离
- 网络请求逻辑必须可测试，禁止全部耦合在 `main()` 中
- 错误输出必须对用户可理解
- 首版优先保证可维护性，而非覆盖更多特性

### 4.3 技术选型决策（normalize 阶段收敛）

| 决策项 | 决策结果 | 理由 |
| --- | --- | --- |
| 同步/异步模型 | 采用异步模型（tokio + reqwest） | reqwest 是 Rust 生态最成熟的 HTTP 客户端，默认异步；tokio 是事实标准运行时 |
| CLI 参数解析库 | clap（derive 模式） | 社区最广泛使用，derive 模式代码简洁，与结构体天然映射 |
| HTTP 客户端库 | reqwest | 成熟、文档完善、支持超时、header 等所有首版需求 |
| 集成测试方案 | wiremock（Rust mock server 库） | 可在测试中启动本地 mock HTTP server，无需依赖外部网络 |
| body 自动推断规则 | 保留：当指定 body 但未指定 method 时自动推断为 POST | 符合 curl 行为习惯，降低用户使用门槛 |
| method 白名单 | 首版仅允许 GET 和 POST | 与 In Scope 一致，避免实现泛化 |
| clippy 判定口径 | `cargo clippy -- -D warnings` 零警告通过 | 明确可执行标准 |
| 错误输出格式 | `mini-curl: error: <可读描述>` 格式输出到 stderr | 统一格式，便于验证 |
| 退出码策略 | 0=成功，1=参数错误，2=网络/请求错误 | 简单明确，可测试 |

## 5. 业务流程

### 5.1 主流程

1. 用户在命令行输入 URL 和可选参数
2. 程序使用 clap 解析命令行参数，生成 `AppConfig`
3. 程序基于 `AppConfig` 构造 reqwest 请求
4. 程序发送请求并等待响应（受 timeout 限制）
5. 程序按参数要求输出状态码、响应头和响应体
6. 程序返回退出码 0

### 5.2 异常流程

| 异常场景 | 处理方式 | 退出码 |
| --- | --- | --- |
| URL 缺失 | clap 自动报错并输出帮助信息 | 1 |
| URL 格式非法 | 输出 `mini-curl: error: invalid URL: <url>` | 1 |
| 命令行参数格式错误 | clap 自动报错并输出帮助信息 | 1 |
| method 不在白名单 | 输出 `mini-curl: error: unsupported method: <method>` | 1 |
| timeout 非正整数 | 输出 `mini-curl: error: invalid timeout value: <value>` | 1 |
| GET 请求显式携带 body | 输出 `mini-curl: error: GET request must not have a body` | 1 |
| 请求超时 | 输出 `mini-curl: error: request timed out` | 2 |
| DNS 解析失败 | 输出 `mini-curl: error: failed to resolve host: <host>` | 2 |
| 连接失败 | 输出 `mini-curl: error: connection failed: <detail>` | 2 |
| 其他网络错误 | 输出 `mini-curl: error: request failed: <detail>` | 2 |

## 6. 模块设计

### 6.1 cli 模块

- 模块职责：使用 clap derive 模式解析命令行参数，生成 `AppConfig`
- 输入：`std::env::args()`
- 输出：`Result<AppConfig, AppError>`
- 依赖：clap
- 边界：不直接发送 HTTP 请求，不格式化输出
- 错误处理：参数校验失败返回 `AppError::InvalidArgs`
- 安全要求：不执行任意命令

### 6.2 request_builder 模块

- 模块职责：将 `AppConfig` 转换为 reqwest 请求配置
- 输入：`&AppConfig`
- 输出：`Result<reqwest::RequestBuilder, AppError>`
- 依赖：reqwest
- 边界：不负责输出展示，不负责实际发送
- 错误处理：
  - method 不在白名单 → `AppError::InvalidArgs`
  - GET + body 冲突 → `AppError::InvalidArgs`
  - header 格式非法 → `AppError::InvalidArgs`
- 安全要求：仅处理输入转换

### 6.3 http_client 模块

- 模块职责：执行 HTTP 请求并返回 `HttpResult`
- 输入：`reqwest::RequestBuilder`，timeout 配置
- 输出：`Result<HttpResult, AppError>`
- 依赖：reqwest, tokio
- 边界：不负责 CLI 解析与终端展示
- 错误处理：
  - 超时 → `AppError::Timeout`
  - DNS 失败 → `AppError::DnsError`
  - 连接失败 → `AppError::ConnectionError`
  - 其他 → `AppError::RequestError`
- 安全要求：遵循超时限制，避免无界等待

### 6.4 output 模块

- 模块职责：根据 `AppConfig` 中的输出选项格式化并打印响应
- 输入：`&HttpResult`，`&AppConfig`
- 输出：写入 stdout（正文）和 stderr（错误）
- 依赖：std::io
- 边界：不参与请求执行
- 错误处理：IO 写入失败返回 `AppError::OutputError`
- 输出规则：
  - 若 `show_status` 为 true，先输出 `HTTP <status_code>`
  - 若 `show_headers` 为 true，逐行输出 `<name>: <value>`，后跟空行
  - 始终输出 body

### 6.5 error 模块

- 模块职责：统一定义领域错误枚举 `AppError`
- 错误变体：

| 变体 | 含义 | 退出码 |
| --- | --- | --- |
| `InvalidArgs(String)` | 参数错误 | 1 |
| `Timeout` | 请求超时 | 2 |
| `DnsError(String)` | DNS 解析失败 | 2 |
| `ConnectionError(String)` | 连接失败 | 2 |
| `RequestError(String)` | 其他请求错误 | 2 |
| `OutputError(String)` | 输出写入失败 | 2 |

- 必须实现 `Display` trait，输出格式为 `mini-curl: error: <描述>`
- 必须提供 `fn exit_code(&self) -> i32` 方法

## 7. 数据设计

### 7.1 核心实体

#### AppConfig

| 字段 | 类型 | 必填 | 默认值 | 约束 | 备注 |
| --- | --- | --- | --- | --- | --- |
| url | `String` | 是 | - | 必须为合法 URL | 请求目标地址 |
| method | `Option<String>` | 否 | `None` | 仅允许 GET/POST | 未指定时按规则推断 |
| headers | `Vec<String>` | 否 | `[]` | 格式为 `Name: Value` | 自定义请求头，可重复 |
| body | `Option<String>` | 否 | `None` | GET 时不允许有 body | 请求体 |
| timeout_secs | `u64` | 否 | `30` | 必须为正整数 | 超时秒数 |
| show_headers | `bool` | 否 | `false` | - | 是否输出响应头 |
| show_status | `bool` | 否 | `false` | - | 是否输出状态码 |

#### HttpResult

| 字段 | 类型 | 必填 | 约束 | 备注 |
| --- | --- | --- | --- | --- |
| status | `u16` | 是 | 合法 HTTP 状态码 | 响应状态 |
| headers | `Vec<(String, String)>` | 是 | 可为空 | 响应头列表 |
| body | `String` | 是 | 允许为空字符串 | 响应内容 |

### 7.2 数据流

```
CLI args → [cli] → AppConfig → [request_builder] → RequestBuilder
                                                         ↓
                                                    [http_client]
                                                         ↓
stdout ← [output] ← HttpResult
```

### 7.3 Method 推断规则

| 用户指定 method | 用户指定 body | 最终 method | 说明 |
| --- | --- | --- | --- |
| 未指定 | 未指定 | GET | 默认行为 |
| 未指定 | 已指定 | POST | 自动推断 |
| GET | 未指定 | GET | 正常 |
| GET | 已指定 | **报错** | GET 不允许 body |
| POST | 未指定 | POST | 正常，body 为空 |
| POST | 已指定 | POST | 正常 |

### 7.4 数据迁移需求

本项目不涉及持久化存储与数据库迁移。

## 8. 接口设计

### 8.1 命令行接口

```
mini-curl [OPTIONS] <URL>
```

| 参数 | 短选项 | 长选项 | 类型 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| URL | - | - | positional | 是 | - | 目标地址 |
| method | `-X` | `--method` | String | 否 | 按规则推断 | 仅允许 GET/POST |
| header | `-H` | `--header` | String（可重复） | 否 | - | 格式 `Name: Value` |
| data | `-d` | `--data` | String | 否 | - | 请求体 |
| timeout | - | `--timeout` | u64 | 否 | 30 | 超时秒数 |
| include | `-i` | `--include` | flag | 否 | false | 显示响应头 |
| show-status | `-s` | `--show-status` | flag | 否 | false | 显示状态码 |

### 8.2 输出格式

正常输出到 stdout：

```
HTTP 200                    ← 仅当 --show-status
content-type: text/html     ← 仅当 --include
content-length: 1234        ← 仅当 --include
                            ← 仅当 --include（空行分隔）
<response body>             ← 始终输出
```

错误输出到 stderr：

```
mini-curl: error: <描述>
```

### 8.3 退出码

| 退出码 | 含义 |
| --- | --- |
| 0 | 成功 |
| 1 | 参数错误 |
| 2 | 网络/请求错误 |

## 9. 状态与规则

### 9.1 请求执行状态

```
Initialized → Parsed → Built → Sent → Received → Printed → Exited(0)
     ↓           ↓        ↓       ↓         ↓          ↓
  ParseFailed BuildFailed  RequestFailed  OutputFailed
     → Exited(1)  → Exited(1)  → Exited(2)    → Exited(2)
```

### 9.2 核心业务规则

1. 未显式指定 method 时默认使用 GET
2. 当指定 body 但未指定 method 时自动推断为 POST
3. 显式指定 GET 且携带 body 时报错
4. header 参数支持重复传入，每个 `-H` 对应一个 header
5. header 格式必须包含 `:` 分隔符
6. timeout 必须为正整数（>0）
7. 输出正文为默认行为；响应头和状态码由参数控制
8. 请求失败时不输出伪造响应内容
9. 首版 method 白名单仅为 GET 和 POST

## 10. 验收标准

### 10.1 功能验收

| 验收项 | 验证方式 |
| --- | --- |
| 能执行 GET 请求并输出响应体 | 单元测试 + wiremock 集成测试 |
| 能执行 POST 请求并发送字符串 body | 单元测试 + wiremock 集成测试 |
| 能设置多个自定义 header | 单元测试 |
| 能设置超时时间 | 单元测试 + wiremock 延迟测试 |
| 能输出状态码 | 单元测试 |
| 能输出响应头 | 单元测试 |
| 非法参数给出可理解错误 | 单元测试 |
| body 自动推断 POST | 单元测试 |
| GET + body 报错 | 单元测试 |

### 10.2 质量验收

| 检查项 | 命令 | 通过标准 |
| --- | --- | --- |
| 格式检查 | `cargo fmt --check` | 零差异 |
| 静态检查 | `cargo clippy -- -D warnings` | 零警告 |
| 编译检查 | `cargo build` | 零错误 |
| 测试检查 | `cargo test` | 全部通过 |

### 10.3 设计一致性要求

- 实现必须保持 `cli`、`request_builder`、`http_client`、`output`、`error` 五个模块边界
- `main()` 仅负责调用各模块并处理退出码，不包含业务逻辑
- 不得超出本设计增加未声明特性
- 错误输出必须遵循 `mini-curl: error: <描述>` 格式

## 11. 风险与待确认项

### 11.1 风险

| 风险 | 影响 | 缓解措施 |
| --- | --- | --- |
| reqwest 异步模型增加复杂度 | main 需要 tokio runtime | 使用 `#[tokio::main]` 宏简化 |
| wiremock 测试启动耗时 | CI 可能变慢 | 首版可接受，后续优化 |
| 大响应体内存占用 | 可能 OOM | 首版不处理，记录为已知限制 |

### 11.2 已知限制（首版接受）

- 响应体完全加载到内存，不支持流式处理
- 不支持 HTTPS 证书自定义
- 不支持重定向跟随控制（使用 reqwest 默认行为）

### 11.3 待确认项

所有原始待确认项已在本 normalize 阶段收敛，当前无未决项。

## 12. AI 实施附录

### 12.1 实现切片建议

| 切片 | 目标 | 依赖 |
| --- | --- | --- |
| slice-001 | 创建 Rust crate 骨架、定义 `AppError` 枚举、建立模块文件结构 | 无 |
| slice-002 | 实现 `cli` 模块：clap derive 定义 + `AppConfig` 生成 + method 推断规则 | slice-001 |
| slice-003 | 实现 `request_builder` 模块：AppConfig → reqwest::RequestBuilder | slice-002 |
| slice-004 | 实现 `http_client` 模块：发送请求、超时处理、错误分类 | slice-003 |
| slice-005 | 实现 `output` 模块：格式化输出状态码、响应头、响应体 | slice-004 |
| slice-006 | 补齐单元测试 + wiremock 集成测试 + 运行 fmt/clippy/test | slice-005 |

### 12.2 推荐测试点

- 默认 method 为 GET
- 携带 body 时 method 推断为 POST
- 显式 GET + body 报错
- header 可重复解析
- header 格式校验
- timeout 非法值报错
- 输出状态码/响应头开关生效
- 请求失败时错误信息格式正确
- 退出码与错误类型匹配

### 12.3 Cargo.toml 依赖建议

```toml
[dependencies]
clap = { version = "4", features = ["derive"] }
reqwest = { version = "0.12", features = ["blocking"] }
tokio = { version = "1", features = ["full"] }

[dev-dependencies]
wiremock = "0.6"
tokio = { version = "1", features = ["full"] }
```

### 12.4 禁止事项

- 禁止首版引入完整 curl 兼容目标
- 禁止在无设计支持下加入认证、代理、重试等扩展
- 禁止把网络请求逻辑与参数解析逻辑硬编码耦合
- 禁止在 `main()` 中放置业务逻辑
- 禁止使用 `unwrap()` / `expect()` 处理可恢复错误
