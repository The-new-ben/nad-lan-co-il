# Aurelia asset prep: PNG renders -> optimized JPEG via System.Drawing; GLB copied.
Add-Type -AssemblyName System.Drawing
$src = 'C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\5599c889-017e-4627-9f31-eb54e990a07b\scratchpad\aurelia\zip\aurelia-master-recipe-1.0.0-rc3\01-DEMO-LAB\assets'
$out = 'C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\5599c889-017e-4627-9f31-eb54e990a07b\scratchpad\aurelia\wp-assets'
New-Item -ItemType Directory -Force $out | Out-Null

function Convert-Jpeg([string]$in, [string]$outName, [int]$maxW, [long]$quality) {
    $img = [System.Drawing.Image]::FromFile($in)
    $w = $img.Width; $h = $img.Height
    if ($w -gt $maxW) { $nh = [int]([math]::Round($h * ($maxW / $w))); $nw = $maxW } else { $nw = $w; $nh = $h }
    $bmp = New-Object System.Drawing.Bitmap($nw, $nh)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.DrawImage($img, 0, 0, $nw, $nh)
    $enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
    $p = New-Object System.Drawing.Imaging.EncoderParameters(1)
    $p.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, $quality)
    $dest = Join-Path $out $outName
    $bmp.Save($dest, $enc, $p)
    $g.Dispose(); $bmp.Dispose(); $img.Dispose()
    "{0}  {1}x{2} -> {3:N0}b" -f $outName, $nw, $nh, (Get-Item $dest).Length
}

# marketing images (downscale to 1800px)
Convert-Jpeg "$src\aurelia-exterior-hero-v1.png"            'aurelia-tower-sde-dov-hero.jpg'      1800 82
Convert-Jpeg "$src\aurelia-interior-living-v1.png"          'aurelia-living-room-interior.jpg'    1800 82
Convert-Jpeg "$src\aurelia-amenities-wellness-v1.png"       'aurelia-wellness-amenities.jpg'      1800 82
Convert-Jpeg "$src\aurelia-environment-aerial-v1.png"       'aurelia-quarter-aerial-view.jpg'     1800 82
# panoramas keep full width (pannellum quality)
Convert-Jpeg "$src\aurelia-interior-panorama-v1.png"        'aurelia-living-panorama-360.jpg'     4096 84
Convert-Jpeg "$src\aurelia-master-bedroom-panorama-v1.png"  'aurelia-bedroom-panorama-360.jpg'    4096 84
Convert-Jpeg "$src\aurelia-pool-panorama-v1.png"            'aurelia-pool-panorama-360.jpg'       4096 84
Convert-Jpeg "$src\aurelia-gym-panorama-v1.png"             'aurelia-gym-panorama-360.jpg'        4096 84

Copy-Item "$src\aurelia-tower-semantic-v2.glb" "$out\aurelia-tower-semantic-v2.glb" -Force
"glb copied: $((Get-Item "$out\aurelia-tower-semantic-v2.glb").Length)b"

# plans: SVG -> PNG via headless chrome
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$plans = @(
    @{svg='aurelia-plan-2br-v1.svg';       png='aurelia-plan-2br.png'},
    @{svg='aurelia-plan-3br-v1.svg';       png='aurelia-plan-3br.png'},
    @{svg='aurelia-plan-4br-v1.svg';       png='aurelia-plan-4br.png'},
    @{svg='aurelia-plan-5br-v1.svg';       png='aurelia-plan-5br.png'},
    @{svg='aurelia-plan-penthouse-v1.svg'; png='aurelia-plan-penthouse.png'},
    @{svg='aurelia-site-plan-v1.svg';      png='aurelia-site-plan.png'}
)
foreach ($pl in $plans) {
    $svgPath = Join-Path $src $pl.svg
    $dest = Join-Path $out $pl.png
    & $chrome --headless=new --disable-gpu --hide-scrollbars --window-size=1400,1000 --default-background-color=FFF8F0FF --screenshot="$dest" ("file:///" + ($svgPath -replace '\\','/')) 2>$null | Out-Null
    if (Test-Path $dest) { "{0}  {1:N0}b" -f $pl.png, (Get-Item $dest).Length } else { "FAILED: $($pl.png)" }
}
