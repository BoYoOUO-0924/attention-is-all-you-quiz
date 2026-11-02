import { shuffle } from "./util.js";
import { store } from "./store.js";
import { loadSiteCourses, normalizeCourse } from "./data.js";
import { buildItems, makeItem, indexCourse, scoreQuiz } from "./engine.js";
import { homeView, courseView, quizView, resultView, loadingView, fatalView } from "./views.js";

const app = document.getElementById("app");
const DEFAULT_SET = { mode: "practice", count: 20, shuffle: true };

// ctx：載入的資料（不放進快照）；S：畫面狀態（可序列化，頁面更新時保留）
const ctx = { site: {}, siteCourses: [], courses: [], problems: [], template: "" };
let S = {
  view: "home", courseId: null,
  set: Object.assign({}, DEFAULT_SET, store.get("settings") || {}),
  quiz: null, filter: "all", ask: null, importMsg: null
};

const course = () => ctx.courses.find(c => c.id === S.courseId);

function render() {
  const c = course();
  if ((S.view !== "home") && !c) S.view = "home";
  app.innerHTML =
    S.view === "course" ? courseView(S, ctx, c) :
    S.view === "quiz" ? quizView(S, ctx, c) :
    S.view === "result" ? resultView(S, ctx, c) :
    homeView(S, ctx);
}
const top = () => window.scrollTo(0, 0);

/* ---------- 匯入的課程 ---------- */
function loadImports() {
  const packs = store.get("imports", []) || [];
  return packs.map(raw => normalizeCourse(raw, { source: "import" }).course).filter(Boolean);
}
function refreshCourses(site) {
  ctx.courses = site.concat(loadImports().filter(c => !site.some(s => s.id === c.id)));
}

async function importFile(file) {
  let raw;
  try {
    raw = JSON.parse(await file.text());
  } catch (e) {
    S.importMsg = { ok: false, title: `${file.name} 不是有效的 JSON`, lines: [e.message] };
    return render();
  }
  const { course: c, errors, warnings } = normalizeCourse(raw, { source: "import" });
  if (!c) {
    S.importMsg = { ok: false, title: `沒有匯入：${file.name} 有 ${errors.length} 個問題要修正`, lines: errors };
    return render();
  }
  if (ctx.siteCourses.some(s => s.id === c.id)) {
    S.importMsg = { ok: false, title: `沒有匯入：課程 id「${c.id}」和網站內建課程重複`, lines: ["請把 id 改成別的名稱再匯入。"] };
    return render();
  }
  const packs = (store.get("imports", []) || []).filter(p => p.id !== c.id);
  packs.push(raw);
  const saved = store.set("imports", packs);
  ctx.courses = ctx.courses.filter(x => x.id !== c.id).concat(c);
  const n = c.units.reduce((s, u) => s + u.questions.length, 0);
  S.importMsg = {
    ok: true,
    title: `已加入「${c.name}」：${c.units.length} 個單元、${n} 題` + (saved ? "" : "（這個瀏覽器不允許儲存，重新整理後會消失）"),
    lines: warnings
  };
  render();
}

/* ---------- 測驗流程 ---------- */
function startQuiz({ scope, items, title, origin }) {
  const c = course();
  S.quiz = {
    scope, origin: origin || scope,
    title: title || (scope === "mix" ? "綜合測驗" : c.units.find(u => u.id === scope).name),
    mode: S.set.mode,
    items: items || buildItems(c, { scope, count: S.set.count, shuffleOptions: S.set.shuffle }),
    cur: 0, start: Date.now(), elapsed: 0, done: false
  };
  S.quiz.picks = S.quiz.items.map(() => null);
  S.view = "quiz"; S.ask = null; S.filter = "all";
  render(); top();
}

function finish() {
  const c = course();
  const quiz = S.quiz;
  quiz.done = true;
  quiz.elapsed = Date.now() - quiz.start;
  const r = scoreQuiz(quiz, c);
  // 只有單元與綜合測驗算成績；錯題練習不覆蓋最佳成績
  if (quiz.scope !== "keys") {
    const key = `best:${c.id}/${quiz.scope}`;
    const rec = store.get(key) || {};
    store.set(key, { best: Math.max(rec.best || 0, r.pct), last: r.pct, tries: (rec.tries || 0) + 1 });
  }
  const wrongKey = `wrong:${c.id}`;
  const book = new Set(store.get(wrongKey, []) || []);
  r.wrongKeys.forEach(k => book.add(k));
  r.rightKeys.forEach(k => book.delete(k));
  store.set(wrongKey, [...book]);
  S.view = "result"; S.ask = null;
  render(); top();
}

function go(i) {
  const quiz = S.quiz;
  if (!quiz || i < 0 || i >= quiz.items.length) return;
  quiz.cur = i; S.ask = null; render();
  const card = document.getElementById("qcard");
  if (card && card.getBoundingClientRect().top < 60) card.scrollIntoView({ block: "start" });
}

function pick(i) {
  const quiz = S.quiz;
  const it = quiz.items[quiz.cur];
  if (i >= it.perm.length) return;
  if (quiz.mode === "practice" && quiz.picks[quiz.cur] !== null) return;
  quiz.picks[quiz.cur] = i; S.ask = null; render();
}

function trySubmit() {
  if (S.quiz.picks.some(p => p === null)) { S.ask = "submit"; render(); top(); }
  else finish();
}

const saveSet = () => store.set("settings", S.set);

/* ---------- 事件 ---------- */
app.addEventListener("click", e => {
  const b = e.target.closest("[data-act]");
  if (!b || b.disabled || b.tagName === "INPUT") return;
  const v = b.dataset.v;
  switch (b.dataset.act) {
    case "home": S.view = "home"; S.quiz = null; S.ask = null; render(); top(); break;
    case "open": S.courseId = b.dataset.course; S.view = "course"; S.quiz = null; S.ask = null; render(); top(); break;
    case "mode": S.set.mode = v; saveSet(); render(); break;
    case "count": S.set.count = v === "all" ? "all" : Number(v); saveSet(); render(); break;
    case "shuffle": S.set.shuffle = v === "true"; saveSet(); render(); break;
    case "start": startQuiz({ scope: b.dataset.scope }); break;
    case "start-wrongbook": {
      const c = course();
      const items = buildItems(c, { keys: store.get(`wrong:${c.id}`, []) || [], shuffleOptions: S.set.shuffle });
      startQuiz({ scope: "keys", items, title: "錯題本", origin: "wrongbook" });
      break;
    }
    case "clear-wrong":
      if (S.ask === "clear-wrong") { store.del(`wrong:${S.courseId}`); S.ask = null; }
      else S.ask = "clear-wrong";
      render(); break;
    case "pick": pick(Number(b.dataset.i)); break;
    case "prev": go(S.quiz.cur - 1); break;
    case "next": go(S.quiz.cur + 1); break;
    case "goto": go(Number(b.dataset.n)); break;
    case "submit": trySubmit(); break;
    case "confirm-submit": finish(); break;
    case "cancel": S.ask = null; render(); break;
    case "exit":
      if (S.quiz.picks.some(p => p !== null)) { S.ask = "exit"; render(); top(); }
      else { S.view = "course"; S.quiz = null; render(); }
      break;
    case "confirm-exit": S.view = "course"; S.quiz = null; S.ask = null; render(); top(); break;
    case "again": {
      const q = S.quiz;
      if (q.origin === "wrongbook") {
        const c = course();
        startQuiz({ scope: "keys", items: buildItems(c, { keys: store.get(`wrong:${c.id}`, []) || [], shuffleOptions: S.set.shuffle }), title: "錯題本", origin: "wrongbook" });
      } else startQuiz({ scope: q.origin });
      break;
    }
    case "retry-wrong": {
      const q = S.quiz;
      const c = course();
      const index = indexCourse(c);
      const items = shuffle(q.items.filter((it, i) => q.picks[i] !== it.ans))
        .map(it => makeItem(it.unit, index.get(it.key).q, S.set.shuffle));
      startQuiz({ scope: "keys", items, title: q.title.replace(/（錯題）$/, "") + "（錯題）", origin: q.origin });
      break;
    }
    case "filter": S.filter = v; render(); break;
    case "remove": S.ask = "remove:" + b.dataset.course; render(); break;
    case "confirm-remove": {
      const id = b.dataset.course;
      store.set("imports", (store.get("imports", []) || []).filter(p => p.id !== id));
      ctx.courses = ctx.courses.filter(c => c.id !== id);
      S.ask = null; S.importMsg = null; render(); break;
    }
    case "copy-template": {
      try {
        navigator.clipboard.writeText(ctx.template).then(() => { b.textContent = "已複製"; }, selectTemplate);
      } catch (err) {
        selectTemplate();
      }
      break;
    }
  }
});

function selectTemplate() {
  const pre = document.getElementById("template-pre");
  if (!pre) return;
  const range = document.createRange();
  range.selectNodeContents(pre);
  const sel = window.getSelection();
  sel.removeAllRanges(); sel.addRange(range);
}

app.addEventListener("change", e => {
  if (e.target.id === "import-file" && e.target.files[0]) {
    importFile(e.target.files[0]);
    e.target.value = "";
  }
});

document.addEventListener("keydown", e => {
  if (S.view !== "quiz" || e.ctrlKey || e.metaKey || e.altKey) return;
  const k = e.key.toLowerCase();
  const map = { 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, a: 0, b: 1, c: 2, d: 3, e: 4, f: 5 };
  if (k in map) { pick(map[k]); e.preventDefault(); }
  else if (k === "arrowright") { go(S.quiz.cur + 1); e.preventDefault(); }
  else if (k === "arrowleft") { go(S.quiz.cur - 1); e.preventDefault(); }
});

setInterval(() => {
  const t = document.getElementById("timer");
  if (t && S.quiz && !S.quiz.done) {
    const s = Math.round((Date.now() - S.quiz.start) / 1000);
    t.textContent = String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0");
  }
}, 1000);

/* ---------- 啟動 ---------- */
async function boot(saved) {
  app.innerHTML = loadingView();
  try {
    const { site, courses, problems } = await loadSiteCourses("data/");
    ctx.site = site; ctx.problems = problems; ctx.siteCourses = courses;
    refreshCourses(courses);
  } catch (e) {
    app.innerHTML = fatalView(e.message);
    return;
  }
  fetch("data/templates/course-pack.example.json").then(r => (r.ok ? r.text() : "")).then(t => {
    ctx.template = t.trim();
    if (S.view === "home") render();
  }).catch(() => {});

  if (saved && saved.S) S = saved.S;
  else {
    // 網址帶 #課程id 時直接進入該課程，例如 …#aai
    const hash = location.hash.slice(1);
    if (hash && ctx.courses.some(c => c.id === hash)) { S.courseId = hash; S.view = "course"; }
  }
  render();
}

window.claude?.hot?.snapshot?.(() => ({ S }));
window.claude?.hot?.ready ? window.claude.hot.ready(boot) : boot(window.claude?.hot?.data ?? {});
