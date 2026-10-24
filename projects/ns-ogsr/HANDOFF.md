# NS OGSR 修改方法與 Anthology 參考交接

保存日期：2026-10-24（台灣時間）。來源為使用者提供的 NS_OGSR_MOD_HANDOFF.zip；本文件合併來源四份主要說明，保留限制與未知項。這是參考文件，不是安裝包。未重新執行遊戲或驗證全部程式；未授權或執行 Anthology 新修改。

來源 ZIP SHA256：a46324e5c32bedb3cb7b2977c7640dff8912af8095ba35cdbd2280d7472a7aad。原始附件保留於使用者聊天。本次只保存技術文字，未上傳 ZIP、EXE、DLL、存檔與完整遊戲素材。下文 EVIDENCE、FILES、DIFFS 等相對路徑指原始 ZIP 內成員，並非本倉庫中的檔案。

## 快速接續

- NS 的一般槍械性能使用共用 LTX 絕對值，並非完整玩家限定技能；不能將其成功經驗當作 Anthology 玩家專屬精準／後座已解決。
- NS 有可參考的角色 slot 合成、玩家相機閉氣與玩家命中事件設計，但各自不是通用槍械 buff 接口。
- NS 確有原生引擎補丁；槍械 Accuracy150／Performance125／Handling25 本身主要是設定修改。精確引擎位址、機器碼不可移植。
- Anthology 舊 Gunfeel 物件暫改版目前停用，新技能方案未完成，暫停研究；此交接不重啟開發。
- Anthology 現有功能正式整合 v1.0 的交付證據已核對；使用者 2026-10-24 回報等待一分多鐘後成功進場，正在實玩。尚非所有功能驗收完成。



---

# 來源文件：README.md

# NS OGSR MOD 交接：供 Anthology 2.1 評估

整理日期：2026-10-24（Asia/Taipei）。這是既有實作與證據的參考包，不是安裝包。沒有讀取Anthology、啟動／修改遊戲、修改保存、執行原生遊戲測試、重新全盤掃描或建立新工作串。此輪只補查槍械／角色機制、接口及指定檔案，並沿用2026-10-23交接。

## 最重要的結論

1. **一般槍械強化不是完整玩家限定方案。** 精準、傷害、後座、磨損、射程與彈種散布主要寫在共用`configs/mods/*.ltx`，相同武器／彈種可被NPC使用。`[actor]`散布項與玩家HUD動作是不同作用層，不能將整包統稱玩家限定。
2. **移動／跳躍另有玩家角色計算層。** `jr_global_params.apply_slots`從initial重算slots後，setter寫`g_actor_obj.walk_accel/jump_speed`；固定倍率在最後，並接神器比值。沒有每次拿目前角色值再乘，亦沒有藉由武器交易前手動還原來完成此功能。
3. **+N是另一套永久物品改裝。** 它使用動態upgrade／私有INI、原生重建新ID、metadata與交易收據。它不是「只在玩家拿著時生效、轉手即復原」的暫時buff；儲物等跨流程仍有缺口。
4. 未找到本專案已完成「玩家計算期間限定精準＋後座，轉手完全不留武器狀態」的證據。不能將NS的成功遊玩經驗當作Anthology這項需求已解決，也沒有在這輪新設計或移植替代方案。

## 實際版本／狀態

- 本機專案稱`S.T.A.L.K.E.R. NS OGSR`；NS整合包正式release／原作版本號與中文化來源版本**未知**。LTX註解的`06.09.2026`不單獨證明正式發行版本。
- 既有日誌標頭：`OGSR Engine (x64)`，build `Sep 6 2026 12:01:13`。上游commit／完整建置源碼**未知**；PE FileVersion／ProductVersion先前查讀為空。
- 當前磁碟EXE：`8C6EAF79B0008F6EA5AA25536B1BBED8CECE4E2E966842CEBD0E3117A025B94E`；最後安裝修正為`ENGINE-INVENTORY-IDENTITY-FIX-004`。匹配PDB與其他選定檔指紋見`EVIDENCE/DELIVERY_STATE.json`。
- **磁碟現用內容**與**已載入執行中的內容**分開：本輪核對指定檔案與先前最終基線，沒有啟動、附掛或觀察執行中遊戲，不宣稱已確認程序載入版本。
- 最後功能交付：任務034；收納袋core012／說明013／UI014；槍匣核心009＋維修包cash002；神器002＋UI003；副教授UI002／TEXT004／HINT005；高斯006；快旅UI005；白字+N005；頭戴005／熱圖003。這些是各功能版本，不是一個通用總版號。
- 208筆是歷史登記，含舊層、撤回、診斷與實驗，不等於208個啟用MOD。三個`gear_*_test`為已安裝實驗；Duty corpse救援假說已撤回；最大體力翻倍／排放後神器循環未完成；舊自訂小地圖縮放被原生快捷提示接替。
- 安裝方式：SQ封包＋loose `gamedata`，`system_mods.ltx`包含`mods/mod_*.ltx`，另有Lua auto_attach／XML／shader與本機原生EXE修改。並非可直接交給另一套X-Ray引擎的統一模組包。

## 包內閱讀順序

1. MOD_CHANGELOG.md（來源包路徑：MOD_CHANGELOG.md）：重點數值、作用範圍、載入層與回退；完整208筆見EVIDENCE/MOD_HISTORY.csv（來源包路徑：EVIDENCE/MOD_HISTORY.csv）。
2. API_AND_IMPLEMENTATION.md（來源包路徑：API_AND_IMPLEMENTATION.md）：實際getter／setter／回呼、呼叫位置、生命週期矩陣與原生修改邊界。
3. PORTING_NOTES_ANTHOLOGY.md（來源包路徑：PORTING_NOTES_ANTHOLOGY.md）：可借鏡、需查證與不可直接搬用。
4. FEATURE_REFERENCE.md（來源包路徑：FEATURE_REFERENCE.md）：沿用既有40個評估分組的逐功能資料。未完成／實驗／診斷亦保留供辨識，並非全部列為已驗收成果。
5. FILES/README.md（來源包路徑：FILES/README.md）、DIFFS/README.md（來源包路徑：DIFFS/README.md）：自製檔案節選與必要差異，保留`gamedata/...`相對路徑；缺基準不猜原值。**有意省略大型NS資料表、圖源與其他依賴，因此FILES不是完整可執行模組。**

## 驗證與已知缺口

`EVIDENCE/VALIDATION_MATRIX.csv`將靜態、模擬、原生遊戲讀值、GUI採證與玩家回報分開。原生指令模擬、Windows CRT／unwind實驗不是原生遊戲內讀值；保存解析也不等同GUI操作。這輪沒有補跑以上遊戲測試。

使用者於本次要求中提供「已遊玩約三分之二且沒有遇到重大問題」的實玩經驗，記為**整體USER_REPORTED_GENERAL_EXPERIENCE**，不分攤成每項功能或每種生命週期的PASS。之前已發生並修復的崩潰、尚未完整驗收的流程仍保留。

任務034尚有249項需補證／分類；神器UI003實測材料是背包而非袋內直供；+N與技師／儲物的REC01/02/04/05/06/07不能概括結案；保存命名編碼、血池checkpoint、舊懸停及效能尖峰等仍有歷史OPEN。最後正式接受的004包只驗同一隱藏背包。來源後來的19:08日誌不在先前驗收範圍，此輪沒有追加診斷。

交付檔案SHA見SHA256_MANIFEST.json（來源包路徑：SHA256_MANIFEST.json）。內容已將私人絕對路徑換成邏輯來源代稱，不含引擎二進位、保存、完整日誌、帳號或金鑰。檔案回退不等於遊戲狀態回退；Anthology是否需新存檔及能用哪些接口均待該專案查證。

整理完成後停止，等候使用者將本包帶到Anthology專案分析。


---

# 來源文件：MOD_CHANGELOG.md

# MOD修改重點與數值

本表區分原始需求、實際作用層與最後累積值。數字「原值」可能是某次補丁安裝前的有效值，並非保證未MOD的原廠值。逐section樣本在EVIDENCE/WEAPON_VALUE_SAMPLES.csv；完整208筆路徑／函式／鍵／前後聲明／依賴／回退見EVIDENCE/MOD_HISTORY.csv。這輪沒有重算全量INI或實景測試。

## 槍械與玩家：做過什麼、沒有做過什麼

| 需求／功能 | 已做方式與數值 | 實際作用範圍／限制 |
|---|---|---|
| 基礎精準 | Accuracy150將weapon fire_dispersion_base與actor disp_*除1.5；Performance125再乘0.8，累積為原相關散布÷1.875 | 201／後續198槍械section含霰彈變體；weapon部分共用NPC，actor部分玩家；不是總彈著誤差固定÷1.875 |
| 玩家散布示例 | actor.disp_base 0.51→0.34→0.272；disp_aim 0.04→0.026666666667→0.021333333334 | 配置內玩家項；沒有證明這是全部精準誤差來源或可等價取代weapon側 |
| 基礎傷害 | hit_power乘1.25；wpn_9a91 0.534→0.6675 | 共用武器，包括NPC；非玩家限定，不等於DPS／護甲後扣血 |
| 後座與回準 | cam_dispersion／inc／step_angle_horz乘0.75；wpn_9a91 0.7→0.525、0.525→0.39375、5.25→3.9375；僅2個正cam_relax_speed乘1.25、196個0保持 | 共用武器設定，具體AI／player分支依引擎；cam_relax_speed_ai保留；未做「全部後座歸零」或強制回原準星 |
| 移動與低耐久散布 | PDM_disp_vel_factor／accel各乘0.75；fire_dispersion_condition_factor乘0.75 | 獨立因子合成，不是最終散布固定減25%；保留owner／feature分支，非統一玩家限定 |
| 磨損 | 單發與正queue磨損乘0.5；缺省／非正queue保持原fallback | 持久物件耐久變化仍走原遊戲；不宣稱只影響玩家槍 |
| 瞄準／換彈 | Timing75時間×0.75／速度÷0.75；Performance125時間再×0.8／速度×1.25。後來Actions150指定動作速度再×1.5／時間÷1.5 | HUD／weapon同名鍵分開看，原相關時間0.60只是較早層；不能宣稱最後所有瞄準固定0.15秒；音效頻率可能升音高，NPC共用聲音可能受影響 |
| 拔收／持槍 | Handling25 show/hide速度×1.25；HUD一般缺省inertion_origin_offset -0.05→-0.0375、zoom offset -0.02→-0.015；9a91個別origin為-0.02→-0.015；後續動作層再覆蓋指定速度 | 主要玩家HUD；未取消全域bobbing、全部呼吸、所有pose與strafe；沒有改射速 |
| 霰彈與射程 | Handling25合法16彈種／匣k_disp×0.75；Actions150真正多彈丸再÷2；fire_distance×2、air resistance÷2 | 彈種／武器共享，會涉及NPC；直升機專用／未引用匣有繼承保護；未提高初速、彈丸數或宣稱無限射程 |
| 自動閉氣 | 配置倍率>=2的合格槍鏡，沿原相機閉氣狀態；免倒數與該項耐力耗損，條件退出清相機 | 玩家only相機／瞄準狀態；不是武器精準／後座setter，也不是總後座降99% |
| 玩家頭部命中 | 只在玩家真槍、活敵人、可靠頭骨條件下event.power×5 | 這項有玩家來源guard；與global基礎傷害×1.25是不同層，不代表全槍強化玩家限定 |
| 永久槍匣+N | 槍械每級線性5%、匣每級+5發；核心009＋維修包cash002可目標+1～+5、備品或盧布 | 物件改裝、私有INI／metadata與新ID；不是離手自動還原，轉手與儲物需看獨立相容性缺口 |
| 沒做成的對應需求 | 沒有已完成的「只在玩家精準／後座計算加倍率、轉手不留值且免手動關閉」程式證據 | 不把共用配置、自動閉氣、+N或命中加傷混稱此方案已成功；Anthology接口待查 |

相關最終路徑：

- gamedata/configs/mods/mod_zzzzzzz_weapon_accuracy150.ltx
- gamedata/configs/mods/mod_zzzzzzzz_weapon_timing75.ltx
- gamedata/configs/mods/mod_zzzzzzzzzz_weapon_performance125.ltx
- gamedata/configs/mods/mod_zzzzzzzzzzz_weapon_handling25.ltx
- gamedata/configs/mods/mod_zzzzzzzzzzzzzzzzzzzzzzzz_meti_actions150_range200.ltx
- gamedata/scripts/jr/jr_weapon_sway.script（DIFFS）；meti_item_enhance.script及相關UI（FILES）

## 角色／其他功能與載入疊加

- 移動：jr_global_params.setters.walk_accel在所有slot之後寫v×1.5×movement_ratio；基礎13.6時、無其他slot／神器，示例20.4。
- 跳躍：setters.jump_speed寫v×sqrt(1.25)×movement_ratio；基礎8時約8.944272。高度×1.25是固定重力理論值，不是本輪實跳量測。
- 負重9999；實體容量後續99999；物資袋13999B／收據<16384B／INI行長限制是另一種容量，不能混同。
- 體力、需求減半、護甲防護、商人6小時／分階段供貨、神器箱、修理零工時、物資袋、快旅、任務034、成像、標記、白字+N與副教授708可見商品等，逐項在FEATURE_REFERENCE保留原需求／最終方式／路徑與原值聲明。原檔缺失則保留缺口。

既有NS有效覆蓋順序在EVIDENCE/CONFIG_LOAD_ORDER.json。前幾層是共同基準，後續Performance125、Handling25、Actions150寫入指定絕對值；不是每次啟動再將所有倍率乘當前物件一次。父子section有絕對值／保護以避免繼承重算，但技師upgrade、永久+N、神器／JR slot與其他MOD仍可能再改同一最終結果；不將這些合理疊加全稱bug，也不宣稱零衝突。

## 回退

多數新增LTX的安裝前是「檔案不存在」，並非有一份可恢復的同名原版；參數基準在既有changes表。NS歷史管理器在正常退出後按SHA與依賴回退，入口為MOD_ROLLBACK/<ID>及_meti_backups/<ID>。本包沒有安裝／回退器，不應執行直接刪檔。

後層可能已把前層效果折入絕對值，刪早期Accuracy檔不等於後續Performance的散布恢復。整份JR／laucer／UI／binder或EXE回退也可能覆蓋其他功能。物品+N、v4帳冊、收據、商人批次、store標記與世界刪除有持久狀態，檔案回退不退款、不還物、不逆轉世界；需對應保存／格式政策。Anthology是否需新檔未知，不能沿用NS宣告。

## 各功能登記索引

下表沿用既有功能分組；完成／舊版／實驗／診斷界線見歷史表ReviewClass與驗收矩陣，不把目錄內全部成果認列已啟用。

| 分組 | 功能 | 作用範圍 |
|---|---|---|
| F01 | 中文化與字型 | 語系／UI |
| F02 | 負重與背包容量 | 玩家角色與其裝備容量 |
| F03 | 體力、移速、跳躍與生存需求 | 玩家角色／生存時序 |
| F04 | 裝備體力與機動測試層 | 指定三件裝備實驗 |
| F05 | 按鍵、草地與準星個人設定 | 本機輸入／顯示 |
| F06 | 視窗化、置中及客戶區修正 | 本機視窗與原生輸入區 |
| F07 | F提示、物件互動與輔助拾取 | 玩家提示／互動 |
| F08 | 槍械平衡、操作速度與自動閉氣 | 混合：共用武器／彈藥＋玩家actor/HUD；非整包玩家限定 |
| F09 | 護甲頭盔耐久與防護 | 裝備／骨骼表，共用類型依消費路徑 |
| F10 | 敵人察覺與可靠頭部命中增傷 | 察覺配置影響敵方類型；頭部加傷另核對玩家來源 |
| F11 | 商人供貨、技師商店與現金商品 | 指定商人／技師及所產商品 |
| F12 | NPC掉落與怪物採集 | NPC/怪物loot與玩家採集 |
| F13 | 維修包四區、神器維修與零工時 | 玩家維修UI／選定物品／訂單 |
| F14 | 技師改裝相容性規則 | 指定改裝物品 |
| F15 | 指定數量移動與預留物保護 | 選定堆疊／交易預留 |
| F16 | 彈匣／槍械R卸彈與補彈整合 | 玩家彈匣UI／物品狀態 |
| F17 | 高斯能源補充與跨使用紀錄UI堆疊 | 指定Gauss型號與UI；混合包彈道共享 |
| F18 | 隨身神器箱ARC擴格與材料整合 | 六款神器容器及材料提供路線 |
| F19 | 神器製作與可攜轉換器 | 合格配方／玩家合成UI |
| F20 | 槍械與彈匣+1～+5核心 | 指定物件永久+N，並非owner限定暫時buff |
| F21 | 神器+N與付費進階 | 指定神器與玩家腰帶效果 |
| F22 | 維修包便攜技師與目標強化頁 | 玩家UI，但改裝結果為物件持久狀態 |
| F23 | 物資收納袋與材料直供 | 玩家物資帳冊／選定物件 |
| F24 | 任務追蹤、標記與中文引導 | NS任務／PDA／目標物件 |
| F25 | 任務與背包查詢效能 | NS任務與背包查詢 |
| F26 | PDA快速旅行與落點預覽 | 玩家PDA／位置與金錢 |
| F27 | 夜視、熱成像與手動保持 | 玩家頭戴成像／渲染 |
| F28 | 自訂PDA標記與方向箭頭 | 玩家自訂標記 |
| F29 | 自動敵人提示 | 玩家HUD中的敵人提示 |
| F30 | 屍體白點與已搜查隱藏 | 屍體標記／搜查事件 |
| F31 | 背包白色+N徽章 | 候選物品cell顯示 |
| F32 | 排放／載入後安全清理 | 離線世界物件清理（高風險） |
| F33 | 特定廢料場物理崩潰救援 | 指定NS損壞物件個案 |
| F34 | 引擎銷毀佇列與背包身分防護 | NS原生UI／物件生命週期 |
| F35 | 副教授全裝備虛擬採購目錄 | 副教授NPC／玩家UI／商品生成 |
| F36 | PDA Esc完整收起 | 玩家PDA輸入 |
| F37 | 小地圖縮放原生快捷提示 | 玩家HUD被動提示 |
| F38 | 槍械說明基礎傷害值 | 玩家物品說明UI |
| F39 | 診斷、控制台與專案整理 | 診斷／部署／個人開發入口 |
| F40 | 未實作或僅研究要求 | 無可認列完成實作 |


---

# 來源文件：API_AND_IMPLEMENTATION.md

# API、實作與生命週期證據

此文件只記錄NS已存在的用法，沒有建立新的玩家限定武器方案。精確來源行號、片段與SHA見EVIDENCE/API_LOCATORS.json（來源包路徑：EVIDENCE/API_LOCATORS.json）及EVIDENCE/CODE_EXCERPTS.md（來源包路徑：EVIDENCE/CODE_EXCERPTS.md）。接口「原始碼中有用」不等於本次在遊戲逐值實測，更不證明Anthology有同一匯出。

## 1. 一般槍械性能：設定層，不是持槍時暫改物件

`system_mods.ltx -> mods/mod_*.ltx -> CWeapon／HUD／彈藥設定讀取`。以原先已解析的有效設定為基準，在產製補丁時算出**絕對值**，寫入每個指定section。不是on_update去讀目前散布再乘0.8，沒有為這組共用倍率建立「拿槍備份、丟槍還原」程式。

- 實際設定鍵：`fire_dispersion_base`、`[actor].disp_base/disp_aim`、`cam_dispersion/cam_dispersion_inc/cam_step_angle_horz`、`PDM_disp_vel_factor/PDM_disp_accel_factor`、`fire_dispersion_condition_factor`、磨損、HUD動作速度／鎖定時間、慣性幅度、`k_disp/fire_distance/k_air_resistance`。
- 槍械與彈種共用值不帶「擁有者必須玩家」guard。NPC可共用傷害／基礎散布／彈道等；後座、回準及低耐久分支要按引擎自己的player/AI路徑理解。補丁保留`cam_relax_speed_ai`，不能因此宣稱全部後座欄位都只影響玩家或都同等影響NPC。
- HUD動作是玩家第一人稱動作；共享聲音設定仍可能影響NPC聲音。玩家HUD換彈速度不能推成NPC換彈速度同比例改變。
- 本次檢查的這些性能LTX與已知相關程式，沒有實作武器統計值的玩家限定暫寫／離手還原。**沒有提供`set_fire_dispersion_base`或`set_cam_dispersion`已被本專案使用的證據**；不從配置鍵反推同名Lua getter／setter存在，也不宣稱NS整個引擎絕無其他API。
- `binary-evidence.json`中`CWeapon::Load/reload`、HUD motion／sound等符號與預設常數是既有唯讀消費接口分析。該Performance125修改沒有改EXE，不可把「用PDB看引擎」寫成「改過引擎傷害／後座公式」。

相同名稱的`zoom_rotate_time`可能同時在槍械section與HUD section。後續Actions150也新增／覆蓋槍械層預設值；不能把某一HUD值0.15直接宣稱最終所有槍實際瞄準耗時0.15。本包列出實際section與值，沒有新量測動畫耗時。

## 2. 角色移動／跳躍：有玩家計算層，但不是精準／後座接口

`jr_global_params`的`global_paramters`保存`initial`及四類slot；`set_slot_add/mul/min/max`與`remove_slot`均呼叫`apply_slots`。

```text
apply_slots(param)
  initial -> slots_mul -> slots_add -> slot min/max -> 參數min/max -> p.setter(value)
  walk_accel setter: g_actor_obj.walk_accel = value * 1.5 * artefact.movement_ratio("walk_accel")
  jump_speed setter: g_actor_obj.jump_speed = value * sqrt(1.25) * artefact.movement_ratio("jump_speed")
```

實際賦值屬性是`g_actor_obj.walk_accel`及`g_actor_obj.jump_speed`，不是對武器呼叫setter。原值來自`get_float("actor",...)`；此檔沒有以getter讀目前actor速度作為下一次倍率基準。原有`db.actor:set_actor_max_weight(v)`／`set_actor_max_walk_weight(v)`也在同一參數框架，但不要把它們與容量或武器統計混為一談。

`attach(sm)`訂閱`on_spawn -> on_spawn`清空slots並套initial。神器UI的`on_update`每250ms呼叫`meti_artefact_enhance.update_movement()`；後者讀腰帶神器、耐久、同種衰減與nanosuit限制，計算「新／原效果」比值，只有比值改變時才`jr_global_params.apply_slots(key)`。它不是每輪在既有速度上無限累乘。

這樣能保留有接入JR slot的飢餓／疲勞／裝備修正；**沒有證據保證**另一个MOD直接寫同一actor屬性時不被下一次重算覆蓋。`initial`也不是每次從所有外部MOD動態重讀。借鏡的是計算層和單一合成入口，不能直接推出精準／後座也有同等接口。

## 3. 光學鏡自動閉氣：玩家相機狀態，不是總後座降低99%

- Getter／判斷：`db.actor:active_item()/alive()/zoom_mode()`、`level.main_input_receiver()`、`isWeaponFireOnly(wpn)`、`wpn:is_weapon_magazined()/is_weapon_gl()/get_gl_mode()/get_addon_flags()/get_weapon()`、`get_float(scope_section,"scope_zoom_factor",0)`。
- 用於區分紅點／倍率鏡、內建／外接鏡與下掛；倍率門檻為配置>=2。這些方法僅在NS現用程式有證據，不是Anthology的匯出清單。
- Getter／setter：`level.get_cam_effector_factor(99215)`、`level.set_cam_effector_factor(99215,...)`與`find_effector_zi().power`；操作的是原呼吸／慣性效應器。持續閉氣時相機動畫使用原有held-breath係數0.01與慣性power目標0.1，非直接設定槍械後座。
- 回呼：`on_update -> main_update -> update_auto_breath -> wants_auto_breath`；`on_sniper_mode -> zoom_in/zoom_out`；`on_spawn/on_destroy -> meti_reset_scope_breath`；鍵盤on_key_down/up保留原手動入口，自動模式跳過手動計時／耗耐力支線。
- 切槍、離開瞄準、死亡、UI有輸入焦點時，update條件會退出；zoom_out及spawn/destroy另清狀態。沒有專屬「交易／丟棄前還原武器散布」回呼，因為這個功能根本未改那兩項武器統計。
- `stop_auto_breath`將效應器power設回1，不是比對與恢復其他MOD的最後寫入值；共用effector同時寫入的衝突未全面驗證。

## 4. 真正有玩家條件的命中回呼

`enemy_headshot500`的`on_npc_before_hit/on_monster_before_hit -> amplify`核對`event.who_id`等於`db.actor:id()`、`event.who`、`weapon_id`、`level.object_by_id`、`target:alive()/is_relation_enemy()`、`hit.fire_wound`與`get_bone_id/bone_head`後，只將本次`event.power`乘5；handler回nil、不創造第二次hit、不改保存或武器配置。

這是已有的**玩家來源／敵對目標／可靠頭骨**條件化傷害事件設計；不是已完成的玩家精準與後座計算hook。資料不足時跳過，不猜骨骼或來源槍。

## 5. +N是永久物件系統，需獨立看待

`UI prepare -> commit -> 預留原件／備品或盧布 -> ALife生成 -> before_register初始化 -> online install_upgrade -> 核對新ID／私有INI／metadata -> settle扣料扣費`。

實際接口與位置：

- 讀取：`g_alife:object(id)`、`level.object_by_id(id)`、`obj:id()/section()/name()/condition()`、`obj:own_setting()`、`has_upgrade`與升級列表、server的`custom_data/parent_id`。
- 寫入／重建：`set_ammo_elapsed(0)`、`set_addon_flags(...)`、`install_upgrade(section,false)`先登記，最後一次`install_upgrade(last,true)`觸發重建並取得新ID；`set_condition`、`get_weapon_m().cur_fire_mode`恢復指定狀態。
- `apply_weight`讀`own_setting():r_string(idsection,"inv_weight")`後寫`obj:get_inventory_item().inv_weight`。這裡有get_inventory_item的client用法，不代表server/CSE也有同一helper；歷史儲物REC01正與此界線有關。
- `ogse.load_var_safe/save_var/delete_var`保存交易收據；`;METI_ITEM_TX_V1=`等custom_data保護原件／輸出。+N不是可在轉手時任意清除的暫時值。
- 核心訂閱`se_item:on_before_register`、`on_update`、`on_load`、`on_before_first_update`、`on_destroy`、`on_item_spawn`。UI另訂閱`on_item_menu/execute`、`on_inventory_hide`、`on_before_save`等。精確列表見片段，不以未用的事件名字補齊表格。
- `install_native_upgrade`在技師改裝時先移除私有grade，裝原生改裝，再將grade置於最後重建；新ID的metadata與JR資料亦須移交。失敗只在原實體仍存在時嘗試恢復私有段，不會隨意生成複製品補償。
- 儲物有`serialize`延伸／`spawn_stored`及`level.client_spawn_manager():add`的延後client處理；**有程式分支不等於所有儲物路線通過**。REC01/02/04與其他技師交易失敗分支仍是交接缺口。
- 現用核心仍有精確舊nonce／section／ID的`recover_001_mag`等歷史故障收據救援。它們是特定NS故障補救，不是可移植的通用交易恢復策略。

## 6. 生命週期矩陣：有處理與沒有的分開

| 情境 | 一般性能LTX | Actor移動／跳躍 | 自動閉氣 | 永久+N |
|---|---|---|---|---|
| 拾取／切換／收槍 | 無暫改／還原hook；按共用配置讀值 | 不取決於武器；由角色slots重算 | 每次update重看active_item／瞄準；不合格退出 | item_spawn排權重工作；未做所有型號逐次採證 |
| 丟棄／交易 | 不還原，NPC可讀同類改值；不是玩家限定 | 無武器待恢復值 | 沒有交易專屬hook，條件退出只清相機狀態 | 不自動清grade；不能當玩家限定；待結算物僅指定guard路線保護 |
| 存放／取回 | 無臨時buff還原流程；特殊私有INI仍需另看 | 與武器保存無直接關係 | 沒有武器統計序列化 | 有storage編解碼與延後初始化，但仍有REC缺口，未全流程保證 |
| 技師改裝 | 不另攔截；原生改裝／私有設定可再作用 | 裝備若接JR slots可重算 | 瞄準／active狀態決定是否繼續 | install_native_upgrade保grade順序與新ID；AEK曾因原生UI快取崩潰另修引擎 |
| 存讀檔 | 重啟重新載入LTX；舊已改裝槍的最終值未全量讀值 | on_spawn重建slot框架；神器比值按更新重算 | spawn/destroy重置；沒有獨立on_load訂閱，不能補稱有 | on_load清暫存、持久收據另恢復；有指定成功與未完整覆蓋分支 |
| 換圖 | 沒有跨圖武器舊值備份／還原 | 依原spawn與slot框架；未逐圖測量 | 沿spawn/destroy原生命週期；換圖全組合未測 | 沿load／before_register／spawn；未宣稱全部容器與新ID交接安全 |

表中「沒有hook」不是判定必要bug，而是不能把它寫成已實作的玩家限定交接機制。共用配置、新建物件與原有特殊私有設定的交互仍需要逐項證據。

## 7. 確實改過的引擎，與沒有改的部分

本串有實際`bin/xrEngine.exe`二進位補丁；沒有完整引擎建置源碼／可重建上游commit，也沒有本次編譯引擎或改DLL。現用EXE／PDB雜湊與若干精確前後區段見`EVIDENCE/NATIVE_BINARY_CHANGES.json`。一般Accuracy150／Timing75／Performance125／Handling25是LTX，不是C++或二進位的玩家限定精準／後座hook。

已知原生變更類別：視窗／客戶區、輔助拾取、MoveQuantity交易入口、+N／高斯cell支援、DestroyQueue游標修正、InventoryCache實體指標檢查、Cell／Group存活驗證與Identity004正確registry全域。早期歷史配套不等於每一版應獨立安裝。

具體例：DestroyQueue001由`eb03 498bde`改`eb00 498bde`，讓既有游標更新執行；AEK InventoryCache001在RVA3942636原區段改身分比較，52個檔案bytes含checksum變更；Identity004修RVA`0x116c067`的RIP位移，將錯誤`0xfa1e28`（message）改指`0xfb1e28`（g_pGameLevel），只變2個檔案bytes含checksum，另Lua binder nil早退。

002／003曾用錯全域，而fixture也同步放錯位址，造成舊PASS不能證明正式查詢正確。004用匹配PDB與三條原生參照獨立建立負面控制後修正。這些位址、ABI、RTTI、vtable與unwind都綁定NS該EXE，不能複製進Anthology。


---

# 來源文件：PORTING_NOTES_ANTHOLOGY.md

# Anthology 2.1：可借鏡與待查契約

目標需求由使用者提供：只強化玩家精準與後座，交易／丟槍前不需手動關閉；先前暫時改武器物件方案已停用。本輪沒有讀目標檔案、恢復該方案、提出新倍率注入方案或開始移植。所有Anthology接口均為待查。

## 一、可以借鏡的既有設計

1. **先分清配置、玩家計算、相機狀態與永久物品。** NS共用武器LTX確實有效調整了性能，但不能當玩家限定範本。Actor slots則展示由原始計算入口合成最終值的方法；自動閉氣展示條件化的相機狀態；+N展示需要持久化的物件交易。四者不可混用。
2. **避免從目前結果反覆累乘。** NS性能檔在製作時以既有有效配置計算絕對值，包含子section繼承保護；Actor每次從initial與slots重算。多個MOD同時寫入時仍需核對所有權與排序，不是靠記住一次舊值便能保證恢復正確。
3. **用實體身分與獨立接口證據驗收。** +N和技師重建會更換ID，快取不能只靠ID／section；同一套錯誤假設寫進程式與fixture會假PASS。API名稱應來自目標實際程式／匹配符號／已觀察回呼，不能由NS鍵名或X-Ray親緣推定。

以上是已發生實作的設計經驗，不是宣稱NS已有適用於目標的玩家限定後座hook。

## 二、Anthology需要自行查證的最小接口

| 要確認什麼 | NS證據能支持什麼 | 尚不能支持什麼 |
|---|---|---|
| 目標的玩家精準／後座計算層與作用時機 | NS有actor散布設定、角色slots與特定hit事件的不同作用層 | 不能由此保證Anthology匯出玩家精準／後座getter/setter或可用同一事件 |
| Getter／setter是否真匯出、單位與持久性 | NS程式確實用g_actor_obj屬性、active_item、own_setting等列明用法 | 不能把NS直接讀欄位／私有INI方法當目標存在；本串也沒有成功暫寫精準／後座setter的證據 |
| 配置與單物件／玩家數值如何相合 | NS一般LTX是共用；+N私有改裝為物件持久狀態 | 不能假定目標同名參數只在玩家路徑讀取，或不影響NPC |
| 生命週期與擁有權變更 | NS重建、交易預留、on_load/spawn/destroy經驗與失敗有明確界線 | 不能認定on_update觀察active_item就涵蓋交易／丟棄前的全部原生順序 |
| MOD疊加與恢復原值的所有權 | Actor slots合成及固定配置的「不反覆累乘」可參考 | 未證實目標有同一slot框架；NS效應器power設回1也可能蓋過其他寫入，不能當完美恢復策略 |
| 保存／改裝／儲物／跨圖 | NS有+N持久metadata、CSE/client分界和失敗案例 | 不能推論目標的暫時物件值不被序列化，或私有INI重建時不會把buff保存 |

是否可做到目標需求，必須先在Anthology專案建立自己的證據；本包不替它選用新實作方式。

## 三、明確不能直接移植的內容

- NS的EXE、機器碼、RIP位移、vtable／RTTI／registry layout與精確地址。不得為相似名稱直接套patch。
- NS `g_alife`、CSE／client、`ogse_signals`、`jr_global_params`、`laucer`彈匣、`ogse`保存變數、`own_setting/install_upgrade(true)`的契約與回呼時機。
- 武器／HUD／ammo section、升級段落、NPC／任務／story ID、地圖graph／座標、圖集與字型／shader／ANM資源名稱。
- `meti_item_enhance`的特定舊nonce／ID救援分支、NS收據格式、NS v1-v4袋帳冊與保存，不能作目標通用migration。
- 全域武器設定方案即使在NS已成功遊玩，也不符合「NPC完全不變」的完整要求。玩家HUD改變也不能代表NPC的相同行為被或未被改變。

## 四、證據與交付界線

使用者「約三分之二流程且無重大問題」是整體實玩經驗，不是每槍／每接口／每GUI／每轉手或存讀組合的採證。既有模型PASS、真Windows函式執行、保存解碼、原生成功日誌及畫面採證在本包分級。

本包FILES是審閱節選，保留來源相對路徑；缺大型NS資料、原資源及其他依賴，沒有安裝器，也不應直接放入目標。文件內原值若僅是某歷史補丁安裝前的有效值會明示，不冒稱未修改原版。未知維持未知，不以新掃描、完整測試或新方案填空。

交付後停止，等使用者將本包回傳給Anthology專案評估。


本次獨立包完整性核對：163 個清單成員的 SHA256 與大小全部相符；164 個總成員包含清單自身。這不是原生遊戲功能驗收。


# 來源文件：EVIDENCE/KNOWN_GAPS.md

# 已知風險、失敗與缺口

1. Anthology 2.1端完全未讀：正式版本／引擎分支／CPU位元／API／物品系統／保存與權利來源全部待核對。沒有直接相容結論。
2. NS整合包精確版本、上游commit與中文化原來源缺失。cached ogsr-base只作既有抽取基準；未重新核驗封包成員或假定未經修改的原廠來源。
3. 任務034仍有249項需補證或分類；全目錄盤點不等於所有階段實測。NS任務ID、故事ID、地圖／spawn／容器資料不可當通用資料庫。
4. 袋／ARC／+N／技師跨流程：既有REC01（CSE helper）、REC02（儲物取回私有INI）、REC04（未結算匣被打包）、REC05（失敗領取憑據）、REC06（付款拒絕補償）、REC07（+N備品被技師消耗）不能概括結案。早期REC03/11/12由交易guard001修了指定自訂路徑，不表示原生拖放／雙擊／其他MOD有全域攔截。見第86、87、98篇；未新跑跨流程測試。
5. 神器UI003的pouch無condition崩潰已在模型修正；玩家實測來源明確是「背包」，直接袋內材料仍NOT_RUN。儲物資料需用實際codec測nil／空字串／非空／普通／+N。
6. 引擎002/003查錯0xfa1e28，而真正g_pGameLevel為0xfb1e28。舊fixture也放錯位置，PASS無法獨立證明正確。004已更正；003點選FAIL保留。不得將舊002/003單獨當可搬補丁。
7. 副教授TEXT004無界原生hint超過1024-byte CRT緩衝而崩潰；005改短hint＋正文分段。白字+N004的8192人為界線與callback錯誤曾導致崩潰並回退，最終為005。維修包CIconParams曾使用不存在的方法，須看003後的靜態預覽。
8. 既有接受紀錄仍有保存命名Illegal byte sequence、BLOODPOOLS checkpoint write、已銷毀物懸停、耗時callback等OPEN。乾淨退出、原生日誌無fatal、單個容器正常均不等於整體穩定／全物品／FPS證明。
9. 最近正式驗收章167涵蓋10/17 13:05場次。現場另有10/17 19:08場次及後續dump；本輪僅讀六行版本標頭，沒有診斷它們，也未把較早驗收推廣為這些後續場次正常。
10. 完整原版diff、所有解包基準的官方來源認證、每個舊功能的逐項玩家實測並不齊全。缺口如實保留；不為交接補做新研究、啟動、全盤掃描或重解包。


# 來源文件：EVIDENCE/HANDLING_CONTRACT.json

```json
{
  "mod_id": "WEAPON-HANDLING25-001",
  "approved_for_staging": true,
  "source": "Root final scope instructions and frozen current matching native-interface-contract.json",
  "native_contract_sha256": "9DD38EE838FF7A107F771709D210F8458796D2BC7B732339D0951BB5277751B6",
  "return_speed": true,
  "return_speed_policy": "Only current positive cam_relax_speed multiplied1.25; preserve196 zeros and all cam_relax_speed_ai; no forced return-to-aim promise",
  "draw_hide": true,
  "draw_hide_sound": true,
  "sound_policy": "Selected firearm per-alias path/volume retained, delay0.8 and frequency1.25; no audio file changes; higher pitch and shared NPC sounds documented",
  "sway_amplitudes": {
    "inertion_origin_offset": "-0.05",
    "inertion_zoom_origin_offset": "-0.02"
  },
  "semantic_defaults": {
    "cam_dispersion_inc": "0",
    "PDM_disp_vel_factor": "1",
    "PDM_disp_accel_factor": "1",
    "inertion_origin_offset": "-0.05",
    "inertion_zoom_origin_offset": "-0.02"
  },
  "strafe_rotation_amplitude": false,
  "condition_accuracy_penalty": "All198 fire_dispersion_condition_factor values0.75; native multiplier1+(1-condition)*factor, preserving owner/feature gating",
  "queue_wear": "Only explicit positive queue value0.5; leave absent and negative/zero sentinel. Current native >0 queue branch uses queue; <=0 falls back to singlewear times shot count",
  "movement": "PDMvel and PDMacc each0.75; additive coefficients neutral0, missing default1 is a penalty; independent angular/linear/accel factors multiply so global scatter ratio is not universally0.75",
  "ammunition": "Exactly16 reachable shotgun ammo/base+mag wrappers; dedicated helicopter ammo_12x76_zhekan_heli remains fully original by inheritance guard",
  "additional_negative_changes": "None beyond root-approved condition_accuracy_penalty; all40 historical upgrade NERFs already neutral and untouched",
  "runtime_game_test": "NOT_PERFORMED"
}

```
