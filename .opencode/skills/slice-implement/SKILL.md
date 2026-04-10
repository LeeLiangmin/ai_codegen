---
name: slice-implement
description: Use when one slice is clearly defined and you need to implement only that slice, inside its allowed boundary, with the smallest necessary code and test changes — using TDD inner loop and language quality checks
---

# slice-implement

## Overview

`slice-implement` 是核心闭环中的执行步。

它的职责被压缩为一句话：**只实现一个切片，不扩张范围，不顺手解决其他问题。**

实现顺序推荐使用 **TDD 内循环**（Red → Green → Refactor），在实现步骤内部即获得快速反馈，而不是等到验证步骤才发现问题。Refactor 阶段同时负责运行语言质量检查工具并修复问题。

与旧体系相比，本版本删除了大量额外治理要求：
- 不要求生成复杂实现说明文档
- 不默认生成偏差报告文件
- 不承担全局流程推进职责
- 不维护复杂切片总表

它关注的唯一目标是：让当前切片进入"可验证"状态。

---

## When to Use

在以下场景使用：

- 已存在一个清晰的切片定义
- 切片边界已明确
- 当前切片前置依赖已满足，或无依赖
- 准备进行最小实现并随后交给 [slice-verify/SKILL.md](../slice-verify/SKILL.md)

通常来源于 [design-to-slices/SKILL.md](../design-to-slices/SKILL.md) 输出的单切片文件。

---

## Input

| 输入项 | 必填 | 说明 |
|---|---|---|
| 切片定义 | 是 | 当前切片的目标、边界、依赖、验证方式 |
| 设计文档 | 建议 | 用于核对接口、数据结构、命名与约束 |
| 现有代码上下文 | 是 | 理解当前仓库结构与允许修改的文件 |
| 会话状态 | 否 | 用于确认当前切片与阻塞信息 |

---

## Procedure

1. **读取当前切片定义**
   先明确以下内容：
   - `objective`
   - `depends_on`
   - `allowed_changes`
   - `forbidden_changes`
   - `expected_outputs`
   - `verification`（含 `criteria` 和可选 `test_sketch`）

2. **确认依赖是否满足**
   如果切片有直接依赖，只检查直接前置项：
   - 前置切片是否已完成并通过验证
   - 如果未满足，则停止，不进入实现

3. **确认修改边界**
   在编码前明确：
   - 哪些文件/目录允许修改
   - 哪些文件/目录明确禁止修改
   - 是否允许新增测试

4. **执行最小实现（TDD 内循环）**

   a. **判断是否有可操作的测试目标**
      - 如果当前切片有明确的行为预期（接口、逻辑、数据处理），进入 TDD 流程（步骤 b）
      - 如果当前切片无可操作的测试目标（纯配置、目录结构、文档模板），直接进入步骤 c 的实现部分

   b. **先写测试**（Red）
      - 根据切片 `verification.criteria` 编写最小失败测试
      - 如切片定义中有 `verification.test_sketch`，以此为骨架
      - 测试只覆盖当前切片目标，不扩张
      - 运行测试，确认失败（Red 状态确认）

   c. **再写实现**（Green）
      - 编写刚好让测试通过的最少业务代码
      - 运行测试，确认通过
      - 不添加测试未覆盖的额外功能

   d. **整理与质量检查**（Refactor）
      在测试通过的基础上，执行当前语言/项目的标准质量检查：

      i. 运行项目配置的质量检查工具（见下方"语言质量检查工具参考"）
      ii. 修复所有可自动修复的问题（如格式、简单 lint 警告）
      iii. 对于需要判断的问题（如设计层面的 clippy 建议），在不改变行为的前提下修复，或记录为已知并说明理由
      iv. 修复后重新运行测试，确认行为未变

      原则：
      - 质量检查修复属于当前切片的职责，不算"范围扩张"
      - 只修复当前切片改动范围内的质量问题，不顺手修复无关文件
      - 如果质量问题涉及切片边界外的代码，记录但不修复

5. **避免范围扩张**
   实现过程中若发现以下情况，默认停止并记录为阻塞，而不是顺手继续：
   - 需要跨多个无关模块大改
   - 需要改变切片未授权的接口契约
   - 需要修复与当前切片无关的问题
   - 需要补做新的设计决策

6. **准备交付验证**
   完成后，确保当前切片已具备进入 [slice-verify/SKILL.md](../slice-verify/SKILL.md) 的最小条件：
   - 代码可读
   - 改动集中
   - 测试已编写且在本地通过（TDD Green 已确认）
   - 质量检查已通过（Refactor 已确认）
   - 未越界修改

7. **最小状态更新（如使用会话状态）**
   如存在 `state.md`，只更新必要信息，例如：
   - `current_slice`
   - `status` 保持 `active`
   - 不写复杂阶段迁移

---

## Output

### 必需输出

- 当前切片边界内的代码改动
- 当前切片所需的最小测试改动

### 可选输出

如果确实出现阻塞或必要说明，可在会话目录中增加轻量记录，例如：
- `.workflow/session/summary.md`
- `.workflow/session/slices/slice-<NNN>-notes.md`

但这些都不是默认要求。

---

## 语言质量检查工具参考

根据项目语言选择对应的质量检查工具链。以下为常见语言的推荐配置：

### Rust

| 检查类型 | 工具 | 命令 | 修复方式 |
|---|---|---|---|
| 编译检查 | `cargo check` | `cargo check` | 修复编译错误 |
| 静态分析 | `clippy` | `cargo clippy -- -D warnings` | `cargo clippy --fix` 或手动修复 |
| 格式化 | `rustfmt` | `cargo fmt --check` | `cargo fmt` |
| 测试 | `cargo test` | `cargo test` | 修复失败测试 |

### TypeScript / JavaScript

| 检查类型 | 工具 | 命令 | 修复方式 |
|---|---|---|---|
| 类型检查 | `tsc` | `npx tsc --noEmit` | 修复类型错误 |
| 静态分析 | `eslint` | `npx eslint .` | `npx eslint . --fix` |
| 格式化 | `prettier` | `npx prettier --check .` | `npx prettier --write .` |
| 测试 | `jest` / `vitest` | `npx jest` / `npx vitest run` | 修复失败测试 |

### Python

| 检查类型 | 工具 | 命令 | 修复方式 |
|---|---|---|---|
| 类型检查 | `mypy` | `mypy .` | 修复类型错误 |
| 静态分析 | `ruff` | `ruff check .` | `ruff check . --fix` |
| 格式化 | `ruff format` | `ruff format --check .` | `ruff format .` |
| 测试 | `pytest` | `pytest` | 修复失败测试 |

### Go

| 检查类型 | 工具 | 命令 | 修复方式 |
|---|---|---|---|
| 编译检查 | `go build` | `go build ./...` | 修复编译错误 |
| 静态分析 | `go vet` + `staticcheck` | `go vet ./...` | 手动修复 |
| 格式化 | `gofmt` | `gofmt -l .` | `gofmt -w .` |
| 测试 | `go test` | `go test ./...` | 修复失败测试 |

> 以上为参考配置。实际使用时以项目已有的工具链配置为准（如 Makefile、CI 配置、package.json scripts 等）。如果项目已定义质量检查命令，优先使用项目定义的命令。

---

## Quality Gate

- [ ] 只实现了一个切片
- [ ] 所有改动都落在允许范围内
- [ ] 未修改禁止修改区域
- [ ] 当前切片相关测试已编写且通过（或该切片无可操作测试目标）
- [ ] 语言质量检查已通过（lint / format / type check）
- [ ] 未引入明显与当前切片无关的扩展功能
- [ ] 已具备进入 [slice-verify/SKILL.md](../slice-verify/SKILL.md) 的条件

---

## Failure Handling

| 场景 | 处理方式 |
|---|---|
| 前置依赖未满足 | 停止实现，等待依赖切片完成 |
| 需要跨边界修改 | 停止实现，回到切片定义重新拆分或调整边界 |
| 设计与代码现状冲突 | 记录冲突，优先保持切片边界，不擅自扩张任务 |
| 当前切片过大 | 暂停实现，回到 [design-to-slices/SKILL.md](../design-to-slices/SKILL.md) 继续拆小 |
| 实现中出现额外问题 | 仅记录，不自动顺手修复无关问题 |
| 质量检查发现边界外问题 | 记录但不修复，只处理当前切片范围内的问题 |

---

## Non-Goals

以下内容不属于本 skill：

- 不验证切片是否通过（由 slice-verify 独立复核）
- 不运行全局集成验证
- 不生成复杂偏差文档
- 不维护全局流程状态机
- 不整理最终交付索引

当前切片实现完成后，下一步应进入 [slice-verify/SKILL.md](../slice-verify/SKILL.md)。
