# 风险清单：mini-curl

## 1. 基本信息

- run_id: demo-mini-curl-run-001
- generated_from: [`mini-curl-implementation-plan.md`](demo/docs/implementation-plan/mini-curl-implementation-plan.md)
- generated_at: 2026-03-30

## 2. 风险矩阵

| # | 风险描述 | 概率 | 影响 | 关联切片 | 缓解措施 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | reqwest 异步模型增加 main 复杂度 | 高 | 低 | slice-001, slice-004 | 使用 `#[tokio::main]` 宏简化 | 已有缓解方案 |
| R-002 | header 解析边界情况多（值中含 `:`、空格、特殊字符） | 中 | 中 | slice-003 | 首版仅按首个 `:` 分割，记录偏差 | 已有缓解方案 |
| R-003 | wiremock 版本与 tokio 版本兼容性 | 低 | 中 | slice-006 | 锁定 `Cargo.toml` 中具体版本 | 已有缓解方案 |
| R-004 | 大响应体导致内存占用过高 | 低 | 低 | slice-004 | 首版接受，记录为已知限制 | 已接受 |
| R-005 | reqwest 默认重定向行为可能与用户预期不一致 | 低 | 低 | slice-004 | 首版不控制，记录为已知限制 | 已接受 |
| R-006 | 响应体编码非 UTF-8 时 `text()` 可能失败 | 低 | 中 | slice-004 | 首版使用 reqwest 默认解码，失败时返回错误 | 已有缓解方案 |

## 3. 升级条件

以下情况需要停止自动推进并升级人工处理：

- 任何风险的实际影响超出预期，导致切片无法在 2 次重试内通过验证
- 出现设计文档未覆盖的新需求或新约束
- `cargo build` 因依赖冲突无法通过

## 4. 风险监控点

| 监控时机 | 检查内容 |
| --- | --- |
| slice-001 完成后 | 确认 tokio + reqwest + clap 依赖可正常编译 |
| slice-003 完成后 | 确认 header 解析边界处理符合预期 |
| slice-004 完成后 | 确认错误分类覆盖超时、DNS、连接失败 |
| slice-006 完成后 | 确认 wiremock 测试稳定可重复 |
