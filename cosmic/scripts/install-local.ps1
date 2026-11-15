# Installs the release build for local use: copies the app and CLI to D:\Coding\Cosmic\bin as
# cosmic.exe and cosmic-cli.exe, then registers the Claude Code MCP servers `cosmic` (headless,
# auto-save) and `cosmic-live` (bridge to an app opened with --control 9878) at that path.
#
# The binaries keep their Cargo names in target\release (effectcraft.exe, effectcraft-cli.exe) so
# upstream merges stay simple; only the installed copies are renamed. The `effectcraft` and
# `effectcraft-live` registrations (the release build, kept for comparison) are not touched.
#
# Run after `cargo build --release -p effectcraft -p effectcraft-cli`:
#   powershell -ExecutionPolicy Bypass -File cosmic/scripts/install-local.ps1

param(
    [string]$BinDir = "D:\Coding\Cosmic\bin",
    [string]$ReadRoot = "D:\Editing\EffectCraft",
    [string]$WriteRoot = "D:\Editing\EffectCraft\mcp-test",
    [int]$LivePort = 9878
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$release = Join-Path $root "target\release"
$copies = @(
    @{ from = "effectcraft.exe"; to = "cosmic.exe" },
    @{ from = "effectcraft-cli.exe"; to = "cosmic-cli.exe" }
)

foreach ($c in $copies) {
    $src = Join-Path $release $c.from
    if (-not (Test-Path $src)) { throw "$src is missing: run cargo build --release -p effectcraft -p effectcraft-cli first" }
}
New-Item -ItemType Directory -Force $BinDir | Out-Null

$running = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path.StartsWith($BinDir, [StringComparison]::OrdinalIgnoreCase) }
if ($running) {
    $names = ($running | ForEach-Object { "$($_.ProcessName) ($($_.Id))" }) -join ", "
    throw "close these first, Windows can't replace a running exe: $names (an MCP server stops when its Claude Code session ends)"
}

foreach ($c in $copies) {
    Copy-Item (Join-Path $release $c.from) (Join-Path $BinDir $c.to) -Force
    Write-Host "copied $($c.from) -> $(Join-Path $BinDir $c.to)"
}
# Copies from before the rename.
foreach ($old in "effectcraft.exe", "effectcraft-cli.exe") {
    $p = Join-Path $BinDir $old
    if (Test-Path $p) { Remove-Item $p -Force; Write-Host "removed old $p" }
}

$cli = Join-Path $BinDir "cosmic-cli.exe"
$servers = @(
    @{ name = "cosmic"; args = @("mcp", "--autosave", "--automation-read-root", $ReadRoot, "--automation-write-root", $WriteRoot) },
    @{ name = "cosmic-live"; args = @("mcp", "--bridge", "$LivePort", "--automation-read-root", $ReadRoot, "--automation-write-root", $WriteRoot) }
)
foreach ($s in $servers) {
    # Remove first so a changed path or option replaces the old registration. Windows PowerShell
    # turns a native command's stderr into an error under "Stop", and remove fails when nothing
    # is registered yet, so this one call runs under "Continue".
    $ErrorActionPreference = "Continue"
    & claude mcp remove $s.name -s user 2>&1 | Out-Null
    $ErrorActionPreference = "Stop"
    # '--' is quoted: unquoted, PowerShell drops it and Claude reads the EffectCraft options as its own.
    & claude mcp add --scope user $s.name '--' $cli @($s.args)
    if ($LASTEXITCODE -ne 0) { throw "claude mcp add $($s.name) failed" }
}

Write-Host ""
Write-Host "installed. Live mode needs the app opened with: $(Join-Path $BinDir 'cosmic.exe') --control $LivePort"
