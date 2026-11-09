from qlib import mc, tf, out, raises, check

U = "types"
S = ["資料型別判斷", "型別轉換", "字串索引與切片", "串列操作", "算術與指派運算子", "比較、邏輯、身分與成員運算子", "運算子優先順序"]
A, B, C, D, E, F, G = S
n = iter(range(1, 999))
i = lambda: f"py1-{next(n):03d}"

out(U, i(), A, """
print(type(7 / 2))
""", ["<class 'int'>", "<class 'str'>", "<class 'bool'>"],
    "在 Python 3，/ 一定回傳 float，即使能整除（例如 4 / 2 得 2.0）。")

out(U, i(), A, """
print(type(7 // 2), type(7.0 // 2))
""", ["<class 'float'> <class 'float'>", "<class 'int'> <class 'int'>", "<class 'float'> <class 'int'>"],
    "// 是整數除法（向下取整）。兩邊都是 int 結果是 int；只要有一邊是 float，結果就是 float（3.0）。")

mc(U, i(), A, "下列哪一個運算式的結果型別是 bool？",
   "5 > 3", ["\"True\"", "1 + 0", "len(\"False\")"],
   "比較運算的結果是 True/False，型別是 bool。\"True\" 加了引號是 str，len() 回傳 int。")

mc(U, i(), A, "變數 x = \"3.14\" 的資料型別是？",
   "str", ["float", "int", "decimal"],
   "有引號就是字串（str），即使內容看起來像數字。要計算得先用 float(x) 轉型。")

out(U, i(), A, """
data = [10, "10", 10.0, True]
for d in data:
    print(type(d).__name__, end=" ")
""", ["int int float bool", "int str float int", "int str int bool"],
    "type(x).__name__ 取得型別名稱。\"10\" 是 str、10.0 是 float、True 是 bool（bool 雖然是 int 的子類別，type() 仍回傳 bool）。")

out(U, i(), B, """
print(int("25") + int(3.99))
""", ["28.99", "29", "253"],
    "int(\"25\") 得 25；int(3.99) 直接截去小數部分得 3（不會四捨五入），所以 25 + 3 = 28。")

raises(U, i(), B, """
print(int("3.5"))
""", ["3", "4", "3.5"],
    "int() 只能轉換整數格式的字串。\"3.5\" 要先 float(\"3.5\") 再 int(...)，否則拋出 ValueError。")

out(U, i(), B, """
a = "5"
b = 3
print(a * b, int(a) * b)
""", ["15 15", "15 555", "拋出錯誤"],
    "字串 * 整數是「重複」：\"5\" * 3 得 \"555\"；轉成 int 後才是乘法 15。")

raises(U, i(), B, """
age = 20
print("年齡：" + age)
""", ["年齡：20", "年齡： 20", "年齡：age"],
    "str 不能直接用 + 接 int，會拋出 TypeError。應寫 \"年齡：\" + str(age)，或用 f\"年齡：{age}\"。")

out(U, i(), B, """
print(bool(""), bool(" "), bool(0), bool([0]))
""", ["False False False False", "False True False False", "True True False True"],
    "空字串、0、空容器為 False；\" \"（含一個空白）與 [0]（含一個元素的串列）都不是空的，所以是 True。")

out(U, i(), B, """
print(float("7"), str(7.0), round(2.675, 2))
""", ["7 7.0 2.68", "7.0 7 2.68", "7.0 7.0 2.68"],
    "float(\"7\") 得 7.0；str(7.0) 得 \"7.0\"。round(2.675, 2) 因浮點數無法精確表示 2.675（實際略小於它），結果是 2.67。")

out(U, i(), C, """
s = "Python"
print(s[0], s[-1], s[2:4])
""", ["P o th", "P n tho", "y n th"],
    "索引從 0 開始，-1 是最後一個字元。切片 [2:4] 取索引 2、3（不含 4），得 \"th\"。")

out(U, i(), C, """
s = "ITSPython"
print(s[::-1])
""", ["ITSPython", "nohtyPSIT", "nohtyP"],
    "步長 -1 代表從尾到頭取，[::-1] 是反轉字串的慣用寫法。")

out(U, i(), C, """
s = "0123456789"
print(s[1:8:3])
""", ["14", "1357", "258"],
    "從索引 1 開始，每次跳 3，到 8 之前停：1、4、7。")

raises(U, i(), C, """
s = "hello"
s[0] = "H"
print(s)
""", ["Hello", "hello", "Hhello"],
    "字串是不可變（immutable）的，不能用索引修改字元，會拋出 TypeError。要改寫成 s = \"H\" + s[1:]。")

out(U, i(), C, """
s = "abc"
print(repr(s[5:]), s[-10:2])
""", ["拋出 IndexError", "'c' ab", "'' abc"],
    "切片超出範圍不會出錯，只會截到有效範圍：s[5:] 是空字串，s[-10:2] 等同 s[0:2] 得 \"ab\"。只有單一索引（例如 s[5]）超出範圍才會拋出 IndexError。")

out(U, i(), D, """
nums = [3, 1, 2]
nums.append([4, 5])
print(len(nums))
""", ["5", "3", "6"],
    "append 把整個參數當成一個元素加到尾端，所以加入的是一個串列 [4, 5]，長度變 4。要逐一加入請用 extend。")

out(U, i(), D, """
nums = [3, 1, 2]
nums.extend([4, 5])
nums.insert(0, 9)
print(nums)
""", ["[9, 3, 1, 2, [4, 5]]", "[3, 1, 2, 4, 5, 9]", "[3, 9, 1, 2, 4, 5]"],
    "extend 逐一加入元素；insert(0, 9) 把 9 插在索引 0 的位置。")

out(U, i(), D, """
a = [5, 2, 8]
b = sorted(a)
a.sort(reverse=True)
print(a, b)
""", ["[2, 5, 8] [2, 5, 8]", "[8, 5, 2] [8, 5, 2]", "[5, 2, 8] [2, 5, 8]"],
    "sorted() 回傳新串列、不動原串列；list.sort() 就地排序並回傳 None。reverse=True 由大到小。")

out(U, i(), D, """
a = [1, 2, 3]
b = a
b.append(4)
print(a)
""", ["[1, 2, 3]", "[4]", "[1, 2, 3, 4, 4]"],
    "b = a 不會複製串列，a 和 b 指向同一個物件，透過 b 修改 a 也會看到。要複製請用 a.copy() 或 a[:]。")

out(U, i(), D, """
items = ["a", "b", "c", "b"]
items.remove("b")
print(items, items.index("b"))
""", ["['a', 'c'] 拋出錯誤", "['a', 'c', 'b'] 1", "['a', 'b', 'c'] 1"],
    "remove 只刪除第一個符合的元素，剩下 ['a', 'c', 'b']；index(\"b\") 回傳第一次出現的位置 2。")

out(U, i(), D, """
nums = [10, 20, 30, 40]
x = nums.pop()
y = nums.pop(0)
print(x, y, nums)
""", ["10 40 [20, 30]", "40 20 [10, 30]", "40 10 [20, 30, 40]"],
    "pop() 不給參數移除並回傳最後一個；pop(0) 移除並回傳索引 0 的元素。")

out(U, i(), D, """
grid = [[1, 2, 3], [4, 5, 6]]
print(grid[1][0] + grid[0][-1])
""", ["5", "6", "9"],
    "grid[1][0] 是第二列第一個 4；grid[0][-1] 是第一列最後一個 3，相加得 7。")

out(U, i(), D, """
print([0] * 3 + [1, 2][::-1])
""", ["[0, 0, 0, 1, 2]", "[0, 3, 2, 1]", "[[0, 0, 0], [2, 1]]"],
    "[0] * 3 得 [0, 0, 0]；[1, 2][::-1] 反轉得 [2, 1]；+ 串接兩個串列。")

out(U, i(), E, """
print(17 % 5, -17 % 5, 17 // -5)
""", ["2 -2 -3", "2 -2 -4", "2 3 -3"],
    "Python 的 // 向負無限大取整：17 // -5 = -4。% 的結果正負號跟除數相同：-17 % 5 = 3（因為 -17 = 5 × -4 + 3）。")

out(U, i(), E, """
print(2 ** 3 ** 2)
""", ["64", "36", "18"],
    "** 是右結合：2 ** 3 ** 2 等於 2 ** (3 ** 2) = 2 ** 9 = 512。")

out(U, i(), E, """
x = 10
x += 5
x //= 4
x **= 2
print(x)
""", ["14.0625", "16", "12"],
    "10 + 5 = 15；15 // 4 = 3；3 ** 2 = 9。")

out(U, i(), E, """
a, b = 3, 7
a, b = b, a + b
print(a, b)
""", ["7 14", "3 10", "10 7"],
    "右邊先整組算完（7, 3 + 7）再一次指派，所以 a = 7、b = 10。這也是交換變數 a, b = b, a 的原理。")

out(U, i(), E, """
print(abs(-7.5), divmod(17, 5), pow(2, 10, 1000))
""", ["7.5 3 2 24", "-7.5 (3, 2) 1024", "7.5 (2, 3) 24"],
    "abs 取絕對值；divmod(a, b) 回傳 (a // b, a % b)；pow(2, 10, 1000) 是 2**10 % 1000 = 24。")

out(U, i(), F, """
a = [1, 2]
b = [1, 2]
c = a
print(a == b, a is b, a is c)
""", ["True True True", "False False True", "True False False"],
    "== 比較內容；is 比較是否為同一個物件。a、b 內容相同但是不同物件；c = a 指向同一個物件。")

out(U, i(), F, """
print("py" in "Python", "Py" in "Python", 3 not in [1, 2, 3])
""", ["True True True", "True True False", "False False False"],
    "in 區分大小寫：\"py\" 不在 \"Python\" 中，\"Py\" 在。3 在串列中，所以 not in 為 False。")

out(U, i(), F, """
x = 15
print(10 < x <= 15, x > 5 and x % 2 == 0, not x == 15 or x < 20)
""", ["True True True", "False False True", "True False False"],
    "10 < x <= 15 是串接比較，等於 10 < x and x <= 15，為 True。15 是奇數，所以第二個為 False。not 優先於 or：(not True) or True = True。")

out(U, i(), F, """
print(0 or "預設", repr("" and "A"), 3 and 5)
""", ["True False True", "預設 'A' 5", "0 'A' 3"],
    "or 回傳第一個為真的值（都假則回傳最後一個）；and 回傳第一個為假的值（都真則回傳最後一個）。\"\" 為假所以回傳 \"\"，3 and 5 回傳 5。")

out(U, i(), F, """
print("apple" < "banana", "Zoo" < "apple", "10" < "9")
""", ["True False True", "True False False", "False True True"],
    "字串依字元的 Unicode 碼逐字比較。大寫字母（Z=90）小於小寫字母（a=97）；\"10\" 與 \"9\" 比的是第一個字元 \"1\" < \"9\"，所以為 True。")

tf(U, i(), F, "None 應該用 is 比較，例如 if result is None:。", True,
   "None 是單例物件，PEP 8 建議用 is / is not 判斷。")

out(U, i(), G, """
print(2 + 3 * 4 ** 2 // 8)
""", ["10", "14", "62"],
    "優先順序：** 最高，再來 * // 由左到右，最後 +。4 ** 2 = 16；3 * 16 = 48；48 // 8 = 6；2 + 6 = 8。")

out(U, i(), G, """
print(not 3 > 2 and 1 == 1)
""", ["True", "拋出錯誤", "1"],
    "比較運算優先於 not，not 又優先於 and：(not (3 > 2)) and (1 == 1) = False and True = False。")

out(U, i(), G, """
print(-3 ** 2, (-3) ** 2)
""", ["9 9", "-9 -9", "9 -9"],
    "** 的優先順序高於單元負號，所以 -3 ** 2 等於 -(3 ** 2) = -9。要平方負數得加括號。")

mc(U, i(), G, "下列運算子的優先順序，由高到低排列何者正確？",
   "** → * / // % → + - → 比較運算 → not → and → or",
   ["* / → ** → + - → and → or → not",
    "比較運算 → ** → + - → or → and",
    "not → and → or → ** → * /"],
   "記憶口訣：次方 > 乘除 > 加減 > 比較 > not > and > or。不確定時就加括號。")

out(U, i(), G, """
x = 5
print(x > 3 or 1 / 0)
""", ["拋出 ZeroDivisionError", "False", "5"],
    "or 會短路求值：左邊已經是 True，右邊的 1 / 0 根本不會執行，所以不會出錯。")
