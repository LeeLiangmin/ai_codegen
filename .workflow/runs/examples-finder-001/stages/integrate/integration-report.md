# 集成验证报告 — examples-finder-001

## 元数据

| 项 | 值 |
| --- | --- |
| run_id | examples-finder-001 |
| generated_at | 2026-04-02T02:45:00+08:00 |
| 设计参考 | `.workflow/docs/design/finder.normalized.md` §5、§6、§8 |

## 1. 验证范围（参与集成的切片）

| slice_id | status | verify_status |
| --- | --- | --- |
| slice-001 | verified | passed |
| slice-002 | verified | passed |
| slice-003 | verified | passed |
| slice-004 | verified | passed |

**结论**：前置条件满足；无 `blocked` / `failed` 切片。

## 2. 接口一致性检查

| 边界 | 结果 | 说明 |
| --- | --- | --- |
| Walker → PathSearch | 通过 | `iter_walk` 产出 `WalkEntry`；`iter_matching_paths` 消费 `Path`/`is_directory` 与 `SearchOptions` |
| Walker → text CLI | 通过 | `iter_walk` + 仅文件节点 + `matches_path_globs` + `iter_text_hits_in_file` |
| PathSearch / ContentSearch → Output | 通过 | `PathHit.path` → `format_path_line`；`TextHit` → `format_text_hit` |
| paths → CLI | 通过 | `resolve_search_root` / `InvalidRootError` → 退出码 **3** |
| argparse → `run()` | 通过 | `SystemExit(2)` 透传；`KeyboardInterrupt` → 130（POSIX）/ 1（Windows） |

## 3. 数据流验证

| 路径 | 结果 | 说明 |
| --- | --- | --- |
| `SearchOptions`（max_depth、follow_symlinks） | 通过 | path/text 均传入 Walker；默认不跟随 symlink |
| 根解析 | 通过 | 相对 `ROOT` 相对 CWD 再校验目录（与 README 一致） |
| 文本管线 | 通过 | 文件路径 → UTF-8 读行 → `TextHit` → `path:line:content` |
| 错误传播 | 通过 | 非法正则/根在 CLI 层映射为 **3**；用法问题 **2** |

## 4. 端到端业务流程（对照 §5.1）

| 流程 | 结果 | 证据 |
| --- | --- | --- |
| §5.1.2 `finder path` | 通过 | `test_cli_path.py`、`test_fixture_path_and_text` |
| §5.1.1 `finder text` | 通过 | `test_cli_text.py`、`test_fixture_path_and_text` |
| §5.2 根无效 / 非法模式 | 通过 | CLI 退出码 **3** 用例 |
| §8.4 成功含零输出 | 通过 | path/text 零命中 **0** |
| §8.3 `--help` | 通过 | 顶层与子命令 help 测试 |
| SIGINT（映射） | 通过 | `test_run_maps_keyboard_interrupt`（按平台断言） |

## 5. 回归测试

详见同目录 [`regression-report.md`](regression-report.md)。

## 6. 总体结论

**passed** — 关键链路可端到端跑通；模块间类型与数据流一致；集成与全量测试通过。

## 7. 失败项与修复建议

无。

## 8. 已知非阻塞项

- **B-14**：仓库级 CI 未添加（slice-004 已 deferred）；不影响集成结论。
