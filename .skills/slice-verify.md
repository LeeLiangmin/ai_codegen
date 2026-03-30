# slice-verify

## 1. 目标

对单个切片执行设计一致性检查和自动化验证。

## 2. 输入

- slice 定义文档
- 代码改动
- 测试改动

## 3. 检查项

- 设计一致性
- 格式检查
- 静态检查
- 类型检查
- 单元测试
- 契约测试（如适用）

## 4. 输出

- verification-report.md
- failed-checks.md（如失败）
- remediation-suggestions.md（如失败）

## 5. 判定规则

通过后方可进入 curate；失败则回到 implement 或升级人工处理。
