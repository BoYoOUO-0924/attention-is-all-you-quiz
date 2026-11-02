// 題庫格式的檢查與正規化。網站載入、首頁匯入、tools/validate.js 都共用這裡的規則。

export const QUESTION_TYPES = ["single", "truefalse"];
export const MIN_OPTIONS = 2;
export const MAX_OPTIONS = 6;

const ID_RE = /^[a-z0-9][a-z0-9-]*$/;
const isStr = s => typeof s === "string" && s.trim() !== "";

export function normalizeQuestion(raw, where, errors) {
  if (!raw || typeof raw !== "object") {
    errors.push(`${where}：題目必須是物件`);
    return null;
  }
  const type = raw.type ?? "single";
  if (!QUESTION_TYPES.includes(type)) {
    errors.push(`${where}：不支援的題型「${type}」，可用 ${QUESTION_TYPES.join("、")}`);
    return null;
  }
  let options = raw.options;
  let answer = raw.answer;
  if (type === "truefalse") {
    options = options ?? ["正確", "錯誤"];
    if (typeof answer === "boolean") answer = answer ? 0 : 1;
  }

  const before = errors.length;
  if (!isStr(raw.id)) errors.push(`${where}：缺少 id`);
  if (!isStr(raw.q)) errors.push(`${where}：缺少題幹 q`);
  if (!Array.isArray(options) || options.length < MIN_OPTIONS || options.length > MAX_OPTIONS || !options.every(isStr)) {
    errors.push(`${where}：options 必須是 ${MIN_OPTIONS}–${MAX_OPTIONS} 個非空字串`);
  } else if (!Number.isInteger(answer) || answer < 0 || answer >= options.length) {
    errors.push(`${where}：answer 必須是 0 到 ${options.length - 1} 的整數（0 代表第一個選項）`);
  }
  if (raw.explain !== undefined && typeof raw.explain !== "string") errors.push(`${where}：explain 必須是字串`);
  if (raw.tags !== undefined && !(Array.isArray(raw.tags) && raw.tags.every(isStr))) errors.push(`${where}：tags 必須是字串陣列`);
  if (errors.length > before) return null;

  return { id: raw.id.trim(), type, q: raw.q, options, answer, explain: raw.explain ?? "", tags: raw.tags ?? [] };
}

// raw.units[].questions 必須已經是陣列（題庫放在單元檔裡的，要先讀進來再傳入）
export function normalizeCourse(raw, { source = "site" } = {}) {
  const errors = [];
  const warnings = [];
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
    return { course: null, errors: ["課程檔必須是 JSON 物件"], warnings };
  }
  if (!isStr(raw.id)) errors.push("課程缺少 id");
  else if (!ID_RE.test(raw.id)) errors.push(`課程 id「${raw.id}」只能用小寫英文、數字與 -`);
  if (!isStr(raw.name)) errors.push("課程缺少 name");
  if (!Array.isArray(raw.units) || raw.units.length === 0) errors.push("課程至少要有一個單元（units）");

  const units = [];
  const unitIds = new Set();
  (Array.isArray(raw.units) ? raw.units : []).forEach((u, ui) => {
    const uw = `單元 ${u && u.id ? u.id : "#" + (ui + 1)}`;
    if (!u || !isStr(u.id)) { errors.push(`${uw}：缺少 id`); return; }
    if (!ID_RE.test(u.id)) errors.push(`${uw}：id 只能用小寫英文、數字與 -`);
    if (unitIds.has(u.id)) errors.push(`${uw}：單元 id 重複`);
    unitIds.add(u.id);
    if (!isStr(u.name)) errors.push(`${uw}：缺少 name`);
    if (!Array.isArray(u.questions)) { errors.push(`${uw}：缺少 questions 陣列`); return; }
    if (u.questions.length === 0) warnings.push(`${uw}：目前沒有題目`);

    const qids = new Set();
    const questions = [];
    u.questions.forEach((q, qi) => {
      const n = normalizeQuestion(q, `${uw} 第 ${qi + 1} 題${q && q.id ? `（${q.id}）` : ""}`, errors);
      if (!n) return;
      if (qids.has(n.id)) { errors.push(`${uw}：題目 id「${n.id}」重複`); return; }
      qids.add(n.id);
      if (!n.explain) warnings.push(`${uw} ${n.id}：沒有解析`);
      questions.push(n);
    });
    // sections 是講義章節清單（選填）。有寫的話，每題的第一個 tag 要對應到其中一章，用來檢查每章都有出題
    const sections = Array.isArray(u.sections) ? u.sections.filter(isStr) : [];
    if (sections.length) {
      const count = new Map(sections.map(s => [s, 0]));
      questions.forEach(q => {
        if (count.has(q.tags[0])) count.set(q.tags[0], count.get(q.tags[0]) + 1);
        else warnings.push(`${uw} ${q.id}：第一個 tag「${q.tags[0] ?? "（沒有）"}」不在 sections 裡`);
      });
      count.forEach((n, s) => { if (!n) warnings.push(`${uw}：章節「${s}」還沒有題目`); });
    }
    units.push({
      id: u.id, name: u.name || u.id, sub: u.sub || "",
      topics: Array.isArray(u.topics) ? u.topics.filter(isStr) : [],
      sections,
      questions
    });
  });

  const course = { id: raw.id, code: raw.code || "", name: raw.name, desc: raw.desc || "", source, units };
  return { course: errors.length ? null : course, errors, warnings };
}

// 網站內建課程：catalog.json → 各課程的 course.json → 單元的 file 題庫檔
export async function loadSiteCourses(base = "data/") {
  const getJSON = async url => {
    const r = await fetch(url, { cache: "no-cache" });
    if (!r.ok) throw new Error(`${url} 讀取失敗（HTTP ${r.status}）`);
    return r.json();
  };
  const catalog = await getJSON(base + "catalog.json");
  const courses = [];
  const problems = [];
  for (const entry of catalog.courses || []) {
    try {
      const path = base + entry.path;
      const dir = path.slice(0, path.lastIndexOf("/") + 1);
      const raw = await getJSON(path);
      raw.units = await Promise.all((raw.units || []).map(async u =>
        u.file ? { ...u, questions: (await getJSON(dir + u.file)).questions } : u));
      const { course, errors } = normalizeCourse(raw);
      if (course) courses.push(course);
      else problems.push(`${entry.path}：${errors.join("；")}`);
    } catch (e) {
      problems.push(e.message);
    }
  }
  return { site: catalog.site || {}, courses, problems };
}
