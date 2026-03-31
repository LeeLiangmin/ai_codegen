# Slice Index：demo-mini-curl-run-001

## 1. 基本信息

- run_id: demo-mini-curl-run-001
- generated_from: [`mini-curl-implementation-plan.md`](demo/docs/implementation-plan/mini-curl-implementation-plan.md)
- total_slices: 6
- generated_at: 2026-03-30

## 2. 切片总览

| slice_id | title | priority | dependency | status |
| --- | --- | --- | --- | --- |
| [slice-001](demo/.runs/demo-mini-curl-run-001/slices/slice-001.md) | Rust crate 骨架与 AppError 枚举 | P0 | 无 | pending |
| [slice-002](demo/.runs/demo-mini-curl-run-001/slices/slice-002.md) | CLI 参数解析与 AppConfig | P0 | slice-001 | pending |
| [slice-003](demo/.runs/demo-mini-curl-run-001/slices/slice-003.md) | 请求构造 request_builder | P1 | slice-002 | pending |
| [slice-004](demo/.runs/demo-mini-curl-run-001/slices/slice-004.md) | HTTP 请求发送 http_client | P1 | slice-003 | pending |
| [slice-005](demo/.runs/demo-mini-curl-run-001/slices/slice-005.md) | 输出格式化与 main 编排 | P2 | slice-004 | pending |
| [slice-006](demo/.runs/demo-mini-curl-run-001/slices/slice-006.md) | 集成测试与全量质量验证 | P2 | slice-005 | pending |

## 3. 依赖图

```
slice-001 → slice-002 → slice-003 → slice-004 → slice-005 → slice-006
```

所有切片为线性依赖，无并行执行可能。

## 4. 并行性说明

首版切片全部为串行依赖。后续如果需要加速，可考虑将 slice-005（output）与 slice-004（http_client）并行，因为 output 模块仅依赖 `HttpResult` 结构体定义而非 http_client 实现。
