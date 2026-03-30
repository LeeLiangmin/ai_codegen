# design-to-plan

## 1. 目标

将结构化设计文档转换为可执行实现计划。

## 2. 输入

- normalized-design.md
- 项目仓库上下文

## 3. 执行动作

- 提取模块、接口、数据对象、规则、约束
- 识别依赖关系
- 生成实现 backlog
- 生成质量门禁要求

## 4. 输出

- implementation-plan.md
- backlog.md
- risks.md

## 5. 关键要求

计划必须可拆分为最小验证切片，且每个切片都具备明确验收标准。
