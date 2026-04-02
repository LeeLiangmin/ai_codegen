---
name: slice-verify
description: Use when one slice has been implemented and you need the smallest reliable verification loop: check design alignment, run the necessary automated checks, and return a single pass/fail result with the next action
---

# slice-verify

## Overview

`slice-verify` 是核心闭环中的验证步。

它的职责也被压缩到最小：**验证一个切片是否通过，不负责验证整个项目。**

与旧版本相比，它不再默认追求厚重验证报告，而是以最小可靠结论为目标：
- 当前切片是否符合设计与边界
- 当前切片的必要自动化检查是否通过
- 下一步是继续、修复，还是阻塞

---

## When to Use

在以下场景使用：

- 一个切片已完成实现
- 需要对当前切片做局部验证
- 需要为是否进入下一个切片提供明确判断

它通常发生在 [slice-implement/SKILL.md](../slice-implement/SKILL.md) 之后。

---

## Input

| 输入项 | 必填 | 说明 |
|---|---|---|
| 当前切片定义 | 是 | 当前切片的目标、边界、验证方式 |
| 当前代码改动 | 是 | 本切片的实际改动范围 |
| 设计文档 | 建议 | 用于核对接口、结构、命名和约束 |
| 测试改动 | 否 | 当前切片对应的新增或修改测试 |
| 会话状态 | 否 | 用于读取当前切片与最近状态 |

---

## Procedure

1. **读取切片定义**
   明确：
   - 当前切片目标
   - 允许修改范围
   - 禁止修改范围
   - 验证要求

2. **检查边界一致性**
   先判断当前改动是否仍在切片边界内：
   - 是否修改了未授权区域
   - 是否新增了与切片无关的功能
   - 是否偏离了切片的单一目标

3. **检查设计一致性**
   根据设计文档和切片定义，检查：
   - 接口签名是否一致
   - 数据结构是否一致
   - 命名和行为是否与目标一致
   - 是否遗漏切片要求中的关键行为

4. **执行最小必要自动化检查**
   只运行当前切片所需、且项目上下文允许的检查，例如：
   - 格式检查
   - lint
   - 类型检查 / 编译
   - 当前切片相关测试

   原则是：
   - 优先局部检查
   - 必要时再扩大到更广范围
   - 不默认把“全仓全量检查”作为首选

5. **汇总为单一结论**
   只给出以下三种结论之一：
   - `pass`：当前切片可视为完成
   - `fail`：需要回到 [slice-implement/SKILL.md](../slice-implement/SKILL.md) 修复
   - `blocked`：存在无法在当前切片内解决的问题

6. **给出单一下一步动作**
   输出时只给一个下一步：
   - 继续下一个切片
   - 回到当前切片修复
   - 回到切片定义重新拆分或调整边界

7. **按需写入轻量结果**
   如使用会话目录，可写入：
   - `.workflow/session/verify/slice-<NNN>-verify.md`

   但只记录最小信息，不展开为厚报告。

---

## Output

### 最小输出

- `slice_id`
- `boundary_check`
- `design_alignment`
- `automated_checks`
- `result`
- `next_step`

### 建议文件输出

- `.workflow/session/verify/slice-<NNN>-verify.md`

建议结构：

```markdown
# Slice Verify

- slice_id: slice-001
- boundary_check: pass | fail
- design_alignment: pass | fail
- automated_checks: pass | fail | partial
- result: pass | fail | blocked
- next_step: <...>

## Notes
- ...
```

---

## Quality Gate

- [ ] 已检查当前改动是否越界
- [ ] 已检查当前实现是否符合切片目标
- [ ] 已执行最小必要自动化检查
- [ ] 已给出唯一明确结论：`pass` / `fail` / `blocked`
- [ ] 已给出唯一明确下一步动作

---

## Failure Handling

| 场景 | 处理方式 |
|---|---|
| 越界修改 | 判定为 `fail`，回到 [slice-implement/SKILL.md](../slice-implement/SKILL.md) 收缩改动 |
| 设计不一致 | 判定为 `fail`，要求按切片目标修正 |
| 测试失败 | 判定为 `fail`，回到实现步修复 |
| 当前切片本身定义不合理 | 判定为 `blocked`，回到 [design-to-slices/SKILL.md](../design-to-slices/SKILL.md) 重拆 |
| 环境原因导致无法验证 | 判定为 `blocked`，明确环境阻塞，不伪造通过 |

---

## Non-Goals

以下内容不属于本 skill：

- 不执行全项目集成验证
- 不整理最终归档材料
- 不维护复杂验证报告体系
- 不替代人工产品验收
- 不自动处理多个切片的调度

当前切片通过后，可继续进入下一个切片的 [slice-implement/SKILL.md](../slice-implement/SKILL.md)；若多个切片都已通过，且确有需要，再进入 [integration-verify/SKILL.md](../integration-verify/SKILL.md)。
