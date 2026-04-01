# OpenCode 与本仓库

## OpenCode 侧交付物与约定

本目录及根配置在仓库中的职责如下；阶段定义的**权威源**为 [`skill/`](../skill/)。

1. **`opencode.json`**（仓库根）  
   - `instructions`：注入 [`skill/SKILL.md`](../skill/SKILL.md)（流水线索引、状态机、目录约定）。  
   - `permission.skill["*"]: allow`：允许代理按需通过 `skill` 工具加载各阶段定义。

2. **`.opencode/skills/<name>/SKILL.md`**  
   与 [OpenCode Skills 文档](https://open-code.ai/en/docs/skills) 一致：目录名须与 frontmatter 中的 `name` 相同。  
   本路径为**生成镜像**，供 OpenCode 列举与按名加载；编辑请改 [`skill/<name>/SKILL.md`](../skill/) 后运行同步脚本。

3. **同步脚本**（修改 `skill/` 后须执行并提交镜像）  
   - 仅 OpenCode：`scripts/sync-opencode-skills.ps1` / `.sh`  
   - Cursor 与 OpenCode 一并更新：`scripts/sync-ide-mirrors.ps1` / `.sh`  
   将变更纳入版本控制：`.opencode/skills/`（及如有更新的 `.cursor/skills/`）。

## 推荐工作流（最小步骤）

1. 在仓库根目录启动 OpenCode（工作目录位于本 git 仓库内）。  
2. 新建运行：加载 `run-init`，并按 [`skill/run-init/SKILL.md`](../skill/run-init/SKILL.md) 提供 `run_id`、`design_doc`、`name`、`objective`。  
3. 仅查询进度、不推进阶段时：加载 `run-status`，并提供 `state.md` 路径。  
4. 阶段顺序（与总索引一致）：`design-intake` → `design-normalize` → `design-to-plan` → `plan-to-slices` → `slice-implement` / `slice-verify`（迭代）→ `integration-verify` → `result-curate`。  
5. 可选：按 `run-init` 模板编辑 `.workflow/runs/<run-id>/run-brief.md`，约束本次运行范围。

## 与 `skill/` 的关系

| 位置 | 用途 |
|------|------|
| `skill/SKILL.md` | 总索引；**不**复制到 `.opencode/skills/`（避免与 instructions 重复一份 `ai-design-toolkit` 全文）。 |
| `skill/<name>/SKILL.md` | 权威阶段定义；编辑后运行同步脚本。 |
| `.opencode/skills/<name>/SKILL.md` | OpenCode `skill` 工具发现用；由脚本生成，应纳入版本控制。 |

## 项目规则入口

根目录 [`AGENTS.md`](../AGENTS.md) 与详细叙事 [`skill/README.md`](../skill/README.md)。
