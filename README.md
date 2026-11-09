# Attention Is All You Quiz

線上網站：https://boyoouo-0924.github.io/attention-is-all-you-quiz/

課程測驗網站。題目全部放在 `data/` 底下的 JSON 檔，網站程式不需要改，也不需要建置：新增題目、單元或課程，只要改資料檔。

## 檔案結構

```
題庫網站/
├─ index.html                 網站入口
├─ assets/
│  ├─ logo.svg                網站標誌與分頁圖示
│  ├─ style.css               樣式（顏色、字型都在最上面的 :root）
│  └─ js/
│     ├─ main.js              狀態、事件、啟動流程
│     ├─ views.js             各畫面的 HTML
│     ├─ engine.js            出題與計分
│     ├─ data.js              讀取題庫、檢查格式（網站與檢查工具共用）
│     ├─ store.js             瀏覽器本機儲存（成績、錯題本、匯入的課程）
│     └─ util.js              共用小工具
├─ data/
│  ├─ catalog.json            課程清單：網站從這裡開始讀
│  ├─ courses/
│  │  ├─ aai/                 一門課一個資料夾
│  │  │  ├─ course.json       課程名稱、單元列表
│  │  │  ├─ transformer.json  單元題庫
│  │  │  ├─ nlp.json
│  │  │  └─ transfer-learning.json
│  │  └─ its-python/          ITS Python 認證練習（由 tools/its-python 產生）
│  └─ templates/
│     └─ course-pack.example.json   匯入用的範例
├─ tools/validate.js          題庫格式檢查
├─ tools/its-python/          產生 ITS Python 題庫的程式（題目寫在 u1.py–u6.py）
└─ package.json
```

## 在自己電腦上開啟

瀏覽器不允許直接雙擊 `index.html` 時讀取 JSON 檔，所以要開一個本機伺服器：

```bash
python -m http.server 8765
```

然後打開 http://localhost:8765 。

## 新增題目

打開單元題庫檔（例如 `data/courses/aai/nlp.json`），在 `questions` 陣列加一筆：

```json
{
  "id": "nlp-031",
  "q": "下列何者是 trigram？",
  "options": ["Why should I", "should I", "learn", "NLP"],
  "answer": 0,
  "explain": "trigram 是連續 3 個詞。",
  "tags": ["n-gram"]
}
```

| 欄位 | 必填 | 說明 |
|---|---|---|
| `id` | 是 | 同一個單元裡不能重複。錯題本與成績靠它辨認題目，**發布後不要改** |
| `q` | 是 | 題幹 |
| `options` | 是 | 2–6 個選項 |
| `answer` | 是 | 正解在 `options` 的位置，**0 代表第一個** |
| `explain` | 否 | 解析，作答後顯示。沒填會出現提醒 |
| `tags` | 否 | 標籤。第一個 tag 當作「講義章節」，作答時會顯示，並用來檢查章節覆蓋 |
| `type` | 否 | `single`（預設，單選）或 `truefalse`（是非題） |
| `code` | 否 | 題目附的程式碼，會以等寬字型、保留縮排顯示在題幹下方。換行寫成 `\n` |

程式題範例：

```json
{
  "id": "py-001",
  "q": "執行下列程式碼後，輸出為何？",
  "code": "x = [1, 2]\nx.append(3)\nprint(len(x))",
  "options": ["2", "3", "4", "拋出 TypeError"],
  "answer": 1,
  "explain": "append 在尾端加入一個元素，長度變 3。"
}
```

是非題可以省略 `options`，`answer` 填 `true` 或 `false`：

```json
{ "id": "tl-031", "type": "truefalse", "q": "凍結層的參數在反向傳播時不會更新。", "answer": true, "explain": "…" }
```

## 新增單元

1. 在課程資料夾放一個新的題庫檔，例如 `data/courses/aai/rag.json`，內容是 `{ "questions": [ … ] }`。
2. 在該課程的 `course.json` 的 `units` 加一筆：

```json
{ "id": "rag", "name": "RAG", "sub": "檢索增強生成", "topics": ["向量資料庫", "chunking"], "file": "rag.json" }
```

單元 `id` 只能用小寫英文、數字與 `-`。

### 用章節確認講義每個重點都有出題

單元可以加上 `sections`，依講義順序列出章節名稱：

```json
{ "id": "tl", "name": "遷移學習", "file": "transfer-learning.json",
  "sections": ["遷移學習基本概念", "預訓練模型", "特徵提取"] }
```

每題的第一個 `tags` 寫它屬於哪一章。`node tools/validate.js` 會列出每章的題數；有章節沒有題目，或題目的章節不在清單裡，都會出現提醒。

## 新增課程

1. 建立資料夾 `data/courses/<課程id>/`，放 `course.json` 與各單元題庫檔（格式照 `aai/`）。
2. 在 `data/catalog.json` 的 `courses` 加一筆 `{ "path": "courses/<課程id>/course.json" }`。

單元也可以不拆檔，直接把 `questions` 寫在 `course.json` 的單元裡，格式和匯入檔一樣。

## ITS Python 題庫

`data/courses/its-python/` 是依 Certiport IT Specialist – Python 公開的六大考試範圍編寫的原創練習題（不是官方考題）。題目寫在 `tools/its-python/u1.py`–`u6.py`，改完後在專案根目錄執行：

```bash
python3 tools/its-python/build.py
```

「執行下列程式碼後，輸出為何？」這類題目的正解是實際執行程式碼得到的，所以不會寫錯答案；如果正解剛好和某個誘答選項相同，或程式碼執行出錯，產生時會直接中斷。產生完記得再跑一次 `node tools/validate.js`。

## 改完先檢查

```bash
node tools/validate.js
```

會列出每門課的題數，以及缺欄位、`answer` 超出範圍、`id` 重複等錯誤。有錯誤時結束代碼是 1。要檢查準備匯入的檔案，把路徑加在後面：

```bash
node tools/validate.js 我的題庫.json
```

## 不改網站，直接匯入

首頁下方的「匯入自己的題庫」可以讀一個課程檔（格式見 `data/templates/course-pack.example.json`，單元的題目直接寫在 `questions` 裡）。匯入的課程只存在那台電腦的瀏覽器，適合先自己試題目；確定沒問題再照上面的步驟放進 `data/`，讓所有人都看得到。

## 資料存在哪裡

成績、錯題本、作答設定、匯入的課程都存在瀏覽器的 localStorage（鍵名以 `aiquiz:` 開頭），只有那個瀏覽器看得到。清除網站資料就會重置。

## 發布

網站用 GitHub Pages 從 `main` 分支的根目錄發布，push 之後約一分鐘會自動更新。網站實際用到的是 `index.html`、`assets/` 與 `data/`；`tools/`、`package.json` 只在本機使用。
