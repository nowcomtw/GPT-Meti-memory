param(
    [string]$SourceRoot = 'D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo',
    [string]$DestinationRoot = (Join-Path $PSScriptRoot 'test_game'),
    [switch]$CheckOnly,
    [switch]$NoLaunch
)
$ErrorActionPreference = 'Stop'
$SourceRoot = [IO.Path]::GetFullPath($SourceRoot).TrimEnd('\')
$DestinationRoot = [IO.Path]::GetFullPath($DestinationRoot).TrimEnd('\')
if ($DestinationRoot -eq $SourceRoot -or $DestinationRoot.StartsWith($SourceRoot + '\', [StringComparison]::OrdinalIgnoreCase) -or $SourceRoot.StartsWith($DestinationRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The isolated test folder must be separate from the Steam installation.'
}
function Assert-NoReparseAncestor([string]$Candidate) {
    $cursor = $Candidate
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            if ((Get-Item -LiteralPath $cursor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Junction/symlink targets are not supported: $cursor"
            }
        }
        $parent = Split-Path -Path $cursor -Parent
        if ($parent -eq $cursor) { break }
        $cursor = $parent
    }
}
function Assert-Hash([string]$Path, [string]$Expected) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Missing file: $Path" }
    $actual = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
    if ($actual -ne $Expected) { throw "Version/hash mismatch: $Path" }
}
Assert-NoReparseAncestor $DestinationRoot
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'package_manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($patch in $manifest.patch_files) {
    Assert-Hash (Join-Path (Join-Path $PSScriptRoot 'payload') $patch.path) $patch.sha256
}
$patchMap = @{}
foreach ($patch in $manifest.patch_files) { $patchMap[$patch.path] = $patch.sha256 }
if (-not (Test-Path -LiteralPath $DestinationRoot)) {
    if ($CheckOnly) { throw 'The isolated test folder does not exist.' }
    foreach ($entry in $manifest.original_files) {
        $taskSourceFile = Join-Path $SourceRoot $entry.path
        $taskSourceHash = (Get-FileHash -LiteralPath $taskSourceFile -Algorithm SHA256).Hash
        $taskAllowed = @($entry.sha256)
        foreach ($taskFormal in $manifest.formal_install_files) { if ($taskFormal.path -eq $entry.path) { $taskAllowed += $taskFormal.sha256 } }
        if ($taskSourceHash -notin $taskAllowed) { throw "Unknown source version: $taskSourceFile" }
    }
    New-Item -ItemType Directory -Path $DestinationRoot | Out-Null
    foreach ($entry in $manifest.original_files) {
        $destinationFile = Join-Path $DestinationRoot $entry.path
        New-Item -ItemType Directory -Path (Split-Path -Parent $destinationFile) -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $SourceRoot $entry.path) -Destination $destinationFile
    }
    foreach ($patch in $manifest.patch_files) {
        Copy-Item -LiteralPath (Join-Path (Join-Path $PSScriptRoot 'payload') $patch.path) -Destination (Join-Path $DestinationRoot $patch.path) -Force
    }
}
foreach ($entry in $manifest.original_files) {
    $expected = $entry.sha256
    if ($patchMap.ContainsKey($entry.path)) { $expected = $patchMap[$entry.path] }
    Assert-Hash (Join-Path $DestinationRoot $entry.path) $expected
}
foreach ($patch in $manifest.patch_files) { Assert-Hash (Join-Path $DestinationRoot $patch.path) $patch.sha256 }
$known = @{}
foreach ($entry in $manifest.original_files) { $known[$entry.path] = $true }
foreach ($entry in $manifest.patch_files) { $known[$entry.path] = $true }
foreach ($file in Get-ChildItem -LiteralPath $DestinationRoot -File -Recurse -Force) {
    $relative = $file.FullName.Substring($DestinationRoot.Length + 1)
    if (-not $known.ContainsKey($relative)) { throw "Unexpected file in isolated copy: $relative" }
}
Write-Output 'PASS: isolated STARHOME zh-Hant 0.2.1 files verified. Steam files were not changed.'
if (-not $CheckOnly -and -not $NoLaunch) {
    $logFolder = Join-Path $PSScriptRoot 'run_logs'
    New-Item -ItemType Directory -Path $logFolder -Force | Out-Null
    $log = Join-Path $logFolder ('Player_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
    Start-Process -FilePath (Join-Path $DestinationRoot 'StarHome.exe') -WorkingDirectory $DestinationRoot -ArgumentList @('-logFile', ('"' + $log + '"')) -WindowStyle Hidden
}
