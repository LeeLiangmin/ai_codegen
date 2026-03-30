# Intake Report：demo-mini-curl-run-001

## 1. 输入信息

- skill：[`design-intake`](.skills/design-intake.md)
- 设计文档：[`demo/docs/design/mini-curl-design.md`](demo/docs/design/mini-curl-design.md)
- run：[`demo-mini-curl-run-001`](demo/.runs/demo-mini-curl-run-001/state.md)
- 检查时间：2026-03-30

## 2. 检查结论

结论：**允许进入 normalize 阶段**

原因：

- 已包含目标、非目标、范围、模块设计、数据设计、接口设计、验收标准与 AI 实施边界。
- 已具备将设计转为实现计划所需的基本结构。
- 存在少量需要收敛的实现决策，但不构成阻塞性缺失。

## 3. 按检查项逐项评估

### 3.1 是否包含目标、范围、模块设计、接口设计、数据设计、验收标准

结果：**通过**

证据：

- 目标与非目标见 [`demo/docs/design/mini-curl-design.md:20`](demo/docs/design/mini-curl-design.md:20) 与 [`demo/docs/design/mini-curl-design.md:28`](demo/docs/design/mini-curl-design.md:28)
- 范围见 [`demo/docs/design/mini-curl-design.md:41`](demo/docs/design/mini-curl-design.md:41)
- 模块设计见 [`demo/docs/design/mini-curl-design.md:111`](demo/docs/design/mini-curl-design.md:111)
- 数据设计见 [`demo/docs/design/mini-curl-design.md:163`](demo/docs/design/mini-curl-design.md:163)
- 接口设计见 [`demo/docs/design/mini-curl-design.md:229`](demo/docs/design/mini-curl-design.md:229)
- 验收标准见 [`demo/docs/design/mini-curl-design.md:271`](demo/docs/design/mini-curl-design.md:271)

### 3.2 是否存在明显冲突或缺失

结果：**部分通过**

发现的问题：

1. [`AppConfig`](demo/docs/design/mini-curl-design.md:167) 中声明“GET 默认不允许有 body”，但在规则部分又声明“当指定 body 但未指定 method 时自动推断为 POST”，两者虽不直接冲突，但需要在 normalize 阶段明确优先级与实现方式。
2. CLI 接口当前只列出 [`GET`](demo/docs/design/mini-curl-design.md:48) / [`POST`](demo/docs/design/mini-curl-design.md:49) 需求，但 [`--method`](demo/docs/design/mini-curl-design.md:238) 参数描述本身对 method 值没有限制，需明确首版是否仅允许这两种方法。
3. 设计中要求最小集成测试，但未明确采用何种测试机制，例如本地 mock server、内嵌测试服务器或外部服务。

### 3.3 是否存在无法落地的模糊表述

结果：**部分通过**

主要模糊项：

- [`Rust HTTP 客户端库`](demo/docs/design/mini-curl-design.md:138) 尚未明确，影响同步/异步模型与测试方式。
- [`参数解析库或标准库`](demo/docs/design/mini-curl-design.md:118) 尚未明确，影响 CLI 定义方式。
- [`cargo clippy`](demo/docs/design/mini-curl-design.md:286) “合理范围内无严重警告”缺乏更明确的判定口径。
- “错误输出需对用户可理解”见 [`demo/docs/design/mini-curl-design.md:89`](demo/docs/design/mini-curl-design.md:89)，但未定义错误输出格式规范。

### 3.4 是否缺少 AI 实施边界说明

结果：**通过**

证据：

- AI 实施附录存在于 [`demo/docs/design/mini-curl-design.md:310`](demo/docs/design/mini-curl-design.md:310)
- 禁止事项存在于 [`demo/docs/design/mini-curl-design.md:333`](demo/docs/design/mini-curl-design.md:333)
- 模块边界存在于 [`demo/docs/design/mini-curl-design.md:292`](demo/docs/design/mini-curl-design.md:292)

## 4. 缺失项清单

当前无阻塞性的关键章节缺失，但存在以下需要补齐或收敛的项：

1. 明确 HTTP 客户端选型，例如 [`reqwest`](demo/docs/design/mini-curl-design.md:138)
2. 明确 CLI 参数解析选型，例如 [`clap`](demo/docs/design/mini-curl-design.md:118)
3. 明确集成测试机制与 mock server 方案
4. 明确首版允许的 method 白名单
5. 明确错误输出格式与退出码策略
6. 明确 [`cargo clippy`](demo/docs/design/mini-curl-design.md:286) 的判定口径

## 5. 风险项清单

1. 若同步/异步模型不先确定，后续模块边界可能重构。
2. 若测试方案不先确定，[`http_client`](demo/docs/design/mini-curl-design.md:133) 模块的可测试性容易退化。
3. 若 method 范围不收敛，CLI 和 request builder 实现会提前泛化。
4. 若错误规范不统一，后续验证与用户体验检查难以稳定执行。

## 6. 推荐进入 normalize 时必须完成的收敛决策

1. 采用同步阻塞式实现还是异步实现。
2. 选择 CLI 库与 HTTP 客户端库。
3. 选择测试框架与本地 mock server 方案。
4. 确认 body 自动推断为 POST 是否保留。
5. 确认首版 method 白名单仅为 GET/POST。

## 7. Intake 最终判定

- 是否允许进入 normalize：**yes**
- 是否建议立即进入实现：**no**
- 推荐下一步：先生成规范化设计稿，再进入 [`design-to-plan`](.skills/design-to-plan.md)
