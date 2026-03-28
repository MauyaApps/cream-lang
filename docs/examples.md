# Cream Examples

Ready-to-run example programs demonstrating Cream features.

---

## Hello World

```cream
say "Hello, World!"
```

---

## Variables and Types

```cream
name   = "Alice"
age    = 25
height = 1.75
active = yes

say "Name:   {name}"
say "Age:    {age}"
say "Height: {height}m"
say "Active: {active}"
```

---

## FizzBuzz

```cream
for each n in range(1, 101)
    if n % 15 == 0
        say "FizzBuzz"
    or if n % 3 == 0
        say "Fizz"
    or if n % 5 == 0
        say "Buzz"
    else
        say n
```

---

## Fibonacci

```cream
action fib(n)
    if n <= 1
        return n
    return fib(n - 1) + fib(n - 2)

for each i in range(0, 15)
    say fib(i)
```

---

## Calculator

```cream
action calculate(a, op, b)
    if op == "+"
        return a + b
    or if op == "-"
        return a - b
    or if op == "*"
        return a * b
    or if op == "/"
        if b == 0
            return "Error: division by zero"
        return a / b
    return "Unknown operator"

say calculate(10, "+", 5)    -- 15
say calculate(10, "-", 3)    -- 7
say calculate(10, "*", 4)    -- 40
say calculate(10, "/", 2)    -- 5.0
```

---

## Data Processing

```cream
scores = [85, 92, 78, 96, 88, 74, 91, 83]

say "Scores:  {scores}"
say "Mean:    {stats(scores, "mean")}"
say "Max:     {stats(scores, "max")}"
say "Min:     {stats(scores, "min")}"
say "Std dev: {stats(scores, "std")}"

high_scores = scores
    | filter(x → x >= 90)
    | sort

say "High scores: {high_scores}"
```

---

## String Processing

```cream
text_ = "  Hello, World! This is Cream.  "

say str_(text_, "trim")
say str_(text_, "upper")
say str_(text_, "lower")
say str_(text_, "words")
say str_(text_, "reverse")
say text_(text_, "word_count")
say text_(text_, "slug")
```

---

## File Operations

```cream
-- Write a file
file("notes.txt", "First line\n")
file("notes.txt", "append", "Second line\n")
file("notes.txt", "append", "Third line\n")

-- Read it back
content = file("notes.txt")
say content

-- Read as lines
lines = file("notes.txt", "lines")
say "Total lines: {length(lines)}"

for each line in lines
    say "  > {line}"

-- File info
info = file("notes.txt", "info")
say "Size: {info.size} bytes"

-- Cleanup
file("notes.txt", "delete")
say "Done!"
```

---

## Working with JSON

```cream
-- Create data
users = [
    { name: "Alice", age: 25, active: yes },
    { name: "Bob",   age: 30, active: no  },
    { name: "Eve",   age: 22, active: yes },
]

-- Save to JSON
file("users.json", "json", users)
say "Saved!"

-- Read back
loaded = file("users.json", "json")
say "Loaded {length(loaded)} users"

for each user in loaded
    say "{user.name} — age {user.age}"
```

---

## HTTP Request

```cream
try
    data = net("https://httpbin.org/json", "json")
    say "Got response!"
    say data
on error e
    say "Request failed: {e.message}"
```

---

## Math Utilities

```cream
say math(16,  "sqrt")           -- 4.0
say math(2,   "pow", 10)        -- 1024.0
say math(7,   "prime")          -- yes
say math(255, "hex")            -- ff
say math(42,  "binary")         -- 101010
say math(6,   "factorial")      -- 720
say math(12,  "gcd", 8)         -- 4

say convert(100, "km",    "miles")  -- 62.1371
say convert(37,  "c",     "f")      -- 98.6
say convert(70,  "kg",    "lbs")    -- 154.324
say convert(1,   "hours", "sec")    -- 3600.0
```

---

## Random & Stats

```cream
say rand()           -- 0.0 – 1.0
say rand(100)        -- 0 – 100
say rand("dice")     -- 1 – 6
say rand("coin")     -- yes / no
say rand("uuid")     -- unique ID

-- Simulate 10 dice rolls
rolls = []
repeat 10
    rolls = list(rolls, "add", rand("dice"))

say "Rolls: {rolls}"
say "Average: {stats(rolls, "mean")}"
say "Min: {stats(rolls, "min")}"
say "Max: {stats(rolls, "max")}"
```

---

## Struct Example

```cream
struct Product
    name:      text
    price:     number
    in_stock:  bool = yes

struct Cart
    items:  list
    total:  number = 0

apple  = Product("Apple",  0.99)
banana = Product("Banana", 0.59)
milk   = Product("Milk",   1.49)

products = [apple, banana, milk]

for each p in products
    say "{p.name}: ${p.price}"

total = products
    | filter(p → p.in_stock == yes)
    | map(p → p.price)
    | sum

say "Total: ${round(total, 2)}"
```

---

## Encoding & Security

```cream
password = "mysecretpassword"

say encode(password, "md5")
say encode(password, "sha256")

secret = encode("Hello, Cream!", "base64")
say "Encoded: {secret}"

decoded = encode(secret, "base64", "decode")
say "Decoded: {decoded}"
```

---

## Date and Time

```cream
now = date()
say "Year:   {now.year}"
say "Month:  {now.month}"
say "Day:    {now.day}"

say date("today")
say date("time")
say date("timestamp")
say date("format", "%A, %B %d %Y")
```

---

## Pipeline Patterns

```cream
words = ["banana", "apple", "cherry", "date", "elderberry"]

-- Sort and take first 3
top3 = words
    | sort
    | list("slice", 0, 3)

say top3

-- Find long words
long_words = words
    | filter(w → length(w) > 5)

say long_words

-- Transform
upper_words = words
    | map(w → str_(w, "upper"))

say upper_words

-- Numbers pipeline
result = range(1, 20)
    | filter(x → num(x, "odd"))
    | map(x → x * x)
    | sum

say "Sum of squares of odd numbers 1-19: {result}"
```
