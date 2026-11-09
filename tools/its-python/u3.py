from qlib import mc, tf, out, raises

U = "io"
S = ["開啟模式與 with", "讀取檔案", "寫入與附加", "檢查與刪除檔案", "input 主控台輸入", "print 與字串格式化", "命令列參數 sys.argv"]
A, B, C, D, E, F, G = S
n = iter(range(1, 999))
i = lambda: f"py3-{next(n):03d}"

mc(U, i(), A, "open() 的模式中，哪一個會「清空原有內容再寫入，檔案不存在就建立」？",
   "\"w\"", ["\"a\"", "\"r\"", "\"x\""],
   "\"w\" 覆寫；\"a\" 附加在檔尾；\"r\" 唯讀（檔案不存在會出錯）；\"x\" 只在檔案不存在時建立，已存在會出錯。")

mc(U, i(), A, "要把資料加在既有檔案 log.txt 的最後面，而不刪除原本內容，應使用哪個模式？",
   "open(\"log.txt\", \"a\")", ["open(\"log.txt\", \"w\")", "open(\"log.txt\", \"r\")", "open(\"log.txt\", \"r+\")"],
   "\"a\"（append）會把寫入位置放在檔尾；\"r+\" 雖可讀寫，但寫入位置從檔頭開始，會蓋掉原本的內容。")

raises(U, i(), A, """
f = open("no_such_file.txt", "r")
print(f.read())
""", ["（沒有輸出）", "建立空白檔案後印出空字串", "拋出 PermissionError"],
    "以 \"r\" 模式開啟不存在的檔案會拋出 FileNotFoundError。")

mc(U, i(), A, "使用 with open(...) as f: 的主要好處是？",
   "離開區塊時會自動關閉檔案，即使中途發生例外也一樣",
   ["讀取速度比較快", "可以同時開啟多個模式", "檔案不存在時會自動建立"],
   "with 是內容管理器（context manager），區塊結束就呼叫 f.close()，不必自己記得關檔。")

tf(U, i(), A, "以 \"w\" 模式開啟一個已經存在的檔案，原本的內容會被清空。", True,
   "\"w\" 一開啟就把檔案截斷為 0 位元組，即使之後什麼都沒寫入。")

out(U, i(), B, """
with open("data.txt") as f:
    print(f.read())
""", ["Line1", "['Line1\\n', 'Line2\\n', 'Line3']", "Line1 Line2 Line3"],
    "read() 一次讀入全部內容成為一個字串，換行字元也會保留。",
    files={"data.txt": "Line1\nLine2\nLine3"})

out(U, i(), B, """
with open("data.txt") as f:
    print(f.readline(), end="")
    print(f.readline(), end="")
""", ["Line1", "Line1\nLine2\nLine3", "Line2\nLine3"],
    "readline() 每次讀一行（含結尾的 \\n），檔案指標會往後移，所以第二次讀到第二行。",
    files={"data.txt": "Line1\nLine2\nLine3"})

out(U, i(), B, """
with open("data.txt") as f:
    lines = f.readlines()
print(len(lines), repr(lines[0]))
""", ["3 'Line1'", "1 'Line1\\nLine2\\nLine3'", "14 'L'"],
    "readlines() 回傳串列，每一行是一個元素，而且保留結尾的換行字元 \\n（最後一行沒有換行就不含）。",
    files={"data.txt": "Line1\nLine2\nLine3"})

out(U, i(), B, """
total = 0
with open("scores.txt") as f:
    for line in f:
        total += int(line.strip())
print(total)
""", ["807090", "拋出 ValueError", "3"],
    "檔案物件可以直接用 for 逐行走訪。line.strip() 去掉換行字元後再轉 int：80 + 70 + 90 = 240。（int() 其實也會忽略頭尾空白。）",
    files={"scores.txt": "80\n70\n90\n"})

out(U, i(), B, """
with open("data.txt") as f:
    print(f.read(3))
    print(f.read())
""", ["Lin\nLine1\nLine2", "Line1\nLine2", "Lin"],
    "read(n) 讀取 n 個字元。第二次 read() 從上次停下的位置繼續讀到檔尾。",
    files={"data.txt": "Line1\nLine2"})

out(U, i(), C, """
with open("out.txt", "w") as f:
    f.write("A")
    f.write("B\\n")
    f.write("C")
with open("out.txt") as f:
    print(f.read())
""", ["A\nB\nC", "ABC", "A B\nC"],
    "write() 不會自動換行，要換行必須自己寫 \\n。所以 A 與 B 接在同一行。")

out(U, i(), C, """
with open("log.txt", "a") as f:
    f.write("new\\n")
with open("log.txt") as f:
    print(f.read().strip())
""", ["new", "old", "new\nold"],
    "\"a\" 模式把新資料寫在檔尾，原本的內容保留。",
    files={"log.txt": "old\n"})

out(U, i(), C, """
with open("log.txt", "w") as f:
    f.write("new\\n")
with open("log.txt") as f:
    print(f.read().strip())
""", ["old\nnew", "new\nold", "old"],
    "\"w\" 模式先清空檔案，所以原本的 old 消失了。",
    files={"log.txt": "old\n"})

out(U, i(), C, """
names = ["Amy", "Ben"]
with open("n.txt", "w") as f:
    f.writelines(names)
    print("Cat", file=f)
with open("n.txt") as f:
    print(f.read().strip())
""", ["Amy\nBen\nCat", "['Amy', 'Ben']Cat", "Amy Ben Cat"],
    "writelines() 不會替每個元素加換行，所以 Amy、Ben 黏在一起。print(..., file=f) 會把內容寫進檔案並自動加上換行。")

raises(U, i(), C, """
with open("n.txt", "w") as f:
    f.write(100)
""", ["寫入 100", "寫入 \"100\"", "（沒有輸出），檔案是空的"],
    "write() 只接受字串，傳入 int 會拋出 TypeError，要寫成 f.write(str(100))。")

out(U, i(), D, """
import os
print(os.path.exists("a.txt"), os.path.isfile("a.txt"), os.path.isdir("a.txt"))
""", ["True False True", "False False False", "True True True"],
    "exists 判斷路徑是否存在；isfile 是否為檔案；isdir 是否為資料夾。a.txt 是檔案，所以 isdir 為 False。",
    files={"a.txt": "x"})

mc(U, i(), D, "下列哪一段程式可以「檔案存在才刪除」，避免出錯？",
   "if os.path.exists(\"old.txt\"):\n    os.remove(\"old.txt\")",
   ["if os.exists(\"old.txt\"):\n    os.delete(\"old.txt\")",
    "if os.path.isfile(\"old.txt\"):\n    os.path.remove(\"old.txt\")",
    "os.remove(\"old.txt\", force=True)"],
   "os.path.exists 檢查路徑是否存在；刪除檔案用 os.remove()（等同 os.unlink）。os 沒有 exists、delete 函式，os.path 也沒有 remove。")

raises(U, i(), D, """
import os
os.remove("ghost.txt")
print("已刪除")
""", ["已刪除", "（沒有輸出）", "拋出 PermissionError"],
    "刪除不存在的檔案會拋出 FileNotFoundError。可先用 os.path.exists 檢查，或用 try/except 處理。")

out(U, i(), D, """
import os
with open("t.txt", "w") as f:
    f.write("hello")
print(os.path.getsize("t.txt"), os.path.basename("/home/user/t.txt"))
""", ["5 /home/user/t.txt", "6 t.txt", "1 t"],
    "getsize 回傳檔案大小（位元組），\"hello\" 是 5 個 ASCII 字元。basename 取出路徑最後的檔名。")

out(U, i(), E, """
a = input()
b = input()
print(a + b)
""", ["5", "2 3", "拋出 TypeError"],
    "input() 永遠回傳字串，\"2\" + \"3\" 是字串串接得 \"23\"。要計算得先 int()。",
    q="使用者依序輸入 2 和 3（各按一次 Enter），輸出為何？", stdin="2\n3\n")

out(U, i(), E, """
a = int(input())
b = float(input())
print(a + b)
""", ["23", "5", "拋出 TypeError"],
    "先轉型再運算。int + float 結果是 float：2 + 3.0 = 5.0。",
    q="使用者依序輸入 2 和 3（各按一次 Enter），輸出為何？", stdin="2\n3\n")

raises(U, i(), E, """
age = int(input("年齡："))
print(age + 1)
""", ["年齡：19", "年齡：18.51", "拋出 TypeError"],
    "使用者輸入 \"18.5\"，int(\"18.5\") 不是整數格式，會拋出 ValueError。",
    q="使用者輸入 18.5 時，下列程式會發生什麼事？", stdin="18.5\n")

out(U, i(), E, """
x, y = input().split(",")
print(int(x) * int(y))
""", ["6,7", "拋出 ValueError", "67"],
    "split(\",\") 以逗號切開成兩個字串，再分別轉 int 相乘：6 × 7 = 42。",
    q="使用者輸入 6,7 時，輸出為何？", stdin="6,7\n")

out(U, i(), F, """
print("A", "B", "C", sep="-", end="!")
print("D")
""", ["A B C!\nD", "A-B-C!\nD", "ABC-!D"],
    "sep 設定各項之間的分隔字（預設空白）；end 設定結尾（預設 \\n）。end=\"!\" 不換行，所以 D 接在同一行。")

out(U, i(), F, """
price = 1234.5678
print(f"{price:.2f}|{price:,.1f}|{price:10.1f}|")
""", ["1234.56|1,234.5|1234.5|", "1234.57|1234.6|    1234.6|", "1234.5678|1,234|1234.6|"],
    ".2f 四捨五入到小數 2 位；, 加千分位；10.1f 總寬 10 字元、靠右，不足補空白。")

out(U, i(), F, """
name, qty = "筆", 3
print("{}共{}支".format(name, qty), "{1}-{0}".format("a", "b"))
""", ["筆共3支 a-b", "{}共{}支 b-a", "筆共 3 支 b-a"],
    "format 依序填入 {}；{1}{0} 用位置編號指定，所以是 b-a。")

out(U, i(), F, """
n = 7
print(f"[{n:03d}] [{n:<4}] [{n:>4}] [{n:^5}]")
""", ["[7] [7   ] [   7] [  7  ]", "[007] [   7] [7   ] [  7  ]", "[700] [7] [7] [7]"],
    "03d 寬 3 不足補 0；< 靠左、> 靠右、^ 置中。")

out(U, i(), F, """
rate = 0.256
print(f"{rate:.1%}", "%.2f" % 3.14159, "%d 個" % 5)
""", ["0.256% 3.14 5 個", "25.6% 3.14159 5 個", "26% 3.1 5.0 個"],
    "f-string 的 % 格式會乘以 100 並加上 %：25.6%。舊式 % 格式化：%.2f 取兩位小數，%d 為整數。")

out(U, i(), F, """
print(len("A\\tB"), len(r"A\\tB"), "C:\\\\data")
""", ["4 4 C:\\\\data", "3 3 C:\\data", "4 3 C:\\data"],
    "一般字串中 \\t 是一個 Tab 字元，所以長度 3；字串前加 r 是原始字串，反斜線不跳脫，長度 4。一般字串要表示一個反斜線得寫成 \\\\。")

out(U, i(), G, """
import sys
print(len(sys.argv), sys.argv[1])
""", ["2 data.csv", "3 main.py", "2 main.py"],
    "sys.argv[0] 是程式名稱本身，後面才是參數。python main.py data.csv 5 得到 ['main.py', 'data.csv', '5']，長度 3。",
    q="以 python main.py data.csv 5 執行下列程式，輸出為何？", argv=["main.py", "data.csv", "5"])

out(U, i(), G, """
import sys
total = 0
for a in sys.argv[1:]:
    total += int(a)
print(total)
""", ["拋出 TypeError", "102030", "3"],
    "sys.argv 裡的每個元素都是字串，必須用 int() 轉換。sys.argv[1:] 跳過程式名稱：10 + 20 + 30 = 60。",
    q="以 python sum.py 10 20 30 執行下列程式，輸出為何？", argv=["sum.py", "10", "20", "30"])

mc(U, i(), G, "要使用命令列參數，程式必須先怎麼做？",
   "import sys，再從 sys.argv 讀取", ["import os，再從 os.argv 讀取", "呼叫 input() 讀取", "宣告 def main(argv)"],
   "命令列參數放在 sys 模組的 argv 串列中。")
