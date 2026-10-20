<#
.SYNOPSIS
  Install the Claude skill/plugin pack for Project 4 (Enterprise OS on ERPNext). See README.md.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File tools\claude-skills\install.ps1 -DryRun
  powershell -ExecutionPolicy Bypass -File tools\claude-skills\install.ps1
  powershell -ExecutionPolicy Bypass -File tools\claude-skills\install.ps1 -Uninstall
  powershell -ExecutionPolicy Bypass -File tools\claude-skills\install.ps1 -Trust frappe-org,anthropic

.NOTES
  -DryRun    fetch + verify everything, change nothing in ~/.claude or Claude Code settings
  -Uninstall remove what this pack installed (skills carrying the pack marker, and the listed plugins)
  -Force     replace a skill folder that already exists
  -Trust     only items whose "trust" in skills.json is listed (frappe-org, anthropic, security-firm, partner, individual)
#>
param([switch]$DryRun, [switch]$Uninstall, [switch]$Force, [string[]]$Trust)

$ErrorActionPreference = 'Stop'
$manifest  = Get-Content -Raw -Encoding UTF8 (Join-Path $PSScriptRoot 'skills.json') | ConvertFrom-Json
$Trust     = @($Trust | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })   # -File passes "a,b" as one string
$items     = @($manifest.items | Where-Object { -not $Trust -or $Trust -contains $_.trust })
if (-not $items) { throw "no items match -Trust $($Trust -join ',')" }
$skillsDir = Join-Path $HOME '.claude\skills'
$marker    = '.claude-skills-pack'
$tag       = if ($DryRun) { '[dry-run, not done] ' } else { '' }
$summary   = New-Object System.Collections.Generic.List[string]
$temps     = @{}

function Note([string]$msg) { $summary.Add($msg); Write-Host $msg }

function Get-Checkout([string]$repo, [string]$commit) {
    $key = "$repo@$commit"
    if ($temps.ContainsKey($key)) { return $temps[$key] }
    $dir = Join-Path ([IO.Path]::GetTempPath()) ('claude-skills-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
    git init -q $dir | Out-Null
    git -C $dir fetch -q --depth 1 $repo $commit
    if ($LASTEXITCODE -ne 0) { throw "cannot fetch $commit from $repo" }
    git -C $dir checkout -q FETCH_HEAD
    $temps[$key] = $dir
    return $dir
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'git not found - install Git for Windows first' }
$claude = Get-Command claude -ErrorAction SilentlyContinue

try {
    # ---------- skills copied into ~/.claude/skills (skill-copy: pinned upstream commit; skill-local: adapted copy kept in this pack) ----------
    foreach ($it in @($items | Where-Object { $_.kind -in 'skill-copy', 'skill-local' })) {
        $dest = Join-Path $skillsDir $it.id
        $ours = Test-Path (Join-Path $dest $marker)

        if ($Uninstall) {
            if (-not $ours) { Note "skip  skill $($it.id): not installed by this pack"; continue }
            if (-not $DryRun) { Remove-Item -Recurse -Force $dest }
            Note "${tag}removed skill $($it.id)"
            continue
        }

        if ((Test-Path $dest) -and -not $Force) { Note "skip  skill $($it.id): already at $dest (use -Force to replace)"; continue }

        $local  = $it.kind -eq 'skill-local'
        $src    = if ($local) { Join-Path $PSScriptRoot $it.path } else { Join-Path (Get-Checkout $it.repo $it.commit) $it.path }
        $origin = if ($local) { "$($it.upstream)@$($it.upstream_commit) (adapted, kept in pack)" } else { "$($it.repo)@$($it.commit)" }
        $md  = Join-Path $src 'SKILL.md'
        if (-not (Test-Path $md)) { throw "$($it.id): SKILL.md missing at $($it.path)" }
        $name = Select-String -Path $md -Pattern '^name:\s*(\S+)' | Select-Object -First 1
        if (-not $name -or $name.Matches[0].Groups[1].Value -ne $it.id) { throw "$($it.id): SKILL.md name does not match the folder" }

        if (-not $DryRun) {
            if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
            New-Item -ItemType Directory -Force $skillsDir | Out-Null
            Copy-Item -Recurse $src $dest
            Set-Content -Encoding ASCII (Join-Path $dest $marker) $origin
        }
        Note "${tag}installed skill $($it.id) <- $origin -> $dest"
    }

    # ---------- plugins from marketplaces ----------
    $plugins = @($items | Where-Object { $_.kind -eq 'plugin' })

    foreach ($mname in @($plugins | Select-Object -ExpandProperty marketplace -Unique)) {
        $m = $manifest.marketplaces.$mname
        $head = (git ls-remote "https://github.com/$($m.source).git" HEAD) -split '\s+' | Select-Object -First 1
        if ($head -and $head -ne $m.reviewed_commit) {
            Note "note  marketplace ${mname} changed since review ($($m.reviewed_commit.Substring(0, 7)) -> $($head.Substring(0, 7))) - read its changes before relying on it"
        }
    }

    if (-not $claude) {
        Note 'claude CLI not found. In the desktop app open: + > Plugins > Add plugin, then install:'
        foreach ($p in $plugins) { Note "      $($p.plugin)@$($p.marketplace)   ($($p.publisher))" }
        Note "      Third-party marketplace to add first: $($manifest.marketplaces.trailofbits.source)"
    }
    else {
        $known = (& claude plugin marketplace list 2>$null | Out-String)
        foreach ($mname in @($plugins | Select-Object -ExpandProperty marketplace -Unique)) {
            if ($Uninstall -or $known -match [regex]::Escape($mname)) { continue }
            $source = $manifest.marketplaces.$mname.source
            if (-not $DryRun) {
                & claude plugin marketplace add $source
                if ($LASTEXITCODE -ne 0) { throw "cannot add marketplace $source" }
            }
            Note "${tag}added marketplace $mname ($source)"
        }
        foreach ($p in $plugins) {
            $full = "$($p.plugin)@$($p.marketplace)"
            $verb = if ($Uninstall) { 'uninstall' } else { 'install' }
            if (-not $DryRun) {
                & claude plugin $verb $full
                if ($LASTEXITCODE -ne 0) { Note "FAIL  plugin $verb ${full} (exit $LASTEXITCODE)"; continue }
            }
            Note "${tag}${verb}ed plugin $full"
        }
    }

    if (-not $Uninstall) {
        $py = $false
        try { $v = & python3 --version 2>&1; $py = ($LASTEXITCODE -eq 0) -and ("$v" -match 'Python 3') } catch { $py = $false }
        if (-not $py) { Note 'warn  "python3" is not a real Python here - claude-security needs it (see README: python3 fix)' }
    }
}
finally {
    foreach ($d in $temps.Values) { Remove-Item -Recurse -Force $d -ErrorAction SilentlyContinue }
}

Write-Host ''
Write-Host '---- summary ----'
$summary | ForEach-Object { Write-Host $_ }
if (-not $Uninstall -and -not $DryRun) {
    Write-Host ''
    Write-Host 'Next: start a new Claude Code session (or run /reload-plugins).'
    if ($items.id -contains 'context7') { Write-Host '      context7 asks you to sign in the first time it is used.' }
}
