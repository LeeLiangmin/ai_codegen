# Cursor 与本仓库（设计驱动流水线）

## 落地内容

1. **项目级 Skills** — `.cursor/skills/<name>/SKILL.md`  
   与 Cursor 约定一致：一 skill 一目录，内含 `SKILL.md`，frontmatter 含 `name` / `description`，且 **`name` 与目录名相同**。  
   内容与权威源 [`skill/`](../skill/) 下对应文件一致，由脚本同步生成。

2. **工作区规则** — [`rules/ai-design-toolkit.mdc`](rules/ai-design-toolkit.mdc)  
   默认 `alwaysApply: false`。若你主要在 Cursor 里走本流水线，可在该文件中把 `alwaysApply` 改为 `true`，或对话里 **@ai-design-toolkit** 引用本规则。

3. **总索引（必读）** — 打开 [`skill/SKILL.md`](../skill/SKILL.md) 看流程图、状态机与目录约定（与 OpenCode 共用同一套文档）。

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

## 在 Cursor 里怎么练

1. 打开本仓库为工作区根目录。  
2. 在 Chat / Agent 中说明当前阶段，或 **附加** `@.cursor/skills/run-init/SKILL.md`（或其它阶段）让模型按步骤执行。  
3. 不确定进度：附加 `@.cursor/skills/run-status/SKILL.md` 并给出 `.workflow/runs/<run-id>/state.md` 路径。  
4. 可选：编辑 `.workflow/runs/<run-id>/run-brief.md` 约束本次范围（见 `run-init` 模板）。

## 与 OpenCode 的对照

| 环境 | 镜像路径 |
|------|-----------|
| OpenCode | `.opencode/skills/<name>/SKILL.md` |
| Cursor | `.cursor/skills/<name>/SKILL.md` |
| 权威源 | `skill/<name>/SKILL.md` |

项目入口说明仍见根目录 [`AGENTS.md`](../AGENTS.md)。
