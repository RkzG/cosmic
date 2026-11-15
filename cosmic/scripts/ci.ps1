# Cosmic's full check before a phase PR is merged: the stages of `cargo xtask ci` without wasm
# (Cosmic targets Windows desktop only) and without the Linux-only audio backend check.
#
# Each stage runs as its own command instead of inside `cargo xtask ci`: on Windows the test
# stage rebuilds xtask.exe while xtask is running it, which fails ("failed to remove file").
# Tests run through cargo-nextest like upstream CI, so the UI tests that share the GPU run one
# at a time (.config/nextest.toml). Every stage runs even after a failure; the exit code is 1 if
# any failed. Logs go to -LogDir (default target/cosmic-ci).
#
#   powershell -ExecutionPolicy Bypass -File cosmic/scripts/ci.ps1

param([string]$LogDir = "")

$ErrorActionPreference = "Continue"
# No incremental cache: a full run builds every crate once anyway, and the cache took ~17 GB of
# disk (a full disk failed the 2026-11-15 run). Daily `cargo test -p` runs keep it.
$env:CARGO_INCREMENTAL = "0"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $root
if (-not $LogDir) { $LogDir = Join-Path $root "target\cosmic-ci" }
New-Item -ItemType Directory -Force $LogDir | Out-Null

$stages = @(
    @{ name = "fmt";          cmd = "cargo fmt --check" },
    @{ name = "clippy";       cmd = "cargo clippy --workspace --all-targets -- -D warnings" },
    # Double quotes around the filter: cmd.exe does not treat single quotes as quoting.
    @{ name = "tests";        cmd = 'cargo nextest run --workspace --lib --bins --tests --no-fail-fast -E "not package(effectcraft-gpu)"' },
    @{ name = "gpu-tests";    cmd = "cargo test -p effectcraft-gpu --lib --no-fail-fast" },
    @{ name = "doctests";     cmd = "cargo test --workspace --doc --no-fail-fast" },
    @{ name = "pdf-deps";     cmd = "cargo xtask pdf-deps" },
    @{ name = "lock-patches"; cmd = "cargo xtask lock-patches" },
    @{ name = "layers";       cmd = "cargo xtask layers" },
    @{ name = "assets";       cmd = "cargo xtask assets" },
    @{ name = "rebrand";      cmd = "python -I cosmic/tools/rebrand.py --check" }
)

$failed = @()
foreach ($s in $stages) {
    $log = Join-Path $LogDir "$($s.name).log"
    $start = Get-Date
    Write-Host "=== $($start.ToString('HH:mm:ss')) $($s.name): $($s.cmd)"
    # cmd /c keeps native stderr out of PowerShell's error stream (Windows PowerShell 5.1).
    cmd /c "$($s.cmd) > `"$log`" 2>&1"
    $code = $LASTEXITCODE
    $mins = [math]::Round(((Get-Date) - $start).TotalMinutes, 1)
    if ($code -eq 0) { Write-Host "    ok ($mins min)" } else { Write-Host "    FAILED, exit $code ($mins min), log: $log"; $failed += $s.name }
}

if ($failed.Count -eq 0) { Write-Host "ci: ok"; exit 0 }
Write-Host "ci failed: $($failed -join ', ')"
exit 1
