# Project rules (OpenCode)

This repository is set up for **[OpenCode](https://open-code.ai/)** as the primary agent workflow.

## Design-driven implementation toolkit

1. Start from [`skill/SKILL.md`](skill/SKILL.md): skill index, pipeline, state machine, directory layout, and `state.md` semantics (`status` vs `current_stage`). For a **compressed five-step path** (merged stages, weaker models), see [`skill/SKILL-LITE.md`](skill/SKILL-LITE.md). Per-run scope extras live in `.workflow/runs/<run-id>/run-brief.md` (optional; see [`skill/run-init/SKILL.md`](skill/run-init/SKILL.md)). To resume or inspect progress without advancing the pipeline, use [`skill/run-status/SKILL.md`](skill/run-status/SKILL.md).
2. For each stage, follow [`skill/<skill-name>/SKILL.md`](skill/) (YAML `name` / `description` in frontmatter).
3. Long-form narrative and steps: [`skill/README.md`](skill/README.md).
4. Machine-readable registry (optional tooling): [`skill/manifest.json`](skill/manifest.json).

## OpenCode vs skill discovery

OpenCode’s `skill` tool discovers skills under `.opencode/skills/<name>/SKILL.md` (and Claude-compatible paths). **Canonical definitions live under `skill/`** (umbrella [`skill/SKILL.md`](skill/SKILL.md)). The `.opencode/skills/` tree is a **synced mirror** of each stage skill—after editing `skill/<name>/SKILL.md`, run `scripts/sync-opencode-skills.ps1` or `scripts/sync-opencode-skills.sh` and commit. [`opencode.json`](opencode.json) merges `instructions` plus `permission.skill` defaults.

## Cursor

- **Rules**: [`.cursor/rules/ai-design-toolkit.mdc`](.cursor/rules/ai-design-toolkit.mdc) — enable `alwaysApply` or @-mention when driving the pipeline in Cursor.
- **Project skills** (mirrored from `skill/`): `.cursor/skills/<name>/SKILL.md` — sync with `scripts/sync-cursor-skills.ps1` / `.sh` or `scripts/sync-ide-mirrors.*` after editing `skill/`.
- **Quickstart**: [`.cursor/README.md`](.cursor/README.md).
