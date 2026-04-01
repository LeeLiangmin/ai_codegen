# 偏差汇总 — examples-finder-001

生成时间：2026-04-02（与 `state.md` 收尾一致）。

## 1. 切片级 deviation 文件

- **磁盘检索**：`.workflow/runs/examples-finder-001/**/slice-*-deviation.md` — **无** 独立 deviation 文件。
- **state.md 切片表**：slice-001…004 的 `deviation` 列均为 **none**；slice-004 备注中说明 B-14 为 deferred（见下「范围偏差」）。

## 2. 按类别汇总

### 2.1 设计偏差

| 项 | 说明 | 结论 |
| --- | --- | --- |
| — | 无与设计稿冲突且未记录的实现选择 | **无** |

### 2.2 实现偏差

| 项 | 说明 | 结论 |
| --- | --- | --- |
| Windows SIGINT | 设计允许 Windows 非 130；实现与 README 写明实际退出码（集成报告：`KeyboardInterrupt` → 1 on Windows） | **accepted**，与设计 §8.4 / §5.2 一致 |
| — | 其他 | **无** |

### 2.3 范围偏差

| 项 | 说明 | 结论 |
| --- | --- | --- |
| **B-14 CI** | Backlog 可选项：在仓库 CI 中增加 `examples/finder` 测试；仓库根 **无** `.github/workflows`，按 slice-004 **未新增** workflow | **accepted deferral**（见 `slice-004-verification-report.md`、`slice-004-implementation-notes.md`、`integration-report.md`） |

## 3. 未解决项（unresolved）

- **normalize**：`stages/normalize/unresolved-items.md` 在设计链路已清空（state 摘要）。
- **集成**：无 `unresolved-integration-issues.md`（integration-verify 通过）。
- **本 run**：无标记为 **unresolved** 的偏差需阻塞关闭。

## 4. 量化摘要

| 指标 | 值 |
| --- | --- |
| 独立 deviation 文档数 | 0 |
| accepted 范围削减 | 1（B-14） |
| accepted 平台行为说明 | 1（Windows SIGINT） |
| unresolved 偏差 | 0 |
