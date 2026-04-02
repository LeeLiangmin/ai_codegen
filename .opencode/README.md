# OpenCode 与本仓库

## OpenCode 侧交付物与约定

本目录及根配置在仓库中的职责如下；skill 定义的**权威源**为 [`skill/`](../skill/)。

1. **`opencode.json`**（仓库根）  
   - `instructions`：注入 [`skill/SKILL.md`](../skill/SKILL.md)（三层模型、流水线图、状态模型、目录约定）。  
   - `permission.skill["*"]: allow`：允许代理按需通过 `skill` 工具加载各 skill 定义。

2. **`.opencode/skills/<name>/SKILL.md`**  
   与 [OpenCode Skills 文档](https://open-code.ai/en/docs/skills) 一致：目录名须与 frontmatter 中的 `name` 相同。  
   本路径为**生成镜像**，供 OpenCode 列举与按名加载；编辑请改 [`skill/<name>/SKILL.md`](../skill/) 后运行同步脚本。

3. **同步脚本**（修改 `skill/` 后须执行并提交镜像）  
   - 仅 OpenCode：`scripts/sync-opencode-skills.ps1` / `.sh`  
   - Cursor 与 OpenCode 一并更新：`scripts/sync-ide-mirrors.ps1` / `.sh`  
   将变更纳入版本控制：`.opencode/skills/`（及如有更新的 `.cursor/skills/`）。

## 推荐工作流（最小步骤）

1. 在仓库根目录启动 OpenCode（工作目录位于本 git 仓库内）。  
2. 可选初始化：加载 `run-init`，按 [`skill/run-init/SKILL.md`](../skill/run-init/SKILL.md) 提供 `design_doc`、`objective`。  
3. 仅查询进度、不推进流程时：加载 `run-status`，并提供 `state.md` 路径。  
4. **核心闭环**：`design-check` → `design-to-slices` → `slice-implement` ↔ `slice-verify`（迭代直到所有切片通过）。  
5. **扩展层**（按需）：`integration-verify` → `result-curate`。

## 与 `skill/` 的关系

| 位置 | 用途 |
|------|------|
| `skill/SKILL.md` | 总索引；**不**复制到 `.opencode/skills/`（避免与 instructions 重复一份 `ai-design-toolkit` 全文）。 |
| `skill/<name>/SKILL.md` | 权威 skill 定义；编辑后运行同步脚本。 |
| `.opencode/skills/<name>/SKILL.md` | OpenCode `skill` 工具发现用；由脚本生成，应纳入版本控制。 |

## 项目规则入口

根目录 [`AGENTS.md`](../AGENTS.md) 与详细叙事 [`skill/README.md`](../skill/README.md)。
