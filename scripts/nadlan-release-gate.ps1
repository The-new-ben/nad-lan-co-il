param(
  [ValidateSet("PreDeploy", "PostDeploy")]
  [string]$Phase = "PreDeploy",
  [string]$Version = "1.72.128",
  [string]$Site = "https://nad-lan.co.il",
  [switch]$PlanOnly
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$PinnedVersion = "1.72.128"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptRoot

function Find-Tool {
  param(
    [Parameter(Mandatory=$true)][string]$Name,
    [string]$Fallback = ""
  )
  $command = Get-Command $Name -ErrorAction SilentlyContinue
  if ($command) { return $command.Source }
  if ($Fallback -and (Test-Path -LiteralPath $Fallback)) {
    return (Resolve-Path -LiteralPath $Fallback).Path
  }
  throw "$Name CLI was not found."
}

function Find-Php {
  $fallback = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages\PHP.PHP.8.3_Microsoft.Winget.Source_8wekyb3d8bbwe\php.exe"
  return Find-Tool -Name "php" -Fallback $fallback
}

function Invoke-NativeStep {
  param(
    [Parameter(Mandatory=$true)][string]$Name,
    [Parameter(Mandatory=$true)][string]$Command,
    [string[]]$CommandArgs = @()
  )
  Write-Host ""
  Write-Host "== $Name =="
  & $Command @CommandArgs
  if ($LASTEXITCODE -ne 0) {
    throw "$Name failed with exit code $LASTEXITCODE."
  }
}

function Assert-ReleaseIdentity {
  param([Parameter(Mandatory=$true)][string]$ExpectedVersion)
  if ($ExpectedVersion -ne $PinnedVersion) {
    throw "This release gate is pinned to UTOPIA $PinnedVersion. Received $ExpectedVersion."
  }
  $mainPath = Join-Path $RepoRoot "plugins\nadlan-config\nadlan-config.php"
  $modulePath = Join-Path $RepoRoot "plugins\nadlan-config\inc\utopia-sde-dov.php"
  $manifestPath = Join-Path $RepoRoot "plugin-dist\nadlan-config.json"
  foreach ($required in @($mainPath, $modulePath, $manifestPath)) {
    if (-not (Test-Path -LiteralPath $required)) {
      throw "Required release file is missing: $required"
    }
  }
  $main = Get-Content -Raw -Encoding UTF8 -LiteralPath $mainPath
  $module = Get-Content -Raw -Encoding UTF8 -LiteralPath $modulePath
  $manifest = Get-Content -Raw -Encoding UTF8 -LiteralPath $manifestPath | ConvertFrom-Json
  $headerMatch = [regex]::Match($main, "(?m)^\s*\*\s*Version:\s*([0-9.]+)\s*$")
  $constantMatch = [regex]::Match($main, "define\(\s*['""]NADLAN_CONFIG_VERSION['""]\s*,\s*['""]([0-9.]+)['""]\s*\)")
  if (-not $headerMatch.Success -or $headerMatch.Groups[1].Value -ne $ExpectedVersion) {
    throw "Plugin header does not equal $ExpectedVersion."
  }
  if (-not $constantMatch.Success -or $constantMatch.Groups[1].Value -ne $ExpectedVersion) {
    throw "NADLAN_CONFIG_VERSION does not equal $ExpectedVersion."
  }
  if ([string]$manifest.version -ne $ExpectedVersion) {
    throw "Release manifest does not equal $ExpectedVersion."
  }
  $expectedDownload = "https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config-$ExpectedVersion.zip"
  if ([string]$manifest.download_url -ne $expectedDownload) {
    throw "Manifest download_url does not point to the exact $ExpectedVersion package."
  }
  if ($module -notmatch "'release'\s*=>\s*'$([regex]::Escape($ExpectedVersion))'" -or
      $module -notmatch "nadlan_utopia_release_v172128") {
    throw "UTOPIA migration identity is not pinned to $ExpectedVersion."
  }
}

function Invoke-PhpLintTree {
  param([Parameter(Mandatory=$true)][string]$Php)
  Write-Host ""
  Write-Host "== PHP lint: complete plugin and UTOPIA harness =="
  $files = @(
    Get-ChildItem -LiteralPath (Join-Path $RepoRoot "plugins\nadlan-config") -Recurse -File -Filter "*.php"
  )
  $files += Get-Item -LiteralPath (Join-Path $RepoRoot "scripts\build-utopia-static-preview.php")
  $files += Get-Item -LiteralPath (Join-Path $RepoRoot "scripts\qa-utopia-release-migration.php")
  foreach ($file in $files) {
    $output = & $Php -l $file.FullName 2>&1
    if ($LASTEXITCODE -ne 0) {
      $output | ForEach-Object { Write-Host $_ }
      throw "PHP lint failed: $($file.FullName)"
    }
  }
  Write-Host "PASS $($files.Count) PHP files"
}

function Invoke-NodeSyntaxChecks {
  param([Parameter(Mandatory=$true)][string]$Node)
  Write-Host ""
  Write-Host "== JavaScript syntax: UTOPIA release surface =="
  $files = @(
    Get-ChildItem -LiteralPath (Join-Path $RepoRoot "scripts") -File -Filter "qa-utopia-*.mjs"
  )
  $files += Get-Item -LiteralPath (Join-Path $RepoRoot "plugins\nadlan-config\assets\showroom-engine\engine.js")
  $files += Get-Item -LiteralPath (Join-Path $RepoRoot "plugins\nadlan-config\assets\showroom-engine\projects\utopia-sde-dov\utopia-i18n.js")
  foreach ($file in $files) {
    & $Node --check $file.FullName
    if ($LASTEXITCODE -ne 0) {
      throw "JavaScript syntax check failed: $($file.FullName)"
    }
  }
  Write-Host "PASS $($files.Count) JavaScript files"
}

function Get-ZipEntryHash {
  param(
    [Parameter(Mandatory=$true)]$Entry
  )
  $stream = $Entry.Open()
  $algorithm = [System.Security.Cryptography.SHA256]::Create()
  try {
    $bytes = $algorithm.ComputeHash($stream)
    return ([BitConverter]::ToString($bytes)).Replace("-", "").ToLowerInvariant()
  } finally {
    $algorithm.Dispose()
    $stream.Dispose()
  }
}

function Assert-UtopiaZip {
  param(
    [Parameter(Mandatory=$true)][string]$ExpectedVersion,
    [Parameter(Mandatory=$true)][string]$Php
  )
  Write-Host ""
  Write-Host "== ZIP content, asset identity and extracted PHP lint =="
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $zipPath = Join-Path $RepoRoot "plugin-dist\nadlan-config-$ExpectedVersion.zip"
  if (-not (Test-Path -LiteralPath $zipPath)) {
    throw "Release ZIP is missing: $zipPath"
  }
  $requiredEntries = @(
    "nadlan-config/inc/utopia-sde-dov.php",
    "nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia.css",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-i18n.js",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/article-he.html",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/article-en.html",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/article-fr.html",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/article-ru.html",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/article-ar.html",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-exterior-v1.webp",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-interior-v1.webp",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-window-view-v1.webp",
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-wellness-v1.webp"
  )
  $expectedHashes = @{
    "nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb" = "ba267a241f7b5d943f5eebd6f32aae9241f14da420207ddadc4d5d74ac392f24"
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-exterior-v1.webp" = "55122e051450af3e2715af36df05837e06f96f73db9f8291bf4a3f3e8dc263c6"
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-interior-v1.webp" = "d89457f00cd52385107072902e7df06fab3750f16b9b18a923396398b59d7c6b"
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-window-view-v1.webp" = "995a982ea8aed6ded92f3ac30c86c86b20737dd5f20b371a9cf8a4aea2c5f9f4"
    "nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-wellness-v1.webp" = "c1d1a1a53b85fc61ad1c39598f4a0a404b92cb4144d3a51c2093cbaabe046a61"
  }
  $archive = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
  $tempRoot = [System.IO.Path]::GetFullPath((Join-Path ([System.IO.Path]::GetTempPath()) ("nadlan-utopia-zip-lint-" + [guid]::NewGuid().ToString("N"))))
  $systemTemp = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
  try {
    $entryMap = @{}
    foreach ($entry in $archive.Entries) { $entryMap[$entry.FullName] = $entry }
    foreach ($required in $requiredEntries) {
      if (-not $entryMap.ContainsKey($required)) {
        throw "Release ZIP is missing UTOPIA entry: $required"
      }
    }
    foreach ($pair in $expectedHashes.GetEnumerator()) {
      $actual = Get-ZipEntryHash -Entry $entryMap[$pair.Key]
      if ($actual -ne $pair.Value) {
        throw "Release ZIP asset hash mismatch: $($pair.Key)"
      }
    }
    New-Item -ItemType Directory -Path $tempRoot | Out-Null
    $phpEntries = @($archive.Entries | Where-Object { $_.FullName.EndsWith(".php", [System.StringComparison]::OrdinalIgnoreCase) })
    foreach ($entry in $phpEntries) {
      $relative = $entry.FullName.Replace("/", [System.IO.Path]::DirectorySeparatorChar)
      $target = [System.IO.Path]::GetFullPath((Join-Path $tempRoot $relative))
      if (-not $target.StartsWith($tempRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Unsafe ZIP extraction path: $($entry.FullName)"
      }
      $parent = Split-Path -Parent $target
      if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
      }
      [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $target, $true)
      $output = & $Php -l $target 2>&1
      if ($LASTEXITCODE -ne 0) {
        $output | ForEach-Object { Write-Host $_ }
        throw "Extracted ZIP PHP lint failed: $($entry.FullName)"
      }
    }
    Write-Host "PASS required UTOPIA entries, exact binary assets and $($phpEntries.Count) extracted PHP files"
  } finally {
    $archive.Dispose()
    if (Test-Path -LiteralPath $tempRoot) {
      $resolvedTemp = [System.IO.Path]::GetFullPath((Resolve-Path -LiteralPath $tempRoot).Path)
      if (-not $resolvedTemp.StartsWith($systemTemp, [System.StringComparison]::OrdinalIgnoreCase) -or
          $resolvedTemp -eq $systemTemp) {
        throw "Refusing to remove unverified temporary path: $resolvedTemp"
      }
      Remove-Item -LiteralPath $resolvedTemp -Recurse -Force
    }
  }
}

if ($Version -ne $PinnedVersion) {
  throw "This release gate is pinned to UTOPIA $PinnedVersion. Received $Version."
}

Push-Location $RepoRoot
try {
  Assert-ReleaseIdentity -ExpectedVersion $Version
  $php = Find-Php
  $node = Find-Tool -Name "node"
  $python = Find-Tool -Name "python"
  $git = Find-Tool -Name "git"

  Write-Host "UTOPIA $Version release gate"
  Write-Host "Phase: $Phase"
  Write-Host "Repository: $RepoRoot"

  if ($PlanOnly) {
    if ($Phase -eq "PreDeploy") {
      Write-Host "Plan: version identity -> complete PHP lint -> UTOPIA JavaScript syntax -> diff check -> local asset/Chrome self-test -> content depth -> atomic migration simulator -> shared-engine isolation -> comparison hashes -> static preview/browser QA -> canonical ZIP build -> package verification -> ZIP asset and extracted-PHP verification."
    } else {
      Write-Host "Plan: version identity -> existing package verification -> ZIP asset and extracted-PHP verification -> read-only five-language live Chrome gate -> post-release comparison hashes -> after screenshots."
    }
    Write-Host "Plan only: no QA, package build, deployment or public-site request was performed."
    return
  }

  if ($Phase -eq "PreDeploy") {
    Invoke-PhpLintTree -Php $php
    Invoke-NodeSyntaxChecks -Node $node
    Invoke-NativeStep -Name "Git whitespace/error check" -Command $git -CommandArgs @("diff", "--check")
    Invoke-NativeStep -Name "Pinned local assets, GLB geometry and Google Chrome self-test" -Command $node -CommandArgs @(
      "scripts/qa-utopia-postdeploy.mjs",
      "--version", $Version,
      "--dry-run",
      "--out", "docs/qa/utopia-postdeploy-$Version-dry-run.json"
    )
    Invoke-NativeStep -Name "Five-language content depth and parity" -Command $node -CommandArgs @(
      "scripts/qa-utopia-content-depth.mjs"
    )
    Invoke-NativeStep -Name "Atomic UTOPIA migration and recovery simulator" -Command $php -CommandArgs @(
      "-d", "error_reporting=E_ALL",
      "scripts/qa-utopia-release-migration.php"
    )
    Invoke-NativeStep -Name "Shared-engine isolation" -Command $node -CommandArgs @(
      "scripts/qa-utopia-shared-engine-isolation.mjs"
    )
    Invoke-NativeStep -Name "Pre-release comparison hash regression" -Command $node -CommandArgs @(
      "scripts/qa-utopia-comparison-regression.mjs"
    )
    Invoke-NativeStep -Name "Build exact five-language static previews" -Command $php -CommandArgs @(
      "scripts/build-utopia-static-preview.php"
    )
    Invoke-NativeStep -Name "Ten-case desktop/mobile preview browser QA" -Command $node -CommandArgs @(
      "scripts/qa-utopia-preview-browser.mjs"
    )
    Invoke-NativeStep -Name "Canonical plugin ZIP build" -Command $python -CommandArgs @(
      "scripts/build-plugin-zip.py", $Version
    )
    Invoke-NativeStep -Name "Plugin release package verification" -Command $python -CommandArgs @(
      "scripts/verify-plugin-release.py", $Version
    )
    Assert-UtopiaZip -ExpectedVersion $Version -Php $php
    Write-Host ""
    Write-Host "PASS UTOPIA $Version predeploy gate. No deployment was performed."
  } else {
    Invoke-NativeStep -Name "Existing plugin release package verification" -Command $python -CommandArgs @(
      "scripts/verify-plugin-release.py", $Version
    )
    Assert-UtopiaZip -ExpectedVersion $Version -Php $php
    Invoke-NativeStep -Name "Read-only UTOPIA live acceptance and comparison QA" -Command $node -CommandArgs @(
      "scripts/qa-utopia-postdeploy.mjs",
      "--version", $Version,
      "--site", $Site,
      "--out", "docs/qa/utopia-postdeploy-$Version.json",
      "--evidence-dir", "docs/qa/screenshots/utopia-live-$Version"
    )
    Write-Host ""
    Write-Host "PASS UTOPIA $Version postdeploy gate. The gate performed read-only public verification only."
  }
} finally {
  Pop-Location
}
