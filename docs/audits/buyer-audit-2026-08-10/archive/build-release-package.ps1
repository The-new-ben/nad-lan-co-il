param(
    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"

$sourceRoot = (Resolve-Path (Split-Path $PSScriptRoot -Parent)).Path
$packageName = Split-Path $sourceRoot -Leaf
$deliverablesParent = Split-Path $sourceRoot -Parent
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $deliverablesParent ($packageName + ".zip")
}
$outputFull = [System.IO.Path]::GetFullPath($OutputPath)
$stageContainer = Join-Path $deliverablesParent ("." + $packageName + "-stage")
$stageRoot = Join-Path $stageContainer $packageName

function Assert-ExactChildPath([string]$Candidate, [string]$Parent, [string]$Label) {
    $candidateFull = [System.IO.Path]::GetFullPath($Candidate)
    $parentFull = [System.IO.Path]::GetFullPath($Parent).TrimEnd('\') + '\'
    if (-not $candidateFull.StartsWith($parentFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "$Label is outside the intended parent: $candidateFull"
    }
    return $candidateFull
}

$stageContainer = Assert-ExactChildPath $stageContainer $deliverablesParent "Stage directory"
$stageRoot = Assert-ExactChildPath $stageRoot $stageContainer "Stage root"

if (Test-Path -LiteralPath $stageContainer) {
    Remove-Item -LiteralPath $stageContainer -Recurse -Force
}
New-Item -ItemType Directory -Path $stageRoot | Out-Null

function Copy-RequiredFile([string]$RelativePath, [string]$DestinationRelativePath = "") {
    $source = Join-Path $sourceRoot $RelativePath
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
        throw "Required package file is missing: $RelativePath"
    }
    if ([string]::IsNullOrWhiteSpace($DestinationRelativePath)) {
        $DestinationRelativePath = $RelativePath
    }
    $destination = Join-Path $stageRoot $DestinationRelativePath
    New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination
}

function Copy-RequiredDirectory([string]$RelativePath) {
    $source = Join-Path $sourceRoot $RelativePath
    if (-not (Test-Path -LiteralPath $source -PathType Container)) {
        throw "Required package directory is missing: $RelativePath"
    }
    $destination = Join-Path $stageRoot $RelativePath
    New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination -Recurse
}

Copy-RequiredFile "README-FIRST.md"
Copy-RequiredFile "migration-and-qa.md"
foreach ($directory in @("data", "research", "proposed-code", "ux", "archive")) {
    Copy-RequiredDirectory $directory
}

New-Item -ItemType Directory -Path (Join-Path $stageRoot "evidence") -Force | Out-Null
foreach ($file in Get-ChildItem -LiteralPath (Join-Path $sourceRoot "evidence") -File) {
    if ($file.Extension -in @(".png", ".txt", ".mjs", ".md")) {
        Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $stageRoot "evidence")
    }
}
Copy-RequiredDirectory "evidence\screenshots"
Copy-RequiredDirectory "evidence\sanitized"

$reportFiles = @(
    "report\artifact.json",
    "report\build-report-artifact.mjs",
    "report\finalize-portable-report.mjs",
    "report\inspect-report.mjs",
    "report\report.html",
    "report\report-desktop.png",
    "report\report-mobile.png",
    "report\report-inspection.json",
    "report\report-verification.json"
)
foreach ($file in $reportFiles) { Copy-RequiredFile $file }

$preRecordCount = @(Get-ChildItem -LiteralPath $stageRoot -Recurse -File).Count
$builtAt = Get-Date -Format 'yyyy-MM-ddTHH:mm:ssK'
$verificationLines = @(
    '# Package verification record',
    '',
    ('- Package: `{0}`' -f $packageName),
    ('- Built: `{0}`' -f $builtAt),
    ('- Files before this record, inventory and manifest: {0}' -f $preRecordCount),
    '- Raw browser JSON with client tokens/local paths: excluded',
    '- Structure-preserving sanitized JSON: included',
    '- Prior unit-journey ZIP: included byte-for-byte under `archive/`',
    '- Live-site or product-repository mutations: none',
    '- Primary entry point: `report/report.html`',
    '- Developer entry point: `README-FIRST.md`',
    '',
    'The outer ZIP is verified again after creation by reopening it, rejecting absolute/traversal/duplicate entries, extracting it to a dedicated temporary directory, validating `MANIFEST.sha256`, parsing all CSV/JSON files, checking code syntax and executing the packaged synthetic proposal fixtures. After upload, delivery must separately download the remote object and compare its SHA-256 with the local archive before giving the link to the user; that post-upload proof cannot truthfully be embedded in this pre-upload record.'
)
$verificationText = [string]::Join("`n", $verificationLines) + "`n"
[System.IO.File]::WriteAllText((Join-Path $stageRoot "PACKAGE-VERIFICATION.md"), $verificationText, [System.Text.UTF8Encoding]::new($false))

$inventoryRows = foreach ($file in Get-ChildItem -LiteralPath $stageRoot -Recurse -File | Sort-Object FullName) {
    $relative = $file.FullName.Substring($stageRoot.Length + 1).Replace('\', '/')
    $category = ($relative -split '/', 2)[0]
    [pscustomobject]@{
        path = $relative
        category = $category
        bytes = $file.Length
        sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    }
}
$inventoryPath = Join-Path $stageRoot "PACKAGE-INVENTORY.csv"
$inventoryRows | Export-Csv -LiteralPath $inventoryPath -NoTypeInformation -Encoding utf8

$manifestFiles = Get-ChildItem -LiteralPath $stageRoot -Recurse -File | Sort-Object FullName
$manifestLines = foreach ($file in $manifestFiles) {
    $relative = $file.FullName.Substring($stageRoot.Length + 1).Replace('\', '/')
    $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "$hash *$relative"
}
$manifestPath = Join-Path $stageRoot "MANIFEST.sha256"
[System.IO.File]::WriteAllLines($manifestPath, $manifestLines, [System.Text.UTF8Encoding]::new($false))

if (Test-Path -LiteralPath $outputFull) {
    Remove-Item -LiteralPath $outputFull -Force
}
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory(
    $stageContainer,
    $outputFull,
    [System.IO.Compression.CompressionLevel]::Optimal,
    $false
)

$zip = [System.IO.Compression.ZipFile]::OpenRead($outputFull)
try {
    $names = @{}
    foreach ($entry in $zip.Entries) {
        $name = $entry.FullName.Replace('\', '/')
        $segments = $name.Split('/')
        if ($name.StartsWith('/') -or $name -match '^[A-Za-z]:' -or $segments -contains '..') {
            throw "Unsafe ZIP entry: $name"
        }
        $key = $name.ToLowerInvariant()
        if ($names.ContainsKey($key)) { throw "Duplicate ZIP entry: $name" }
        $names[$key] = $true
    }
    $requiredEntry = "$packageName/report/report.html".ToLowerInvariant()
    if (-not $names.ContainsKey($requiredEntry)) { throw "Final report is missing from ZIP" }
} finally {
    $zip.Dispose()
}

Remove-Item -LiteralPath $stageContainer -Recurse -Force

[pscustomobject]@{
    path = $outputFull
    bytes = (Get-Item -LiteralPath $outputFull).Length
    sha256 = (Get-FileHash -LiteralPath $outputFull -Algorithm SHA256).Hash.ToLowerInvariant()
} | ConvertTo-Json -Compress
