# Slice-006：集成测试与全量质量验证

## 1. 基本信息

- run_id: demo-mini-curl-run-001
- slice_id: slice-006
- title: 集成测试与全量质量验证
- priority: P2
- owner: AI
- status: pending

## 2. 切片目标

使用 wiremock 编写集成测试，覆盖核心功能场景，运行全量质量检查（fmt/clippy/test）。

## 3. 输入依据

- 设计章节：[`normalized § 10 验收标准`](demo/docs/design/mini-curl-design.normalized.md)、[`normalized § 12.2 推荐测试点`](demo/docs/design/mini-curl-design.normalized.md)
- 关联模块：全部
- 关联接口：全部
- 关联数据结构：全部
- 前置依赖：slice-005

## 4. 实现边界

### 4.1 允许修改范围

- 创建 `demo/mini-curl/tests/` 目录下的集成测试文件
- 可修改已有模块以修复测试发现的问题（需记录）

### 4.2 禁止修改范围

- 不得新增设计未声明的功能
- 不得删除已有单元测试

## 5. 预期产出

- `demo/mini-curl/tests/integration_test.rs`：wiremock 集成测试
- 验证报告

## 6. 验证要求

- `cargo fmt --check` 零差异
- `cargo clippy -- -D warnings` 零警告
- `cargo test` 全部通过
- 集成测试覆盖：
  - GET 请求并输出响应体
  - POST 请求并发送 body
  - 自定义 header 传递
  - 超时处理
  - 状态码输出（`--show-status`）
  - 响应头输出（`--include`）
  - 错误信息格式正确

## 7. 偏差与升级策略

### 7.1 允许记录偏差的条件

- wiremock 某些边界场景无法模拟时，可跳过并记录

### 7.2 必须升级人工处理的条件

- `cargo clippy -- -D warnings` 反复失败且无法自动修复
- 集成测试因 tokio runtime 问题不稳定

## 8. 完成定义

- [x] 集成测试文件已创建
- [x] 所有功能验收项已覆盖
- [x] `cargo fmt --check` 通过
- [x] `cargo clippy -- -D warnings` 通过
- [x] `cargo test` 全部通过
