// 檢查題庫格式。用法：
//   node tools/validate.js                 檢查 data/catalog.json 底下所有課程
//   node tools/validate.js 我的題庫.json     另外檢查要在首頁匯入的課程檔
// 有錯誤時結束代碼為 1，可放進 CI 或 git hook。
import { readFileSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { normalizeCourse } from "../assets/js/data.js";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const dataDir = join(root, "data");
let errorCount = 0;
let warnCount = 0;

const readJSON = path => {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch (e) {
    throw new Error(`${path} 無法讀取或不是有效的 JSON：${e.message}`);
  }
};

function report(label, { course, errors, warnings }) {
  if (errors.length) {
    console.log(`✗ ${label}`);
    errors.forEach(e => console.log(`    錯誤：${e}`));
  } else {
    const n = course.units.reduce((s, u) => s + u.questions.length, 0);
    console.log(`✓ ${label}：${course.units.length} 個單元、${n} 題`);
    course.units.forEach(u => console.log(`    ${u.id.padEnd(12)} ${String(u.questions.length).padStart(3)} 題  ${u.name}`));
  }
  warnings.forEach(w => console.log(`    提醒：${w}`));
  errorCount += errors.length;
  warnCount += warnings.length;
}

const seen = new Map();
const catalog = readJSON(join(dataDir, "catalog.json"));
for (const entry of catalog.courses || []) {
  const path = join(dataDir, entry.path);
  try {
    if (!existsSync(path)) throw new Error(`catalog.json 列了 ${entry.path}，但檔案不存在`);
    const raw = readJSON(path);
    raw.units = (raw.units || []).map(u => {
      if (!u.file) return u;
      const f = join(dirname(path), u.file);
      if (!existsSync(f)) throw new Error(`單元 ${u.id} 的 file「${u.file}」不存在`);
      return { ...u, questions: readJSON(f).questions };
    });
    const result = normalizeCourse(raw);
    if (result.course) {
      if (seen.has(result.course.id)) result.errors.push(`課程 id「${result.course.id}」和 ${seen.get(result.course.id)} 重複`);
      seen.set(result.course.id, entry.path);
    }
    report(entry.path, result);
  } catch (e) {
    console.log(`✗ ${entry.path}\n    錯誤：${e.message}`);
    errorCount++;
  }
}

for (const arg of process.argv.slice(2)) {
  try {
    const result = normalizeCourse(readJSON(resolve(arg)), { source: "import" });
    if (result.course && seen.has(result.course.id)) {
      result.errors.push(`課程 id「${result.course.id}」和網站內建課程重複，匯入時會被拒絕`);
    }
    report(arg, result);
  } catch (e) {
    console.log(`✗ ${arg}\n    錯誤：${e.message}`);
    errorCount++;
  }
}

console.log(`\n${errorCount ? `共 ${errorCount} 個錯誤` : "沒有錯誤"}${warnCount ? `，${warnCount} 個提醒` : ""}。`);
process.exit(errorCount ? 1 : 0);
