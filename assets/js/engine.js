// 出題、計分。只處理資料，不碰畫面。
import { range, shuffle } from "./util.js";

export const qkey = (unitId, qid) => unitId + "/" + qid;

// 課程內所有題目的索引：key → { unit, q }
export function indexCourse(course) {
  const map = new Map();
  course.units.forEach(u => u.questions.forEach(q => map.set(qkey(u.id, q.id), { unit: u, q })));
  return map;
}

// 作答紀錄（picks）的格式依題型不同：
//   single / truefalse：選到的顯示位置（數字）
//   order：使用者排好的順序，元素是 q.items 的原始索引
//   fill：每個空格選到的選項原始索引（未選為 null）
export function makeItem(unitId, q, shuffleOptions) {
  const base = { key: qkey(unitId, q.id), unit: unitId, kind: q.type };
  if (q.type === "order") {
    // 打亂順序；盡量避免一開始就剛好是正確順序
    let perm = shuffle(range(q.items.length));
    for (let t = 0; t < 10 && orderRight(q, perm); t++) perm = shuffle(range(q.items.length));
    return { ...base, perm };
  }
  if (q.type === "fill") {
    return { ...base, perm: q.blanks.map(b => (shuffleOptions ? shuffle(range(b.options.length)) : range(b.options.length))) };
  }
  const perm = shuffleOptions ? shuffle(range(q.options.length)) : range(q.options.length);
  return { ...base, perm, ans: perm.indexOf(q.answer) };
}

// 排序題用文字比對，所以內容相同的兩行（例如兩個 break）互換位置也算對
const orderRight = (q, order) => order.every((oi, k) => q.items[oi] === q.items[k]);

// 排序題、填空題作答中的暫存狀態（按「確認作答」才會寫進 picks）
export const initialWork = it =>
  it.kind === "order" ? it.perm.slice() : it.kind === "fill" ? it.perm.map(() => null) : null;

export function isRight(q, it, pick) {
  if (pick === null || pick === undefined) return false;
  if (q.type === "order") return orderRight(q, pick);
  if (q.type === "fill") return pick.every((v, b) => v === q.blanks[b].answer);
  return pick === it.ans;
}

// scope：單元 id、"mix"（全部單元平均抽題）或傳入 keys（錯題本、重做錯題）
export function buildItems(course, { scope, count, shuffleOptions, keys }) {
  const index = indexCourse(course);
  if (keys) {
    return shuffle(keys.filter(k => index.has(k))).map(k => {
      const { unit, q } = index.get(k);
      return makeItem(unit.id, q, shuffleOptions);
    });
  }
  const units = scope === "mix" ? course.units : course.units.filter(u => u.id === scope);
  const total = units.reduce((n, u) => n + u.questions.length, 0);
  const n = count === "all" ? total : Math.min(count, total);

  // 各單元輪流抽一題，題目少的單元抽完就跳過，所以題數會盡量平均
  const pools = shuffle(units).map(u => ({ unit: u, qs: shuffle(u.questions) }));
  const items = [];
  while (items.length < n) {
    let took = false;
    for (const p of pools) {
      if (items.length >= n) break;
      const q = p.qs.pop();
      if (q) { items.push(makeItem(p.unit.id, q, shuffleOptions)); took = true; }
    }
    if (!took) break;
  }
  return shuffle(items);
}

export function scoreQuiz(quiz, course) {
  const index = indexCourse(course);
  const okArr = quiz.items.map((it, i) => index.has(it.key) && isRight(index.get(it.key).q, it, quiz.picks[i]));
  const correct = okArr.filter(Boolean).length;
  const total = quiz.items.length;
  const byUnit = course.units
    .map(u => {
      const idx = quiz.items.map((it, i) => (it.unit === u.id ? i : -1)).filter(i => i >= 0);
      return { unit: u, correct: idx.filter(i => okArr[i]).length, total: idx.length };
    })
    .filter(r => r.total > 0);
  return {
    okArr, correct, total,
    pct: total ? Math.round((correct / total) * 100) : 0,
    byUnit,
    wrongKeys: quiz.items.filter((_, i) => !okArr[i]).map(it => it.key),
    rightKeys: quiz.items.filter((_, i) => okArr[i]).map(it => it.key)
  };
}
