# Digital Marketplace - non-destructive Codex skill installation diagnostic.
# Verifies files and metadata, not activation inside an authenticated Codex session.
[CmdletBinding()]
param(
    [string]$SkillsRoot = (Join-Path $HOME ".agents\skills"),
    [switch]$RunLocalScoringCheck
)
$ErrorActionPreference = "Stop"
$path = Join-Path $SkillsRoot "digital-marketplace"
$skill = Join-Path $path "SKILL.md"
$required = @(
    "SKILL.md", "AGENTS.md", "LICENSE", "DISCLAIMER.md",
    "config/business-profile.yaml", "config/scoring-weights.json",
    "workflows/discover.md", "workflows/validate.md",
    "policies/evidence-quality.md", "scripts/score_opportunities.py"
)
$problems = @()
foreach ($item in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $path $item) -PathType Leaf)) {
        $problems += "Missing installed skill file: $item"
    }
}
if (Test-Path -LiteralPath $skill -PathType Leaf) {
    $content = Get-Content -LiteralPath $skill -Raw -Encoding UTF8
    if ($content -notmatch '(?m)^name: digital-marketplace\s*$') {
        $problems += "Incorrect SKILL.md name field"
    }
    if ($content -notmatch '(?m)^description:\s*\S+') {
        $problems += "Missing SKILL.md description"
    }
    if ($content -notmatch '(?m)^---') {
        $problems += "Missing SKILL.md YAML frontmatter"
    }
}
if ($RunLocalScoringCheck -and $problems.Count -eq 0) {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        $problems += "Python executable not available for optional scoring check"
    } else {
        $example = Join-Path $path "tests/sample-opportunities.json"
        if (-not (Test-Path -LiteralPath $example -PathType Leaf)) {
            # The Codex skill ZIP intentionally excludes unit-test fixtures.
            Write-Warning "Example fixture not included in skill ZIP; skipping scoring check."
        } else {
            & python (Join-Path $path "scripts/score_opportunities.py") $example
            if ($LASTEXITCODE -ne 0) {
                $problems += "Local scoring command failed"
            }
        }
    }
}
if ($problems.Count) {
    foreach ($problem in $problems) { Write-Error $problem }
    exit 1
}
Write-Host "PASS: Digital Marketplace skill installed in $path"
Write-Host "PASS: required files, YAML identifier, and description"
Write-Host "NOT VERIFIED: whether Codex Desktop has discovered or invoked the skill."
Write-Host "Restart Codex, open a new chat, and ask: 'Use Digital Marketplace to research one US digital product idea. Cite sources, and label unknown metrics.'"
