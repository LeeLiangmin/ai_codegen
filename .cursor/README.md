# Cursor 与本仓库（设计驱动流水线）

## Cursor 侧交付物与约定

本目录在仓库中的职责如下；与 OpenCode 共用同一套 [`skill/`](../skill/) 权威定义。

1. **项目级 Skills**（`.cursor/skills/<name>/SKILL.md`）  
   符合 Cursor 约定：每个 skill 独立目录，内含 `SKILL.md`；frontmatter 含 `name` / `description`，且 **`name` 与目录名一致**。  
   正文与 [`skill/`](../skill/) 下对应文件一致，由同步脚本生成，**勿手改镜像**（应改 `skill/` 后同步）。

2. **工作区规则**（[`rules/ai-design-toolkit.mdc`](rules/ai-design-toolkit.mdc)）  
   默认 `alwaysApply: false`。若在本仓库中持续使用设计驱动流水线，可将该文件中的 `alwaysApply` 设为 `true`，或在对话中通过 **@ai-design-toolkit** 显式引用。

3. **流程总索引**（必读）  
   [`skill/SKILL.md`](../skill/SKILL.md)：流水线阶段、状态机与目录约定。

## 同步脚本（改 `skill/` 后执行）

与 OpenCode 镜像一起更新可跑：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/sync-ide-mirrors.ps1
```

仅更新 Cursor：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/sync-cursor-skills.ps1
```

Unix：

```bash
bash scripts/sync-ide-mirrors.sh
# 或
bash scripts/sync-cursor-skills.sh
```

然后 **提交** `.cursor/skills/`（及如有变更的 `.opencode/skills/`）。

## 在 Cursor 中的使用方式

1. 以本仓库根目录作为工作区打开。  
2. 在 Chat / Agent 中声明当前流水线阶段，或 **附加** `@.cursor/skills/run-init/SKILL.md`（或其它阶段 skill）以按步骤执行。  
3. 需查询进度而不推进阶段时：附加 `@.cursor/skills/run-status/SKILL.md`，并提供 `.workflow/runs/<run-id>/state.md` 路径。  
4. 可选：按 `run-init` 模板编辑 `.workflow/runs/<run-id>/run-brief.md`，约束本次运行范围。

## 与 OpenCode 的对照

| 环境 | 镜像路径 |
|------|-----------|
| OpenCode | `.opencode/skills/<name>/SKILL.md` |
| Cursor | `.cursor/skills/<name>/SKILL.md` |
| 权威源 | `skill/<name>/SKILL.md` |

项目入口说明仍见根目录 [`AGENTS.md`](../AGENTS.md)。
