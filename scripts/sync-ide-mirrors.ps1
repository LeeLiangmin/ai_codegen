# Sync skill/ mirrors for both OpenCode (.opencode/skills) and Cursor (.cursor/skills).
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $here "sync-opencode-skills.ps1")
& (Join-Path $here "sync-cursor-skills.ps1")
Write-Host "All IDE skill mirrors updated."
