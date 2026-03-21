# ============================================
#   Cream Language — Test Suite v0.1
#   Запуск: python tests/test_cream.py
# ============================================

import sys
import os

# добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cream import Lexer, Parser, Interpreter, LexerError, ParseError, CreamRuntimeError

# ══════════════════════════════════════════
#  Вспомогательные функции
# ══════════════════════════════════════════

passed = 0
failed = 0
errors = []

def run(code):
    """Запускает Cream код и возвращает список выведенных строк."""
    output = []
    original_print = __builtins__.__dict__['print'] if isinstance(__builtins__, dict) else print

    import builtins
    original = builtins.print

    def capture(*args, **kwargs):
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        output.append(sep.join(str(a) for a in args))

    builtins.print = capture
    try:
        Interpreter().run(code)
    finally:
        builtins.print = original

    return output

def test(name, code, expected):
    """Проверяет что код выводит ожидаемый результат."""
    global passed, failed
    try:
        result = run(code)
        actual = result[0] if result else ""
        if isinstance(expected, list):
            if result == expected:
                passed += 1
                print(f"  ✅ {name}")
            else:
                failed += 1
                errors.append(name)
                print(f"  ❌ {name}")
                print(f"     Expected: {expected}")
                print(f"     Got:      {result}")
        else:
            if actual == str(expected):
                passed += 1
                print(f"  ✅ {name}")
            else:
                failed += 1
                errors.append(name)
                print(f"  ❌ {name}")
                print(f"     Expected: {repr(str(expected))}")
                print(f"     Got:      {repr(actual)}")
    except Exception as e:
        failed += 1
        errors.append(name)
        print(f"  ❌ {name} — Exception: {e}")

def test_raises(name, code, error_type):
    """Проверяет что код бросает ожидаемую ошибку."""
    global passed, failed
    try:
        run(code)
        failed += 1
        errors.append(name)
        print(f"  ❌ {name} — Expected {error_type.__name__} but no error raised")
    except error_type:
        passed += 1
        print(f"  ✅ {name}")
    except Exception as e:
        failed += 1
        errors.append(name)
        print(f"  ❌ {name} — Got {type(e).__name__} instead of {error_type.__name__}: {e}")

def section(title):
    print(f"\n{'─'*45}")
    print(f"  {title}")
    print(f"{'─'*45}")


# ══════════════════════════════════════════
#  ТЕСТЫ
# ══════════════════════════════════════════

print("=" * 45)
print("  Cream Test Suite v0.1")
print("=" * 45)

# ── Переменные ────────────────────────────
section("Variables & Types")

test("number integer",   'x = 42\nsay x',           "42")
test("number float",     'x = 3.14\nsay x',          "3.14")
test("string",           'x = "hello"\nsay x',        "hello")
test("bool yes",         'x = yes\nsay x',            "yes")
test("bool no",          'x = no\nsay x',             "no")
test("empty",            'x = empty\nsay x',          "empty")
test("string interp",    'n = "World"\nsay "Hello, {n}!"', "Hello, World!")
test("reassign",         'x = 1\nx = 2\nsay x',      "2")

# ── Арифметика ────────────────────────────
section("Arithmetic")

test("addition",       'say 3 + 4',        "7")
test("subtraction",    'say 10 - 3',       "7")
test("multiplication", 'say 3 * 4',        "12")
test("division",       'say 10 / 4',       "2.5")
test("modulo",         'say 10 % 3',       "1")
test("negative",       'say 0 - 5',        "-5")
test("float add",      'say 1.5 + 1.5',    "3.0")
test("string concat",  'say "a" + "b"',    "ab")
test("precedence",     'say 2 + 3 * 4',    "14")

# ── Условия ───────────────────────────────
section("Conditions")

test("if true",  'if yes\n    say "ok"',              "ok")
test("if false", 'if no\n    say "ok"\nelse\n    say "no"', "no")
test("if eq",    'x = 5\nif x == 5\n    say "yes"',  "yes")
test("if neq",   'x = 5\nif x != 3\n    say "yes"',  "yes")
test("if gt",    'if 5 > 3\n    say "yes"',           "yes")
test("if lt",    'if 3 < 5\n    say "yes"',           "yes")
test("if gte",   'if 5 >= 5\n    say "yes"',          "yes")
test("if lte",   'if 5 <= 6\n    say "yes"',          "yes")
test("or if", '''
score = 85
if score >= 90
    say "A"
or if score >= 80
    say "B"
else
    say "C"
''', "B")

# ── Циклы ─────────────────────────────────
section("Loops")

test("repeat", 'repeat 3\n    say "x"', ["x", "x", "x"])
test("for each list", 'for each x in [1,2,3]\n    say x', ["1", "2", "3"])
test("for each range", 'for each i in range(0, 3)\n    say i', ["0", "1", "2"])
test("while", 'i = 0\nwhile i < 3\n    say i\n    i = i + 1', ["0", "1", "2"])

# ── Функции ───────────────────────────────
section("Functions")

test("basic action", '''
action add(a, b)
    return a + b
say add(3, 4)
''', "7")

test("default param", '''
action greet(name, greeting = "Hello")
    return "{greeting}, {name}!"
say greet("Alice")
''', "Hello, Alice!")

test("recursive", '''
action fib(n)
    if n <= 1
        return n
    return fib(n - 1) + fib(n - 2)
say fib(7)
''', "13")

test("lambda", '''
double = x → x * 2
say double(7)
''', "14")

# ── Структуры ─────────────────────────────
section("Structs")

test("basic struct", '''
struct Point
    x: number
    y: number
p = Point(10, 20)
say p.x
''', "10")

test("struct default", '''
struct Item
    name: text
    active: bool = yes
i = Item("test")
say i.active
''', "yes")

# ── Списки ────────────────────────────────
section("Lists")

test("list access",  'lst = [1,2,3]\nsay lst[0]',      "1")
test("list length",  'say length([1,2,3,4])',           "4")
test("list sum",     'say sum([1,2,3,4,5])',            "15")
test("list min",     'say min([3,1,4,1,5])',            "1")
test("list max",     'say max([3,1,4,1,5])',            "5")
test("list sort",    'say sort([3,1,2])',               "[1, 2, 3]")
test("list reverse", 'say reverse([1,2,3])',            "[3, 2, 1]")
test("list first",   'say first([10,20,30])',           "10")
test("list last",    'say last([10,20,30])',            "30")

# ── Pipeline ──────────────────────────────
section("Pipeline")

test("filter", '''
result = [1,2,3,4,5]
    | filter(x → x > 3)
say result
''', "[4, 5]")

test("map", '''
result = [1,2,3]
    | map(x → x * 2)
say result
''', "[2, 4, 6]")

test("sum pipeline", '''
result = [1,2,3,4,5]
    | filter(x → x % 2 == 0)
    | sum
say result
''', "6")

test("chain pipeline", '''
result = [1,2,3,4,5,6,7,8,9,10]
    | filter(x → x % 2 == 0)
    | map(x → x * 3)
    | sum
say result
''', "90")

# ── Таблицы ───────────────────────────────
section("Tables")

test("table access", '''
t = { name: "Alice", age: 25 }
say t.name
''', "Alice")

test("nested table", '''
t = { user: { name: "Bob" } }
say t.user.name
''', "Bob")

# ── Stdlib: math ──────────────────────────
section("Stdlib: math")

test("math sqrt",    'say math(16, "sqrt")',       "4")
test("math pow",     'say math(2, "pow", 8)',      "256")
test("math floor",   'say math(3.9, "floor")',     "3")
test("math ceil",    'say math(3.1, "ceil")',      "4")
test("math abs",     'say math(-5, "abs")',        "5")
test("math prime 7", 'say math(7, "prime")',       "yes")
test("math prime 4", 'say math(4, "prime")',       "no")
test("math hex",     'say math(255, "hex")',       "ff")
test("math binary",  'say math(10, "binary")',     "1010")
test("math clamp",   'say math(15, "clamp", 0, 10)', "10")

# ── Stdlib: num ───────────────────────────
section("Stdlib: num")

test("num odd",      'say num(7, "odd")',           "yes")
test("num even",     'say num(4, "even")',          "yes")
test("num positive", 'say num(5, "positive")',      "yes")
test("num negative", 'say num(-3, "negative")',     "yes")
test("num between",  'say num(5, "between", 1, 10)', "yes")
test("num format",   'say num(3.14159, "format", 2)', "3.14")

# ── Stdlib: str_ ──────────────────────────
section("Stdlib: str_")

test("str upper",    'say str_("hello", "upper")',        "HELLO")
test("str lower",    'say str_("HELLO", "lower")',        "hello")
test("str title",    'say str_("hello world", "title")',  "Hello World")
test("str trim",     'say str_("  hi  ", "trim")',        "hi")
test("str reverse",  'say str_("hello", "reverse")',      "olleh")
test("str repeat",   'say str_("ha", "repeat", 3)',       "hahaha")
test("str length",   'say str_("hello", "length")',       "5")
test("str contains", 'say str_("hello world", "contains", "world")', "yes")
test("str starts",   'say str_("hello", "starts", "he")', "yes")
test("str ends",     'say str_("hello", "ends", "lo")',   "yes")
test("str replace",  'say str_("hello", "replace", "l", "r")', "herro")
test("str slice",    'say str_("hello", "slice", 1, 3)',  "el")
test("str is_num",   'say str_("42", "is_num")',          "yes")
test("str is_alpha", 'say str_("abc", "is_alpha")',       "yes")

# ── Stdlib: convert ───────────────────────
section("Stdlib: convert")

test("km to miles",  'say convert(100, "km", "miles")',  "62.1371")
test("c to f",       'say convert(0, "c", "f")',         "32.0")
test("kg to lbs",    'say convert(1, "kg", "lbs")',      "2.20462")
test("bytes to kb",  'say convert(1024, "bytes", "kb")', "1.0")

# ── Stdlib: stats ─────────────────────────
section("Stdlib: stats")

test("stats mean",   'say stats([1,2,3,4,5], "mean")',   "3")
test("stats min",    'say stats([1,2,3,4,5], "min")',    "1")
test("stats max",    'say stats([1,2,3,4,5], "max")',    "5")
test("stats sum",    'say stats([1,2,3,4,5], "sum")',    "15")
test("stats count",  'say stats([1,2,3,4,5], "count")', "5")

# ── Stdlib: list ──────────────────────────
section("Stdlib: list")

test("list add",     'say list([1,2], "add", 3)',           "[1, 2, 3]")
test("list has",     'say list([1,2,3], "has", 2)',         "yes")
test("list index",   'say list([10,20,30], "index", 20)',   "1")
test("list unique",  'say list([1,1,2,2,3], "unique")',     "[1, 2, 3]")
test("list concat",  'say list([1,2], "concat", [3,4])',    "[1, 2, 3, 4]")
test("list slice",   'say list([1,2,3,4,5], "slice", 1, 3)', "[2, 3]")
test("list chunk",   'say list([1,2,3,4], "chunk", 2)',     "[[1, 2], [3, 4]]")
test("list reverse", 'say list([1,2,3], "reverse")',        "[3, 2, 1]")
test("list count",   'say list([1,2,1,3,1], "count", 1)',   "3")
test("list fill",    'say list([], "fill", 3, 0)',           "[0, 0, 0]")

# ── Stdlib: table ─────────────────────────
section("Stdlib: table")

test("table get",    'say table({a: 1, b: 2}, "get", "a")',    "1")
test("table has",    'say table({a: 1}, "has", "a")',          "yes")
test("table has no", 'say table({a: 1}, "has", "z")',          "no")
test("table size",   'say table({a: 1, b: 2}, "size")',        "2")
test("table keys",   'say table({a: 1, b: 2}, "keys")',        "[a, b]")

# ── Error handling ────────────────────────
section("Error Handling")

test("try catch", '''
try
    x = 1 / 0
on error e
    say "caught"
''', "caught")

test_raises("undefined var", 'say undefined_xyz', CreamRuntimeError)

# ── Encode ────────────────────────────────
section("Stdlib: encode")

test("encode md5",    'say length(encode("hello", "md5"))',    "32")
test("encode sha256", 'say length(encode("hello", "sha256"))', "64")
test("encode b64",    'say encode("hello", "base64")',         "aGVsbG8=")
test("decode b64",    'say encode("aGVsbG8=", "base64", "decode")', "hello")

# ── Итог ──────────────────────────────────
total = passed + failed
print(f"\n{'=' * 45}")
print(f"  Results: {passed}/{total} passed")
if failed > 0:
    print(f"  Failed:  {failed}")
    print(f"\n  Failed tests:")
    for e in errors:
        print(f"    - {e}")
else:
    print(f"  All tests passed! ✅")
print(f"{'=' * 45}")

sys.exit(0 if failed == 0 else 1)
