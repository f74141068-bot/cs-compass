# CS Compass｜資工學習知識庫

以 C++、資料結構與演算法為主的繁體中文學習網站。核心在於以 `AGENTS.md` 定義 AI 的工作方式，使任何下一次的內容擴充都能遵守同一結構、設計與驗收規則。此專案使用原生 HTML/CSS/JavaScript，部署不需要伺服器或 API。

## 瀏覽與部署

直接雙擊 `index.html` 即可在本機瀏覽；所有頁面已生成，不必執行建置程式。

GitHub Pages：建立 Public repository `cs-compass`，將此資料夾**內的檔案與子資料夾**上傳到 repository 根目錄（不要將整個外層資料夾或 ZIP 上傳）。確認 `index.html`、`AGENTS.md` 在根目錄。進入 Settings → Pages → Deploy from a branch → `main` → `/(root)` → Save；部署成功後開啟 Visit site，確認網站可公開瀏覽。

## 修改內容（選用）

需要 Python 3.9+（標準函式庫即可）。在專案目錄開啟終端機：

```sh
python3 scripts/build.py
python3 scripts/check.py
```

請先讀 `AGENTS.md`，再修改 `content/notes.json`。每一筆 JSON 記錄會產生一個筆記頁，首頁會自動更新索引、搜尋資料與總數，不需要人工複製 HTML。檢查通過後一起提交原始 JSON 與生成的 HTML。

## 擴充案例：Binary Search

初始內容規劃為 Pointer、Linked List、Stack、Queue 四篇。第五篇 Binary Search 是依手冊資料欄位新增的擴充案例：

- 在 `content/notes.json` 增加 ID `binary-search`，分類 `algorithm`、難度 `進階`、完整 13 個欄位。
- `scripts/build.py` 依資料產出 `notes/binary-search.html`，更新首頁筆數、搜尋資料及卡片。
- 網站的「AI 開發規則」頁可直接連到擴充案例。

下一次可把以下指令交給能存取專案資料夾的 AI：

> 先讀 AGENTS.md。新增一篇廣度優先搜尋（BFS），分類 algorithm、難度進階，相關筆記連結到 queue，依既有格式提供 C++17 範例與測驗，執行 build.py 和 check.py，不修改無關檔案，最後回報驗收結果。

此提示詞為下一次擴充示例，BFS 尚未收入網站。

## 驗收

- `scripts/check.py`：驗證資料契約、可重現的靜態 HTML、首頁索引、每頁結構、所有相對路徑與錨點。
- 瀏覽器：首頁搜尋、分類、空結果、筆記連結、測驗答案展開與手機排版。
- C++17：編譯各筆記程式並比對預期輸出。

實際本機驗收記錄見 `TESTS.md`。公開網址需在自己的 GitHub 帳號部署後才會產生。
