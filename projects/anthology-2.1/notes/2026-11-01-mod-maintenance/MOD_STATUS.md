# MOD 狀態清單

快照時間：2026-11-01T11:21:51+08:00。只讀目前 Profile；勾選不等於每個檔案都勝出，也不等於實機通過。非本輪項目的做法取自 10/29 歷史盤點，沒有重測。

共 43 個 Meti 列，40 啟用、3 停用。

| 模組目錄 | Profile | 做法／版本／邊界 |
|---|---|---|
| `Meti_AutodocRefill_v0.1.0` | 啟用 | 0.1.0；自動醫療模組右鍵相容藥品補充；已安裝待玩家驗收。 |
| `Meti_Needs_Half_v0.1.0` | 啟用 | 只調飢餓／口渴／睏倦惡化率一半，睡眠檢查300保留；詳主記錄。 |
| `Meti_ThermalGreenScopes_v0.1.0_TRIAL` | 啟用 | 10/31 同場景投影版；綠光／自然背景＋彩色熱像，玩家附圖成功；非全鏡具驗收。 |
| `Meti_SameMapPrewarm_v0.1.0` | 啟用 | 0.1.2 TRIAL；已就緒即傳、未就緒短試約1秒、超時原讀圖；已安裝未遊玩。 |
| `Meti_AmmoTextAndYield_v0.1.0` | 啟用 | 0.2.0審查版；68配方、18條過量材料修正，保留原有利產量；208登錄條目文字檢查。 |
| `Meti_AuditFixes_v0.1.0` | 啟用 | 已留存talents_gui門檻／動態音樂callback／夜視MCM路徑修正回執；不等於選單閃退確診。 |
| `Meti_ArtefactServices_v0.1.0_TRIAL` | 啟用 | 既有技師接神器維修；共享 37 種配方聯集、35 種完整配方；缺資料的 af_gubka／af_sluda 隱藏。沿用原費用與一次選項規則。 |
| `Meti_TechnicianUndo_v0.4.0_TRIAL` | 啟用 | 僅支援審核過的口徑／瞄具替換；卸彈、處理附件，再重建武器物件，物件 ID 會改變。 |
| `Meti_CraftingExpansion_v0.1.0_TRIAL` | 啟用 | 新增 22 類彈藥、10 類裝備配方並保留 4 條既有路線；移除兩處初始化刪除，保留 VOG-25／M209。 |
| `Meti_AmmoMaterialsSupply_v0.1.0_TRIAL` | 啟用 | 0.3.0 low stock；一般技師16類材料、兩科學家各四碎片，3/4/5盒瓶；舊停補guard略過。 |
| `Meti_TalentChineseTooltip_v0.1.0` | 啟用 | 描述欄 font=di → letterica16；190 段中文描述字形核對。 |
| `Meti_TechnicianFull80_v1.5.0_TRIAL` | 啟用 | 射程／初速／射速／回正 ×1.8；支援散布、PDM、耗損 ×0.2；10 個後座角欄位 ×0.1；傷害／衝擊 ×1.3；一般彈匣 ×1.8 向上取整。 |
| `Meti_ChineseUILabels_v0.1.0` | 啟用 | 調整成就字型與箱子標記中文；箱子標記的現行腳本由本層提供。 |
| `Meti_TalentRespecKeepLevels_v0.1.0` | 啟用 | 保留四類等級與當前經驗，重設職業／天賦及已花點數；可用點回到等級值，避免重複累加。 |
| `Meti_LootEquipment100_v0.1.0` | 啟用 | 新死亡 NPC／首次箱子生成的槍械、護甲、頭盔外觀耐久設 100%。 |
| `Meti_PackCompatibility_v0.1.0` | 啟用 | 多項舊功能實際勝出層；最新取消Ctrl+V榴彈轉送，沿用B；不能整層拆掉當局部回退。 |
| `Meti_WorkshopUpgradeParity_v0.1.0_TRIAL` | 啟用 | 工作台的槍械／護甲滿改補足與技師對齊，保留原工具、材料及價格規則。 |
| `Meti_ArmorFull50_v0.1.0_TRIAL` | 啟用 | 188 個 section／168 組基準／4258 目標：滿改後正向防護與恢復至少達基準 ×1.5；以 ma50 持久升級補足。 |
| `Meti_LegacyFavoriteCleanup_v0.1.0` | 啟用 | 一次性清掉彈藥／配件的舊收藏並記錄；後續同類新增收藏限右鍵選單，阻止原快速路徑。 |
| `Meti_CraftNoWait_v0.1.0_TRIAL` | 啟用 | 跳過約 3 秒演出等待，保留真正扣料、生成及完成事件；由相容層接到 Banjaji 入口。 |
| `Meti_Levsha_MeetingFix_v0.1.0_TRIAL` | 啟用 | 兩處帶條件的 NPC 會面路徑修正；不強制灌入完成旗標。 |
| `Meti_Levsha_Diagnosis_v0.1.0_READONLY` | 停用 | 任務診斷記錄腳本保留備查。 |
| `Meti_AmmoCompactLabels_v0.1.0_TRIAL` | 啟用 | 歷史最新回執為0.1.4字體可顯示修正；資料夾名沿用。 |
| `Meti_MaterialRepair25_v0.1.0_TRIAL` | 啟用 | Attachments 材料分支採 math.max(toolbonus,0.25)；鋼板／克維拉板依工具相容性使用。 |
| `Meti_InventoryActions_v0.2.0_TRIAL` | 啟用 | 修理子選單按相容工具顯示；垃圾彈藥批次拆解最多 1024 物件；普通電池可手選，另有每秒檢查的自動換電池。 |
| `Meti_InventoryActions_v0.1.0_TRIAL` | 停用 | 保留舊試驗檔，已由 v0.2.0 及相容層接替。 |
| `Meti_BatteryDrain25_v0.1.0_TRIAL` | 啟用 | 既有消耗乘0.25保留；最新item_device移除B夜視亮度，短N亮度／長N原夜視。 |
| `Meti_RegionalToolsRecipes_v0.1.0_TRIAL` | 啟用 | 8 份商店 DLTX 擴充地區工具及配方紙供應。 |
| `Meti_ArtefactSpecialty_v0.1.0_TRIAL` | 啟用 | 35 種原料、105 個結果，102 項有變更；既有正向防護不足 15% 者目標 18%（gd_novice）；恢復與負輻射排除 ×1.2。 |
| `Meti_InventoryCounterBatch_v0.1.0_TRIAL` | 啟用 | 批次計數／裝飾、圖示軸快取；玩家背包與搜刮背包增量更新。128 次變更重整，32768 上限回退；交易仍走相應刷新。 |
| `Meti_NVG_ClearFocus_v0.1.0` | 啟用 | 三種夜視 shader 各移除一處 NEARBLUR。 |
| `Meti_RVR_Materials_v0.1.0_EXPERIMENTAL` | 啟用 | Materials0.7.2／Mouse0.5.1；完整物品、同種類500、取出修正與[任务]顯示；後續遊玩待驗。 |
| `Meti_NVG_CtrlBrightness_v0.1.0` | 啟用 | 普通夜視以右 Ctrl＋主鍵盤 −／＝調整，每次按下調一次；相容層排除熱像。另提供跨模組按鍵說明文字。 |
| `Meti_WeaponActions150_v0.1.0_TRIAL` | 啟用 | 玩家持有時拔槍、收槍、一般換彈動畫 ×2.25；8766 個共享 section 的 ADS 時間 ÷2.25；保留例外與原技能疊加。 |
| `Meti_AN94_SightAlignment_v0.1.0_TRIAL` | 啟用 | 16 個 HUD section、80 欄位由 ALT 定位恢復成包內 RAK BASE 定位。 |
| `Meti_LootMarkers_v0.1.0_TRIAL` | 啟用 | 按住 F 顯示 40 米內箱子／藏匿點，最多 32 個；不操作 PDA 地圖點。 |
| `Meti_TechnicianNumeric_v1.0_TRIAL` | 啟用 | 提供既有技師數值／文字／資料及 mf13、mf14 相容定義，是 Full80 依賴的一部分。 |
| `Meti_EnemyMarkers100m_v0.2.0` | 啟用 | 100 米內敵人姓名／距離中文標記，最多 64 個；掃描與繪製節拍約 16.67 ms。 |
| `Meti_ActorJumpHeight25_v0.1.0_EXPERIMENTAL` | 啟用 | jump_speed 6.85 → 7.658533，依拋體關係設計約增加 25% 跳躍高度。 |
| `Meti_LoadTipWrap_v0.2.0_EXPERIMENTAL` | 啟用 | 改善中文長載入提示換行，保留已採用的版面。 |
| `Meti_PlayerGunfeel_v0.1.0_TRIAL` | 停用 | 試驗檔保留，現行 Profile 未啟用。 |
| `Meti_Anthology_BaseCarry999999_v0.2.0` | 啟用 | 基礎負重改為 999999；保留裝備、天賦及分組倍率；行走門檻仍由原邏輯推算。 |
| `Meti_Anthology_StartPoints_100000_v0.1.0` | 啟用 | 新遊戲裝備購買點數設為 100000。 |

舊盤點的直接改原模組、persistent ID、實際勝出者與版本漂移問題仍需保留。這份清單不宣稱找到了全部來源不明的歷史改動。
