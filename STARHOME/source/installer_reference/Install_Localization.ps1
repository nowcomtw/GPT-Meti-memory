[CmdletBinding()]
param([string]$GameRoot='D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo',[switch]$CheckOnly)
$ErrorActionPreference='Stop'
$taskPackageRoot=$PSScriptRoot
$taskManifest=Get-Content -LiteralPath (Join-Path $taskPackageRoot 'package_manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$taskGameRoot=(Resolve-Path -LiteralPath $GameRoot).Path
if(-not $CheckOnly -and (Get-Process -Name StarHome -ErrorAction SilentlyContinue)){throw '請先關閉 STARHOME 遊戲。'}
function Get-TaskHash([string]$TaskPath){(Get-FileHash -LiteralPath $TaskPath -Algorithm SHA256).Hash.ToLowerInvariant()}
$taskPlan=@()
foreach($taskFile in $taskManifest.formal_install_files){
 $taskTarget=Join-Path $taskGameRoot $taskFile.path
 $taskPayload=Join-Path (Join-Path $taskPackageRoot 'payload') $taskFile.path
 if((Get-TaskHash $taskPayload) -ne $taskFile.sha256){throw "補丁完整性不符：$($taskFile.path)"}
 $taskCurrent=Get-TaskHash $taskTarget
 if($taskCurrent -ne $taskFile.original_sha256 -and $taskCurrent -ne $taskFile.sha256 -and $taskCurrent -ne $taskFile.previous_0_2_0_sha256 -and $taskCurrent -ne $taskFile.accepted_previous_0_2_1_sha256){throw "遊戲檔案不是已知版本，已停止：$($taskFile.path)"}
 $taskBackup=Join-Path (Join-Path $taskPackageRoot 'backup_original') $taskFile.path
 if(Test-Path -LiteralPath $taskBackup){if((Get-TaskHash $taskBackup) -ne $taskFile.original_sha256){throw '原版備份雜湊不符，已停止。'}}
 elseif($taskCurrent -ne $taskFile.original_sha256){throw '目前已安裝補丁，但缺少原版備份，已停止。'}
 $taskPlan+=@{file=$taskFile;target=$taskTarget;payload=$taskPayload;backup=$taskBackup;current=$taskCurrent}
}
if($CheckOnly){Write-Output 'CHECK_PASS: payload / game version / original backup constraints verified';return}
$taskChanged=@()
$taskUpgradeBackup=Join-Path $taskPackageRoot ("installation_checkpoint_"+(Get-Date -Format "yyyyMMdd_HHmmss_fff"))
try{
 foreach($taskStep in $taskPlan){
  if(-not(Test-Path -LiteralPath $taskStep.backup)){
   New-Item -ItemType Directory -Path (Split-Path -Parent $taskStep.backup) -Force | Out-Null
   Copy-Item -LiteralPath $taskStep.target -Destination $taskStep.backup
   if((Get-TaskHash $taskStep.backup) -ne $taskStep.file.original_sha256){throw '原版備份驗證失敗。'}
  }
  if($taskStep.current -ne $taskStep.file.sha256){
   $taskCheckpointFile=Join-Path $taskUpgradeBackup $taskStep.file.path
   New-Item -ItemType Directory -Path (Split-Path -Parent $taskCheckpointFile) -Force | Out-Null
   Copy-Item -LiteralPath $taskStep.target -Destination $taskCheckpointFile
   if((Get-TaskHash $taskCheckpointFile) -ne $taskStep.current){throw "升級前備份驗證失敗。"}
   $taskStep.checkpoint=$taskCheckpointFile
   $taskChanged+=$taskStep
   Copy-Item -LiteralPath $taskStep.payload -Destination $taskStep.target
  }
  if((Get-TaskHash $taskStep.target) -ne $taskStep.file.sha256){throw '安裝後驗證失敗。'}
 }
 $taskResult=@{version='0.2.1';game_root=$taskGameRoot;time=(Get-Date).ToString('o');status='INSTALLED_HASH_VERIFIED';files=@($taskPlan | ForEach-Object {@{path=$_.file.path;sha256=(Get-TaskHash $_.target);backup=$_.backup}})}
 $taskResult | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskPackageRoot 'deployment_result.json') -Encoding UTF8
 Write-Output 'INSTALL_PASS: 2 localization files installed; original backups verified'
}catch{
 foreach($taskStep in $taskChanged){Copy-Item -LiteralPath $taskStep.checkpoint -Destination $taskStep.target}
 throw
}
