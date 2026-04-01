# OpenCode 与本仓库

## 你要的「落地」结果

1. **`opencode.json`**（仓库根）  
   - `instructions`：注入 [`skill/SKILL.md`](../skill/SKILL.md)（流水线索引、状态机、目录约定）。  
   - `permission.skill["*"]: allow`：允许代理按需加载各阶段 skill。

2. **`.opencode/skills/<name>/SKILL.md`**  
   与 [OpenCode Skills 文档](https://open-code.ai/en/docs/skills) 一致：目录名必须等于 frontmatter 里的 `name`。本仓库的**权威定义**仍在根目录 [`skill/`](../skill/)；此处为**镜像**，供 `skill` 工具列举与按名加载。

3. **同步脚本（修改 skill 后必跑）**  
   - 仅 OpenCode: `scripts/sync-opencode-skills.ps1` / `.sh`  
   - **Cursor + OpenCode 一次更新**: `scripts/sync-ide-mirrors.ps1` / `.sh`  
   然后在 git 中提交 `.opencode/skills/`（及如已更新的 `.cursor/skills/`）。

## 实战最小步骤

1. 在仓库根打开 OpenCode（工作区 cwd 在 git 仓库内）。  
2. 新 run：让代理加载 `run-init`，按 [`skill/run-init/SKILL.md`](../skill/run-init/SKILL.md) 提供 `run_id`、`design_doc`、`name`、`objective`。  
3. 不确定进度：加载 `run-status`，传入 `state.md` 路径。  
4. 按索引顺序：`design-intake` → `design-normalize` → `design-to-plan` → `plan-to-slices` → `slice-implement` / `slice-verify`（循环）→ `integration-verify` → `result-curate`。  
5. 可选：编辑 `.workflow/runs/<run-id>/run-brief.md` 约束本次范围（见 `run-init` 模板）。

## 与 `skill/` 的关系

| 位置 | 用途 |
|------|------|
| `skill/SKILL.md` | 总索引；**不**复制到 `.opencode/skills/`（避免与 instructions 重复一份 `ai-design-toolkit` 全文）。 |
| `skill/<name>/SKILL.md` | 权威阶段定义；编辑后运行同步脚本。 |
| `.opencode/skills/<name>/SKILL.md` | OpenCode `skill` 工具发现用；由脚本生成，应纳入版本控制。 |

## 项目规则入口

根目录 [`AGENTS.md`](../AGENTS.md) 与详细叙事 [`skill/README.md`](../skill/README.md)。
