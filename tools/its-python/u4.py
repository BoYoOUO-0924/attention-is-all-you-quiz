from qlib import mc, tf, out, raises

U = "docs"
S = ["註解與 docstring", "縮排與程式結構", "函式定義與呼叫", "參數與預設值", "回傳值", "變數範圍"]
A, B, C, D, E, F = S
n = iter(range(1, 999))
i = lambda: f"py4-{next(n):03d}"

mc(U, i(), A, "在 Python 中，單行註解使用哪個符號開頭？",
   "#", ["//", "--", "/*"],
   "# 之後到行尾都是註解，直譯器會忽略。// 是 Python 的整數除法運算子。")

mc(U, i(), A, "函式的 docstring 應該寫在哪裡？",
   "def 那一行的下一行，作為函式本體的第一個敘述",
   ["def 那一行的上一行", "函式的最後一行", "任何位置都可以，只要用三引號"],
   "docstring 必須是模組、類別或函式本體的第一個字串，才會被存進 __doc__，help() 與 pydoc 才讀得到。")

out(U, i(), A, '''
def area(r):
    """計算圓面積。"""
    return 3.14 * r * r

print(area.__doc__)
''', ["None", "area", "3.14 * r * r"],
    "寫在函式第一行的字串會成為 __doc__ 屬性，可以用 help(area) 或 area.__doc__ 查看。")

out(U, i(), A, '''
def f():
    # 這是一般註解
    return 1

print(f.__doc__)
''', ["# 這是一般註解", "這是一般註解", "1"],
    "# 開頭的是一般註解，不會成為 docstring，所以 __doc__ 是 None。")

mc(U, i(), A, "要從命令列查看某個模組（例如 math）的說明文件，可以使用哪個指令？",
   "python -m pydoc math", ["python -m doc math", "python --help math", "pip show math"],
   "pydoc 會讀取模組、類別、函式的 docstring 產生說明文件；python -m pydoc -w 模組名 還能輸出成 HTML。")

tf(U, i(), A, "以三引號包住、但沒有指派給變數的多行字串，常被拿來當作多行註解使用。", True,
   "Python 沒有專門的多行註解語法。沒有指派的字串只是被計算後丟棄；放在函式第一行則成為 docstring。")

raises(U, i(), B, """
def greet():
    print("Hi")
      print("Bye")
greet()
""", ["Hi\nBye", "Hi", "拋出 NameError"],
    "同一個程式區塊內的縮排必須一致。第三行多縮了兩格，會拋出 IndentationError。")

mc(U, i(), B, "PEP 8 建議一層縮排使用幾個空白？",
   "4 個空白", ["2 個空白", "1 個 Tab 加 2 個空白", "8 個空白"],
   "PEP 8 建議每層縮排 4 個空白，且不要混用 Tab 與空白。")

out(U, i(), B, """
x = 5
if x > 3:
    print("A")
print("B")
if x > 10:
    print("C")
print("D")
""", ["A\nB\nC\nD", "A", "B\nD"],
    "沒有縮排的 print 不屬於 if 區塊，無論條件如何都會執行。x > 10 不成立，所以只略過 C。")

raises(U, i(), B, """
def todo():

print("完成")
""", ["完成", "（沒有輸出）", "拋出 NameError"],
    "函式本體不能是空的，會拋出 IndentationError（expected an indented block）。還沒寫好的函式可以先放 pass。")

mc(U, i(), B, "關於 if __name__ == \"__main__\": 的用途，何者正確？",
   "檔案被直接執行時才會執行該區塊，被 import 時不會執行",
   ["讓檔案只能被 import", "宣告主程式的進入點，沒有它程式無法執行", "讓函式可以被其他檔案呼叫"],
   "直接執行時 __name__ 是 \"__main__\"；被 import 時 __name__ 是模組名稱。常用來放測試或主程式。")

out(U, i(), C, """
def show():
    print("in show")

print("start")
show()
show
print("end")
""", ["start\nin show\nin show\nend", "in show\nstart\nend", "start\nend"],
    "def 只是定義函式，不會執行。加上括號 show() 才是呼叫；只寫 show 不會執行函式。")

raises(U, i(), C, """
say_hi()

def say_hi():
    print("Hi")
""", ["Hi", "（沒有輸出）", "拋出 SyntaxError"],
    "Python 由上往下執行，呼叫時 say_hi 還沒被定義，會拋出 NameError。函式必須先定義再呼叫。")

mc(U, i(), C, "下列哪一個函式定義的語法正確？",
   "def add(a, b):", ["def add(a, b)", "function add(a, b):", "def add[a, b]:"],
   "def 函式名稱(參數): 最後一定要有冒號，下一行開始縮排撰寫本體。")

out(U, i(), C, """
def square(n):
    return n * n

print(square(square(2)))
""", ["4", "8", "256"],
    "先算內層 square(2) = 4，再算 square(4) = 16。")

out(U, i(), D, """
def power(base, exp=2):
    return base ** exp

print(power(3), power(3, 3), power(exp=0, base=9))
""", ["9 9 9", "6 9 0", "3 27 1"],
    "exp 沒給就用預設值 2；用關鍵字引數時順序可以調換。9 ** 0 = 1。")

raises(U, i(), D, """
def f(a=1, b):
    return a + b
""", ["定義成功", "回傳 None", "拋出 TypeError"],
    "有預設值的參數必須放在沒有預設值的參數後面，否則是 SyntaxError。")

raises(U, i(), D, """
def info(name, age):
    print(name, age)

info("Amy")
""", ["Amy None", "Amy", "Amy 0"],
    "呼叫時少給了必要參數 age，會拋出 TypeError（missing 1 required positional argument）。")

out(U, i(), D, """
def add_item(item, box=[]):
    box.append(item)
    return box

add_item("a")
print(add_item("b"))
""", ["['b']", "['a']", "拋出 TypeError"],
    "預設值只在定義函式時建立一次。可變的預設值（串列）會在多次呼叫之間共用。正確寫法是 box=None，再在函式內 if box is None: box = []。")

out(U, i(), D, """
def total(*nums):
    return sum(nums)

print(total(), total(1, 2, 3))
""", ["拋出 TypeError", "None 6", "0 [1, 2, 3]"],
    "*nums 把多個位置引數收集成 tuple，沒有傳也可以（空 tuple）。sum(()) 為 0。")

out(U, i(), D, """
def show(a, b=2, c=3):
    print(a, b, c)

show(1, c=5)
""", ["1 5 3", "1 2 3", "拋出 TypeError"],
    "b 沒給用預設值 2；c 用關鍵字引數指定為 5。")

out(U, i(), E, """
def f(x):
    if x > 0:
        return "正"
    print("非正")

print(f(5))
print(f(-1))
""", ["正\n非正", "正\n非正\n非正", "正\n拋出錯誤"],
    "return 會立刻結束函式。f(-1) 沒有執行到 return，印出「非正」後回傳 None。")

out(U, i(), E, """
def stats(nums):
    return min(nums), max(nums)

lo, hi = stats([4, 9, 1])
print(lo, hi, type(stats([1])).__name__)
""", ["4 9 list", "1 9 list", "9 1 tuple"],
    "return a, b 會回傳一個 tuple，可以用多個變數拆開接收。")

out(U, i(), E, """
def f():
    return 1
    return 2

print(f())
""", ["2", "1 2", "拋出 SyntaxError"],
    "第一個 return 執行後函式就結束了，之後的程式碼永遠不會執行。")

out(U, i(), E, """
result = print("Hi")
print(result)
""", ["Hi\nHi", "Hi", "（沒有輸出）"],
    "print() 本身沒有 return 值，所以回傳 None。沒有 return 的函式都回傳 None。")

out(U, i(), F, """
x = 10
def change():
    x = 20
    print(x, end=" ")

change()
print(x)
""", ["20 20", "10 10", "拋出 UnboundLocalError"],
    "函式內指派 x 會建立一個新的區域變數，不影響外面的全域變數 x。")

out(U, i(), F, """
x = 10
def change():
    global x
    x = 20

change()
print(x)
""", ["10", "拋出 NameError", "None"],
    "宣告 global x 之後，函式內的 x 就是全域變數，修改會反映到外面。")

raises(U, i(), F, """
count = 0
def inc():
    count += 1

inc()
print(count)
""", ["1", "0", "拋出 NameError"],
    "函式內對 count 指派，Python 就把它當成區域變數；但 += 需要先讀取它的值，而區域的 count 還沒有值，所以拋出 UnboundLocalError。加上 global count 才能修改全域變數。")

raises(U, i(), F, """
def f():
    secret = 42

f()
print(secret)
""", ["42", "None", "拋出 UnboundLocalError"],
    "secret 是 f 的區域變數，函式結束就消失，在外面使用會拋出 NameError。")

out(U, i(), F, """
x = 5
def show():
    print(x)

x = 7
show()
""", ["5", "拋出 NameError", "None"],
    "函式內只讀取、沒有指派 x，就會使用全域變數。呼叫時 x 已經改成 7。")
