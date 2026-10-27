# 任務箱圖標修補狀態

日期：2026-10-27。修補版本：Meti 0.1.0；原腳本版本標記改為 `1.0.2+Meti.1`。

## 原因與證據界線

使用者回報兩個任務已交還、任務物品已取走，空箱圖標仍在，放入再取出無效。

整合包 `[DBG] Kristiano Fixes ALL IN ONE NEW/gamedata/scripts/fix_quest_stash_hint.script` 在讀檔時只憑任務變數 target_id／stash_created 補標記，沒有檢查是否已搜過。Grok 的取物清理只在 cache=true 時執行一次並改成 false。此組合可產生殘留；兩個現場箱子的確切 ID／cache 尚未原生確認，不能稱為唯一歸因。

## 已安裝的修補

只修改上述原提供者的一份腳本，沒有新增 MO2 項目或重排清單。

- cache=false 不補回圖標。
- stage=1、完成／失敗與 stage=255 冷卻任務，不再由讀檔補標記。
- 原生成失敗不額外補標記。
- 玩家開啟或取物時，只對當下已搜過且空的箱子，排除活動任務與已記錄的私人、工坊、Anomalous 儲物箱後，移除三種原生 treasure 圖標。
- 不改物品、任務進度、獎勵、統計、cache 或存檔格式，不掃描全世界。
- 錯誤後停用清理層；日誌標記 `[METI_STASH01]`，限量 24 筆。
- 舊殘留需再次開啟該箱觸發檢查。箱子本體保留。

原始 SHA-256：
`20ab0cbe57c5b5c19087192664de61b0ac4a8d3056106a87a12a6a9b638dd51e`

修補 SHA-256：
`ce00ac6ea4c52ea718e1e3de7d353edd303b38f0f79898eaeddae6d156d68776`

## 驗收與回退

30 項合計語法、靜態與 Lua 5.1 模型檢查通過；不是 30 項原生遊戲測試。正式檔案與保護檔雜湊確認完成，實際兩箱清理為 NOT_RUN，尚未收到使用者成功回報。

原始備份與限定 SHA 還原工具留在原工作區 `work/stash_marker_fix_v01`，審查包為 `Meti_QuestStashMarkerFix_v0.1.0_REVIEW.zip`。此 GitHub 記錄不包含遊戲腳本整檔、備份或存檔。

回退只還原腳本；已清除並由遊戲保存的圖標不會自動重建。整合包更新可能覆蓋此差異；不同來源 SHA 必須重新比對，不能直接套用舊檔。
