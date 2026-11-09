from qlib import mc, tf, out, raises, check

U = "errors"
S = ["語法、執行期與邏輯錯誤", "常見例外類型", "try / except", "else 與 finally", "raise 主動拋出例外", "unittest 單元測試"]
A, B, C, D, E, F = S
n = iter(range(1, 999))
i = lambda: f"py5-{next(n):03d}"

mc(U, i(), A, "程式可以執行、沒有出現錯誤訊息，但計算結果不正確，這屬於哪一種錯誤？",
   "邏輯錯誤（logic error）", ["語法錯誤（syntax error）", "執行期錯誤（runtime error）", "縮排錯誤（indentation error）"],
   "邏輯錯誤不會讓程式停止，只會得到錯誤的結果，最難發現，通常要靠測試或除錯找出。")

mc(U, i(), A, "下列程式碼想計算平均，但結果錯誤。錯誤的原因是？",
   "運算子優先順序：只有 c 被除以 3，應寫成 (a + b + c) / 3",
   ["/ 會做整數除法", "變數名稱不能是單一字母", "缺少 return 時 avg 不會被指派"],
   "除法優先於加法，a + b + c / 3 等於 a + b + (c / 3)。這是典型的邏輯錯誤。",
   code="""
a, b, c = 80, 90, 70
avg = a + b + c / 3
print(avg)
""")

raises(U, i(), A, """
if True
    print("ok")
""", ["ok", "（沒有輸出）", "拋出 NameError"],
    "if 敘述最後少了冒號，屬於語法錯誤，程式在執行前就會被拒絕，拋出 SyntaxError。")

mc(U, i(), A, "下列程式要印出 1 到 5 的總和，但結果是 10。應如何修正？",
   "把 range(1, 5) 改成 range(1, 6)",
   ["把 total = 0 改成 total = 1", "把 += 改成 =+", "把 print 移進迴圈內"],
   "range 不含終點，range(1, 5) 只有 1 到 4。這種「差一」（off-by-one）是很常見的邏輯錯誤。",
   code="""
total = 0
for i in range(1, 5):
    total += i
print(total)
""")

tf(U, i(), A, "語法錯誤（SyntaxError）可以用 try / except 包住同一段程式碼來攔截。", False,
   "語法錯誤在程式開始執行前、解析階段就發生了，try 根本還沒執行，所以攔不到。")

raises(U, i(), B, """
nums = [1, 2, 3]
print(nums[3])
""", ["3", "None", "拋出 KeyError"],
    "串列只有索引 0 到 2，nums[3] 超出範圍，拋出 IndexError。")

raises(U, i(), B, """
d = {"a": 1}
print(d["b"])
""", ["None", "拋出 IndexError", "拋出 NameError"],
    "字典沒有這個鍵時拋出 KeyError。不確定鍵是否存在可以用 d.get(\"b\")，找不到會回傳 None。")

raises(U, i(), B, """
print(total_score)
""", ["0", "None", "拋出 KeyError"],
    "使用尚未定義的變數會拋出 NameError，常見原因是拼錯變數名稱。")

raises(U, i(), B, """
print(len(5))
""", ["1", "5", "拋出 ValueError"],
    "int 沒有長度，傳入不支援的型別會拋出 TypeError。")

raises(U, i(), B, """
x = "abc"
x.append("d")
""", ["abcd", "拋出 TypeError", "拋出 NameError"],
    "str 物件沒有 append 方法，存取不存在的屬性或方法會拋出 AttributeError。")

mc(U, i(), B, "int(\"abc\") 和 int([1]) 分別會拋出哪種例外？",
   "ValueError、TypeError", ["TypeError、TypeError", "ValueError、ValueError", "TypeError、ValueError"],
   "型別對但值不合法（字串的內容無法轉成整數）是 ValueError；型別本身就不支援（串列不能轉 int）是 TypeError。")

out(U, i(), C, """
try:
    x = 10 / 0
    print("A")
except ZeroDivisionError:
    print("B")
print("C")
""", ["A\nC", "A\nB\nC", "B"],
    "第一行就出錯，try 區塊剩下的程式不會執行，直接跳到對應的 except。處理完後程式繼續往下執行。")

out(U, i(), C, """
try:
    n = int("x")
except ZeroDivisionError:
    print("除以零")
except ValueError:
    print("格式錯誤")
except Exception:
    print("其他")
""", ["除以零", "格式錯誤\n其他", "其他"],
    "except 由上往下比對，只會執行第一個符合的。ValueError 在 Exception 之前被攔下。")

out(U, i(), C, """
try:
    items = [1, 2]
    print(items[5])
except (IndexError, KeyError) as e:
    print("錯誤：", type(e).__name__)
""", ["錯誤： KeyError", "錯誤： (IndexError, KeyError)", "拋出 IndexError"],
    "一個 except 可以用 tuple 攔截多種例外；as e 取得例外物件。")

mc(U, i(), C, "下列 except 的排列有什麼問題？",
   "Exception 放在最前面會攔下所有例外，後面的 ValueError 永遠不會執行",
   ["沒有問題", "except 後面不能接 Exception", "一個 try 只能有一個 except"],
   "子類別例外要寫在父類別之前。Exception 幾乎是所有例外的父類別，應放在最後。",
   code="""
try:
    n = int(input())
except Exception:
    print("錯誤")
except ValueError:
    print("請輸入數字")
""")

out(U, i(), C, """
def safe_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(safe_div(6, 3), safe_div(1, 0))
""", ["2 None", "2.0 拋出 ZeroDivisionError", "2.0 0"],
    "6 / 3 = 2.0；1 / 0 被攔下回傳 None。")

out(U, i(), D, """
try:
    x = int("5")
except ValueError:
    print("錯誤")
else:
    print("成功", x)
finally:
    print("結束")
""", ["成功 5", "錯誤\n結束", "結束"],
    "沒有發生例外時執行 else；finally 不論有沒有例外都會執行。")

out(U, i(), D, """
try:
    x = int("five")
except ValueError:
    print("錯誤")
else:
    print("成功")
finally:
    print("結束")
""", ["錯誤", "成功\n結束", "錯誤\n成功\n結束"],
    "發生例外時跳過 else，執行 except，最後一定執行 finally。")

out(U, i(), D, """
def f():
    try:
        return "try"
    finally:
        print("finally")

print(f())
""", ["try", "try\nfinally", "finally"],
    "即使 try 裡面已經 return，finally 仍會在函式真正離開前執行，所以先印 finally，再印回傳值。")

mc(U, i(), D, "finally 區塊最適合用來做什麼？",
   "釋放資源，例如關閉檔案或網路連線",
   ["只在發生例外時顯示錯誤訊息", "只在沒有例外時儲存結果", "重新執行 try 區塊"],
   "finally 一定會執行，適合放清理工作。只在成功時要做的事放 else；只在失敗時要做的事放 except。")

out(U, i(), E, """
def set_age(age):
    if age < 0:
        raise ValueError("年齡不可為負數")
    return age

try:
    set_age(-3)
except ValueError as e:
    print(e)
""", ["ValueError", "-3", "拋出 ValueError"],
    "raise 主動拋出例外，並可附上說明文字。print(e) 會印出這段文字。")

raises(U, i(), E, """
def check(score):
    if not 0 <= score <= 100:
        raise ValueError("分數超出範圍")
    print("OK")

check(120)
""", ["OK", "（沒有輸出）", "拋出 TypeError"],
    "120 不在 0 到 100 之間，raise 拋出 ValueError；沒有 try 攔截，程式就停止。")

out(U, i(), E, """
try:
    try:
        1 / 0
    except ZeroDivisionError:
        print("內層")
        raise
except ZeroDivisionError:
    print("外層")
""", ["內層", "外層", "拋出 ZeroDivisionError"],
    "except 裡單獨寫 raise 會把同一個例外再往外拋，讓外層也能處理。")

mc(U, i(), E, "要定義自己的例外類別，下列寫法何者正確？",
   "class ScoreError(Exception):\n    pass",
   ["def ScoreError(Exception):\n    pass", "exception ScoreError:\n    pass", "class ScoreError(raise):\n    pass"],
   "自訂例外是繼承 Exception 的類別，之後可以 raise ScoreError(\"訊息\")。")

UT = """
import unittest

def add(a, b):
    return a + b

class TestAdd(unittest.TestCase):
    def test_int(self):
        self.assertEqual(add(2, 3), 5)

    def test_float(self):
        self.assertEqual(add(0.1, 0.2), 0.3)

    def helper(self):
        self.assertEqual(add(1, 1), 3)

if __name__ == "__main__":
    unittest.main()
"""
check(UT.replace("unittest.main()", "r = unittest.TextTestRunner(stream=open('log', 'w')).run(unittest.TestLoader().loadTestsFromTestCase(TestAdd)); print(r.testsRun, len(r.failures))"), "2 1")
mc(U, i(), F, "執行下列測試檔，結果為何？",
   "執行 2 個測試，1 個失敗",
   ["執行 3 個測試，2 個失敗", "執行 2 個測試，全部通過", "執行 3 個測試，1 個失敗"],
   "只有名稱以 test 開頭的方法才會被當成測試，helper 不會執行。0.1 + 0.2 在浮點數運算下是 0.30000000000000004，assertEqual 失敗；比較浮點數應改用 assertAlmostEqual。",
   code=UT)

mc(U, i(), F, "使用 unittest 撰寫測試時，測試類別必須繼承哪一個類別？",
   "unittest.TestCase", ["unittest.Test", "unittest.main", "object.TestCase"],
   "測試類別繼承 unittest.TestCase，裡面以 test 開頭的方法才會被當成測試案例執行。")

mc(U, i(), F, "要確認「呼叫 int(\"abc\") 會拋出 ValueError」，應使用哪一個斷言方法？",
   "self.assertRaises(ValueError, int, \"abc\")",
   ["self.assertEqual(int(\"abc\"), ValueError)", "self.assertTrue(ValueError)", "self.assertIs(int(\"abc\"), None)"],
   "assertRaises(例外類別, 函式, 引數…)，也可以用 with self.assertRaises(ValueError): 的寫法。")

mc(U, i(), F, "要檢查 result 不是 None，應使用哪一個斷言方法？",
   "assertIsNotNone(result)", ["assertNotEqual(result)", "assertNotNone(result)", "assertNone(result, False)"],
   "常用斷言：assertEqual / assertNotEqual、assertTrue / assertFalse、assertIs / assertIsNot、assertIsNone / assertIsNotNone、assertIn / assertNotIn、assertIsInstance、assertRaises。")

mc(U, i(), F, "要確認 3 在串列 nums 之中，應使用哪一個斷言？",
   "self.assertIn(3, nums)", ["self.assertIn(nums, 3)", "self.assertEqual(3, nums)", "self.assertIs(3 in nums)"],
   "assertIn(成員, 容器)，順序是先成員後容器。")

mc(U, i(), F, "每個測試方法執行前都要建立一份新的測試資料，應該寫在哪個方法？",
   "setUp(self)", ["__init__(self)", "tearDown(self)", "setUpClass(cls)"],
   "setUp 在每個測試方法之前執行；tearDown 在每個測試方法之後執行；setUpClass 整個類別只執行一次。")

tf(U, i(), F, "在測試檔最後寫 if __name__ == \"__main__\": unittest.main()，就可以用 python 測試檔.py 直接執行所有測試。", True,
   "unittest.main() 會自動找出這個模組中所有 TestCase 的 test 方法並執行。")
