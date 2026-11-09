"""排序題（拖曳）與填空題（下拉選單），分別加進六個單元。
有給 expect / cases 的題目會實際執行：填空題確認每個誘答都會失敗，排序題確認只有一種順序正確。"""
from qlib import order, fill
import u1, u2, u3, u4, u5, u6

# ---------- 1 資料型別與運算子 ----------
U = "types"
fill(U, "py1-f01", u1.S[1], "完成程式碼：距離可能有小數，分鐘必須是整數，最後把結果接在字串前面印出。",
     """
distance = [[1]](input())
minutes = [[2]](input())
print([[3]](round(distance / minutes, 1)) + " 公尺/分")
""", [("float", ["int", "str", "bool"]),
      ("int", ["str", "bool", "len"]),
      ("str", ["int", "float", "print"])],
     "input() 回傳字串。距離可能有小數用 float()；分鐘要整數用 int()；最後用 + 接字串，數值必須先 str() 轉型，否則拋出 TypeError。",
     cases=[dict(stdin="1500.5\n12\n", expect="125.0 公尺/分"), dict(stdin="1500.5\n10\n", expect="150.1 公尺/分")])

fill(U, "py1-f02", u1.S[2], "完成切片，讓程式依序印出 Python 和 nohtyP。",
     """
s = "ITSPython"
print(s[[[1]]])
print(s[[[2]]])
""", [("3:", ["4:", "3:-1", "2:"]),
      (":2:-1", ["::-1", ":3:-1", "-1:3"])],
     "s[3:] 從索引 3（P）取到結尾得 Python。s[:2:-1] 從最後一個字元往回取，停在索引 2 之前（不含 S），得 nohtyP；s[::-1] 會把整個字串反轉。",
     expect="Python\nnohtyP")

order(U, "py1-o01", u1.S[3], "排列下列程式碼，讓程式印出 [1, 2, 3]。",
      ["nums = [3, 1]", "nums.append(2)", "nums.sort()", "print(nums)"],
      "先建立串列，append 把 2 加到尾端得 [3, 1, 2]，sort() 就地排序成 [1, 2, 3]，最後印出。若先 sort 再 append，會得到 [1, 3, 2]。",
      expect="[1, 2, 3]")

order(U, "py1-o02", u1.S[6], "依運算子優先順序，由高（最先計算）到低排列。",
      ["()  括號", "**  次方", "-x  負號", "*  /  //  %", "+  -", "==  !=  <  >  in  is", "not", "and", "or"],
      "括號最優先；** 高於負號（所以 -3 ** 2 是 -9）；接著乘除、加減、比較；邏輯運算子 not > and > or 最後。")

# ---------- 2 流程控制 ----------
U = "flow"
fill(U, "py2-f01", u2.S[0], "完成程式碼：90 分以上為 A，60 分以上為 B，其他為 F。",
     """
score = int(input())
[[1]] score >= 90:
    grade = "A"
[[2]] score >= 60:
    grade = "B"
[[3]]
    grade = "F"
print(grade)
""", [("if", ["elif", "else", "for"]),
      ("elif", ["if", "else if", "else"]),
      ("else:", ["elif:", "else", "if:"])],
     "第一個條件用 if；中間的條件用 elif（不是 else if）；最後的 else 不能接條件，但要有冒號。若第二個也寫 if，95 分會先被設成 A，再被第二個 if 改成 B。",
     cases=[dict(stdin="95\n", expect="A"), dict(stdin="75\n", expect="B"), dict(stdin="30\n", expect="F")])

fill(U, "py2-f02", u2.S[2], "猜數字遊戲最多猜 3 次，猜中就結束。完成程式碼。",
     """
secret = 7
chance = 1
[[1]] chance <= 3:
    guess = int(input())
    if guess == secret:
        print("答對")
        [[2]]
    chance [[3]] 1
else:
    print("機會用完")
""", [("while", ["if", "for", "until"]),
      ("break", ["continue", "pass", "chance = 0"]),
      ("+=", ["=+", "-=", "=="])],
     "while 搭配 chance 計數最多跑 3 次；猜中用 break 跳出（同時略過 while 的 else）；每次猜完 chance += 1。注意 =+ 1 等於 = +1，chance 永遠是 1。迴圈沒有被 break 而正常結束時，才會執行 else。",
     cases=[dict(stdin="3\n7\n", expect="答對"), dict(stdin="1\n2\n3\n", expect="機會用完")])

order(U, "py2-o01", u2.S[3], "排列下列程式碼，計算 1 到 5 的總和並印出 15。",
      ["total = 0", "for i in range(1, 6):", "    total += i", "print(total)"],
      "先把 total 設為 0，for 迴圈把 1 到 5 依序加進 total，迴圈結束後（沒有縮排）才印出。",
      expect="15")

order(U, "py2-o02", u2.S[5], "排列下列程式碼，判斷輸入的 n 是不是質數：輸入 7 印出「是質數」，輸入 9 印出「不是質數」。",
      ["n = int(input())", "for d in range(2, n):", "    if n % d == 0:", "        print('不是質數')", "        break", "else:", "    print('是質數')"],
      "for…else：迴圈跑完都沒有遇到 break，才執行 else。找到因數時要先印出「不是質數」再 break；break 之後的程式不會執行。",
      cases=[dict(stdin="7\n", expect="是質數"), dict(stdin="9\n", expect="不是質數")])

# ---------- 3 輸入與輸出 ----------
U = "io"
fill(U, "py3-f01", u3.S[3], "檔案存在就顯示內容；不存在就建立檔案並寫入第一行。完成程式碼。",
     """
import os
if [[1]]("data.txt"):
    with open("data.txt", [[2]]) as f:
        print(f.[[3]]())
else:
    with open("data.txt", [[4]]) as f:
        f.write("first line")
    print("已建立")
""", [("os.path.isfile", ["os.isfile", "os.path.isdir", "os.exists"]),
      ('"r"', ['"w"', '"a"', '"x"']),
      ("read", ["write", "readlines", "close"]),
      ('"w"', ['"r"', '"rb"', '"rt"'])],
     "os.path.isfile 檢查檔案是否存在；讀取用 \"r\" 模式、f.read() 讀出全部內容；建立新檔用 \"w\"（\"a\" 也能建立，但本題沒有這個選項）。\"r\" 開啟不存在的檔案會拋出 FileNotFoundError。",
     cases=[dict(files={"data.txt": "hello"}, expect="hello"), dict(expect="已建立")])

fill(U, "py3-f02", u3.S[5], "姓名占 10 格靠左，分數占 8 格靠右、四捨五入到小數 2 位。完成 f-string。",
     """
name = "Amy"
score = 87.456
print(f"{name:[[1]]}|{score:[[2]]}|")
""", [("<10", [">10", "^10", "10d"]),
      ("8.2f", ["2.8f", ".2", "8.2d"])],
     "冒號後面是格式：< 靠左、> 靠右、^ 置中，10 是寬度；8.2f 是寬度 8、小數 2 位的浮點數（數字預設靠右）。d 只能用在整數；.2 沒有 f 時代表「2 位有效數字」，會得到 87。",
     expect="Amy       |   87.46|")

order(U, "py3-o01", u3.S[2], "排列下列程式碼：先建立檔案寫入第一行，再附加第二行，最後讀出全部內容。",
      ["with open('log.txt', 'w') as f:", "    f.write('第一行\\n')", "with open('log.txt', 'a') as f:",
       "    f.write('第二行\\n')", "with open('log.txt') as f:", "    print(f.read().strip())"],
      "\"w\" 會清空檔案後寫入，所以要放在最前面；\"a\" 附加在檔尾；最後用預設的 \"r\" 模式讀出。若先附加再用 \"w\"，第二行會被清掉。",
      expect="第一行\n第二行")

# ---------- 4 程式文件與結構 ----------
U = "docs"
fill(U, "py4-f01", u4.S[3], "calc_score 把 value 加到目前分數並回傳；沒有給 value 時加 1。完成程式碼。",
     """
[[1]] calc_score(current, value[[2]]):
    current += value
    [[3]] current

print(calc_score(10), calc_score(10, 5))
""", [("def", ["function", "define", "lambda"]),
      ("=1", ["=0", ":=1", "=None"]),
      ("return", ["print", "yield", "pass"])],
     "定義函式用 def；value=1 讓參數有預設值；用 return 把結果傳回。若用 print，函式本身會回傳 None。",
     expect="11 15")

fill(U, "py4-f02", u4.S[5], "讓 add() 能修改函式外面的 count。完成程式碼。",
     """
count = 0
def add():
    [[1]] count
    count += 1

add()
add()
print(count)
""", [("global", ["local", "nonlocal", "static"])],
     "在函式內對全域變數重新指派，必須先宣告 global。沒有宣告時 count += 1 會拋出 UnboundLocalError。nonlocal 用在巢狀函式，不能指向模組層級的變數。",
     expect="2")

order(U, "py4-o01", u4.S[0], "排列下列程式碼，讓程式印出面積 12.57，再印出函式的 docstring。",
      ["def area(r):", '    """回傳圓面積。"""', "    import math", "    return math.pi * r ** 2",
       "print(round(area(2), 2))", "print(area.__doc__)"],
      "docstring 必須是函式本體的第一個敘述，才會存進 __doc__；如果放在 import 後面，只是一個沒用到的字串，__doc__ 會是 None。",
      expect="12.57\n回傳圓面積。")

# ---------- 5 除錯與例外處理 ----------
U = "errors"
fill(U, "py5-f01", u5.S[2], "使用者輸入的不是整數時，提示並要求重新輸入；輸入正確才印出並結束。完成程式碼。",
     """
while True:
    [[1]]
        n = int(input())
    [[2]] ValueError:
        print("請輸入整數")
    [[3]]
        print("收到", n)
        break
""", [("try:", ["try", "except:", "finally:"]),
      ("except", ["catch", "else", "raise"]),
      ("else:", ["finally:", "else", "elif:"])],
     "try 包住可能出錯的轉型；except ValueError 處理格式錯誤；else 只在沒有例外時執行，所以印出並 break。若用 finally，出錯時也會執行，n 還沒有值就會拋出 NameError。Python 沒有 catch。",
     cases=[dict(stdin="abc\n3\n", expect="請輸入整數\n收到 3"), dict(stdin="8\n", expect="收到 8")])

order(U, "py5-o01", u5.S[3], "排列下列程式碼，讓輸出為「成功 5」再「結束」。",
      ["try:", "    x = int('5')", "except ValueError:", "    print('錯誤')", "else:", "    print('成功', x)", "finally:", "    print('結束')"],
      "順序固定是 try → except → else → finally。else 在沒有例外時執行，finally 不論如何都會執行。",
      expect="成功 5\n結束")

fill(U, "py5-f02", u5.S[5], "完成單元測試，確認 add(2, 3) 等於 5。",
     """
import unittest

def add(a, b):
    return a + b

class TestAdd([[1]]):
    def [[2]](self):
        self.[[3]](add(2, 3), 5)

if __name__ == "__main__":
    unittest.main()
""", [("unittest.TestCase", ["unittest", "TestCase.unittest", "object"]),
      ("test_add", ["add_test", "check_add", "Test_add"]),
      ("assertEqual", ["assertIn", "assertIsNone", "assertRaises"])],
     "測試類別繼承 unittest.TestCase；方法名稱要以小寫 test 開頭才會被執行；比較兩個值是否相等用 assertEqual。")

# ---------- 6 模組與工具 ----------
U = "modules"
fill(U, "py6-f01", u6.S[0], "只匯入 randint，並模擬擲一次骰子。完成程式碼。",
     """
[[1]] random [[2]] randint
dice = [[3]](1, 6)
print(1 <= dice <= 6)
""", [("from", ["import", "include", "using"]),
      ("import", ["from", "as", "use"]),
      ("randint", ["random.randint", "randrange.int", "rand"])],
     "from 模組 import 名稱，匯入後直接用 randint(1, 6) 呼叫。這種寫法沒有定義 random 這個名稱，所以 random.randint 會拋出 NameError。",
     expect="True")

fill(U, "py6-f02", u6.S[3], "印出 2024/03/09 以及當天是星期幾（星期一為 0）。完成程式碼。",
     """
from datetime import date
d = date(2024, 3, 9)
print(d.[[1]]("%Y/%m/%d"), d.[[2]]())
""", [("strftime", ["strptime", "format_date", "isoformat"]),
      ("weekday", ["isoweekday", "day", "week"])],
     "strftime 把日期格式化成字串（strptime 是反過來解析字串）。weekday() 星期一為 0，2024/3/9 是星期六，所以是 5；isoweekday() 星期一為 1，會得到 6。",
     expect="2024/03/09 5")

order(U, "py6-o01", u6.S[1], "排列下列程式碼：把輸入的數取絕對值後，再無條件進位成整數。輸入 -3.2 時應印出 4。",
      ["import math", "x = math.fabs(float(input()))", "x = math.ceil(x)", "print(x)"],
      "先 fabs 取絕對值得 3.2，再 ceil 無條件進位得 4。若順序相反，ceil(-3.2) 是 -3，取絕對值後變成 3.0。",
      stdin="-3.2\n", expect="4")
