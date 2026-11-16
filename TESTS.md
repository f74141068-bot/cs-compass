# 本機驗收紀錄

日期：2026-11-16

| 測試項目 | 實際結果 |
|---|---|
| JSON 資料契約及唯一 ID | 通過：5 篇筆記 |
| 靜態頁面生成可重現性 | 通過：7 頁 |
| 站內路徑與錨點 | 通過：95 個 href/src 參照 |
| C++17 編譯與實際執行 | 通過：5 篇範例，輸出與解說相符 |
| 新增筆記測試 | 暫存副本新增 linear-search；成功產生第六篇、共 8 頁，110 個參照通過驗收；不改動正式網站 |
| Chromium 互動測試 | 通過：分類、關鍵字、空結果、筆記連結目標、展開測驗答案 |
| Chromium 版面測試 | 7 頁於 375、768、1280px 寬度均無整頁水平溢出；無 JavaScript 執行錯誤 |
| GitHub Pages 公開部署 | 尚未部署，需由帳號持有人進行 |

瀏覽器測試說明：測試環境的政策封鎖 file:// 及 localhost 頁面導覽，因此直接將生成的 HTML 與相同的 CSS、JavaScript 載入 Chromium 測試。互動與版面已檢查；實際 URL 導覽由 check.py 驗證檔案與錨點存在，尚須於公開部署後點擊確認。

重現資料與連結的驗收：`python3 scripts/build.py` 後執行 `python3 scripts/check.py`。C++ 範例以 `g++ -std=c++17 -Wall -Wextra -pedantic` 編譯。
