# 重建條件與歷史流程

## 此備份可以與不能做什麼

翻譯、原理、腳本與驗證證據已保存。**本次整理沒有在全新環境獨立重建補丁**，也沒有把原有腳本包裝成一鍵編譯器。`source/historical/` 是保留原工作流程的歷史來源，仍有工作目錄、前階段輸出與本機相依路徑；直接執行不等於能取得 0.2.1 安裝套件。

若只需要遊玩，使用原本本機完整 0.2.1 套件。若要繼續開發，先準備以下資料，再在遊戲隔離副本中工作。

## 需要自行提供

- 與 `evidence/file_versions.json` 原版 SHA256 相符的 STARHOME Demo 0.4.7b 原始檔案；不可用已翻譯版本充當原版。
- .NET 9 與相容的 Cpp2IL/LibCpp2IL/Iced 工具及參考 DLL；依 `source/historical/work/*/*.csproj` 配置。這些工具二進位沒有上傳。
- 從原版 `GameAssembly.dll` 與 metadata v39 產生的 dummy assemblies、型別與 assembly 對照、型別樹解析資料。`read_typed.py` 依賴 `work/prototype_evidence/dummy_dll` 與 `type_assembly_map.json`，其抽取內容沒有上傳。
- 原本使用的 Python 相依：UnityPy 1.25.4、TypeTreeGeneratorAPI 0.0.10、fonttools 4.67.0。這是本機版本紀錄，不表示任意新版相容。
- Noto Sans TC 字型來源。`prepare_font.py` 的本機來源路徑是 `C:\Windows\Fonts\NotoSansTC-VF.ttf`，建立 400 字重實例並保留 OFL 通知。

## 原流程與相依鏈

1. 指定工作根目錄、原版遊戲路徑、Python 相依與工具路徑，核對原版檔案及存檔檢查點。
2. 建立索引、dummy assemblies 與 `MappedGenerator` 所需對照，對目標物件做逐位元 no-op 驗證。
3. **0.1.2 基底**：`build_prototype.py` 使用前期翻譯、字型與型別資料，產生字型後備及早期翻譯。前期資料條件可由原碼路徑與歷史翻譯對照確認；不是本儲存庫內已備妥的階段輸出。
4. **0.2.0 擴充**：`build_full_localization.py` 依賴 0.1.2 payload、掃描索引、全量翻譯、section titles 與原生字串用途資料。完整 source→translation glossary 在 `translations/glossary-*.json`，依 source 合併即可，不需要重新排列舊 source ID。
5. **0.2.1 補翻**：`build_021.py` 依賴 0.2.0 的完整隔離副本與 release 基底，補資源覆寫、人口對話、威脅等級、共享標題、動態按鈕與四個描述。
6. 使用 `translations/runtime-literals-*.json` 核對最終 **212** 個已翻譯索引；`metadata_requests_0.2.0.json` 是歷史請求，部分項目當時因查找名稱衝突被跳過，不能把它當最終套用清單。
7. 重載資產、驗證非文字資料、字型覆蓋、metadata 索引與其他檔案，完成隔離實機驗證後才建立正式安裝 payload。

`source/installer_reference/` 保存實際交付過的安裝／還原腳本與去除本機路徑的 manifest。它們依賴同層的 `payload/`、`backup_original/`、`backup_previous_0.2.0/`；本儲存庫沒有這些二進位，所以不可當成可直接安裝的發行包。

## 後續版本

Steam 更新後，先重新核對引擎、metadata 版本、檔案 hash、物件 ID、型別與共享字串用途。遇到未知檔案版本應停止套用，不能強制覆蓋。保存使用者既有存檔與自訂艦名，不把本方案中的測試進度寫回正式存檔。
