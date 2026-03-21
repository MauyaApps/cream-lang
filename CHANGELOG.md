# Changelog

All notable changes to Cream are documented here.  
Format: `[version] — date — description`

---

## [0.1.0] — 2026-03 — Initial Release

### Language
- Lexer — tokenizes Cream source code
- Parser — builds Abstract Syntax Tree (AST)
- Interpreter — executes AST directly
- Variables with dynamic typing
- String interpolation with `{variable}`
- Conditions — `if / or if / else`
- Loops — `repeat`, `for each`, `while`
- Functions — `action` with default parameters
- Lambda expressions — `x → expression`
- Pipeline operator — `|`
- Structs — typed data with default fields
- Tables — inline key-value objects `{ key: value }`
- Error handling — `try / on error`
- Async functions — `task` and `wait`
- Boolean literals — `yes` / `no`
- Null literal — `empty`

### Standard Library (450+ operations)
- `math` — sqrt, pow, sin, cos, log, prime, hex, binary, clamp...
- `num` — even, odd, between, format, positive, negative...
- `rand` — random numbers, dice, coin, uuid, shuffle, sample...
- `stats` — mean, median, std, variance, freq, unique...
- `convert` — units: km, miles, c, f, kg, lbs, bytes, mb...
- `str_` — upper, lower, trim, reverse, repeat, slice, replace...
- `text_` — slug, palindrome, similarity, extract emails/urls...
- `regex` — match, all, test, replace, split, groups...
- `list` — add, remove, chunk, unique, flat, zip, shuffle...
- `table` — get, set, has, keys, values, merge...
- `file` — read, write, append, json, csv, info, copy...
- `folder` — list, create, delete, find, files, folders...
- `sys_` — run, env, sleep, cwd, exit, cpu, time...
- `encode` — md5, sha256, base64, url, json, hex...
- `net` — GET, POST, JSON, download, status, headers...
- `date` — today, time, timestamp, format...
- `print_` — colored output, bold, separator line...

### Runner
- Run `.cream` files: `python cream.py file.cream`
- Interactive REPL: `python cream.py`
- `import` — load and run external `.cream` files

### Project
- Single-file interpreter `cream.py`
- Documentation site `docs/cream-lang.html`
- Syntax reference `docs/syntax.md`
- Stdlib reference `docs/stdlib.md`
- Examples guide `docs/examples.md`
- 8 example programs in `examples/`
- Auto-build workflow `.github/workflows/build.yml`
- MIT License — © 2026 Mauya Apps

---

## Roadmap

### [0.2.0] — planned
- [ ] Classes and inheritance
- [ ] Package manager — `cream install`
- [ ] More stdlib modules — `image`, `audio`, `ui`
- [ ] Better error messages with line highlights
- [ ] VS Code syntax highlighting extension

### [0.3.0] — planned
- [ ] Compiler to Python / JavaScript
- [ ] Standalone `.exe` via PyInstaller
- [ ] Online playground website

### [1.0.0] — planned
- [ ] Stable language spec
- [ ] Full test coverage
- [ ] Performance optimizations
- [ ] Official package registry
