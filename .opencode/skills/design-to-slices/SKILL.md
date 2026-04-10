---
name: design-to-slices
description: Use when the design is sufficient to act and you need to derive the smallest safe, verifiable slices directly from the design without generating a heavy implementation plan first
---

# design-to-slices

## Overview

`design-to-slices` 是新体系中的第二个核心 skill。

它直接把设计材料转换为**最小可验证切片**，不再要求先生成厚重的 implementation plan，再从计划二次拆分切片。

核心原则：

- 切片是主资产，不是中间报告
- 一个切片只承载一个足够小、足够清晰、足够可验证的目标
- 如果设计不完整，只定义仍然安全的切片，不伪造全量计划

---

## When to Use

在以下场景使用：

- 已完成 [design-check/SKILL.md](../design-check/SKILL.md)，结论为 `ready-for-slicing` 或 `ready-with-risks`
- 对于复杂任务，已完成 [design-plan/SKILL.md](../design-plan/SKILL.md)，已建立整体结构认知
- 已经明确任务目标，准备开始落地实现
- 需要把大目标切成弱模型也能稳定执行的小任务
- 续跑时，需要重新整理剩余可执行切片

---

## Input

| 输入项 | 必填 | 说明 |
|---|---|---|
| 设计文档 | 是 | 原始设计文档或用户直接提供的结构化描述 |
| design-check 结果 | 建议 | 用于继承目标、范围、约束、风险、缺失项、复杂度 |
| design-plan 结果 | 建议 | 复杂任务时提供；用于继承模块边界、主流程、依赖关系、切片策略 |
| 现有代码上下文 | 否 | 用于识别可修改边界与已有实现 |
| 用户附加约束 | 否 | 例如仅做 MVP、只动 API 层、不改数据库等 |
| 会话状态 | 否 | 若存在，可用于识别已完成切片与剩余任务 |

---

## Procedure

1. **读取设计目标与约束**
   从设计文档和 `design-check` 结果中提取：
   - 总体目标
   - 当前范围
   - 非目标
   - 技术约束
   - 风险与缺失项

   若存在 `design-plan` 结果，还应继承：
   - 模块边界与职责
   - 主执行流
   - 关键接口与依赖
   - 切片策略建议

2. **识别可独立推进的实现单元**
   从以下维度寻找候选切片：
   - 单一模块
   - 单一接口
   - 单一数据结构变更
   - 单一业务流程中的一小段
   - 单一修复目标

3. **按"最小可验证"原则切分**
   每个切片必须满足：
   - 能在一次实现-验证闭环中完成
   - 目标单一，不混合多个大问题
   - 修改边界清楚
   - 有明确验证方式
   - 不依赖大量隐含前提

4. **为每个切片定义最小属性**
   每个切片至少包含：
   - `slice_id`
   - `title`
   - `objective`
   - `depends_on`
   - `wave`（执行波次，见步骤 6）
   - `allowed_changes`
   - `forbidden_changes`
   - `expected_outputs`
   - `verification`：必须足够具体到可直接编写自动化检查或执行手动验证步骤
     - `criteria`（必填）：具体的验收条件，描述可观测的行为或状态
     - `test_sketch`（可选）：建议的测试骨架或验证伪代码，帮助 `slice-implement` 阶段快速进入 TDD Red 步骤
   - `risks`

   **⚠️ `verification.criteria` 的反例指导**

   不接受以下类型的 verification：
   - "功能正常工作"
   - "测试通过"
   - "符合预期"
   - "代码质量良好"

   ✅ 有效的 verification 示例：
   - `criteria: "调用 POST /users 返回 201，数据库中新增对应记录"`
   - `criteria: "配置文件加载失败时抛出 ConfigError，包含文件路径信息"`
   - `criteria: "输入超过 1000 条记录时处理时间 < 2 秒"`
   - `criteria: "CLI 运行 --help 时输出包含所有子命令名称"`

5. **控制切片粒度**
   如果某切片存在以下现象，应继续拆小：
   - 同时涉及多个模块的大改动
   - 同时包含数据、接口、UI、测试等多个层面的大范围变更
   - 验证方式不清晰
   - 需要多个前置条件同时成立
   - 失败后难以回退

6. **建立最小依赖关系与并行分组**
   只保留执行所必需的依赖关系：
   - 每个切片只引用直接前置项（`depends_on`）
   - 不建模间接依赖

   基于 `depends_on` 关系，为每个切片分配执行波次（Wave）：
   - 规则：`wave = max(所有 depends_on 切片的 wave) + 1`
   - 无依赖切片：`wave = 1`
   - 同一 Wave 内的切片互不依赖，可并行执行

7. **排序并选择起始切片**
   优先级规则默认如下：
   - 先低风险、可快速验证的切片
   - 先基础能力，再扩展能力
   - 先解锁后续工作的前置切片
   - 先修改范围小、验证成本低的切片
   - 在同一优先级内，Wave 编号小的先执行

8. **输出切片集合**
   最终输出：
   - 一个切片索引（含 Wave 分组）
   - 若干单切片定义
   - 一个建议先执行的首切片

---

## Output

### 最小输出

- `slices_index`
- `slice_definitions`
- `recommended_first_slice`

### 建议文件输出

如果使用会话目录，建议写入：

- `.workflow/session/slices/index.md`
- `.workflow/session/slices/slice-001.md`
- `.workflow/session/slices/slice-002.md`
- ...

### 切片索引建议结构

```markdown
# Slices Index

| slice_id | title | depends_on | wave | objective | verification | status |
|---|---|---|---|---|---|---|
| slice-001 | ... | — | 1 | ... | ... | pending |
| slice-002 | ... | — | 1 | ... | ... | pending |
| slice-003 | ... | slice-001, slice-002 | 2 | ... | ... | pending |

## Execution Waves

- **Wave 1** (可并行): slice-001, slice-002
- **Wave 2** (需 Wave 1 完成): slice-003
```

### 单切片建议结构

```markdown
# Slice Definition

- slice_id: slice-001
- title: <...>
- objective: <...>
- depends_on: []
- wave: 1

## Allowed Changes
- ...

## Forbidden Changes
- ...

## Expected Outputs
- code: ...
- tests: ...
- docs: ...

## Verification
- criteria: <具体的、可观测的验收条件>
- test_sketch: |    （可选）
    test("描述测试目标", () => {
      // 测试骨架
    })

## Risks
- ...
```

---

## 续拆场景

当从 `slice-implement` 或 `slice-verify` 回退到本 skill 时：

- 保留已完成且已通过验证的切片，不重新定义
- 只对当前失败/阻塞的切片进行重新拆分
- 新切片 ID 在原切片基础上延续（如 slice-003a, slice-003b）
- 重新计算受影响切片的 Wave 编号
- 更新 `slices/index.md` 反映变更
- 确保新切片的 `verification.criteria` 同样满足操作化要求

---

## Quality Gate

一次有效的 `design-to-slices` 结果，至少应满足：

- [ ] 已定义至少一个可安全执行的切片
- [ ] 每个切片目标单一且可验证
- [ ] 每个切片的允许修改范围清晰
- [ ] 每个切片的 `verification.criteria` 足够具体到可直接写测试或执行验证命令
- [ ] 切片依赖关系最小化
- [ ] 每个切片已分配 Wave 编号
- [ ] 已明确推荐的首个执行切片

---

## Failure Handling

| 场景 | 处理方式 |
|---|---|
| 设计太模糊，无法定义任何安全切片 | 停止并返回 `design-check`，要求补充最小必要信息 |
| 只能识别一个过大的切片 | 强制继续拆分，直到可单次闭环验证 |
| 存在循环依赖 | 调整切片边界，优先提取更底层的前置切片 |
| 风险太高但并非完全阻塞 | 允许生成低风险切片，推迟高风险部分 |
| 代码现状与设计冲突 | 在切片中显式记录边界与风险，不静默扩展范围 |

---

## Non-Goals

以下内容不属于本 skill：

- 不生成大而全的 implementation plan
- 不生成 backlog 治理文档
- 不直接写代码
- 不执行测试或验证命令
- 不维护复杂全局阶段状态

完成后，下一步应进入：
- 首个切片的 [slice-implement/SKILL.md](../slice-implement/SKILL.md)
- 实现完成后进入 [slice-verify/SKILL.md](../slice-verify/SKILL.md)
