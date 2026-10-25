# STARHOME Demo 繁體中文漢化方案

此資料夾保存已交付的 **0.2.1 漢化方案、完整翻譯對照、處理腳本與限定實機驗證紀錄**。

- 適用原始遊戲：STARHOME Demo **0.4.7b**，Windows x64。
- 引擎：Unity **6000.3.15f1**，IL2CPP metadata **v39**。
- 本機交付／實測日期：2026-10-22；GitHub 方案整理日期：2026-10-25。
- 正式安裝只修改 `StarHome_Data/sharedassets1.assets` 與 `StarHome_Data/il2cpp_data/Metadata/global-metadata.dat`。

## 先看這個範圍

這是**方案與原始資料備份**，不是可直接安裝的 Release。遊戲本體、原版或修改後的二進位資產、原版備份、存檔、原生完整紀錄、遊戲截圖、字型二進位及第三方工具執行檔沒有上傳。

原本 69,524,365 bytes 的完整安裝套件仍保存在本機，檔名 `STARHOME_Localization_0.2.1_繁中補翻套件.zip`，SHA256：

```text
14be003abcea5b3aa401f002f4d4805cf28d29e60fcfa422e10966b1f412505b
```

## 導覽

| 內容 | 位置 |
|---|---|
| 引擎結構、文字來源與修補原理 | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 重建所需資料與已知相依條件 | [docs/REBUILD.md](docs/REBUILD.md) |
| 已驗證、保留項目與未完成驗收 | [docs/VALIDATION.md](docs/VALIDATION.md) |
| 版本變更 | [CHANGELOG.md](CHANGELOG.md) |
| 全部翻譯對照分片及索引 | [translations/index.json](translations/index.json) |
| 歷史處理腳本與安裝還原參考 | [source/README.md](source/README.md) |
| 版本雜湊與結構／實機證據摘要 | [evidence/](evidence/) |

## 讀取及檢查

使用 Python 3 執行 `python verify_snapshot.py`，只讀取本資料夾，核對所有已列檔案的 SHA256、Git blob ID、翻譯分片筆數及執行期索引唯一性，不修改遊戲或存檔。

完整劇情分支、全部解析度與所有存讀檔路徑尚未逐一完成原生遊玩驗收。不可將字串或資料掃描筆數視為遊玩完成度。
