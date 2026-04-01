# AI 设计驱动实现 Toolkit

- **索引与流程**：[SKILL.md](SKILL.md)  
- **轻量五步**：[SKILL-LITE.md](SKILL-LITE.md)  
- **项目规则**：[AGENTS.md](../AGENTS.md) ；OpenCode：[opencode.json](../opencode.json)

## 原则（五条）

文档先行 · 切片执行 · 状态可恢复 · 验证内建 · 结果沉淀

## 同步镜像

修改 `skill/` 后运行 **`scripts/sync-ide-mirrors.ps1`** 或 **`sync-ide-mirrors.sh`**（或分别 `sync-opencode-skills` / `sync-cursor-skills`）。说明：[.opencode/README.md](../.opencode/README.md)、[.cursor/README.md](../.cursor/README.md)。

## 各阶段

`skill/<name>/SKILL.md`（YAML `name` / `description`），与 [superpowers/skills](https://github.com/obra/superpowers/tree/main/skills) 目录约定一致。
