# 來源腳本與相依

`historical/` 為原工作流程的歷史程式來源，保留原檔內容與工作目錄假設。它們不是獨立可執行的重建套件，尚有原版資產、dummy DLL、型別對照、字型及前階段 payload 等本機相依。

- `work/read_typed.py`：Unity 6 型別解析／寫回相容處理，原相依目錄為另一個本機工作資料夾；重用前須調整。
- `work/odin_context.py`：Odin 節點上下文與字串解析。
- `work/prepare_font.py`：Noto Sans TC 400 字型實例。
- `work/build_prototype.py` → `build_full_localization.py` → `build_021.py`：階段建置相依鏈。
- `work/*_inspect/`、`dummy_export/`：原生／metadata 觀察與 dummy 匯出參考來源；第三方 DLL 不包含。
- `installer_reference/`：已交付過的安裝及雙還原腳本。缺少 payload／二進位備份，不能直接當成安裝包。

完整條件、缺少的階段產物與驗證流程見 [重建條件](../docs/REBUILD.md)。

本次沒有替使用者自行選定或授予新的程式／翻譯開源授權；字型既有 OFL 通知另附於 notices。
