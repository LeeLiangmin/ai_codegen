# Sync canonical skill/* into .opencode/skills/* for OpenCode native skill discovery.
# OpenCode requires: .opencode/skills/<name>/SKILL.md where <name> matches YAML `name`.
# Run from repo root:  pwsh -File scripts/sync-opencode-skills.ps1
# Or:  cd scripts; ./sync-opencode-skills.ps1

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$skillRoot = Join-Path $repoRoot "skill"
$destRoot = Join-Path $repoRoot ".opencode/skills"

$leafSkills = @(
    "design-check",
    "design-plan",
    "design-to-slices",
    "slice-implement",
    "slice-verify",
    "run-init",
    "run-status",
    "integration-verify",
    "result-curate"
)

if (-not (Test-Path $skillRoot)) {
    Write-Error "Missing skill directory: $skillRoot"
}

New-Item -ItemType Directory -Force -Path $destRoot | Out-Null

foreach ($name in $leafSkills) {
    $src = Join-Path (Join-Path $skillRoot $name) "SKILL.md"
    if (-not (Test-Path $src)) {
        Write-Error "Missing source: $src"
    }
    $destDir = Join-Path $destRoot $name
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    Copy-Item -LiteralPath $src -Destination (Join-Path $destDir "SKILL.md") -Force
    Write-Host "Synced $name"
}

Write-Host "Done. $($leafSkills.Count) skills -> $destRoot"
