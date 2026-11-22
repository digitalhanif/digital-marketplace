# Digital Marketplace - Windows Codex installer
# Run from the extracted project directory in PowerShell.
$ErrorActionPreference = "Stop"
$source = (Get-Location).Path
if (-not (Test-Path -LiteralPath (Join-Path $source "SKILL.md") -PathType Leaf)) {
    throw "Run this script inside the extracted folder containing SKILL.md"
}
$skillsDir = Join-Path $HOME ".agents\skills"
$target = Join-Path $skillsDir "digital-marketplace"
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null

# Stage a complete copy before touching any previous installation.
$staging = Join-Path $skillsDir ("digital-marketplace-staging-" + [guid]::NewGuid().ToString("N"))
$backup = $null
$installed = $false
try {
    New-Item -ItemType Directory -Path $staging | Out-Null
    # Install only audited release files; never copy arbitrary local secrets.
    $releaseFiles = @(
        "SKILL.md", "AGENTS.md", "README.md", "LICENSE", "DISCLAIMER.md",
        "SECURITY.md", "config/business-profile.yaml",
        "config/data-sources.md", "config/scoring-weights.json"
    )
    $releaseDirs = @("agents", "workflows", "policies", "scripts", "templates")
    $releasePatterns = @{
        agents = "*.md"; workflows = "*.md"; policies = "*.md";
        scripts = "*.py"; templates = "*.md,*.csv"
    }
    foreach ($relative in $releaseFiles) {
        $file = Join-Path $source $relative
        if (-not (Test-Path -LiteralPath $file -PathType Leaf)) {
            throw "Missing required release file: $relative"
        }
        $destination = Join-Path $staging $relative
        New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
        Copy-Item -LiteralPath $file -Destination $destination -Force -ErrorAction Stop
    }
    foreach ($directory in $releaseDirs) {
        $folder = Join-Path $source $directory
        if (-not (Test-Path -LiteralPath $folder -PathType Container)) {
            throw "Missing required release folder: $directory"
        }
        $destination = Join-Path $staging $directory
        New-Item -ItemType Directory -Force -Path $destination | Out-Null
        $patterns = $releasePatterns[$directory].Split(",")
        foreach ($pattern in $patterns) {
            Get-ChildItem -LiteralPath $folder -File -Filter $pattern |
                ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $destination -Force -ErrorAction Stop }
        }
    }
    if (-not (Test-Path -LiteralPath (Join-Path $staging "SKILL.md") -PathType Leaf)) {
        throw "Staging verification failed: SKILL.md missing"
    }
    if (Test-Path -LiteralPath $target) {
        $backup = "$target-backup-$(Get-Date -Format yyyyMMdd-HHmmss)-$([guid]::NewGuid().ToString('N').Substring(0,8))"
        Move-Item -LiteralPath $target -Destination $backup -ErrorAction Stop
    }
    Move-Item -LiteralPath $staging -Destination $target -ErrorAction Stop
    $installed = $true
    Write-Host "Skill installed at $target. Restart Codex to load it."
    if ($backup) { Write-Host "Previous installation backed up at $backup" }
}
catch {
    if (-not $installed -and $backup -and (Test-Path -LiteralPath $backup) -and -not (Test-Path -LiteralPath $target)) {
        Move-Item -LiteralPath $backup -Destination $target -ErrorAction Stop
        Write-Warning "Previous installation restored after installation failure."
    }
    throw
}
finally {
    if (Test-Path -LiteralPath $staging) {
        Remove-Item -LiteralPath $staging -Recurse -Force
    }
}
# No older skill directories are modified or enumerated automatically.
# Review duplicate installations manually after verifying Digital Marketplace.
