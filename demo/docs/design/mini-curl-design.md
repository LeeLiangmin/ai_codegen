# Demo：Rust 小型 curl 工具设计文档

## 1. 文档元信息

- 项目名称：mini-curl
- 文档标题：Rust 小型 curl 命令行工具设计
- 版本：v0.1
- 作者：AI Toolkit Demo
- 日期：2026-03-30
- 状态：草稿
- 关联需求：在 demo 目录下验证设计驱动实现流程
- 关联 run：demo-mini-curl-run-001

## 2. 背景与目标

### 2.1 业务背景

需要在 [`demo/`](demo/) 下构建一个体量较小、边界清晰、适合作为 AI 设计驱动实现试验对象的 Rust CLI 程序。该程序模仿 [`curl`](demo/docs/design/mini-curl-design.md) 的最小子集，用于向 HTTP 服务发起请求并输出结果。

### 2.2 目标

实现一个可执行的 Rust 命令行工具，支持最小但完整的 HTTP 请求能力，便于验证以下流程：

- 设计文档能否驱动实现计划生成
- 实现是否能按切片逐步推进
- 自动化测试与结果沉淀是否能闭环

### 2.3 非目标

本项目首版不追求兼容完整 [`curl`](demo/docs/design/mini-curl-design.md) 功能，不包含以下内容：

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

首版需要支持：

- 通过命令行传入 URL
- 支持 GET 请求
- 支持 POST 请求
- 支持自定义请求头
- 支持字符串请求体
- 支持输出响应状态码
- 支持输出响应头
- 支持输出响应体
- 支持请求超时时间设置
- 具备基本错误处理
- 具备单元测试与最小集成测试

### 3.2 Out of Scope

首版暂不支持：

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

- CLI：命令行程序
- request：一次 HTTP 请求
- response：一次 HTTP 响应
- header：HTTP 请求头或响应头
- body：HTTP 消息体

### 4.2 全局约束

- 编程语言必须为 Rust
- 优先使用稳定版 Rust 生态
- 工程应可通过 [`cargo build`](demo/) 与 [`cargo test`](demo/)
- CLI 参数解析逻辑应与请求执行逻辑分离
- 网络请求逻辑应可测试，避免全部耦合在 [`main()`](demo/src/main.rs:1) 中
- 错误输出需对用户可理解
- 首版实现应优先保证可维护性，而非覆盖更多特性

## 5. 业务流程

### 5.1 主流程

1. 用户在命令行输入 URL 和可选参数。
2. 程序解析命令行参数。
3. 程序构造 HTTP 请求配置。
4. 程序发送请求并等待响应。
5. 程序按参数要求输出状态码、响应头和响应体。
6. 程序返回成功退出码。

### 5.2 异常流程

- 若 URL 缺失或格式非法，程序直接报错并退出。
- 若命令行参数格式错误，程序输出帮助信息并退出。
- 若请求超时，程序返回可识别错误信息。
- 若网络失败、DNS 失败或连接失败，程序返回错误信息。
- 若请求体与请求方法组合非法，程序应报错而非静默忽略。

## 6. 模块设计

### 6.1 cli 模块

- 模块职责：解析命令行参数并生成内部配置。
- 输入：命令行参数数组。
- 输出：运行配置对象。
- 依赖：参数解析库或标准库。
- 边界：不直接负责发送 HTTP 请求。
- 错误处理：返回结构化参数错误。
- 安全要求：避免执行任意命令或访问非预期资源。

### 6.2 request_builder 模块

- 模块职责：将运行配置转换为请求对象。
- 输入：运行配置对象。
- 输出：HTTP 请求构造参数。
- 依赖：HTTP 客户端库。
- 边界：不负责输出展示。
- 错误处理：处理 method/body/header 的组合约束。
- 安全要求：仅处理输入转换，不扩展额外行为。

### 6.3 http_client 模块

- 模块职责：执行 HTTP 请求并返回响应结果。
- 输入：标准化请求配置。
- 输出：响应结果对象。
- 依赖：Rust HTTP 客户端库。
- 边界：不负责 CLI 参数解析与终端展示。
- 错误处理：统一封装请求失败、超时、连接失败等错误。
- 安全要求：遵循超时限制，避免无界等待。

### 6.4 output 模块

- 模块职责：根据配置格式化输出。
- 输入：响应结果对象与输出选项。
- 输出：终端文本输出。
- 依赖：标准输出。
- 边界：不参与请求执行。
- 错误处理：输出阶段错误需明确报告。
- 安全要求：避免隐藏关键错误信息。

### 6.5 error 模块

- 模块职责：统一定义领域错误。
- 输入：各模块错误。
- 输出：统一错误类型与用户可读信息。
- 依赖：标准错误处理机制。
- 边界：不承担业务逻辑。
- 错误处理：负责错误归一化。
- 安全要求：不泄露不必要内部细节。

## 7. 数据设计

### 7.1 核心实体

- 实体名：AppConfig
  - 字段：url
  - 类型：String
  - 是否必填：是
  - 约束：必须为合法 URL
  - 备注：请求目标地址
  - 字段：method
  - 类型：String / Enum
  - 是否必填：否
  - 约束：默认 GET
  - 备注：请求方法
  - 字段：headers
  - 类型：Vec<(String, String)>
  - 是否必填：否
  - 约束：可为空
  - 备注：自定义请求头
  - 字段：body
  - 类型：Option<String>
  - 是否必填：否
  - 约束：GET 默认不允许有 body
  - 备注：请求体
  - 字段：timeout_secs
  - 类型：u64
  - 是否必填：否
  - 约束：默认 30
  - 备注：超时秒数
  - 字段：show_headers
  - 类型：bool
  - 是否必填：否
  - 约束：默认 false
  - 备注：是否输出响应头
  - 字段：show_status
  - 类型：bool
  - 是否必填：否
  - 约束：默认 false
  - 备注：是否输出状态码

- 实体名：HttpResult
  - 字段：status
  - 类型：u16
  - 是否必填：是
  - 约束：合法 HTTP 状态码
  - 备注：响应状态
  - 字段：headers
  - 类型：Vec<(String, String)>
  - 是否必填：是
  - 约束：可为空
  - 备注：响应头列表
  - 字段：body
  - 类型：String
  - 是否必填：是
  - 约束：允许为空字符串
  - 备注：响应内容

### 7.2 数据关系

[`cli`](demo/docs/design/mini-curl-design.md:77) 模块生成 [`AppConfig`](demo/docs/design/mini-curl-design.md:136)，[`request_builder`](demo/docs/design/mini-curl-design.md:89) 与 [`http_client`](demo/docs/design/mini-curl-design.md:101) 消费该配置，最终由 [`output`](demo/docs/design/mini-curl-design.md:113) 处理 [`HttpResult`](demo/docs/design/mini-curl-design.md:171)。

### 7.3 数据迁移需求

本项目不涉及持久化存储与数据库迁移。

## 8. 接口设计

### 8.1 命令行接口

- 目的：接收用户请求参数
- 方法：CLI Invocation
- 路径：mini-curl [OPTIONS] <URL>
- 请求参数：
  - `<URL>`：目标地址
  - `-X, --method <METHOD>`：请求方法
  - `-H, --header <HEADER>`：请求头，可重复
  - `-d, --data <BODY>`：请求体
  - `--timeout <SECONDS>`：超时时间
  - `-i, --include`：显示响应头
  - `-s, --show-status`：显示状态码
- 响应结构：终端文本输出
- 错误码：进程退出码，非 0 代表失败
- 幂等要求：GET 请求天然幂等，POST 不保证幂等
- 权限要求：普通用户可执行
- 限流要求：首版无内建限流

## 9. 状态与规则

### 9.1 状态机

请求执行状态可简化为：

`Initialized -> Parsed -> Built -> Sent -> Received -> Printed -> Exited`

失败时可进入：

`ParseFailed / BuildFailed / RequestFailed / OutputFailed`

### 9.2 核心业务规则

- 未显式指定 method 时默认使用 GET。
- 当指定 body 但未指定 method 时，可自动推断为 POST，或者直接报错；首版采用“自动推断为 POST”。
- header 参数支持重复传入。
- timeout 必须为正整数。
- 输出正文为默认行为；响应头和状态码由参数控制是否额外输出。
- 若请求失败，不输出伪造响应内容。

## 10. 验收标准

### 10.1 功能验收

- 能执行 GET 请求并输出响应体。
- 能执行 POST 请求并发送字符串 body。
- 能设置多个自定义 header。
- 能设置超时时间。
- 能输出状态码。
- 能输出响应头。
- 非法参数会给出可理解错误。

### 10.2 质量验收

- [`cargo fmt`](demo/) 可通过。
- [`cargo clippy`](demo/) 在合理范围内无严重警告。
- [`cargo test`](demo/) 可通过。
- 参数解析、请求构造、输出格式至少具备单元测试。

### 10.3 设计一致性要求

- 实现必须保持 [`cli`](demo/docs/design/mini-curl-design.md:77)、[`request_builder`](demo/docs/design/mini-curl-design.md:89)、[`http_client`](demo/docs/design/mini-curl-design.md:101)、[`output`](demo/docs/design/mini-curl-design.md:113)、[`error`](demo/docs/design/mini-curl-design.md:125) 模块边界。
- 不得把主要逻辑全部放入 [`main()`](demo/src/main.rs:1)。
- 不得超出本设计增加大量未声明特性。

## 11. 风险与待确认项

### 11.1 风险

- Rust HTTP 客户端的同步/异步选型会影响实现复杂度。
- CLI 框架选型可能影响参数定义简洁度。
- 网络相关测试若直接依赖外部网络，稳定性较差。

### 11.2 待确认项

- 首版是否采用同步阻塞式实现。
- 首版测试是否通过本地 mock server 实现。
- 是否接受 body 自动推断 method 为 POST 的规则。

## 12. AI 实施附录

### 12.1 实现切片建议

建议按以下切片推进：

1. 创建 Rust 工程骨架与基础错误类型。
2. 实现 CLI 参数解析与配置对象。
3. 实现请求构造与方法/body 规则。
4. 实现 HTTP 请求发送。
5. 实现输出格式化。
6. 补齐单元测试与最小集成测试。
7. 运行格式化、静态检查和测试。

### 12.2 推荐测试点

- 默认 method 为 GET
- 携带 body 时 method 推断为 POST
- header 可重复解析
- timeout 非法值报错
- 输出状态码/响应头开关生效
- 请求失败时错误信息可读

### 12.3 禁止事项

- 禁止首版直接引入完整 [`curl`](demo/docs/design/mini-curl-design.md) 兼容目标。
- 禁止在无设计支持下加入复杂认证、代理、重试等扩展。
- 禁止把网络请求逻辑与参数解析逻辑硬编码耦合。
