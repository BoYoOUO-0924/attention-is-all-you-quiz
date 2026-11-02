// 瀏覽器本機儲存。私密視窗或封鎖網站資料時會讀寫失敗，所以一律包 try/catch，失敗就當作沒有資料。
const PREFIX = "aiquiz:";

export const store = {
  get(key, fallback = null) {
    try {
      const v = localStorage.getItem(PREFIX + key);
      return v ? JSON.parse(v) : fallback;
    } catch (e) {
      return fallback;
    }
  },
  set(key, value) {
    try {
      localStorage.setItem(PREFIX + key, JSON.stringify(value));
      return true;
    } catch (e) {
      return false;
    }
  },
  del(key) {
    try { localStorage.removeItem(PREFIX + key); } catch (e) {}
  }
};
