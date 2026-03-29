# Changelog

All notable changes to Cream are documented here.
Format: `[version] — date — description`

---

## [0.2.2] — 2026-03-29 — Android IDE Release

### 📱 Cream IDE for Android (NEW)
- First mobile IDE for Cream — built with Flutter
- Syntax highlighting with real Cream keywords
- Dark and Light themes
- 15 interface languages (EN, RU, ES, FR, DE, ZH, JA, KO, PT, IT, PL, TR, AR, HI, UK)
- File manager with burger menu
- Separate output window (like Pydroid)
- Run button with built-in mini interpreter
- Save / New file support
- Line numbers
- Custom project folder setting
- Minimum Android version: 7.0 (API 24)

### Tested devices
- ✅ Pixel 6 (Android 12), Pixel 7 (Android 13), Pixel 8 (Android 14)
- ✅ Samsung Galaxy S21, S23 Ultra, A34, Galaxy Tab S7
- ✅ Redmi Note 9, Redmi Note 12
- ✅ OnePlus 9, Huawei P30
- ✅ Samsung Galaxy M32 (Android 11)

### Mini interpreter fixes
- Fixed string interpolation `{variable}` — now correctly substitutes values
- Variables properly stored and resolved during execution
- `repeat N` loop now executes body N times
- `for each x in range(a, b)` now iterates correctly
- Numbers display as integers when whole (10 not 10.0)

### Website
- Download page updated with Android section
- PDF learning guide v2 with real Cream syntax

---

## [0.2.1] — 2026-03-22 — Stable Release

### Language
- Fixed pipeline operator `|` edge cases
- Improved string interpolation `{expr}`
- Fixed `for each` with `range()` step parameter
- `break` and `continue` now work correctly inside nested loops
- Fixed `try / on error` not catching all runtime errors
- Arrow syntax: both `->` and `→` now supported

### Standard Library
- `rand("coin")`, `rand("uuid")`
- `stats(lst, "freq")` — frequency map
- `convert()` — added `m↔ft`, `gb↔mb`
- `date("weekday")`, `encode(x, "from_json")`, `sys_("platform")`

### IDE & Toolchain
- Desktop IDE (PyQt6) — `cream_ide_standalone.py`
- VS Code extension — `MauyaApps.cream-language`
- CI/CD via GitHub Actions
- Windows `.exe`, Linux and macOS binaries

### Website
- creamlang.org launched
- Download, FAQ, PDF guide pages

---

## [0.2.0] — 2026-03 — ⚠️ Broken release (do not use)

> Critical bugs in the interpreter. Use 0.2.1 instead.

---

## [0.1.1] — 2026-03 — Bug Fix Release

- Fixed `repeat N with i` counter
- Fixed `for each` iteration over tables
- Fixed string interpolation with nested `{}`
- Fixed `action` default parameter order
- Fixed multi-line pipeline parsing
- `null`, `yes`/`no` now print correctly

---

## [0.1.0] — 2026-03 — Initial Release

### Language
- Lexer, Parser, AST, Interpreter
- Variables, string interpolation, conditions, loops
- Functions (`action`), lambdas, pipelines (`|`)
- Structs, tables, error handling (`try / on error`)
- `yes` / `no` booleans, `null`, comments (`--`)
- Import system

### Standard Library (450+ operations)
- `math`, `num`, `rand`, `stats`, `convert`
- `str_`, `text_`, `regex`, `list`, `table`
- `file`, `folder`, `sys_`, `encode`, `net`, `date`

### Project
- Single-file interpreter `cream.py`
- 8 example programs
- Auto-build workflow
- MIT License — © 2026 MauyaApps

---

## Roadmap

### [0.3.0] — planned
- [ ] Cream IDE for Android — full Cream interpreter integration
- [ ] Classes and inheritance
- [ ] Package manager — `cream install`

### [0.4.0] — planned
- [ ] Compiler to Python / JavaScript
- [ ] Online playground at creamlang.org

### [1.0.0] — planned
- [ ] Stable language spec, full test coverage
- [ ] Performance optimizations
- [ ] Official package registry
