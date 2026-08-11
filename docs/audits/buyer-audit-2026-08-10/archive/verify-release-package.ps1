param(
    [Parameter(Mandatory = $true)]
    [string]$ZipPath
)

$ErrorActionPreference = "Stop"
$zipFull = (Resolve-Path -LiteralPath $ZipPath).Path
$parent = Split-Path $zipFull -Parent
$verifyRoot = Join-Path $parent ("." + [System.IO.Path]::GetFileNameWithoutExtension($zipFull) + "-verify")
$verifyFull = [System.IO.Path]::GetFullPath($verifyRoot)
$parentFull = [System.IO.Path]::GetFullPath($parent).TrimEnd('\') + '\'
if (-not $verifyFull.StartsWith($parentFull, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Verification directory escaped the ZIP parent"
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [System.IO.Compression.ZipFile]::OpenRead($zipFull)
try {
    $seen = @{}
    foreach ($entry in $archive.Entries) {
        $name = $entry.FullName.Replace('\', '/')
        $segments = $name.Split('/')
        if ($name.StartsWith('/') -or $name -match '^[A-Za-z]:' -or $segments -contains '..') {
            throw "Unsafe ZIP entry: $name"
        }
        $key = $name.ToLowerInvariant()
        if ($seen.ContainsKey($key)) { throw "Duplicate ZIP entry: $name" }
        $seen[$key] = $true
    }
    $entryCount = $archive.Entries.Count
} finally {
    $archive.Dispose()
}

if (Test-Path -LiteralPath $verifyFull) {
    Remove-Item -LiteralPath $verifyFull -Recurse -Force
}
New-Item -ItemType Directory -Path $verifyFull | Out-Null

try {
    [System.IO.Compression.ZipFile]::ExtractToDirectory($zipFull, $verifyFull)
    $roots = @(Get-ChildItem -LiteralPath $verifyFull -Directory)
    if ($roots.Count -ne 1) { throw "Expected exactly one package root; found $($roots.Count)" }
    $root = $roots[0].FullName
    foreach ($required in @("README-FIRST.md", "report\report.html", "MANIFEST.sha256", "PACKAGE-INVENTORY.csv", "PACKAGE-VERIFICATION.md")) {
        if (-not (Test-Path -LiteralPath (Join-Path $root $required) -PathType Leaf)) {
            throw "Required file missing after extraction: $required"
        }
    }

    $packageName = Split-Path $root -Leaf
    $verificationPath = Join-Path $root "PACKAGE-VERIFICATION.md"
    $strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)
    $verificationText = $strictUtf8.GetString([System.IO.File]::ReadAllBytes($verificationPath))
    if ([regex]::IsMatch($verificationText, '[\x00-\x08\x0B-\x1F\x7F]')) {
        throw "PACKAGE-VERIFICATION.md contains a forbidden C0/DEL control character"
    }
    if ($verificationText.Contains('$packageName') -or $verificationText.Contains('$(Get-Date')) {
        throw "PACKAGE-VERIFICATION.md contains an unresolved build placeholder"
    }
    $verificationLines = @($verificationText -split "`n")
    $expectedPackageLine = '- Package: `' + $packageName + '`'
    if (@($verificationLines | Where-Object { $_ -eq $expectedPackageLine }).Count -ne 1) {
        throw "PACKAGE-VERIFICATION.md does not identify the exact package root"
    }
    $builtLines = @($verificationLines | Where-Object { $_.StartsWith('- Built: ') })
    if ($builtLines.Count -ne 1 -or $builtLines[0] -notmatch '^- Built: `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})`$') {
        throw "PACKAGE-VERIFICATION.md has an invalid or unresolved build timestamp"
    }
    foreach ($expectedLine in @(
        '- Primary entry point: `report/report.html`',
        '- Developer entry point: `README-FIRST.md`'
    )) {
        if (@($verificationLines | Where-Object { $_ -eq $expectedLine }).Count -ne 1) {
            throw "PACKAGE-VERIFICATION.md is missing an exact entry point: $expectedLine"
        }
    }
    $countLines = @($verificationLines | Where-Object { $_.StartsWith('- Files before this record, inventory and manifest: ') })
    if ($countLines.Count -ne 1 -or $countLines[0] -notmatch '^.*: (\d+)$') {
        throw "PACKAGE-VERIFICATION.md has an invalid file-count record"
    }
    $recordedPreRecordCount = [int]$Matches[1]
    $actualPreRecordCount = @(Get-ChildItem -LiteralPath $root -Recurse -File).Count - 3
    if ($recordedPreRecordCount -ne $actualPreRecordCount) {
        throw "PACKAGE-VERIFICATION.md file count mismatch: recorded=$recordedPreRecordCount actual=$actualPreRecordCount"
    }

    $manifestPath = Join-Path $root "MANIFEST.sha256"
    $manifestCount = 0
    $manifestPaths = @{}
    foreach ($line in Get-Content -LiteralPath $manifestPath) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if ($line -notmatch '^([0-9a-fA-F]{64}) \*(.+)$') { throw "Malformed manifest line: $line" }
        $expected = $Matches[1].ToLowerInvariant()
        $relative = $Matches[2].Replace('/', '\')
        $candidate = [System.IO.Path]::GetFullPath((Join-Path $root $relative))
        $rootPrefix = [System.IO.Path]::GetFullPath($root).TrimEnd('\') + '\'
        if (-not $candidate.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Manifest path escaped package root: $relative"
        }
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) { throw "Manifest file missing: $relative" }
        $actual = (Get-FileHash -LiteralPath $candidate -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -ne $expected) { throw "Manifest hash mismatch: $relative" }
        $manifestKey = $relative.Replace('\', '/').ToLowerInvariant()
        if ($manifestPaths.ContainsKey($manifestKey)) { throw "Duplicate manifest path: $relative" }
        $manifestPaths[$manifestKey] = $true
        $manifestCount++
    }

    $manifestCandidates = @(Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object {
        $_.FullName -ne $manifestPath
    })
    if ($manifestCandidates.Count -ne $manifestPaths.Count) {
        throw "Manifest completeness mismatch: files=$($manifestCandidates.Count), manifest=$($manifestPaths.Count)"
    }
    foreach ($file in $manifestCandidates) {
        $relative = $file.FullName.Substring($root.Length + 1).Replace('\', '/').ToLowerInvariant()
        if (-not $manifestPaths.ContainsKey($relative)) { throw "File is not covered by manifest: $relative" }
    }

    $inventoryPath = Join-Path $root "PACKAGE-INVENTORY.csv"
    $inventory = @(Import-Csv -LiteralPath $inventoryPath)
    $inventoryPaths = @{}
    foreach ($row in $inventory) {
        $relative = ([string]$row.path).Replace('\', '/')
        if ([string]::IsNullOrWhiteSpace($relative)) { throw "Inventory contains a blank path" }
        $key = $relative.ToLowerInvariant()
        if ($inventoryPaths.ContainsKey($key)) { throw "Duplicate inventory path: $relative" }
        $candidate = [System.IO.Path]::GetFullPath((Join-Path $root $relative.Replace('/', '\')))
        $rootPrefix = [System.IO.Path]::GetFullPath($root).TrimEnd('\') + '\'
        if (-not $candidate.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Inventory path escaped package root: $relative"
        }
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) { throw "Inventory file missing: $relative" }
        $file = Get-Item -LiteralPath $candidate
        $hash = (Get-FileHash -LiteralPath $candidate -Algorithm SHA256).Hash.ToLowerInvariant()
        if ([long]$row.bytes -ne $file.Length -or ([string]$row.sha256).ToLowerInvariant() -ne $hash) {
            throw "Inventory metadata mismatch: $relative"
        }
        $inventoryPaths[$key] = $true
    }
    $inventoryCandidates = @(Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object {
        $_.FullName -notin @($manifestPath, $inventoryPath)
    })
    if ($inventoryCandidates.Count -ne $inventoryPaths.Count) {
        throw "Inventory completeness mismatch: files=$($inventoryCandidates.Count), inventory=$($inventoryPaths.Count)"
    }
    foreach ($file in $inventoryCandidates) {
        $relative = $file.FullName.Substring($root.Length + 1).Replace('\', '/').ToLowerInvariant()
        if (-not $inventoryPaths.ContainsKey($relative)) { throw "File is not covered by inventory: $relative" }
    }

    $csvCount = 0
    foreach ($file in Get-ChildItem -LiteralPath $root -Recurse -Filter *.csv) {
        $rows = @(Import-Csv -LiteralPath $file.FullName)
        if ($rows.Count -eq 0) { throw "CSV has no data rows: $($file.FullName)" }
        $csvCount++
    }

    $jsonCount = 0
    foreach ($file in Get-ChildItem -LiteralPath $root -Recurse -Filter *.json) {
        Get-Content -Raw -LiteralPath $file.FullName | ConvertFrom-Json | Out-Null
        $jsonCount++
    }

    $secretPatterns = @(
        ('NadLan' + '2026'),
        'pk\.eyJ[A-Za-z0-9._-]{20,}',
        'sk_(?:live|test)_[A-Za-z0-9]{12,}',
        'ghp_[A-Za-z0-9]{30,}',
        'AIza[0-9A-Za-z_-]{30,}',
        '-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'
    )
    $textExtensions = @('.md', '.txt', '.csv', '.json', '.mjs', '.js', '.css', '.php', '.html', '.ps1')
    $textFiles = Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object {
        $_.Extension.ToLowerInvariant() -in $textExtensions
    }
    foreach ($pattern in $secretPatterns) {
        $matches = @($textFiles | Select-String -Pattern $pattern)
        if ($matches.Count -gt 0) { throw "Sensitive pattern found: $pattern in $($matches[0].Path)" }
    }

    $nodeFiles = @(Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object { $_.Extension -in @('.js', '.mjs') })
    foreach ($file in $nodeFiles) {
        & node --check $file.FullName | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "JavaScript syntax failed: $($file.FullName)" }
    }
    $phpFiles = @(Get-ChildItem -LiteralPath (Join-Path $root "proposed-code") -Filter *.php -File)
    foreach ($file in $phpFiles) {
        & php -l $file.FullName | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "PHP syntax failed: $($file.FullName)" }
    }

    $jsFixtureFiles = @(Get-ChildItem -LiteralPath (Join-Path $root "proposed-code") -Filter *.fixture.test.js -File)
    foreach ($file in $jsFixtureFiles) {
        & node $file.FullName | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "JavaScript proposal fixture failed: $($file.FullName)" }
    }
    $browserFixtureFiles = @(Get-ChildItem -LiteralPath (Join-Path $root "proposed-code") -Filter *.browser.fixture.mjs -File)
    foreach ($file in $browserFixtureFiles) {
        & node $file.FullName | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "Real-browser proposal fixture failed: $($file.FullName)" }
    }
    $phpFixtureFiles = @(Get-ChildItem -LiteralPath (Join-Path $root "proposed-code") -Filter *.fixture.test.php -File)
    foreach ($file in $phpFixtureFiles) {
        & php $file.FullName | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "PHP proposal fixture failed: $($file.FullName)" }
    }
    $sandboxCacheFixture = Join-Path $root "proposed-code\commercial-sandbox-integration.fixture.test.php"
    if (-not (Test-Path -LiteralPath $sandboxCacheFixture -PathType Leaf)) {
        throw "Sandbox cache-conflict fixture is missing: $sandboxCacheFixture"
    }
    & php $sandboxCacheFixture --predefined-cache-false | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Sandbox cache-conflict fixture failed: $sandboxCacheFixture --predefined-cache-false"
    }
    $phpFixtureExecutionCount = $phpFixtureFiles.Count + 1

    [pscustomobject]@{
        ok = $true
        zip = $zipFull
        bytes = (Get-Item -LiteralPath $zipFull).Length
        sha256 = (Get-FileHash -LiteralPath $zipFull -Algorithm SHA256).Hash.ToLowerInvariant()
        entries = $entryCount
        manifest_files_verified = $manifestCount
        csv_files_parsed = $csvCount
        json_files_parsed = $jsonCount
        javascript_files_checked = $nodeFiles.Count
        php_files_checked = $phpFiles.Count
        javascript_fixtures_executed = $jsFixtureFiles.Count
        browser_fixtures_executed = $browserFixtureFiles.Count
        php_fixtures_executed = $phpFixtureExecutionCount
        sensitive_pattern_matches = 0
    } | ConvertTo-Json -Compress
} finally {
    if (Test-Path -LiteralPath $verifyFull) {
        Remove-Item -LiteralPath $verifyFull -Recurse -Force
    }
}
