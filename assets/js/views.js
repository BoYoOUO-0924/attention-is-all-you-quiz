// 各畫面的 HTML。每個函式只讀狀態、回傳字串；互動由 main.js 用 data-act 統一處理。
import { esc, fmtTime, LETTERS } from "./util.js";
import { indexCourse, scoreQuiz } from "./engine.js";
import { store } from "./store.js";

const countQs = course => course.units.reduce((n, u) => n + u.questions.length, 0);
const unitName = (course, id) => (course.units.find(u => u.id === id) || { name: id }).name;

function seg(act, cur, opts) {
  return `<div class="seg" role="group">${opts.map(([v, l]) =>
    `<button type="button" data-act="${act}" data-v="${v}" aria-pressed="${String(cur) === String(v)}">${l}</button>`).join("")}</div>`;
}

function bestLine(courseId, scope) {
  const r = store.get(`best:${courseId}/${scope}`);
  return r ? `最佳 <b>${r.best}</b> 分 · 上次 <b>${r.last}</b> 分` : "尚未作答";
}

function topBar(ctx, right = "") {
  return `<header class="top"><button type="button" class="brand" data-act="home">${esc(ctx.site.name || "課程題庫")}</button>${right}</header>`;
}

/* ---------- 首頁：課程列表＋匯入 ---------- */
export function homeView(S, ctx) {
  const problems = ctx.problems.length
    ? `<div class="notice" role="alert"><span>有些題庫沒有載入：${ctx.problems.map(esc).join("；")}</span></div>` : "";
  const cards = ctx.courses.map(c => {
    const ask = S.ask === "remove:" + c.id;
    return `
    <article class="course-card">
      <div class="course-card-head">
        <span class="unit-code">${esc(c.code || "課程")} · ${c.units.length} 個單元 · ${countQs(c)} 題</span>
        ${c.source === "import" ? `<span class="badge">本機匯入</span>` : ""}
      </div>
      <h2>${esc(c.name)}</h2>
      ${c.desc ? `<p class="sub">${esc(c.desc)}</p>` : ""}
      <div class="chips">${c.units.map(u => `<span class="chip">${esc(u.name)}</span>`).join("")}</div>
      <div class="unit-foot">
        <span class="stat">綜合測驗 ${bestLine(c.id, "mix")}</span>
        <span class="acts">
          ${c.source === "import" ? (ask
            ? `<button class="btn danger" type="button" data-act="confirm-remove" data-course="${c.id}">確定移除</button><button class="btn ghost" type="button" data-act="cancel">取消</button>`
            : `<button class="btn ghost" type="button" data-act="remove" data-course="${c.id}">移除</button>`) : ""}
          <button class="btn" type="button" data-act="open" data-course="${c.id}">進入課程</button>
        </span>
      </div>
    </article>`;
  }).join("");

  const msg = S.importMsg;
  const importResult = msg ? `
    <div class="import-msg ${msg.ok ? "ok" : "bad"}" role="status">
      <b>${esc(msg.title)}</b>
      ${msg.lines.length ? `<ul>${msg.lines.slice(0, 12).map(l => `<li>${esc(l)}</li>`).join("")}${msg.lines.length > 12 ? `<li>……另外還有 ${msg.lines.length - 12} 項</li>` : ""}</ul>` : ""}
    </div>` : "";

  return `
  ${topBar(ctx)}
  ${problems}
  <section class="course-head">
    <p class="eyebrow">${ctx.courses.length} 門課程 · ${ctx.courses.reduce((n, c) => n + countQs(c), 0)} 題</p>
    <h1>選一門課開始練習</h1>
    <p class="lede">${esc(ctx.site.tagline || "")}</p>
  </section>
  <section class="course-list">${cards}</section>

  <section class="import">
    <div class="import-text">
      <h2>匯入自己的題庫</h2>
      <p>把題目照下面的格式寫成一個 JSON 檔，就能在這台電腦的瀏覽器裡新增一門課。匯入的課程只存在你的瀏覽器，別人看不到；要讓所有人都看到，請把檔案加進網站的 data 資料夾（見 README）。</p>
      <label class="btn file-btn" for="import-file">選擇 JSON 檔<input id="import-file" type="file" accept=".json,application/json" data-act="import"></label>
      ${importResult}
    </div>
    <details class="format">
      <summary>題庫格式範例</summary>
      <p class="hint">answer 是正解在 options 裡的位置，0 代表第一個。是非題用 <code>"type": "truefalse"</code>，answer 填 true 或 false。</p>
      <div class="pre-wrap"><button class="btn ghost copy" type="button" data-act="copy-template">複製範例</button>
      <pre id="template-pre">${esc(ctx.template || "範例檔讀取失敗，請看 data/templates/course-pack.example.json")}</pre></div>
    </details>
  </section>`;
}

/* ---------- 課程頁：設定＋單元＋綜合＋錯題本 ---------- */
export function courseView(S, ctx, course) {
  const total = countQs(course);
  const index = indexCourse(course);
  const wrong = (store.get(`wrong:${course.id}`, []) || []).filter(k => index.has(k));
  return `
  ${topBar(ctx, `<button class="btn ghost" type="button" data-act="home">← 所有課程</button>`)}
  <section class="course-head">
    <p class="eyebrow">${esc(course.code || "課程")} · ${course.units.length} 個單元 · ${total} 題</p>
    <h1>${esc(course.name)}</h1>
    ${course.desc ? `<p class="lede">${esc(course.desc)}</p>` : ""}
  </section>
  <section class="settings" aria-label="測驗設定">
    <div class="field"><span class="field-label">作答模式</span>
      ${seg("mode", S.set.mode, [["practice", "練習：每題即時看解析"], ["exam", "考試：交卷後公布答案"]])}</div>
    <div class="field"><span class="field-label">題數</span>
      ${seg("count", S.set.count, [[10, "10"], [20, "20"], [30, "30"], ["all", "全部"]])}</div>
    <div class="field"><span class="field-label">選項順序</span>
      ${seg("shuffle", S.set.shuffle, [[true, "打亂"], [false, "固定"]])}</div>
  </section>
  <section class="units">
    ${course.units.map((u, i) => `
    <article class="unit">
      <span class="unit-code">單元 ${LETTERS[i] || i + 1} · ${u.questions.length} 題</span>
      <h2>${esc(u.name)}</h2>
      ${u.sub ? `<p class="sub">${esc(u.sub)}</p>` : ""}
      ${u.topics.length ? `<div class="chips">${u.topics.map(t => `<span class="chip">${esc(t)}</span>`).join("")}</div>` : ""}
      <div class="unit-foot"><span class="stat">${bestLine(course.id, u.id)}</span>
        <button class="btn" type="button" data-act="start" data-scope="${u.id}" ${u.questions.length ? "" : "disabled"}>開始測驗</button></div>
    </article>`).join("")}
  </section>
  ${course.units.length > 1 ? `
  <section class="mixed">
    <div><h2>綜合測驗</h2>
      <p>從 ${course.units.length} 個單元輪流抽題後打亂順序。題數選「全部」會一次考完 ${total} 題。</p></div>
    <div class="mixed-right"><span class="stat">${bestLine(course.id, "mix")}</span>
      <button class="btn" type="button" data-act="start" data-scope="mix">開始綜合測驗</button></div>
  </section>` : ""}
  <section class="wrongbook">
    <div><h2>錯題本 <span class="mono">${wrong.length}</span></h2>
      <p>${wrong.length ? "這門課所有答錯、還沒答對過的題目。再答對一次就會移出錯題本。" : "目前沒有錯題。測驗中答錯的題目會自動收進這裡。"}</p></div>
    <div class="mixed-right">
      ${wrong.length ? `<button class="btn ghost" type="button" data-act="clear-wrong">${S.ask === "clear-wrong" ? "再按一次確認清空" : "清空"}</button>
      <button class="btn" type="button" data-act="start-wrongbook">練習錯題</button>` : ""}
    </div>
  </section>`;
}

/* ---------- 作答 ---------- */
export function optsHtml(q, it, pick, reveal) {
  return it.perm.map((oi, di) => {
    let cls = "opt", mark = "";
    if (reveal) {
      if (di === it.ans) { cls += " right"; mark = di === pick ? "答對" : "正解"; }
      else if (di === pick) { cls += " wrong"; mark = "你的答案"; }
    } else if (di === pick) cls += " sel";
    return `<button type="button" class="${cls}" data-act="pick" data-i="${di}" aria-pressed="${di === pick}" ${reveal ? "disabled" : ""}>
      <span class="bub">${LETTERS[di]}</span><span class="txt">${esc(q.options[oi])}</span>${mark ? `<span class="mark">${mark}</span>` : ""}</button>`;
  }).join("");
}

export function quizView(S, ctx, course) {
  const quiz = S.quiz;
  const index = indexCourse(course);
  const it = quiz.items[quiz.cur];
  const q = index.get(it.key).q;
  const pick = quiz.picks[quiz.cur];
  const n = quiz.items.length;
  const answered = quiz.picks.filter(p => p !== null).length;
  const reveal = quiz.mode === "practice" && pick !== null;
  const last = quiz.cur === n - 1;
  const practice = quiz.mode === "practice";

  const fb = reveal ? `<div class="explain ${pick === it.ans ? "ok" : "bad"}"><b>${pick === it.ans ? "答對了" : "答錯了，正確答案是 " + LETTERS[it.ans]}</b>${esc(q.explain || "這題沒有附解析。")}</div>` : "";
  const ask = S.ask === "submit"
    ? `<div class="notice" role="alert"><span>還有 <b class="mono">${n - answered}</b> 題沒作答，未作答的題目會算錯。確定要交卷嗎？</span>
        <span class="acts"><button class="btn" type="button" data-act="confirm-submit">確定交卷</button><button class="btn ghost" type="button" data-act="cancel">繼續作答</button></span></div>`
    : S.ask === "exit"
    ? `<div class="notice" role="alert"><span>離開後這次作答不會保留。</span>
        <span class="acts"><button class="btn" type="button" data-act="confirm-exit">離開</button><button class="btn ghost" type="button" data-act="cancel">繼續作答</button></span></div>`
    : "";

  return `
  <div class="qbar">
    <button class="btn ghost" type="button" data-act="exit">← 離開</button>
    <span class="title">${esc(quiz.title)}</span>
    <span class="mode">${practice ? "練習模式" : "考試模式"}</span>
    <span class="spacer"></span>
    <span class="prog mono">${quiz.cur + 1} / ${n}</span>
    <span class="timer mono" id="timer">${fmtTime(Date.now() - quiz.start)}</span>
  </div>
  <div class="progress"><i style="width:${(answered / n) * 100}%"></i></div>
  ${ask}
  <div class="quiz-grid">
    <main class="qcard" id="qcard">
      <div class="qmeta"><span class="qno">Q${quiz.cur + 1}</span><span class="tag">${esc(unitName(course, it.unit))}</span>
        ${q.type === "truefalse" ? `<span class="tag">是非題</span>` : ""}</div>
      <h2 class="qtext">${esc(q.q)}</h2>
      <div class="opts">${optsHtml(q, it, pick, reveal)}</div>
      ${fb}
      <div class="qnav">
        <button class="btn ghost" type="button" data-act="prev" ${quiz.cur === 0 ? "disabled" : ""}>上一題</button>
        ${last
          ? `<button class="btn" type="button" data-act="submit">${practice ? "看成績" : "交卷"}</button>`
          : `<button class="btn" type="button" data-act="next">下一題</button>`}
      </div>
      <p class="keys">鍵盤：按數字鍵或 A–F 選答案，← → 切換題目。</p>
    </main>
    <aside class="sheet" aria-label="答案卡">
      <div class="sheet-head"><b>答案卡</b><span class="mono">已答 ${answered} / ${n}</span></div>
      <div class="cells">${quiz.items.map((x, i) => {
        let c = "cell";
        const p = quiz.picks[i];
        if (p !== null) c += practice ? (p === x.ans ? " ok" : " bad") : " ans";
        if (i === quiz.cur) c += " cur";
        return `<button type="button" class="${c}" data-act="goto" data-n="${i}" aria-label="第 ${i + 1} 題">${i + 1}</button>`;
      }).join("")}</div>
      <div class="legend">${practice
        ? `<span><i class="o"></i>答對</span><span><i class="x"></i>答錯</span><span><i></i>未答</span>`
        : `<span><i class="a"></i>已作答</span><span><i></i>未作答</span>`}</div>
      <button class="btn ghost" type="button" data-act="submit">${practice ? "結束並看成績" : "交卷"}</button>
    </aside>
  </div>`;
}

/* ---------- 成績與檢討 ---------- */
export function resultView(S, ctx, course) {
  const quiz = S.quiz;
  const index = indexCourse(course);
  const r = scoreQuiz(quiz, course);
  const wrong = r.total - r.correct;
  const msg = r.pct >= 90 ? "很穩。可以改用考試模式，或挑戰綜合測驗。"
    : r.pct >= 70 ? "大致掌握了，把答錯題目的解析看過一遍。"
    : r.pct >= 50 ? "有基礎了，建議重讀對應的講義段落，再重做錯題。"
    : "先複習講義重點，再用練習模式從頭做一次。";
  const breakdown = r.byUnit.length > 1 ? `
    <section class="breakdown"><h3>各單元答對率</h3>
      ${r.byUnit.map(b => `<div class="brow"><span>${esc(b.unit.name)}</span>
        <div class="bar"><i style="width:${Math.round((b.correct / b.total) * 100)}%"></i></div>
        <span class="mono">${b.correct}/${b.total}</span></div>`).join("")}
    </section>` : "";
  const list = quiz.items.map((it, i) => ({ it, i })).filter(x => S.filter === "all" || !r.okArr[x.i]);

  return `
  ${topBar(ctx, `<button class="btn ghost" type="button" data-act="open" data-course="${course.id}">回課程</button>`)}
  <section class="score">
    <div class="big">${r.pct}<small>分</small></div>
    <div class="score-info">
      <p class="eyebrow">${esc(course.name)} · ${esc(quiz.title)} · ${quiz.mode === "practice" ? "練習模式" : "考試模式"}</p>
      <h1>${msg}</h1>
      <div class="facts"><span>答對 <b>${r.correct}</b> / ${r.total}</span><span>答錯或未答 <b>${wrong}</b></span><span>用時 <b>${fmtTime(quiz.elapsed)}</b></span></div>
    </div>
  </section>
  <div class="actions">
    <button class="btn" type="button" data-act="retry-wrong" ${wrong ? "" : "disabled"}>重做這次的錯題（${wrong}）</button>
    <button class="btn ghost" type="button" data-act="again">同範圍再考一次</button>
    <button class="btn ghost" type="button" data-act="open" data-course="${course.id}">換一個單元</button>
  </div>
  ${breakdown}
  <section>
    <div class="review-head"><h2>逐題檢討</h2>
      ${seg("filter", S.filter, [["all", "全部題目"], ["wrong", "只看答錯"]])}</div>
    <div class="rlist">
      ${list.length ? list.map(({ it, i }) => {
        const q = index.get(it.key).q;
        const ok = r.okArr[i];
        const p = quiz.picks[i];
        return `<article class="ritem ${ok ? "isok" : "isbad"}">
          <div class="qmeta"><span class="qno">Q${i + 1}</span><span class="tag">${esc(unitName(course, it.unit))}</span>
            <span class="tag">${ok ? "答對" : p === null ? "未作答" : "答錯"}</span></div>
          <h3 class="qtext">${esc(q.q)}</h3>
          <div class="opts">${optsHtml(q, it, p, true)}</div>
          ${q.explain ? `<div class="explain"><b>解析</b>${esc(q.explain)}</div>` : ""}
        </article>`;
      }).join("") : `<p class="empty">這次全部答對，沒有需要檢討的題目。</p>`}
    </div>
  </section>`;
}

export function loadingView() {
  return `<p class="empty">正在載入題庫……</p>`;
}

export function fatalView(message) {
  return `<section class="course-head"><h1>題庫載入失敗</h1>
    <p class="lede">${esc(message)}</p>
    <p class="lede">如果是在自己電腦上直接雙擊 index.html 開啟，瀏覽器不允許讀取 JSON 檔，請照 README 用本機伺服器開啟。</p></section>`;
}
