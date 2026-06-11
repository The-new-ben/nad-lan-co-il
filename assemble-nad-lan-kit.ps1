# Assembles C:\Users\pro\nad-lan from the public repo. Safe to re-run (refreshes content).
$ErrorActionPreference = 'Stop'
$dest = 'C:\Users\pro\nad-lan'
$tmp  = Join-Path $env:TEMP ('nadlan-kit-' + (Get-Date -Format 'yyyyMMddHHmmss'))
git clone --depth 1 https://github.com/The-new-ben/nad-lan-co-il.git $tmp
New-Item -ItemType Directory -Force -Path $dest | Out-Null
foreach ($item in @('skills','docs','START-HERE.md','README.md','AGENTS.md','HANDOFF.md','BACKLOG.md')) {
  $src = Join-Path $tmp $item
  if (Test-Path $src) { Copy-Item $src -Destination $dest -Recurse -Force }
}
# plugin source for reference (read-only copy; live edits happen via the repo)
Copy-Item (Join-Path $tmp 'plugins') -Destination $dest -Recurse -Force
Remove-Item $tmp -Recurse -Force
Write-Output "DONE. Kit assembled at $dest"
Get-ChildItem $dest | Select-Object Name
