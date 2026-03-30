# plan-to-slices

## 1. 目标

将实现计划拆分为可独立执行和验证的切片任务。

## 2. 输入

- implementation-plan.md
- backlog.md

## 3. 执行动作

- 按模块边界和依赖关系切片
- 为每个切片定义输入、产出、验证方式
- 标注并行性与阻塞条件

## 4. 输出

- slices/index.md
- slices/<slice-id>.md

## 5. 关键要求

切片必须足够小，能够在一次实现-验证闭环中完成。
