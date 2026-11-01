# 來源與查詢入口

本輪沿用已有研究，不重新啟動功能研究。以下 URL 為既有查證的原作者／引擎資料；上游同名函數不代表本整合包同一建置或相容性保證。

## 公開來源

- 熱像原始計算與顆粒：https://github.com/WhiteAnge1/anomaly-heatvision-tweaks ，以及 `gamedata/shaders/r3/infrared.h`。其 Green Channel Fix 處理靜態幾何熱遮罩，不能直接當成本次綠光倍率重影修法。
- 3DSS 場景拷貝／鏡片前置資料：https://github.com/themrdemonized/xray-monolith/blob/all-in-one-vs2022-wpo/src/Layers/xrRender/rendertarget_phase_nightvision.cpp ，既有研究位置約185行；行號可能隨上游改版。
- 原生武器／榴彈按鍵：https://github.com/themrdemonized/xray-monolith/blob/all-in-one-vs2022-wpo/src/xrGame/Weapon.cpp ，及同建置 `console_commands.cpp` 的 `use_separate_ubgl_keybind`（整數設定，不能用錯讀取API）。
- A-Life online 判斷：https://github.com/TheMrDemonized/xray-monolith/blob/all-in-one-vs2022-wpo/src/xrGame/alife_dynamic_object.cpp ，含 can_switch_online／online_distance；不是任意範圍內所有實體都能立即上線。
- 同圖直接移動的作者實作參照：https://github.com/damiansirbu-stalker/AlifePlus/blob/main/gamedata/scripts/ap_core_map.script 。同level set_actor_position／跨level ChangeLevel，僅參照，沒有安裝 AlifePlus。
- 旅行時間補丁：https://www.moddb.com/mods/stalker-anomaly/addons/fair-fast-travel-duration-for-anomaly-151 。不是本次直接採用的修正；同時改 game_fast_travel 的補丁需處理覆寫衝突。

查閱時段：本專案2026-10-29至2026-11-01研究。未鎖定commit的連結可能改變；本機候選與安裝回執比浮動行號更適合還原本次實作。

## 本機資料入口（保留原路徑，未整套上傳）

`${PROJECT}` 為本聊天專案根；`${MO2}`／`${GAME}` 為正式安裝根。確切個人絕對路徑留在本機索引，不散布到倉庫。

- `_PROJECT_RECORDS/INDEX.md`、`RESEARCH.md`：10/31歷史整合；最新11/01變更以本包覆蓋其過時狀態。
- `outputs/Anthology_2.1_修改清單與問題分析_2026-10-29.txt`：37 MOD、7直接修改腳本、11維護發現；本包保留路徑代號化全文。
- `outputs/Anthology_2.1_修正與實機驗證結果_2026-10-29.txt`：有限舊原生測試證據，不外推全部場景。
- `outputs/Anthology_全彈藥審查與修正_2026-10-29.txt`，`work/ammo_all/INSTALLED.json`、`RECIPE_AUDIT.csv`、`RECIPE_CHANGES.json`：配方／中文與有限原生記錄。
- `outputs/Anthology_補貨錯誤修正與驗證_2026-10-30.txt`、`work/crash_ammo_51000/INSTALLED.json`、`work/regional_review/CURRENT_STATE.txt`：過量供貨及guard歷史，不是現在重裝命令。
- `work/material_supply/LOW_STOCK.md`、`LOW_STOCK_INSTALLED.json`：3/4/5低量版及兩個guard略過入口。
- `work/travel_prewarm_v011/TRIAL012.txt`、`TRIAL012_INSTALLED.json`、`candidate_trial012`：最新一秒試用版；`work/fast_travel_review/evidence/011/scripts/game_fast_travel.script` 留存原旅行分支。
- `work/thermal_combined/aligned_scene_candidate`、`outputs/thermal_scene_aligned_before_20261031_184945/INSTALLATION.json`：同投影五檔與回退。
- `work/needs_half_source`、`work/ubgl_b_only/INSTALLED.json`、`work/autodoc_refill/INSTALLED.json`：需求、B鍵與自動醫療選單。
- `work/rvr_batch500`、`rvr_ammo_return_fix`、`rvr_return_review`、`rvr_task_marks/README.md`、`rvr_task_marks/VERIFICATION.json`：500批次、回傳值、核心與顯示標記。
- `${MO2}/mods/[HUD] Utjans QoL Bundle — Пакет QoL от Utjans/gamedata/scripts/fetch_item_icon.script`：沿用任務圖示判斷；原始碼不隨本文件再散布。
- `${MO2}/mods/[GAM] Optimized Storage System — Оптимизированная система хранения/gamedata/scripts/rvr_storage_system_engine.script`：MakeListElement、GetMarkedName、Reset 的本機依據；未擅自上傳第三方原碼。
- `outputs/id_usage_after_rvr_20261101T001131Z/COMPARISON.json`：既有保存物件分類。本包只收摘要，未收存檔。
- `work/crash_monitor/README_繁中.md`：記錄範圍、漏記與程序限制；未上傳原始輸入紀錄。

備份均留本機，不在本次文字包。各備份只涵蓋其回執列出的檔案，不能把最新一份局部備份當全部MOD還原包。持久資料相容性與原始第三方授權須另確認。
