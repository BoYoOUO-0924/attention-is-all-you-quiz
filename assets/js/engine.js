// 出題、計分。只處理資料，不碰畫面。
import { range, shuffle } from "./util.js";

export const qkey = (unitId, qid) => unitId + "/" + qid;

// 課程內所有題目的索引：key → { unit, q }
export function indexCourse(course) {
  const map = new Map();
  course.units.forEach(u => u.questions.forEach(q => map.set(qkey(u.id, q.id), { unit: u, q })));
  return map;
}

export function makeItem(unitId, q, shuffleOptions) {
  const perm = shuffleOptions ? shuffle(range(q.options.length)) : range(q.options.length);
  return { key: qkey(unitId, q.id), unit: unitId, perm, ans: perm.indexOf(q.answer) };
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
  const okArr = quiz.items.map((it, i) => quiz.picks[i] === it.ans);
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
