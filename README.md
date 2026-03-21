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
2. Download `cream-windows.exe`
3. Open terminal in the same folder
4. Run your `.cream` file:

```
cream hello.cream
```

No Python or anything else required.

---

### 🐧 Linux

1. Go to [Releases](../../releases/latest)
2. Download `cream-linux`
3. Make it executable and run:

```bash
chmod +x cream-linux
./cream-linux hello.cream
```

Or move it to PATH for global use:

```bash
sudo mv cream-linux /usr/local/bin/cream
cream hello.cream
```

---

### 🍎 macOS

1. Go to [Releases](../../releases/latest)
2. Download `cream-macos`
3. Make it executable and run:

```bash
chmod +x cream-macos
./cream-macos hello.cream
```

If macOS blocks it — go to System Settings → Privacy → allow it.

---

### 🐍 Python (any platform)

If you have Python 3.8+ installed:

```bash
# Clone or download cream.py
git clone https://github.com/yourusername/cream.git
cd cream

# Run a file
python cream.py hello.cream

# Start interactive REPL
python cream.py
```

---

### 📱 Android (Pydroid 3)

1. Download `cream.py` from this repo
2. Create your `.cream` file in the same folder
3. Add this line at the very top of `cream.py`:
   ```python
   # Add after imports, before the test:
   ```
4. Or use this tiny launcher — create `run.py`:
   ```python
   from cream import Interpreter
   Interpreter().run(open("hello.cream").read())
   ```
5. Run `run.py` in Pydroid

---

### 🌐 Browser (no install)

Open `docs/cream-lang.html` in any browser — write and run Cream code directly, no installation needed.

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
cream hello.cream
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
├── .github/
│   └── workflows/
│       └── build.yml      -- Auto-build .exe for all platforms
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
└── tests/
    └── test_cream.py
```

---

## Roadmap

- [x] Lexer
- [x] Parser + AST
- [x] Interpreter
- [x] Standard library (450+ operations)
- [x] HTTP / networking
- [x] Auto-build for Windows, Linux, macOS
- [ ] `import` — load external .cream files
- [ ] Classes and inheritance
- [ ] Package manager (`cream install`)
- [ ] Compiler to Python / JavaScript
- [ ] VS Code syntax highlighting extension

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

*Cream is open source. © 2026 Mauya Apps*
