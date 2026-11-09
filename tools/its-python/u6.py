from qlib import mc, tf, out, raises, check

U = "modules"
S = ["import 語法", "math 模組", "random 模組", "datetime 模組", "os、os.path 與 sys 模組"]
A, B, C, D, E = S
n = iter(range(1, 999))
i = lambda: f"py6-{next(n):03d}"

out(U, i(), A, """
import math as m
print(m.sqrt(49))
""", ["7", "49.0", "拋出 NameError"],
    "import 模組 as 別名 之後，用別名存取模組內容。math.sqrt 回傳 float：7.0。")

raises(U, i(), A, """
from math import sqrt
print(math.sqrt(16))
""", ["4.0", "4", "拋出 ImportError"],
    "from math import sqrt 只匯入 sqrt 這個名稱，並沒有定義 math，所以 math.sqrt 會拋出 NameError。應直接寫 sqrt(16)。")

mc(U, i(), A, "只想使用 random 模組中的 randint，並直接以 randint(1, 6) 呼叫，應如何匯入？",
   "from random import randint", ["import randint from random", "import random.randint", "include random.randint"],
   "from 模組 import 名稱，匯入後可直接使用該名稱。import random 則必須寫 random.randint(1, 6)。")

tf(U, i(), A, "from math import * 會匯入 math 中所有公開名稱，但容易與自己的變數名稱衝突，一般不建議使用。", True,
   "萬用匯入讓人看不出名稱從哪裡來，也可能蓋掉同名的變數或函式。")

out(U, i(), B, """
import math
print(math.ceil(4.1), math.floor(4.9), math.ceil(-4.1), math.floor(-4.1))
""", ["5 4 -5 -4", "4 5 -4 -5", "5 5 -4 -4"],
    "ceil 往正無限大取整（無條件進位）；floor 往負無限大取整（無條件捨去）。負數時要特別注意：ceil(-4.1) = -4、floor(-4.1) = -5。")

out(U, i(), B, """
import math
print(math.trunc(-4.7), math.floor(-4.7), int(-4.7))
""", ["-5 -5 -5", "-4 -4 -4", "-5 -4 -4"],
    "trunc 與 int() 直接截去小數（往 0 取整）得 -4；floor 往負無限大取整得 -5。")

out(U, i(), B, """
import math
print(math.fabs(-3), abs(-3))
""", ["3 3", "3.0 3.0", "-3.0 3"],
    "math.fabs 一律回傳 float（3.0）；內建 abs 保留原本型別（int 3）。")

out(U, i(), B, """
import math
print(math.fmod(-7, 3), -7 % 3)
""", ["-1 2", "2.0 2", "-1.0 -1"],
    "math.fmod 結果的正負號跟被除數相同（-1.0）；% 運算子結果的正負號跟除數相同（2）。")

out(U, i(), B, """
import math
print(math.pow(2, 3), 2 ** 3, math.sqrt(2) ** 2 == 2)
""", ["8 8 True", "8.0 8.0 True", "8 8.0 False"],
    "math.pow 一律回傳 float（8.0）；** 兩邊是整數就回傳 int。sqrt(2) 的平方因浮點誤差得 2.0000000000000004，不等於 2。")

out(U, i(), B, """
import math
print(math.isqrt(17), round(math.pi, 3), math.factorial(5))
""", ["4.123 3.141 120", "4 3.14 25", "5 3.142 120"],
    "isqrt 回傳整數平方根（無條件捨去）：4；math.pi 四捨五入到 3 位：3.142；5! = 120。")

out(U, i(), B, """
import math
x = math.nan
print(x == x, math.isnan(x))
""", ["True True", "True False", "False False"],
    "NaN（Not a Number）跟任何值比較都不相等，連自己也不等於自己。要判斷 NaN 必須用 math.isnan()。")

out(U, i(), B, """
import math
print(math.frexp(8))
""", ["(8, 0)", "(1.0, 3)", "(0.5, 3)"],
    "frexp(x) 回傳 (m, e)，使 x = m × 2**e 且 0.5 <= |m| < 1。8 = 0.5 × 2**4。")

mc(U, i(), C, "random.randint(1, 6) 可能回傳哪些值？",
   "1、2、3、4、5、6 其中之一", ["1 到 5 的整數", "0 到 6 的整數", "1 到 6 之間的任意浮點數"],
   "randint(a, b) 包含兩端點 a 與 b，這點與 range 不同。")

mc(U, i(), C, "random.randrange(0, 10, 3) 可能回傳哪些值？",
   "0、3、6、9", ["3、6、9", "0、3、6、9、10", "0 到 10 的任意整數"],
   "randrange 的參數與 range 一樣：從 0 開始每次加 3，不含 10，所以從 0、3、6、9 中隨機挑一個。")
check("import random\nprint(sorted({random.randrange(0, 10, 3) for _ in range(2000)}))", "[0, 3, 6, 9]")

mc(U, i(), C, "random.random() 回傳值的範圍是？",
   "0.0 <= x < 1.0 的浮點數", ["0.0 <= x <= 1.0 的浮點數", "0 或 1", "0 到 100 的整數"],
   "random() 回傳 [0.0, 1.0) 之間的浮點數，包含 0 但不包含 1。要其他範圍可以用 uniform(a, b)。")

out(U, i(), C, """
import random
cards = ["A", "B", "C"]
result = random.shuffle(cards)
print(result, len(cards))
""", ["['B', 'C', 'A'] 3", "拋出 TypeError", "None 0"],
    "shuffle 就地打亂原串列，回傳值是 None。常見錯誤是寫成 cards = random.shuffle(cards)，結果 cards 變成 None。")

mc(U, i(), C, "要從串列 names 中隨機抽出 3 個「不重複」的人，應使用？",
   "random.sample(names, 3)", ["random.choice(names, 3)", "random.shuffle(names, 3)", "random.randint(names, 3)"],
   "sample(母體, k) 回傳 k 個不重複的元素組成的新串列；choice(seq) 只抽一個；choices(seq, k=3) 會抽 3 個但可能重複。")

out(U, i(), C, """
import random
random.seed(42)
a = random.randint(1, 100)
random.seed(42)
b = random.randint(1, 100)
print(a == b)
""", ["False", "可能是 True 也可能是 False", "拋出 ValueError"],
    "設定相同的 seed，接下來產生的亂數序列就完全相同，常用於讓實驗結果可以重現。")

mc(U, i(), C, "要模擬擲骰子，下列哪一個運算式「不能」得到 1 到 6 的整數？",
   "random.randrange(1, 6)",
   ["random.randint(1, 6)", "random.choice([1, 2, 3, 4, 5, 6])", "random.randrange(1, 7)"],
   "randrange(1, 6) 不含 6，只會得到 1 到 5。")

out(U, i(), D, """
from datetime import datetime
d = datetime(2024, 3, 9, 14, 5)
print(d.strftime("%Y/%m/%d %H:%M"))
""", ["2024/3/9 14:5", "24/03/09 02:05", "2024/09/03 14:05"],
    "%Y 四位數年、%m 兩位數月、%d 兩位數日、%H 24 小時制、%M 分鐘，不足兩位補 0。")

out(U, i(), D, """
from datetime import date
d = date(2024, 3, 9)
print(d.weekday(), d.isoweekday())
""", ["6 7", "5 5", "6 6"],
    "2024/3/9 是星期六。weekday() 星期一為 0、星期日為 6，所以是 5；isoweekday() 星期一為 1、星期日為 7，所以是 6。")

out(U, i(), D, """
from datetime import date, timedelta
d = date(2024, 2, 27) + timedelta(days=3)
print(d)
""", ["2024-02-30", "2024-03-02", "2024-3-1"],
    "timedelta 表示時間間隔，可以直接加減日期，會自動處理月底與閏年：2024 年 2 月有 29 天，所以是 3 月 1 日。")

out(U, i(), D, """
from datetime import date
d1 = date(2024, 1, 1)
d2 = date(2024, 3, 1)
print((d2 - d1).days)
""", ["59", "2", "61"],
    "兩個日期相減得到 timedelta，.days 是相差的天數：1 月 31 天 + 2 月 29 天（2024 是閏年）= 60。")

out(U, i(), D, """
from datetime import datetime
d = datetime(2024, 12, 25)
print(d.strftime("%A %B %j"), d.year, d.month)
""", ["Wed Dec 360 2024 12", "Wednesday December 25 2024 12", "Tuesday December 359 2024 12"],
    "%A 星期全名、%B 月份全名、%j 一年中的第幾天（001–366）。2024 是閏年，12/25 是第 360 天。")

mc(U, i(), D, "要取得「現在的日期與時間」，應使用？",
   "datetime.datetime.now()", ["datetime.now.datetime()", "datetime.date.now()", "time.datetime()"],
   "datetime.datetime.now() 回傳目前的日期與時間；只要日期可用 datetime.date.today()。")

mc(U, i(), D, "strftime 與 strptime 的差別是？",
   "strftime 把日期時間轉成字串；strptime 把字串解析成日期時間",
   ["兩者完全相同", "strftime 把字串解析成日期時間；strptime 把日期時間轉成字串", "strptime 只能處理日期，不能處理時間"],
   "記法：f = format（格式化輸出成字串），p = parse（解析字串）。例如 datetime.strptime(\"2024-03-09\", \"%Y-%m-%d\")。")

out(U, i(), E, """
import os
print(os.path.join("data", "2024", "a.csv"))
""", ["data2024a.csv", "data\\2024\\a.csv（所有系統都一樣）", "data, 2024, a.csv"],
    "os.path.join 依作業系統使用正確的路徑分隔字元串接：Linux / macOS 是 /，Windows 是 \\。（本題在 Linux 上執行。）")

out(U, i(), E, """
import os
p = "/home/amy/report.final.txt"
print(os.path.splitext(p)[1], os.path.dirname(p))
""", [".final.txt /home/amy/report", "txt /home/amy", "report.final /home"],
    "splitext 只從最後一個點切開，取得副檔名 \".txt\"；dirname 取得所在資料夾。")

mc(U, i(), E, "要取得目前的工作目錄、並列出某資料夾裡的所有檔案名稱，應分別使用？",
   "os.getcwd() 與 os.listdir(路徑)", ["os.path.cwd() 與 os.path.list(路徑)", "sys.getcwd() 與 sys.listdir(路徑)", "os.pwd() 與 os.ls(路徑)"],
   "os.getcwd() 取得目前工作目錄；os.listdir() 回傳資料夾中檔案與子資料夾名稱的串列；os.mkdir() 建立資料夾。")

out(U, i(), E, """
import os
os.mkdir("backup")
with open("backup/a.txt", "w") as f:
    f.write("x")
print(os.listdir("backup"), os.path.isdir("backup"))
""", ["['backup/a.txt'] True", "['a.txt'] False", "[] True"],
    "os.mkdir 建立資料夾；listdir 只回傳名稱，不含路徑。")

mc(U, i(), E, "sys 模組中，哪一個可以讓程式立刻結束，並回傳結束代碼？",
   "sys.exit()", ["sys.stop()", "sys.quit()", "sys.end()"],
   "sys.exit(0) 代表正常結束，非 0 通常代表錯誤。它其實是拋出 SystemExit 例外。")

mc(U, i(), E, "要查詢目前使用的 Python 版本，可以使用？",
   "sys.version", ["os.version", "sys.python()", "math.version"],
   "sys.version 是版本字串；sys.version_info 是可以比較的結構，例如 sys.version_info >= (3, 8)。")
