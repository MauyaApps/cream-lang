# Cream Language — VS Code Extension

Syntax highlighting, snippets and language support for the **Cream** programming language.

## Features

- ✅ Syntax highlighting for `.cream` files
- ✅ Code snippets for common patterns
- ✅ Auto-closing brackets and quotes
- ✅ Comment toggling with `--`
- ✅ Code folding

## Syntax Highlighting

Highlights:
- Keywords: `if`, `else`, `action`, `repeat`, `for each`, `while`, `struct`, `try`...
- Built-in functions: `say`, `math`, `str_`, `file`, `net`, `list`, `table`...
- Constants: `yes`, `no`, `empty`, `PI`, `E`
- Strings with `{interpolation}` support
- Numbers, operators, lambda `→`, pipeline `|`
- Comments `--`

## Snippets

| Prefix | Description |
|--------|-------------|
| `say` | Print to console |
| `if` | If condition |
| `ife` | If/else condition |
| `action` | Define a function |
| `repeat` | Repeat N times |
| `for` | For each loop |
| `while` | While loop |
| `struct` | Define a struct |
| `try` | Try/catch |
| `pipe` | Pipeline chain |
| `net` | HTTP GET request |
| `file` | Read a file |
| `import` | Import .cream file |

## Example

```cream
-- Hello World
name = "World"
say "Hello, {name}!"

action greet(name, greeting = "Hello")
    return "{greeting}, {name}!"

numbers = [1, 2, 3, 4, 5]
result = numbers
    | filter(x → x % 2 == 0)
    | sum
say result
```

## Links

- [Cream Language](https://github.com/mauyaapps/cream)
- [Documentation](https://github.com/mauyaapps/cream/tree/main/docs)

## License

MIT © 2026 Mauya Apps
