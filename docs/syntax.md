# Cream Syntax Reference

Complete reference for the Cream programming language syntax.

---

## Comments

```cream
-- This is a comment
name = "Alice"  -- inline comment
```

---

## Variables

```cream
name   = "Alice"     -- text
age    = 25          -- integer
score  = 9.8         -- decimal
active = yes         -- boolean (yes / no)
empty_ = empty       -- null value
```

### String Interpolation

```cream
city = "London"
say "I live in {city}"   -- I live in London
```

---

## Data Types

| Type | Example | Notes |
|------|---------|-------|
| number | `42`, `3.14`, `-7` | integers and decimals |
| text | `"hello"` | supports `{interpolation}` |
| bool | `yes`, `no` | true / false |
| list | `[1, 2, 3]` | zero-indexed |
| table | `{key: value}` | key-value pairs |
| empty | `empty` | null / None |

---

## Conditions

```cream
if score >= 90
    say "A"
or if score >= 80
    say "B"
or if score >= 70
    say "C"
else
    say "F"
```

### Comparison Operators

| Operator | Meaning |
|----------|---------|
| `==` | equal |
| `!=` | not equal |
| `>` | greater than |
| `<` | less than |
| `>=` | greater or equal |
| `<=` | less or equal |
| `and` | logical AND |
| `or` | logical OR |
| `not` | logical NOT |

---

## Loops

### repeat N

```cream
repeat 5
    say "Hello!"
```

### for each

```cream
for each name in ["Alice", "Bob", "Eve"]
    say "Hi, {name}!"

for each i in range(0, 10)
    say i
```

### while

```cream
i = 0
while i < 5
    say i
    i = i + 1
```

---

## Functions

### action (regular function)

```cream
action greet(name, greeting = "Hello")
    return "{greeting}, {name}!"

say greet("Alice")
say greet("Bob", "Hi")
```

### Lambda

```cream
double = x → x * 2
say double(7)   -- 14

square = x → x * x
```

### task (async function)

```cream
task fetch_data(url)
    response = wait net(url, "json")
    return response
```

---

## Structs

```cream
struct User
    name:  text
    age:   number
    admin: bool = no

alice = User("Alice", 25)
say alice.name    -- Alice
say alice.admin   -- no
```

---

## Tables (inline objects)

```cream
config = {
    host:  "localhost"
    port:  8080
    debug: yes
}

say config.host   -- localhost
say config.port   -- 8080
```

---

## Lists

```cream
colors = ["red", "green", "blue"]
say colors[0]        -- red
say length(colors)   -- 3
```

---

## Pipeline

The `|` operator passes a value through a chain of operations:

```cream
result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    | filter(x → x % 2 == 0)
    | map(x → x * 3)
    | sum

say result   -- 90
```

### Pipeline steps

| Step | Description |
|------|-------------|
| `filter(x → cond)` | keep elements matching condition |
| `map(x → expr)` | transform each element |
| `sort` | sort ascending |
| `reverse` | reverse order |
| `sum` | sum all numbers |
| `first` | first element |
| `last` | last element |
| `length` | count elements |

---

## Error Handling

```cream
try
    data = net("https://api.example.com", "json")
    say data
on error e
    say "Error: {e.message}"
```

---

## Arithmetic Operators

| Operator | Example | Result |
|----------|---------|--------|
| `+` | `3 + 4` | 7 |
| `-` | `10 - 3` | 7 |
| `*` | `3 * 4` | 12 |
| `/` | `10 / 4` | 2.5 |
| `%` | `10 % 3` | 1 |

---

## Keywords Reference

| Keyword | Usage |
|---------|-------|
| `if` | start condition |
| `or if` | else-if branch |
| `else` | fallback branch |
| `for each X in Y` | iterate collection |
| `repeat N` | loop N times |
| `while cond` | while loop |
| `action name(params)` | define function |
| `task name(params)` | async function |
| `return expr` | return value |
| `struct Name` | define data type |
| `try` | start error handling |
| `on error e` | catch error |
| `wait expr` | await async result |
| `say expr` | print to console |
| `yes` / `no` | boolean values |
| `empty` | null value |
| `and` / `or` / `not` | logic operators |
