# AI 課程題庫

課程測驗網站。題目全部放在 `data/` 底下的 JSON 檔，網站程式不需要改，也不需要建置：新增題目、單元或課程，只要改資料檔。

## 檔案結構

```
題庫網站/
├─ index.html                 網站入口
├─ assets/
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
│  │  └─ aai/                 一門課一個資料夾
│  │     ├─ course.json       課程名稱、單元列表
│  │     ├─ transformer.json  單元題庫
│  │     ├─ nlp.json
│  │     └─ transfer-learning.json
│  └─ templates/
│     └─ course-pack.example.json   匯入用的範例
├─ tools/validate.js          題庫格式檢查
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
| `tags` | 否 | 標籤，目前只存著，之後可做依標籤出題 |
| `type` | 否 | `single`（預設，單選）或 `truefalse`（是非題） |

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

## 新增課程

1. 建立資料夾 `data/courses/<課程id>/`，放 `course.json` 與各單元題庫檔（格式照 `aai/`）。
2. 在 `data/catalog.json` 的 `courses` 加一筆 `{ "path": "courses/<課程id>/course.json" }`。

單元也可以不拆檔，直接把 `questions` 寫在 `course.json` 的單元裡，格式和匯入檔一樣。

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

目前發布在 claude.ai Artifact。發布的檔案是 `index.html`、`assets/` 與 `data/`；`tools/`、`README.md`、`package.json` 只在本機使用。
