param(
  [Parameter(Mandatory=$true)][string]$Version,
  [string]$Site = "https://nad-lan.co.il",
  [string]$Slug = "rainbow-tel-aviv",
  [int]$PostId = 4464
)

$ErrorActionPreference = "Stop"

function Find-Php {
  $cmd = Get-Command php -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }
  $wingetPhp = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages\PHP.PHP.8.3_Microsoft.Winget.Source_8wekyb3d8bbwe\php.exe"
  if (Test-Path $wingetPhp) { return $wingetPhp }
  throw "PHP CLI not found. Install with: winget install --id PHP.PHP.8.3 --exact"
}

$php = Find-Php

Write-Host "== PHP lint =="
& $php -l plugins\nadlan-config\nadlan-config.php
& $php -l plugins\nadlan-config\inc\project-3d.php
& $php -l plugins\nadlan-config\inc\project-page-assembly.php
& $php -l plugins\nadlan-config\inc\health.php

Write-Host "== Payload + factory checks =="
node scripts\validate-project-showroom-payload.mjs --payload assets\projects\rainbow-tel-aviv\showroom-payload.json
node scripts\qa-project-factory-smoke.mjs

Write-Host "== Build + verify ZIP =="
python scripts\build-plugin-zip.py $Version
python scripts\verify-plugin-release.py $Version

Write-Host "== Live gate, if deployed =="
node scripts\qa-rainbow-postdeploy.mjs --version $Version --site $Site --slug $Slug --post-id $PostId --out "docs\qa\rainbow-postdeploy-$Version.json"

Write-Host "Release gate complete for $Version"
