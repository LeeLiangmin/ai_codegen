# Finder 实现 backlog（examples-finder-001）

与 `finder-implementation-plan.md` 及 `.workflow/docs/design/finder.normalized.md` 对齐。优先级 P0 先于 P1，依拓扑：公共类型/Walker → PathSearch/Output/CLI 路径 → ContentSearch/CLI 文本 → 文档与全链路。

| id | 标题 | 模块 | 优先级 | 依赖 | 验收要点 |
| --- | --- | --- | --- | --- | --- |
| B-01 | 定义 `SearchOptions`、`TextHit`、`PathHit`、`SearchRoot`（或等价） | 公共类型 | P0 | — | 字段与 §7.1 一致 |
| B-02 | 实现路径解析、规范化与「仍在根目录子树下」校验 | Walker / CLI | P0 | B-01 | 非法根 → 退出码 3 |
| B-03 | 实现 Walker：`maxDepth`、默认 `followSymlinks=false`、可集成类型过滤 | Walker | P0 | B-02 | 深度 0/1/n fixture |
| B-04 | 实现 Output：`TextHit` → `path:line:content`；纯路径一行一条 | Output | P1 | B-01 | README 说明 `:` 与 Windows 路径 |
| B-05 | 实现 PathSearch：basename + `re.search`、`--type f\|d\|a` | PathSearch | P1 | B-03 | 非法 `--name` 正则 → 码 3 |
| B-06 | CLI：`finder path` 参数解析、帮助、编排、退出码 0/2/3 | CLI | P1 | B-03,B-04,B-05 | §10.1 path 与码表 |
| B-07 | 实现 ContentSearch：逐行、默认正则、`--fixed-strings` 互斥 | ContentSearch | P2 | B-03 | 特殊字符字面匹配 |
| B-08 | 编码失败策略二选一（跳过或诊断）在代码注释与 README 固定 | ContentSearch | P2 | B-07 | 与设计 §3.1、§6.3 一致 |
| B-09 | 二进制启发式跳过或 README 风险说明（§9.2） | ContentSearch | P2 | B-07 | 文档与实现一致 |
| B-10 | CLI：`finder text`、glob 包含/排除、与 B-07 编排 | CLI | P2 | B-04,B-07 | §10.1 text 项 |
| B-11 | 全局退出码与 SIGINT：用法 2、不可恢复 3、成功 0、Unix 130 | CLI | P2 | B-06,B-10 | §8.4 |
| B-12 | README：安装（uv）、示例、平台差异、SIGINT（Windows）、相对路径解析顺序 | 文档 | P2 | B-11 | 与实现一致 |
| B-13 | Fixture 与测试：空目录、混合深度、Unicode/空格文件名、symlink | 测试 | P2 | B-03 | §10.2、§12.2 |
| B-14 | 可选：仓库 CI 中增加 `examples/finder` 测试任务 | 工程 | P3 | B-12,B-13 | 与现有 CI 风格一致 |

**Run brief 对齐**：`run-brief.md` 当前无实质约束，无额外 backlog 项。
