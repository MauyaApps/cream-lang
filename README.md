# Cream 🍦

> A universal programming language — 50× simpler than Python.

Cream is a clean, readable programming language. One syntax for web, data, automation, and everything in between.

```cream
-- Hello, World!
name = "World"
say "Hello, {name}!"

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = numbers
    | filter(x → x % 2 == 0)
    | map(x → x * 3)
    | sum
say "Result: {result}"
```

---

## Installation

### 🪟 Windows

1. Go to [Releases](../../releases/latest)
2. Download `cream.exe`
3. Open terminal in the same folder
4. Run your `.cream` file:

```
cream.exe hello.cream
```

No Python or anything else required.

---

### 🐧 Linux

> 🚧 Coming soon — Linux build is in development.

For now use the Python version below.

---

### 🍎 macOS

> 🚧 Coming soon — macOS build is in development.

For now use the Python version below.

---

### 🐍 Python (any platform)

If you have Python 3.8+ installed:

```bash
# Clone or download cream.py
git clone https://github.com/MauyaApps/cream-lang.git
cd cream-lang

# Run a file
python cream.py hello.cream

# Start interactive REPL
python cream.py
```

---

### 📱 Android (Pydroid 3)

1. Download `cream.py` from this repo
2. Create your `.cream` file in the same folder
3. Create `run.py`:
   ```python
   from cream import Interpreter
   Interpreter().run(open("hello.cream").read())
   ```
4. Run `run.py` in Pydroid

---

### 🌐 Browser (no install)

Open `docs/cream-lang.html` in any browser — write and run Cream code directly, no installation needed.

---

## VS Code Extension

Install **Cream Language** syntax highlighting directly in VS Code:

1. Open VS Code
2. Press `Ctrl+Shift+X`
3. Search **Cream Language** by MauyaApps
4. Click Install

Or install directly:

[![VS Code Marketplace](https://img.shields.io/badge/VS%20Code-Cream%20Language-blue?logo=visualstudiocode)](https://marketplace.visualstudio.com/items?itemName=MauyaApps.cream-language)

Features:
- ✅ Syntax highlighting for `.cream` files
- ✅ Code snippets (`if`, `action`, `repeat`, `pipe`...)
- ✅ Auto-closing brackets and quotes
- ✅ Comment toggling with `--`

---

## Quick Start

Create a file `hello.cream`:

```cream
name = "World"
say "Hello, {name}!"

repeat 3
    say "Cream is simple!"

numbers = [1, 2, 3, 4, 5]
result = numbers
    | filter(x → x % 2 == 0)
    | sum
say "Sum of evens: {result}"
```

Run it:

```bash
cream.exe hello.cream
# or
python cream.py hello.cream
```

---

## Language Overview

```cream
-- Variables
name   = "Alice"
age    = 25
active = yes

-- Conditions
if age >= 18
    say "Adult"
else
    say "Minor"

-- Loops
repeat 3
    say "Hello!"

for each x in [1, 2, 3, 4, 5]
    say x * 2

-- Functions
action greet(name, greeting = "Hello")
    return "{greeting}, {name}!"

say greet("Bob")

-- Structs
struct Point
    x: number
    y: number

p = Point(10, 20)
say "Point: {p.x}, {p.y}"

-- Pipeline
[1,2,3,4,5,6,7,8,9,10]
    | filter(x → x % 2 == 0)
    | map(x → x * x)
    | sum

-- Error handling
try
    data = net("https://api.example.com", "json")
on error e
    say "Failed: {e.message}"
```

---

## Standard Library

450+ operations through smart multi-purpose commands:

| Command | Operations |
|---------|------------|
| `math(x, op)` | sqrt, pow, sin, cos, prime, factorial, clamp, hex, binary... |
| `num(x, op)` | even, odd, between, format, positive, negative... |
| `rand(...)` | random number, dice, coin, uuid, shuffle, sample... |
| `stats(lst, op)` | mean, median, std, variance, min, max, freq... |
| `convert(x, from, to)` | km↔miles, c↔f, kg↔lbs, bytes↔mb... |
| `str_(x, op)` | upper, lower, trim, reverse, repeat, slice, replace... |
| `text_(x, op)` | slug, palindrome, similarity, extract emails/urls... |
| `regex(pat, txt, op)` | match, all, test, replace, split, groups... |
| `list(lst, op)` | add, remove, chunk, unique, flat, zip, shuffle... |
| `table(t, op)` | get, set, has, keys, values, merge... |
| `file(path, op)` | read, write, append, json, csv, info, copy... |
| `folder(path, op)` | list, create, delete, find, tree... |
| `sys_(op)` | run commands, env vars, sleep, cwd, exit... |
| `encode(x, op)` | md5, sha256, base64, url, json, hex... |
| `net(url, op)` | GET, POST, JSON, download, status, headers... |
| `date(op)` | today, time, timestamp, format... |

---

## Examples

See the [`examples/`](examples/) folder:

| File | Description |
|------|-------------|
| [`hello.cream`](examples/hello.cream) | Hello World |
| [`fibonacci.cream`](examples/fibonacci.cream) | Fibonacci sequence |
| [`fizzbuzz.cream`](examples/fizzbuzz.cream) | FizzBuzz |
| [`calculator.cream`](examples/calculator.cream) | Calculator with math |
| [`todo.cream`](examples/todo.cream) | Todo list with file storage |
| [`weather.cream`](examples/weather.cream) | Live weather from API |
| [`data_processing.cream`](examples/data_processing.cream) | Student grades analysis |
| [`strings.cream`](examples/strings.cream) | String manipulation |

---

## Documentation

| Resource | Description |
|----------|-------------|
| [`docs/syntax.md`](docs/syntax.md) | Full syntax reference |
| [`docs/stdlib.md`](docs/stdlib.md) | All 450+ built-in operations |
| [`docs/examples.md`](docs/examples.md) | Code examples guide |
| [`docs/cream-lang.html`](docs/cream-lang.html) | Interactive docs website |

---

## Project Structure

```
cream/
├── cream.py               -- The entire language (one file)
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .github/
│   └── workflows/
│       └── build.yml
├── docs/
│   ├── syntax.md
│   ├── stdlib.md
│   ├── examples.md
│   └── cream-lang.html
├── examples/
│   ├── hello.cream
│   ├── fibonacci.cream
│   ├── fizzbuzz.cream
│   ├── calculator.cream
│   ├── todo.cream
│   ├── weather.cream
│   ├── data_processing.cream
│   └── strings.cream
├── tests/
│   └── test_cream.py
└── vscode-extension/
    ├── package.json
    ├── syntaxes/
    │   └── cream.tmLanguage.json
    └── snippets/
        └── cream.json
```

---

## Roadmap

- [x] Lexer
- [x] Parser + AST
- [x] Interpreter
- [x] Standard library (450+ operations)
- [x] HTTP / networking
- [x] Windows `.exe` build
- [x] VS Code syntax highlighting extension
- [x] import system for .cream files
- [ ] Linux / macOS builds
- [ ] Classes and inheritance
- [ ] Package manager (`cream install`)
- [ ] Compiler to Python / JavaScript
- [ ] Website

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Contributing

Contributions are welcome! Feel free to:
- Report bugs via Issues
- Suggest new features
- Submit pull requests
- Add more examples

---

*Cream is open source. © 2026 Mauya Apps*****
