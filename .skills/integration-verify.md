# integration-verify

## 1. 目标

对多个切片组合后的结果进行集成验证。

## 2. 输入

- 已通过验证的多个切片
- 集成场景定义

## 3. 检查项

- 关键业务流程是否闭环
- 模块之间接口是否一致
- 联调行为是否符合设计
- 关键回归场景是否通过

## 4. 输出

- integration-report.md
- regression-report.md
- unresolved-integration-issues.md

## 5. 判定规则

若关键链路失败，则不允许 close。
