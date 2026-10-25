[CmdletBinding()]
param([string]$GameRoot='D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo',[switch]$CheckOnly)
$ErrorActionPreference='Stop'
if(-not $CheckOnly -and (Get-Process -Name StarHome -ErrorAction SilentlyContinue)){throw '請先關閉 STARHOME 遊戲。'}
$taskManifest=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'package_manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$taskGameRoot=(Resolve-Path -LiteralPath $GameRoot).Path
function Get-TaskHash([string]$TaskPath){(Get-FileHash -LiteralPath $TaskPath -Algorithm SHA256).Hash.ToLowerInvariant()}
$taskPlan=@()
foreach($taskFile in $taskManifest.formal_install_files){
 $taskTarget=Join-Path $taskGameRoot $taskFile.path
 $taskBackup=Join-Path (Join-Path $PSScriptRoot 'backup_previous_0.2.0') $taskFile.path
 if((Get-TaskHash $taskBackup) -ne $taskFile.previous_0_2_0_sha256){throw '原版備份不符，已停止。'}
 $taskCurrent=Get-TaskHash $taskTarget
 if($taskCurrent -ne $taskFile.sha256 -and $taskCurrent -ne $taskFile.previous_0_2_0_sha256){throw "目前檔案已被其他更新修改，已停止：$($taskFile.path)"}
 $taskPlan+=@{target=$taskTarget;backup=$taskBackup;file=$taskFile}
}
if($CheckOnly){Write-Output 'ROLLBACK_CHECK_PASS';return}
foreach($taskStep in $taskPlan){Copy-Item -LiteralPath $taskStep.backup -Destination $taskStep.target;if((Get-TaskHash $taskStep.target) -ne $taskStep.file.previous_0_2_0_sha256){throw '還原後驗證失敗。'}}
Write-Output 'RESTORE_PASS: previous localization 0.2.0 restored'
