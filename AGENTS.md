# Project rules (OpenCode)

This repository is set up for **[OpenCode](https://open-code.ai/)** as the primary agent workflow.

## Design-driven implementation toolkit

The system uses a **minimal slice loop** as the default path, not a heavy document pipeline.

1. Start from [`skill/SKILL.md`](skill/SKILL.md): three-layer model (Core / Infra / Extensions), pipeline diagram, minimal state model, and recommended session layout.
2. **Core loop**: `design-check` → `design-to-slices` → `slice-implement` ↔ `slice-verify` — repeat until all slices pass.
3. **Infra** (optional): `run-init` creates a minimal session directory and `state.md`; `run-status` reads current state and suggests the next step.
4. **Extensions** (on demand): `integration-verify` for cross-slice checks; `result-curate` for archival assets.
5. For each stage, follow [`skill/<skill-name>/SKILL.md`](skill/) (YAML `name` / `description` in frontmatter).
6. Long-form narrative and design principles: [`skill/README.md`](skill/README.md).
7. Machine-readable registry: [`skill/manifest.json`](skill/manifest.json).

### Minimal state model

`state.md` only tracks recovery-essential fields: `objective`, `design_doc`, `status`, `current_slice`, `last_completed_slice`, `last_verify_result`, `blocked`, `block_reason`. No complex stage tables or slice inventories.

## OpenCode vs skill discovery

OpenCode's `skill` tool discovers skills under `.opencode/skills/<name>/SKILL.md` (and Claude-compatible paths). **Canonical definitions live under `skill/`** (umbrella [`skill/SKILL.md`](skill/SKILL.md)). The `.opencode/skills/` tree is a **synced mirror** of each active skill — after editing `skill/<name>/SKILL.md`, run `scripts/sync-opencode-skills.ps1` or `scripts/sync-opencode-skills.sh` and commit. [`opencode.json`](opencode.json) merges `instructions` plus `permission.skill` defaults.

## Cursor

- **Rules**: [`.cursor/rules/ai-design-toolkit.mdc`](.cursor/rules/ai-design-toolkit.mdc) — enable `alwaysApply` or @-mention when driving the pipeline in Cursor.
- **Project skills** (mirrored from `skill/`): `.cursor/skills/<name>/SKILL.md` — sync with `scripts/sync-cursor-skills.ps1` / `.sh` or `scripts/sync-ide-mirrors.*` after editing `skill/`.
- **Quickstart**: [`.cursor/README.md`](.cursor/README.md).
