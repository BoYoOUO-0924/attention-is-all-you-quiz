"""產生 ITS Python 練習題庫。用法（在專案根目錄）：
    python3 tools/its-python/build.py data/courses/its-python
u1.py–u6.py 是六個單元的題目。輸出題的正解由實際執行程式碼取得，
正解若與誘答選項重複、或程式碼執行出錯，產生時就會中斷。
"""
import json, os, sys
import qlib, u1, u2, u3, u4, u5, u6

out_dir = sys.argv[1] if len(sys.argv) > 1 else "data/courses/its-python"
os.makedirs(out_dir, exist_ok=True)
meta = [
    (u1, "types", "1 資料型別與運算子", "Data Types and Operators", ["型別判斷與轉換", "索引與切片", "串列操作", "運算子優先順序"]),
    (u2, "flow", "2 流程控制", "Flow Control with Decisions and Loops", ["if / elif / else", "while", "for / range", "break / continue"]),
    (u3, "io", "3 輸入與輸出", "Input and Output Operations", ["檔案讀寫", "os.path", "input / print", "f-string", "sys.argv"]),
    (u4, "docs", "4 程式文件與結構", "Code Documentation and Structure", ["註解與 docstring", "縮排", "函式與參數", "變數範圍"]),
    (u5, "errors", "5 除錯與例外處理", "Troubleshooting and Error Handling", ["錯誤類型", "try / except / finally", "raise", "unittest"]),
    (u6, "modules", "6 模組與工具", "Operations Using Modules and Tools", ["math", "random", "datetime", "os / sys"]),
]
units = []
for mod, uid, name, sub, topics in meta:
    qs = qlib.ALL[uid]
    with open(os.path.join(out_dir, f"{uid}.json"), "w", encoding="utf-8") as f:
        json.dump({"questions": qs}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    units.append({"id": uid, "name": name, "sub": sub, "topics": topics, "file": f"{uid}.json", "sections": mod.S})
    print(uid, len(qs))
course = {
    "id": "its-python",
    "code": "ITS Python",
    "name": "ITS Python 認證練習",
    "desc": "依 Certiport IT Specialist – Python 公開的六大考試範圍編寫的原創練習題（非官方考題）。程式題的答案都實際執行 Python 3 驗證過。",
    "units": units,
}
with open(os.path.join(out_dir, "course.json"), "w", encoding="utf-8") as f:
    json.dump(course, f, ensure_ascii=False, indent=2)
    f.write("\n")
