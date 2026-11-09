from qlib import mc, tf, out, raises

U = "flow"
S = ["if / elif / else", "巢狀與複合條件", "while 迴圈", "for 迴圈與 range", "break、continue、pass", "巢狀迴圈與迴圈 else"]
A, B, C, D, E, F = S
n = iter(range(1, 999))
i = lambda: f"py2-{next(n):03d}"

out(U, i(), A, """
score = 85
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("D")
""", ["A", "B\nC", "D"],
    "elif 由上往下檢查，第一個成立（score >= 80）就執行並跳出整個 if 結構，後面的 elif 不會再檢查。")

out(U, i(), A, """
score = 85
if score >= 70:
    print("C")
if score >= 80:
    print("B")
if score >= 90:
    print("A")
""", ["C", "B", "C\nB\nA"],
    "三個獨立的 if 會各自判斷，條件成立的都會執行，所以印出 C 和 B。要「只取一個等第」必須用 if / elif。")

mc(U, i(), A, "依年齡判斷票價：未滿 12 歲 100 元、12 到 64 歲 250 元、65 歲以上 150 元。下列程式碼的空格依序應填入？",
   "if、elif、else", ["if、if、else", "elif、if、else", "if、else、elif"],
   "第一個條件用 if，中間的條件用 elif，最後「其他情況」用 else，而且 else 不能寫條件。",
   code="""
___ age < 12:
    price = 100
___ age < 65:
    price = 250
___:
    price = 150
""")

raises(U, i(), A, """
x = 3
if x > 0:
print("正數")
""", ["正數", "（沒有輸出）", "拋出 NameError"],
    "if 下面的程式區塊必須縮排。沒有縮排會拋出 IndentationError（屬於 SyntaxError 的一種），程式根本無法執行。")

out(U, i(), A, """
x = 0
if x:
    print("有值")
else:
    print("沒有值")
""", ["有值", "（沒有輸出）", "False"],
    "if 會把條件轉成 bool：0、空字串、空串列、None 都視為 False。")

out(U, i(), B, """
age, member = 20, False
if age >= 18 and member:
    print("會員價")
elif age >= 18 or member:
    print("一般價")
else:
    print("兒童價")
""", ["會員價", "兒童價", "會員價\n一般價"],
    "age >= 18 為 True、member 為 False：and 需要兩者都真，不成立；or 只要一個真就成立，所以印出「一般價」。")

out(U, i(), B, """
x = 7
if x > 5:
    if x % 2 == 0:
        print("大偶數")
    else:
        print("大奇數")
else:
    print("小")
""", ["大偶數", "小", "大奇數\n小"],
    "x > 5 成立進入外層，7 % 2 為 1 不等於 0，所以執行內層的 else。")

mc(U, i(), B, "要判斷 year 是不是閏年（能被 4 整除但不能被 100 整除，或能被 400 整除），哪一個條件正確？",
   "(year % 4 == 0 and year % 100 != 0) or year % 400 == 0",
   ["year % 4 == 0 or year % 100 != 0 and year % 400 == 0",
    "year % 4 == 0 and (year % 100 != 0 or year % 400 != 0)",
    "year % 400 == 0 and year % 4 == 0 or year % 100 == 0"],
   "照題意直接翻譯：前半段「能被 4 整除且不能被 100 整除」用 and，再跟「能被 400 整除」用 or 連接。例如 1900 不是閏年、2000 是閏年。")

out(U, i(), B, """
temp = 28
rain = True
msg = "出門" if temp < 30 and not rain else "在家"
print(msg)
""", ["出門", "True", "拋出 SyntaxError"],
    "條件運算式 A if 條件 else B。not rain 為 False，所以整個條件不成立，取 else 後的 \"在家\"。")

out(U, i(), B, """
n = 15
if n % 3 == 0 and n % 5 == 0:
    print("FizzBuzz")
elif n % 3 == 0:
    print("Fizz")
elif n % 5 == 0:
    print("Buzz")
""", ["Fizz", "Buzz", "Fizz\nBuzz"],
    "15 同時是 3 和 5 的倍數，第一個條件就成立。如果把「同時整除」放在後面，會先被 n % 3 == 0 攔下，永遠印不出 FizzBuzz。")

out(U, i(), C, """
n = 1
while n < 20:
    n *= 3
print(n)
""", ["9", "20", "18"],
    "1 → 3 → 9 → 27，n 等於 27 時 27 < 20 不成立，離開迴圈後印出 27。")

out(U, i(), C, """
count = 0
n = 10
while n > 0:
    n -= 3
    count += 1
print(count, n)
""", ["3 1", "4 -1", "3 -2"],
    "n 的變化：10 → 7 → 4 → 1 → -2，共執行 4 次，最後 n = -2。")

mc(U, i(), C, "下列程式碼會發生什麼問題？",
   "無窮迴圈，因為 i 永遠不會改變", ["印出 0 到 4", "拋出 SyntaxError", "只印出 0"],
   "迴圈內沒有改變 i，條件 i < 5 永遠成立。while 迴圈一定要讓條件有機會變成 False（例如加上 i += 1）。",
   code="""
i = 0
while i < 5:
    print(i)
""")

out(U, i(), C, """
total = 0
nums = [4, 8, 15, 16, 23, 42]
i = 0
while i < len(nums) and total < 20:
    total += nums[i]
    i += 1
print(i, total)
""", ["2 12", "4 43", "6 108"],
    "複合條件：每次都要 i 還在範圍內且 total < 20。4 + 8 = 12、再加 15 = 27，此時 total 不再小於 20，停止，i = 3。")

out(U, i(), D, """
for i in range(2, 10, 3):
    print(i, end=" ")
""", ["2 5 8 11", "2 3 4 5 6 7 8 9", "3 6 9"],
    "range(start, stop, step)：從 2 開始每次加 3，不含 10，得 2、5、8。")

out(U, i(), D, """
print(list(range(5, 0, -2)))
""", ["[5, 4, 3, 2, 1]", "[5, 3, 1, -1]", "[]"],
    "step 為負數時由大往小數，不含 stop（0），得 [5, 3, 1]。")

out(U, i(), D, """
print(list(range(3)), list(range(3, 3)))
""", ["[1, 2, 3] []", "[0, 1, 2, 3] [3]", "[0, 1, 2] [3]"],
    "range(3) 是 0、1、2（不含 3）；range(3, 3) 起點等於終點，是空的。")

out(U, i(), D, """
total = 0
for n in range(1, 11):
    if n % 2 == 0:
        total += n
print(total)
""", ["55", "25", "20"],
    "1 到 10 的偶數 2 + 4 + 6 + 8 + 10 = 30。")

out(U, i(), D, """
word = "banana"
count = 0
for ch in word:
    if ch == "a":
        count += 1
print(count, word.count("a"))
""", ["2 3", "3 2", "6 3"],
    "for 可以直接走訪字串的每個字元。\"banana\" 有 3 個 a，str.count 也能得到一樣的結果。")

out(U, i(), D, """
fruits = ["蘋果", "香蕉", "芒果"]
for idx, f in enumerate(fruits, start=1):
    print(idx, f, end="；")
""", ["0 蘋果；1 香蕉；2 芒果；", "蘋果 1；香蕉 2；芒果 3；", "1；2；3；"],
    "enumerate 同時取得索引與元素；start=1 讓編號從 1 開始。")

mc(U, i(), D, "要印出 10、8、6、4、2，range 應如何填寫？",
   "range(10, 0, -2)", ["range(10, 2, -2)", "range(2, 10, 2)", "range(10, 1, 2)"],
   "從 10 開始每次減 2，終點必須「超過」2 一格：0 或 1 都可以，range(10, 2, -2) 只會到 4。",
   code="""
for i in ______:
    print(i)
""")

out(U, i(), E, """
for i in range(1, 10):
    if i % 4 == 0:
        break
    print(i, end=" ")
""", ["1 2 3 4", "1 2 3 5 6 7 9", "4 8"],
    "break 直接結束整個迴圈。i = 4 時跳出，所以只印出 1 2 3。")

out(U, i(), E, """
for i in range(1, 10):
    if i % 4 == 0:
        continue
    print(i, end=" ")
""", ["1 2 3", "4 8", "1 2 3 4 5 6 7 8 9"],
    "continue 跳過這一輪剩下的程式，直接進入下一輪。4 和 8 被跳過。")

out(U, i(), E, """
for i in range(3):
    pass
print(i)
""", ["（沒有輸出）", "3", "拋出 NameError"],
    "pass 什麼都不做，只是佔位。迴圈結束後 i 仍保留最後一次的值 2。")

mc(U, i(), E, "關於 pass、continue、break 的敘述，何者正確？",
   "pass 不做任何事，常用來保留之後要寫的程式區塊",
   ["pass 會跳過這一輪迴圈", "continue 會結束整個迴圈", "break 只能用在 while 迴圈"],
   "continue 是跳到下一輪；break 結束整個迴圈，for 和 while 都能用；pass 只是語法上的佔位。")

out(U, i(), E, """
n = 0
while True:
    n += 1
    if n == 2:
        continue
    if n > 4:
        break
    print(n, end=" ")
""", ["1 2 3 4", "1 3 4 5", "1"],
    "while True 搭配 break 是常見寫法。n = 2 時 continue 跳過列印；n = 5 時 break 離開。")

out(U, i(), F, """
for i in range(1, 4):
    for j in range(1, i + 1):
        print("*", end="")
    print()
""", ["***\n***\n***", "*\n*\n*", "***\n**\n*"],
    "外層跑 3 次；內層次數等於 i，所以每列的星號是 1、2、3 個。內層結束後 print() 換行。")

out(U, i(), F, """
count = 0
for i in range(3):
    for j in range(4):
        count += 1
print(count)
""", ["7", "3", "4"],
    "巢狀迴圈的總次數是外層次數 × 內層次數：3 × 4 = 12。")

out(U, i(), F, """
for i in range(3):
    for j in range(3):
        if j == 1:
            break
        print(i, j)
""", ["0 0", "0 0\n0 1\n1 0\n1 1\n2 0\n2 1", "0 0\n0 2\n1 0\n1 2\n2 0\n2 2"],
    "break 只會跳出它所在的那一層（內層），外層仍繼續執行。所以每個 i 都只印出 j = 0。")

out(U, i(), F, """
for n in [3, 5, 7]:
    if n % 2 == 0:
        print("找到偶數")
        break
else:
    print("沒有偶數")
""", ["找到偶數", "（沒有輸出）", "沒有偶數\n沒有偶數\n沒有偶數"],
    "for 後面的 else 在迴圈「正常結束」（沒有被 break 打斷）時執行一次。串列裡沒有偶數，所以印出「沒有偶數」。")

out(U, i(), F, """
for i in range(2, 4):
    for j in range(1, 3):
        print(i * j, end=" ")
""", ["2 3 4 6 8", "2 3 4 6", "1 2 2 4"],
    "i = 2 時印 2、4；i = 3 時印 3、6。")
