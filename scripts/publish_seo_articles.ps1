param(
    [string]$File1 = "C:\Users\pro\nad-lan\content\guides\buying-real-estate-israel-foreign-investor-2026.md",
    [string]$File2 = "C:\Users\pro\nad-lan\docs\seo-content\2026-07-foreign-investor-guide.md"
)

$user = "nadlvzld_admin"
$pass = "A0Fv r6l8 wj1Q syhH NXtG lKE6"
$base = "https://nad-lan.co.il/wp-json"
$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${user}:${pass}"))
$headers = @{ 
    Authorization = "Basic $cred"
    "Content-Type" = "application/json; charset=utf-8"
}

function Publish-Article {
    param([string]$FilePath)
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "File not found: $FilePath" -ForegroundColor Red
        return
    }
    
    Write-Host "Processing $FilePath..."
    # Force UTF8 encoding
    $content = Get-Content -Path $FilePath -Raw -Encoding UTF8
    
    $title = ""
    $slug = ""
    $keyword = ""
    
    if ($content -match '(?s)^---\r?\n(.*?)\r?\n---\r?\n(.*)$') {
        $frontmatter = $matches[1]
        $body = $matches[2]
        
        if ($frontmatter -match 'title:\s*"(.*?)"') { $title = $matches[1] }
        if ($frontmatter -match 'slug:\s*(.*?)\r?\n') { $slug = $matches[1] }
        if ($frontmatter -match 'primary_keyword:\s*"(.*?)"') { $keyword = $matches[1] }
    } else {
        Write-Host "Could not parse frontmatter for $FilePath" -ForegroundColor Red
        return
    }
    
    $htmlBody = $body -replace '\r?\n\r?\n', '</p><p>'
    $htmlBody = "<p>$htmlBody</p>"
    
    $postData = @{
        title = $title
        content = $htmlBody
        status = "publish"
        slug = $slug
    } | ConvertTo-Json -Depth 5 -Compress
    
    # We must explicitly convert the JSON string to UTF8 bytes before sending
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($postData)
    
    try {
        $resp = Invoke-RestMethod -Uri "$base/wp/v2/posts" -Method Post -Headers $headers -Body $utf8Bytes
        Write-Host "Success! Post ID: $($resp.id) URL: $($resp.link)" -ForegroundColor Green
    } catch {
        Write-Host "Failed to publish post: $_" -ForegroundColor Red
        if ($_.ErrorDetails) {
            Write-Host "Error Details: $($_.ErrorDetails.Message)"
        }
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response Body: $responseBody" -ForegroundColor Yellow
    }
}

Publish-Article -FilePath $File1
Publish-Article -FilePath $File2

Write-Host "Done."
