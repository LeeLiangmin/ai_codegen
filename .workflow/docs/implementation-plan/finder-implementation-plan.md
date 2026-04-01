# Finder 实现计划

### 1. 基本信息

- run_id: examples-finder-001
- design_doc: `.workflow/docs/design/finder.normalized.md`（权威规范化稿；源编辑见 `examples/finder/DESIGN.md`）
- run_brief: `.workflow/runs/examples-finder-001/run-brief.md`（已启用；当前各节为「无」，无附加裁剪/优先级约束）
- scope: 在 `examples/finder` 内实现 Python 3.10+ CLI（`finder text` / `finder path`）、安全遍历、最小 fixture 与测试、README；依赖由 uv 管理
- owner: AI（见 `state.md` stage_owner）
- generated_at: 2026-04-01T20:00:00+08:00

### 2. 总体实现目标

- **业务目标**：在本地单进程下提供文本内容查找与按名称/类型/深度的路径查找，输出符合设计 §8.1 的 stdout 格式，退出码符合 §8.4。
- **技术目标**：模块边界与 `finder.normalized.md` §6 一致；路径不得逃逸根目录；默认不跟随符号链接；`finder text` 默认正则、`--fixed-strings` 字面；`finder path --name` 为对 basename 的 Python 正则 `re.search`。
- **交付目标**：可安装的包或入口脚本、最小 fixture、可本地/CI 运行的测试、与行为一致的 `README.md`（含 Windows 与 POSIX 差异、编码/二进制策略、SIGINT 说明）。

### 3. 模块分解

| 模块 | 职责 | 依赖 | 风险 | 优先级 |
| --- | --- | --- | --- | --- |
| 公共类型与选项 | `SearchRoot`、`SearchOptions`、`TextHit`、`PathHit` 等（§7） | 无 | 与 CLI 标志映射不一致 | P0 |
| Walker | 自顶向下枚举路径；`maxDepth`、`followSymlinks`（默认 false）；类型过滤钩子 | 标准库 fs | 权限/symlink 边界 | P0 |
| PathSearch | 在 Walker 产出上应用 `--name` 正则（basename）与 `--type f\|d\|a` | Walker | 正则编译失败 → 退出码 3 | P1（依赖 Walker） |
| ContentSearch | 单文件按行匹配；正则/字面；UTF-8 为主；编码失败策略二选一固定；二进制启发式或文档说明 | Walker 或上层迭代 | 超长行内存、非 UTF-8 | P2（依赖 Walker） |
| Output | `path:line:content` 与路径行格式化；可选控制字符处理 | 无业务依赖 | Windows 路径与 `:` 分隔策略需在 README 说明 | P1 |
| CLI 入口 | 子命令解析、`--help`、编排各模块、§8.4 退出码、SIGINT（Unix 130） | 上述全部 | 互斥选项、用法错误码 2 | P1 |

### 4. 接口实现清单

| 接口 | 所属模块 | 输入 | 输出 | 权限/约束 | 验收点 |
| --- | --- | --- | --- | --- | --- |
| `finder text <root> <pattern>` | CLI + ContentSearch + Walker + Output | root、pattern、可选 `--regex`/`--fixed-strings`、`--max-depth`、`--glob`/`--glob-exclude` | stdout 命中行；stderr 错误信息 | 只读；路径在根下 | §10.1 文本验收项 |
| `finder path <root> --name PATTERN ...` | CLI + PathSearch + Walker + Output | root、`--name`、`--type`、`--max-depth` | stdout 每行一路径 | 列目录/stat；路径在根下 | §10.1 path 验收项 |
| `finder --help` / `finder <sub> --help` | CLI | argv | 帮助文本 | — | 与实现一致 |
| 路径规范化与根下校验 | Walker（及 CLI 启动校验） | 用户给定 root、join 结果 | 合法则继续，否则码 3 | 禁止 `..` 逃逸 | fixture：树外 symlink 不跟随时不逃逸 |
| Walker 迭代协议 | Walker | `SearchRoot`、`SearchOptions` | 路径序列（或回调） | — | 深度、不跟随 symlink |
| 名称正则匹配 | PathSearch | basename、已编译 `re` | 是否命中 | 编译失败 → 码 3 | `--name` 非法正则 stderr + 3 |
| 单行内容匹配 | ContentSearch | 行文本、模式、regex 标志 | 是否命中 | 单行长度上限（常数） | 正则默认与 `--fixed-strings` |
| 格式化 TextHit / 路径 | Output | `TextHit` 或路径字符串 | 字符串行 | — | `path:line:content` |

### 5. 数据变更清单

| 数据对象 | 变更类型 | 影响范围 | 风险 | 验证方式 |
| --- | --- | --- | --- | --- |
| SearchOptions / TextHit / PathHit 等 | 新增（内存态） | `examples/finder` 包内 | 与 CLI 默认值不一致 | 单元测试 + CLI 集成测试 |
| pyproject.toml / 锁文件 | 新增或扩展 | `examples/finder` | uv 与 CI 版本漂移 | `uv sync` + 测试命令 |
| fixture 目录 | 新增 | 测试资源 | 路径可移植性 | 相对路径、跨平台说明 |
| 无数据库 | — | — | — | — |

### 6. 切片计划

| slice_id | 目标 | 输入 | 产出 | 依赖 | 验证标准 |
| --- | --- | --- | --- | --- | --- |
| slice-001 | 公共类型、路径规范化与根下校验、Walker（深度、默认不跟随 symlink） | 规范化设计 §6.2、§7 | `examples/finder` 内 Walker + 路径工具 + 对应测试 | 无 | 单测：规范化、根下校验、深度、symlink 不跟随时不逃逸 |
| slice-002 | `finder path` 子命令与 PathSearch | slice-001 | CLI `path`、`--name`、`--type`、`--max-depth`、fixture、测试 | slice-001 | 匹配文件/目录/二者；非法正则码 3；零匹配 stdout 空仍码 0 |
| slice-003 | `finder text` 子命令与 ContentSearch | slice-001 | CLI `text`、glob 选项、编码/二进制策略（README 固定）、测试 | slice-001 | 默认正则与 `--fixed-strings`；零命中码 0；非法根/正则码 3 |
| slice-004 | Output  polish、全局退出码与 SIGINT、README、测试入口与 CI（若仓库已有） | slice-002、slice-003 | README、§8.4 全链路、可选 CI 配置 | slice-002、slice-003 | 用法错误码 2；Unix SIGINT 130；`--help` 一致 |

### 7. 质量门禁

#### 7.1 设计一致性检查

- 子命令、标志位与 §8.1–§8.2 一致；退出码与 §8.4、§5.2 一致。
- 名称模式语义：Python 正则 + basename + `re.search`（§4.1）。
- 安全：不执行 shell；路径 join 后仍在根下（§4.2、§6）。
- 不引入设计外第三大主功能（§10.3）。

#### 7.2 自动化检查

- 格式检查：按仓库惯例（如 `ruff format`）若已引入则启用。
- 静态检查：`ruff check` 或项目等价物。
- 类型检查：若 `pyproject` 启用 `mypy`/`pyright` 则与之一致。
- 单元测试：`pytest`（或项目选定框架）覆盖路径校验、basename 正则、至少一种内容匹配（§10.2）。
- 契约测试：以 CLI 子进程或 click/typer 测试断言退出码与 stdout/stderr（§10.1）。

### 8. 风险与偏差策略

#### 8.1 风险项

见 `.workflow/docs/implementation-plan/risks.md`（与设计 §11.1 对齐并补充本 run 项）。

#### 8.2 可接受偏差

- 「仅统计文件数/目录数」非 v1 阻塞（§3.1）。
- Windows SIGINT 退出码若无法保证 130，以 README 记载的实际行为为准（§8.4）。
- v1 若仅在一类 OS 上跑通 CI，须在 README 声明，并保留 POSIX/Windows 行为说明（§10.2）。

### 9. 最终交付物

- **代码产出**：`examples/finder` 下可安装/可执行的 `finder` CLI 及模块（Walker、PathSearch、ContentSearch、Output）。
- **测试产出**：fixture 目录或生成脚本；单元/集成测试；可选 CI 配置片段。
- **文档产出**：`examples/finder/README.md`（使用说明、编码策略、路径分隔、SIGINT、平台差异）。
- **报告产出**：各阶段 `slice-verify` 验证报告（后续切片阶段写入 run 目录）。
