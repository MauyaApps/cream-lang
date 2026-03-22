#!/usr/bin/env python3
# ============================================
#   Cream IDE v0.1 — PyQt6
#   Standalone — includes Cream interpreter
# ============================================

# ══════════════════════════════════════════
#  ВСТРОЕННЫЙ ИНТЕРПРЕТАТОР CREAM
# ══════════════════════════════════════════

# ============================================
#   Cream Language — Interpreter v0.1
#   Выполняет AST напрямую
#   Включает лексер и парсер целиком
# ============================================

# ══════════════════════════════════════════
#  ЛЕКСЕР
# ══════════════════════════════════════════

class TT:
    NUMBER   = "NUMBER";   STRING   = "STRING"
    BOOL     = "BOOL";     EMPTY    = "EMPTY"
    IDENT    = "IDENT";    KEYWORD  = "KEYWORD"
    PLUS     = "PLUS";     MINUS    = "MINUS"
    STAR     = "STAR";     SLASH    = "SLASH"
    PERCENT  = "PERCENT";  ARROW    = "ARROW"
    PIPE     = "PIPE";     DOT      = "DOT"
    ASSIGN   = "ASSIGN";   EQ       = "EQ"
    NEQ      = "NEQ";      LT       = "LT"
    GT       = "GT";       LTE      = "LTE"
    GTE      = "GTE";      LPAREN   = "LPAREN"
    RPAREN   = "RPAREN";   LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"; LBRACE   = "LBRACE"
    RBRACE   = "RBRACE";   COMMA    = "COMMA"
    COLON    = "COLON";    NEWLINE  = "NEWLINE"
    INDENT   = "INDENT";   DEDENT   = "DEDENT"
    EOF      = "EOF"

KEYWORDS = {
    "if", "else", "or if", "for each", "in",
    "repeat", "while", "action", "return",
    "task", "wait", "together", "try", "on error",
    "struct", "yes", "no", "empty",
    "and", "or", "not", "say",
    "page", "block", "card", "button", "text", "animation",
    "import",
}

class Token:
    def __init__(self, type_, value, line=0, col=0):
        self.type = type_; self.value = value
        self.line = line;  self.col   = col
    def __repr__(self):
        return f"Token({self.type:<12}| {repr(self.value):<20}| line {self.line})"

class LexerError(Exception):
    def __init__(self, msg, line, col):
        super().__init__(f"[Lexer Error] Line {line}, Col {col}: {msg}")

class Lexer:
    def __init__(self, source):
        self.source = source; self.pos = 0
        self.line = 1;        self.col = 1
        self.tokens = []

    def current(self):
        return self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self, offset=1):
        p = self.pos + offset
        return self.source[p] if p < len(self.source) else None

    def advance(self):
        ch = self.source[self.pos]; self.pos += 1
        if ch == '\n': self.line += 1; self.col = 1
        else: self.col += 1
        return ch

    def add(self, type_, value):
        self.tokens.append(Token(type_, value, self.line, self.col))

    def skip_spaces(self):
        while self.current() in (' ', '\t'): self.advance()

    def read_string(self):
        col_start = self.col; self.advance(); result = ""
        while self.current() and self.current() != '"':
            if self.current() == '\\':
                self.advance()
                esc = self.advance()
                result += {'n':'\n','t':'\t','"':'"','\\':'\\'}.get(esc, esc)
            else: result += self.advance()
        if not self.current():
            raise LexerError("Незакрытая строка", self.line, col_start)
        self.advance()
        self.tokens.append(Token(TT.STRING, result, self.line, col_start))

    def read_number(self):
        col_start = self.col; num = ""
        while self.current() and (self.current().isdigit() or self.current() == '.'):
            num += self.advance()
        value = float(num) if '.' in num else int(num)
        self.tokens.append(Token(TT.NUMBER, value, self.line, col_start))

    def read_ident(self):
        col_start = self.col; word = ""
        while self.current() and (self.current().isalnum() or self.current() == '_'):
            word += self.advance()

        for compound in ("or if", "for each", "on error"):
            first, second = compound.split(' ', 1)
            if word == first:
                saved = (self.pos, self.col, self.line)
                self.skip_spaces()
                if self.source[self.pos:self.pos+len(second)] == second:
                    self.pos += len(second); self.col += len(second)
                    self.tokens.append(Token(TT.KEYWORD, compound, self.line, col_start))
                    return
                else:
                    self.pos, self.col, self.line = saved

        if word in ("yes", "no"):
            self.tokens.append(Token(TT.BOOL, word == "yes", self.line, col_start))
        elif word == "empty":
            self.tokens.append(Token(TT.EMPTY, None, self.line, col_start))
        elif word in KEYWORDS:
            self.tokens.append(Token(TT.KEYWORD, word, self.line, col_start))
        else:
            self.tokens.append(Token(TT.IDENT, word, self.line, col_start))

    def handle_indents(self, lines):
        indent_stack = [0]; result = []
        for line_num, line in enumerate(lines, 1):
            stripped = line.lstrip()
            if not stripped or stripped.startswith('--'): continue
            if stripped.startswith('|'):
                result.append(("LINE", stripped, line_num)); continue
            indent = len(line) - len(line.lstrip(' '))
            if indent > indent_stack[-1]:
                indent_stack.append(indent)
                result.append(Token(TT.INDENT, indent, line_num, 1))
                result.append(("LINE", stripped, line_num))
            elif indent == indent_stack[-1]:
                result.append(("LINE", stripped, line_num))
            else:
                while indent < indent_stack[-1]:
                    indent_stack.pop()
                    result.append(Token(TT.DEDENT, indent_stack[-1], line_num, 1))
                result.append(("LINE", stripped, line_num))
        while len(indent_stack) > 1:
            indent_stack.pop()
            result.append(Token(TT.DEDENT, 0, 0, 0))
        return result

    def tokenize(self):
        lines = self.source.split('\n')
        pre   = self.handle_indents(lines)
        all_tokens = []
        for item in pre:
            if isinstance(item, Token): all_tokens.append(item); continue
            _, text, line_num = item
            self.source = text; self.pos = 0
            self.line = line_num; self.col = 1; self.tokens = []
            self._tokenize_line()
            all_tokens.extend(self.tokens)
            all_tokens.append(Token(TT.NEWLINE, '\n', line_num, len(text)))
        all_tokens.append(Token(TT.EOF, None, self.line, self.col))
        return all_tokens

    def _tokenize_line(self):
        while self.pos < len(self.source):
            ch = self.current()
            if ch in (' ', '\t'): self.skip_spaces()
            elif ch == '-' and self.peek() == '-': break
            elif ch == '"': self.read_string()
            elif ch.isdigit(): self.read_number()
            elif ch.isalpha() or ch == '_': self.read_ident()
            elif ch == '→': self.add(TT.ARROW, '→'); self.advance()
            elif ch == '-' and self.peek() == '>':
                self.advance(); self.advance(); self.add(TT.ARROW, '->')
            elif ch == '=' and self.peek() == '=':
                self.advance(); self.advance(); self.add(TT.EQ, '==')
            elif ch == '!' and self.peek() == '=':
                self.advance(); self.advance(); self.add(TT.NEQ, '!=')
            elif ch == '<' and self.peek() == '=':
                self.advance(); self.advance(); self.add(TT.LTE, '<=')
            elif ch == '>' and self.peek() == '=':
                self.advance(); self.advance(); self.add(TT.GTE, '>=')
            elif ch == '=': self.advance(); self.add(TT.ASSIGN,   '=')
            elif ch == '+': self.advance(); self.add(TT.PLUS,     '+')
            elif ch == '-': self.advance(); self.add(TT.MINUS,    '-')
            elif ch == '*': self.advance(); self.add(TT.STAR,     '*')
            elif ch == '/': self.advance(); self.add(TT.SLASH,    '/')
            elif ch == '%': self.advance(); self.add(TT.PERCENT,  '%')
            elif ch == '|': self.advance(); self.add(TT.PIPE,     '|')
            elif ch == '.': self.advance(); self.add(TT.DOT,      '.')
            elif ch == '<': self.advance(); self.add(TT.LT,       '<')
            elif ch == '>': self.advance(); self.add(TT.GT,       '>')
            elif ch == '(': self.advance(); self.add(TT.LPAREN,   '(')
            elif ch == ')': self.advance(); self.add(TT.RPAREN,   ')')
            elif ch == '[': self.advance(); self.add(TT.LBRACKET, '[')
            elif ch == ']': self.advance(); self.add(TT.RBRACKET, ']')
            elif ch == '{': self.advance(); self.add(TT.LBRACE,   '{')
            elif ch == '}': self.advance(); self.add(TT.RBRACE,   '}')
            elif ch == ',': self.advance(); self.add(TT.COMMA,    ',')
            elif ch == ':': self.advance(); self.add(TT.COLON,    ':')
            else: raise LexerError(f"Неизвестный символ: {repr(ch)}", self.line, self.col)


# ══════════════════════════════════════════
#  УЗЛЫ AST
# ══════════════════════════════════════════

class Node: pass

class Program(Node):
    def __init__(self, body): self.body = body

class NumberLiteral(Node):
    def __init__(self, value): self.value = value

class StringLiteral(Node):
    def __init__(self, value): self.value = value

class BoolLiteral(Node):
    def __init__(self, value): self.value = value

class EmptyLiteral(Node): pass

class ListLiteral(Node):
    def __init__(self, elements): self.elements = elements

class TableLiteral(Node):
    def __init__(self, pairs): self.pairs = pairs

class Identifier(Node):
    def __init__(self, name): self.name = name

class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left; self.op = op; self.right = right

class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = op; self.operand = operand

class FieldAccess(Node):
    def __init__(self, obj, field):
        self.obj = obj; self.field = field

class IndexAccess(Node):
    def __init__(self, obj, index):
        self.obj = obj; self.index = index

class Lambda(Node):
    def __init__(self, param, body):
        self.param = param; self.body = body

class Call(Node):
    def __init__(self, callee, args):
        self.callee = callee; self.args = args

class Pipeline(Node):
    def __init__(self, value, steps):
        self.value = value; self.steps = steps

class Assign(Node):
    def __init__(self, name, value):
        self.name = name; self.value = value

class Say(Node):
    def __init__(self, value): self.value = value

class Return(Node):
    def __init__(self, value): self.value = value

class If(Node):
    def __init__(self, condition, then_body, elseif_clauses, else_body):
        self.condition = condition; self.then_body = then_body
        self.elseif_clauses = elseif_clauses; self.else_body = else_body

class ForEach(Node):
    def __init__(self, var, iterable, body):
        self.var = var; self.iterable = iterable; self.body = body

class Repeat(Node):
    def __init__(self, count, body):
        self.count = count; self.body = body

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition; self.body = body

class ActionDef(Node):
    def __init__(self, name, params, body):
        self.name = name; self.params = params; self.body = body

class TaskDef(Node):
    def __init__(self, name, params, body):
        self.name = name; self.params = params; self.body = body

class Wait(Node):
    def __init__(self, value): self.value = value

class TryCatch(Node):
    def __init__(self, try_body, error_var, catch_body):
        self.try_body = try_body; self.error_var = error_var
        self.catch_body = catch_body

class StructDef(Node):
    def __init__(self, name, fields):
        self.name = name; self.fields = fields

class Import(Node):
    """import "file.cream" — загрузить внешний .cream файл"""
    def __init__(self, path): self.path = path


# ══════════════════════════════════════════
#  ПАРСЕР
# ══════════════════════════════════════════

class ParseError(Exception):
    def __init__(self, msg, token=None):
        loc = f" (line {token.line})" if token else ""
        super().__init__(f"[Parse Error]{loc}: {msg}")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens; self.pos = 0

    def current(self): return self.tokens[self.pos]
    def peek(self, offset=1):
        p = self.pos + offset
        return self.tokens[p] if p < len(self.tokens) else self.tokens[-1]

    def advance(self):
        tok = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1: self.pos += 1
        return tok

    def skip_newlines(self):
        while self.current().type == TT.NEWLINE: self.advance()

    def expect(self, type_, value=None):
        tok = self.current()
        if tok.type != type_:
            raise ParseError(f"Ожидался {type_}, получен {tok.type} ({repr(tok.value)})", tok)
        if value is not None and tok.value != value:
            raise ParseError(f"Ожидалось {repr(value)}, получено {repr(tok.value)}", tok)
        return self.advance()

    def match(self, type_, value=None):
        tok = self.current()
        if tok.type != type_: return False
        if value is not None and tok.value != value: return False
        return True

    def match_keyword(self, kw):
        return self.current().type == TT.KEYWORD and self.current().value == kw

    def parse_block(self):
        self.skip_newlines()
        self.expect(TT.INDENT)
        stmts = []
        while not self.match(TT.DEDENT) and not self.match(TT.EOF):
            self.skip_newlines()
            if self.match(TT.DEDENT) or self.match(TT.EOF): break
            stmts.append(self.parse_statement())
            self.skip_newlines()
        self.expect(TT.DEDENT)
        return stmts

    def parse_statement(self):
        tok = self.current()
        if tok.type == TT.KEYWORD:
            kw = tok.value
            if kw == "if":       return self.parse_if()
            if kw == "for each": return self.parse_for_each()
            if kw == "repeat":   return self.parse_repeat()
            if kw == "while":    return self.parse_while()
            if kw == "action":   return self.parse_action()
            if kw == "task":     return self.parse_task()
            if kw == "return":   return self.parse_return()
            if kw == "say":      return self.parse_say()
            if kw == "wait":     return self.parse_wait_stmt()
            if kw == "try":      return self.parse_try()
            if kw == "struct":   return self.parse_struct()
            if kw == "import":   return self.parse_import()
        if tok.type == TT.IDENT and self.peek().type == TT.ASSIGN:
            return self.parse_assign()
        expr = self.parse_expression()
        self.skip_newlines()
        return expr

    def parse_say(self):
        self.advance()
        value = self.parse_expression()
        self.skip_newlines()
        return Say(value)

    def parse_assign(self):
        name = self.advance().value
        self.advance()
        value = self.parse_pipeline()
        self.skip_newlines()
        return Assign(name, value)

    def parse_return(self):
        self.advance()
        value = self.parse_expression()
        self.skip_newlines()
        return Return(value)

    def parse_wait_stmt(self):
        self.advance()
        value = self.parse_expression()
        self.skip_newlines()
        return Wait(value)

    def parse_if(self):
        self.advance()
        condition = self.parse_expression()
        self.skip_newlines()
        then_body = self.parse_block()
        elseif_clauses = []; else_body = None
        while True:
            self.skip_newlines()
            if self.match_keyword("or if"):
                self.advance()
                cond = self.parse_expression()
                self.skip_newlines()
                body = self.parse_block()
                elseif_clauses.append((cond, body))
            elif self.match_keyword("else"):
                self.advance()
                self.skip_newlines()
                if self.match_keyword("if"):
                    self.advance()
                    cond = self.parse_expression()
                    self.skip_newlines()
                    body = self.parse_block()
                    elseif_clauses.append((cond, body))
                else:
                    else_body = self.parse_block()
                    break
            else:
                break
        return If(condition, then_body, elseif_clauses, else_body)

    def parse_for_each(self):
        self.advance()
        var = self.expect(TT.IDENT).value
        self.expect(TT.KEYWORD, "in")
        iterable = self.parse_expression()
        self.skip_newlines()
        body = self.parse_block()
        return ForEach(var, iterable, body)

    def parse_repeat(self):
        self.advance()
        count = self.parse_expression()
        self.skip_newlines()
        body = self.parse_block()
        return Repeat(count, body)

    def parse_while(self):
        self.advance()
        condition = self.parse_expression()
        self.skip_newlines()
        body = self.parse_block()
        return While(condition, body)

    def parse_action(self):
        self.advance()
        name   = self.expect(TT.IDENT).value
        params = self.parse_params()
        self.skip_newlines()
        body   = self.parse_block()
        return ActionDef(name, params, body)

    def parse_task(self):
        self.advance()
        name   = self.expect(TT.IDENT).value
        params = self.parse_params()
        self.skip_newlines()
        body   = self.parse_block()
        return TaskDef(name, params, body)

    def parse_params(self):
        self.expect(TT.LPAREN)
        params = []
        while not self.match(TT.RPAREN):
            name = self.expect(TT.IDENT).value
            default = None
            if self.match(TT.ASSIGN):
                self.advance(); default = self.parse_expression()
            params.append((name, default))
            if self.match(TT.COMMA): self.advance()
        self.expect(TT.RPAREN)
        return params

    def parse_try(self):
        self.advance()
        self.skip_newlines()
        try_body = self.parse_block()
        self.skip_newlines()
        self.expect(TT.KEYWORD, "on error")
        error_var = self.expect(TT.IDENT).value
        self.skip_newlines()
        catch_body = self.parse_block()
        return TryCatch(try_body, error_var, catch_body)

    def parse_struct(self):
        self.advance()
        name = self.expect(TT.IDENT).value
        self.skip_newlines()
        self.expect(TT.INDENT)
        fields = []
        while not self.match(TT.DEDENT):
            self.skip_newlines()
            if self.match(TT.DEDENT): break
            fname = self.expect(TT.IDENT).value
            self.expect(TT.COLON)
            tok = self.current()
            if tok.type in (TT.IDENT, TT.KEYWORD):
                ftype = self.advance().value
            else:
                raise ParseError(f"Ожидался тип поля", tok)
            default = None
            if self.match(TT.ASSIGN):
                self.advance(); default = self.parse_expression()
            fields.append((fname, ftype, default))
            self.skip_newlines()
        self.expect(TT.DEDENT)
        return StructDef(name, fields)

    def parse_expression(self): return self.parse_pipeline()

    def parse_pipeline(self):
        left = self.parse_logical()
        if not self.match(TT.PIPE):
            if not (self.match(TT.NEWLINE) and self.peek().type == TT.PIPE):
                return left
        steps = []
        while True:
            if self.match(TT.NEWLINE) and self.peek().type == TT.PIPE:
                self.advance()
            if not self.match(TT.PIPE): break
            self.advance()
            step = self.parse_call_or_ident()
            steps.append(step)
        if not steps: return left
        return Pipeline(left, steps)

    def parse_logical(self):
        left = self.parse_comparison()
        while self.current().type == TT.KEYWORD and self.current().value in ("and", "or"):
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        return left

    def parse_comparison(self):
        left = self.parse_addition()
        cmp_types = {TT.EQ, TT.NEQ, TT.LT, TT.GT, TT.LTE, TT.GTE}
        while self.current().type in cmp_types:
            op = self.advance().value
            right = self.parse_addition()
            left = BinaryOp(left, op, right)
        return left

    def parse_addition(self):
        left = self.parse_multiply()
        while self.current().type in (TT.PLUS, TT.MINUS):
            op = self.advance().value
            right = self.parse_multiply()
            left = BinaryOp(left, op, right)
        return left

    def parse_multiply(self):
        left = self.parse_unary()
        while self.current().type in (TT.STAR, TT.SLASH, TT.PERCENT):
            op = self.advance().value
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        return left

    def parse_unary(self):
        if self.match_keyword("not"):
            self.advance(); return UnaryOp("not", self.parse_unary())
        if self.match(TT.MINUS):
            self.advance(); return UnaryOp("-", self.parse_unary())
        return self.parse_postfix()

    def parse_postfix(self):
        node = self.parse_primary()
        while True:
            if self.match(TT.DOT):
                self.advance()
                field = self.expect(TT.IDENT).value
                node  = FieldAccess(node, field)
            elif self.match(TT.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.expect(TT.RBRACKET)
                node  = IndexAccess(node, index)
            elif self.match(TT.LPAREN):
                args = self.parse_args()
                node = Call(node, args)
            else: break
        return node

    def parse_call_or_ident(self): return self.parse_postfix()

    def parse_args(self):
        self.expect(TT.LPAREN)
        args = []
        while not self.match(TT.RPAREN):
            if self.match(TT.IDENT) and self.peek().type == TT.ARROW:
                param = self.advance().value
                self.advance()
                body  = self.parse_expression()
                args.append(Lambda(param, body))
            else:
                args.append(self.parse_expression())
            if self.match(TT.COMMA): self.advance()
        self.expect(TT.RPAREN)
        return args

    def parse_primary(self):
        tok = self.current()
        if tok.type == TT.NUMBER:   self.advance(); return NumberLiteral(tok.value)
        if tok.type == TT.STRING:   self.advance(); return StringLiteral(tok.value)
        if tok.type == TT.BOOL:     self.advance(); return BoolLiteral(tok.value)
        if tok.type == TT.EMPTY:    self.advance(); return EmptyLiteral()
        if tok.type == TT.IDENT:    self.advance(); return Identifier(tok.value)
        if tok.type == TT.LBRACKET: return self.parse_list()
        if tok.type == TT.LBRACE:   return self.parse_table()
        if tok.type == TT.LPAREN:
            self.advance()
            node = self.parse_expression()
            self.expect(TT.RPAREN)
            return node
        if tok.type == TT.KEYWORD:
            if tok.value == "wait":
                self.advance(); return Wait(self.parse_expression())
            if tok.value == "not":
                self.advance(); return UnaryOp("not", self.parse_primary())
            self.advance()
            if self.match(TT.LPAREN):
                args = self.parse_args()
                return Call(Identifier(tok.value), args)
            return Identifier(tok.value)
        raise ParseError(f"Неожиданный токен: {tok.type} {repr(tok.value)}", tok)

    def parse_list(self):
        self.expect(TT.LBRACKET)
        elements = []
        while not self.match(TT.RBRACKET):
            elements.append(self.parse_expression())
            if self.match(TT.COMMA): self.advance()
        self.expect(TT.RBRACKET)
        return ListLiteral(elements)

    def parse_table(self):
        self.expect(TT.LBRACE)
        self.skip_newlines()
        pairs = []
        while not self.match(TT.RBRACE):
            self.skip_newlines()
            key = self.expect(TT.IDENT).value
            self.expect(TT.COLON)
            value = self.parse_expression()
            pairs.append((key, value))
            self.skip_newlines()
            if self.match(TT.COMMA): self.advance()
            self.skip_newlines()
        self.expect(TT.RBRACE)
        return TableLiteral(pairs)

    def parse_import(self):
        self.advance()  # "import"
        path = self.expect(TT.STRING).value
        self.skip_newlines()
        return Import(path)

    def parse(self):
        body = []
        self.skip_newlines()
        while not self.match(TT.EOF):
            body.append(self.parse_statement())
            self.skip_newlines()
        return Program(body)


# ══════════════════════════════════════════
#  СРЕДА ВЫПОЛНЕНИЯ (Environment / Scope)
# ══════════════════════════════════════════

class Environment:
    """Хранит переменные. Поддерживает вложенные области видимости."""
    def __init__(self, parent=None):
        self.vars   = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise CreamRuntimeError(f"Переменная '{name}' не определена")

    def set(self, name, value):
        self.vars[name] = value

    def assign(self, name, value):
        """Присваивает в ту область видимости где переменная уже есть."""
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            self.vars[name] = value


# ══════════════════════════════════════════
#  ТИПЫ CREAM
# ══════════════════════════════════════════

class CreamFunction:
    """Пользовательская функция (action)."""
    def __init__(self, name, params, body, closure):
        self.name    = name
        self.params  = params   # [(name, default_node), ...]
        self.body    = body
        self.closure = closure  # среда где была определена

    def __repr__(self):
        return f"<action {self.name}>"

class CreamStruct:
    """Экземпляр структуры."""
    def __init__(self, type_name, fields):
        self.type_name = type_name
        self.fields    = fields  # dict

    def __repr__(self):
        items = ", ".join(f"{k}={repr(v)}" for k, v in self.fields.items())
        return f"{self.type_name}({items})"

class CreamStructType:
    """Тип структуры (конструктор)."""
    def __init__(self, name, fields):
        self.name   = name
        self.fields = fields  # [(name, type, default_node), ...]

    def __repr__(self):
        return f"<struct {self.name}>"

class CreamLambda:
    """Лямбда-функция: x → expr."""
    def __init__(self, param, body, closure):
        self.param   = param
        self.body    = body
        self.closure = closure

    def __repr__(self):
        return f"<lambda {self.param}>"


# ══════════════════════════════════════════
#  СИГНАЛЫ УПРАВЛЕНИЯ ПОТОКОМ
# ══════════════════════════════════════════

class ReturnSignal(Exception):
    def __init__(self, value): self.value = value

class CreamRuntimeError(Exception):
    def __init__(self, msg): super().__init__(f"[Runtime Error] {msg}")


# ══════════════════════════════════════════
#  ИНТЕРПРЕТАТОР
# ══════════════════════════════════════════

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self._setup_builtins()

    # ── встроенные функции ──────────────────

    def _setup_builtins(self):
        import math as _math
        import os as _os
        import re as _re
        import json as _json
        import csv as _csv
        import random as _random
        import datetime as _datetime
        import hashlib as _hashlib
        import base64 as _base64
        import glob as _glob
        import shutil as _shutil
        import subprocess as _subprocess
        import time as _time_mod
        import statistics as _statistics

        env = self.global_env
        cs  = self._cream_str

        # ── базовые ──────────────────────────
        env.set("say",     lambda args: print(cs(args[0])) or None)
        env.set("input",   lambda args: input(cs(args[0]) if args else ""))
        env.set("length",  lambda args: len(args[0]))
        env.set("sum",     lambda args: sum(args[0]) if isinstance(args[0], list) else args[0])
        env.set("min",     lambda args: min(args[0]) if isinstance(args[0], list) else args[0])
        env.set("max",     lambda args: max(args[0]) if isinstance(args[0], list) else args[0])
        env.set("abs",     lambda args: abs(args[0]))
        env.set("round",   lambda args: round(args[0], int(args[1]) if len(args) > 1 else 0))
        env.set("number",  lambda args: float(args[0]) if '.' in str(args[0]) else int(float(str(args[0]))))
        env.set("bool",    lambda args: bool(args[0]))
        env.set("range",   lambda args: list(range(int(args[0]), int(args[1]))))
        env.set("sort",    lambda args: sorted(args[0]))
        env.set("reverse", lambda args: list(reversed(args[0])))
        env.set("first",   lambda args: args[0][0] if args[0] else None)
        env.set("last",    lambda args: args[0][-1] if args[0] else None)
        env.set("join",    lambda args: (cs(args[1]) if len(args) > 1 else ", ").join(cs(x) for x in args[0]))
        env.set("upper",   lambda args: str(args[0]).upper())
        env.set("lower",   lambda args: str(args[0]).lower())
        env.set("trim",    lambda args: str(args[0]).strip())
        env.set("split",   lambda args: str(args[0]).split(str(args[1]) if len(args) > 1 else " "))
        env.set("contains",lambda args: args[1] in args[0])

        # константы
        env.set("PI",  _math.pi)
        env.set("E",   _math.e)
        env.set("INF", _math.inf)

        # ══════════════════════════════════════
        #  math(x, op, ...)
        # ══════════════════════════════════════
        def cream_math(args):
            x = args[0]
            if len(args) == 1: return x
            op = args[1]
            if op == "sqrt":      return _math.sqrt(x)
            if op == "pow":       return _math.pow(x, args[2])
            if op == "log":       return _math.log(x, args[2]) if len(args) > 2 else _math.log(x)
            if op == "log2":      return _math.log2(x)
            if op == "log10":     return _math.log10(x)
            if op == "sin":       return _math.sin(_math.radians(x))
            if op == "cos":       return _math.cos(_math.radians(x))
            if op == "tan":       return _math.tan(_math.radians(x))
            if op == "asin":      return _math.degrees(_math.asin(x))
            if op == "acos":      return _math.degrees(_math.acos(x))
            if op == "atan":      return _math.degrees(_math.atan(x))
            if op == "floor":     return _math.floor(x)
            if op == "ceil":      return _math.ceil(x)
            if op == "round":     return round(x, int(args[2]) if len(args) > 2 else 0)
            if op == "abs":       return abs(x)
            if op == "factorial": return _math.factorial(int(x))
            if op == "gcd":       return _math.gcd(int(x), int(args[2]))
            if op == "lcm":
                a, b = int(x), int(args[2])
                return abs(a * b) // _math.gcd(a, b)
            if op == "prime":
                n = int(x)
                if n < 2: return False
                for i in range(2, int(_math.sqrt(n)) + 1):
                    if n % i == 0: return False
                return True
            if op == "digits":   return [int(d) for d in str(abs(int(x)))]
            if op == "binary":   return bin(int(x))[2:]
            if op == "hex":      return hex(int(x))[2:]
            if op == "octal":    return oct(int(x))[2:]
            if op == "clamp":    return max(args[2], min(args[3], x))
            if op == "sign":     return (1 if x > 0 else -1 if x < 0 else 0)
            if op == "percent":  return (x / args[2]) * 100 if len(args) > 2 else x / 100
            raise CreamRuntimeError(f"math: неизвестная операция '{op}'")
        env.set("math", cream_math)

        # ══════════════════════════════════════
        #  num(x, op, ...)
        # ══════════════════════════════════════
        def cream_num(args):
            x = args[0]
            if len(args) == 1:
                try: return int(x) if '.' not in str(x) else float(x)
                except: return 0
            op = args[1]
            if op == "int":      return int(float(x))
            if op == "float":    return float(x)
            if op == "is":
                try: float(x); return True
                except: return False
            if op == "between":  return args[2] <= x <= args[3]
            if op == "format":   return f"{x:.{int(args[2])}f}"
            if op == "positive": return x > 0
            if op == "negative": return x < 0
            if op == "zero":     return x == 0
            if op == "even":     return int(x) % 2 == 0
            if op == "odd":      return int(x) % 2 != 0
            raise CreamRuntimeError(f"num: неизвестная операция '{op}'")
        env.set("num", cream_num)

        # ══════════════════════════════════════
        #  rand(...)
        # ══════════════════════════════════════
        def cream_rand(args):
            if not args: return _random.random()
            if len(args) == 1:
                a = args[0]
                if isinstance(a, str):
                    if a == "uuid":
                        import uuid; return str(uuid.uuid4())
                    if a == "coin":  return _random.choice([True, False])
                    if a == "dice":  return _random.randint(1, 6)
                if isinstance(a, (int, float)): return _random.randint(0, int(a))
                if isinstance(a, list): return _random.choice(a)
            if len(args) == 2:
                op = args[0]
                if op == "list":    return _random.choice(args[1])
                if op == "shuffle": return _random.sample(args[1], len(args[1]))
                if op == "dice":    return _random.randint(1, int(args[1]))
                if isinstance(op, (int, float)): return _random.randint(int(op), int(args[1]))
            if len(args) == 3 and args[0] == "sample":
                return _random.sample(args[1], int(args[2]))
            return _random.random()
        env.set("rand", cream_rand)

        # ══════════════════════════════════════
        #  stats(list, op)
        # ══════════════════════════════════════
        def cream_stats(args):
            lst = args[0]
            if not lst: return None
            if len(args) == 1:
                return {
                    "mean":     _statistics.mean(lst),
                    "median":   _statistics.median(lst),
                    "std":      _statistics.stdev(lst) if len(lst) > 1 else 0,
                    "min":      min(lst), "max": max(lst),
                    "sum":      sum(lst), "count": len(lst),
                    "range":    max(lst) - min(lst),
                }
            op = args[1]
            if op == "mean":     return _statistics.mean(lst)
            if op == "median":   return _statistics.median(lst)
            if op == "mode":     return _statistics.mode(lst)
            if op == "std":      return _statistics.stdev(lst) if len(lst) > 1 else 0
            if op == "variance": return _statistics.variance(lst) if len(lst) > 1 else 0
            if op == "min":      return min(lst)
            if op == "max":      return max(lst)
            if op == "sum":      return sum(lst)
            if op == "count":    return len(lst)
            if op == "range":    return max(lst) - min(lst)
            if op == "unique":   return list(dict.fromkeys(lst))
            if op == "freq":
                freq = {}
                for x in lst: freq[x] = freq.get(x, 0) + 1
                return freq
            raise CreamRuntimeError(f"stats: неизвестная операция '{op}'")
        env.set("stats", cream_stats)

        # ══════════════════════════════════════
        #  list(lst, op, ...)
        # ══════════════════════════════════════
        def cream_list(args):
            lst = list(args[0])
            if len(args) == 1: return lst
            op = args[1]
            if op == "add":      lst.append(args[2]); return lst
            if op == "remove":
                if args[2] in lst: lst.remove(args[2])
                return lst
            if op == "pop":
                i = int(args[2]) if len(args) > 2 else -1
                lst.pop(i); return lst
            if op == "insert":   lst.insert(int(args[2]), args[3]); return lst
            if op == "has":      return args[2] in lst
            if op == "index":    return lst.index(args[2]) if args[2] in lst else -1
            if op == "count":    return lst.count(args[2])
            if op == "slice":
                a = int(args[2]); b = int(args[3]) if len(args) > 3 else len(lst)
                return lst[a:b]
            if op == "flat":
                result = []
                for item in lst:
                    if isinstance(item, list): result.extend(item)
                    else: result.append(item)
                return result
            if op == "zip":      return [[a, b] for a, b in zip(lst, args[2])]
            if op == "chunk":
                n = int(args[2])
                return [lst[i:i+n] for i in range(0, len(lst), n)]
            if op == "unique":   return list(dict.fromkeys(lst))
            if op == "concat":   return lst + list(args[2])
            if op == "reverse":  return list(reversed(lst))
            if op == "sort":     return sorted(lst)
            if op == "shuffle":  _random.shuffle(lst); return lst
            if op == "sum":      return sum(lst)
            if op == "min":      return min(lst)
            if op == "max":      return max(lst)
            if op == "first":    return lst[0] if lst else None
            if op == "last":     return lst[-1] if lst else None
            if op == "empty":    return len(lst) == 0
            if op == "fill":
                n = int(args[2]); val = args[3] if len(args) > 3 else 0
                return [val] * n
            raise CreamRuntimeError(f"list: неизвестная операция '{op}'")
        env.set("list", cream_list)

        # ══════════════════════════════════════
        #  table(t, op, ...)
        # ══════════════════════════════════════
        def cream_table(args):
            t = dict(args[0]) if isinstance(args[0], dict) else {}
            if len(args) == 1: return t
            op = args[1]
            if op == "get":      return t.get(args[2])
            if op == "set":      t[args[2]] = args[3]; return t
            if op == "has":      return args[2] in t
            if op == "delete":   t.pop(args[2], None); return t
            if op == "keys":     return list(t.keys())
            if op == "values":   return list(t.values())
            if op == "merge":    return {**t, **args[2]}
            if op == "size":     return len(t)
            if op == "empty":    return len(t) == 0
            if op == "to_list":  return [[k, v] for k, v in t.items()]
            raise CreamRuntimeError(f"table: неизвестная операция '{op}'")
        env.set("table", cream_table)

        # ══════════════════════════════════════
        #  convert(x, from, to)
        # ══════════════════════════════════════
        def cream_convert(args):
            x = float(args[0])
            if len(args) < 3: return x
            from_, to_ = str(args[1]).lower(), str(args[2]).lower()
            conv = {
                ("km","miles"): lambda v: v*0.621371,   ("miles","km"):  lambda v: v*1.60934,
                ("m","ft"):     lambda v: v*3.28084,     ("ft","m"):      lambda v: v/3.28084,
                ("kg","lbs"):   lambda v: v*2.20462,     ("lbs","kg"):    lambda v: v/2.20462,
                ("kg","g"):     lambda v: v*1000,        ("g","kg"):      lambda v: v/1000,
                ("c","f"):      lambda v: v*9/5+32,      ("f","c"):       lambda v: (v-32)*5/9,
                ("c","k"):      lambda v: v+273.15,      ("k","c"):       lambda v: v-273.15,
                ("bytes","kb"): lambda v: v/1024,        ("kb","mb"):     lambda v: v/1024,
                ("mb","gb"):    lambda v: v/1024,        ("bytes","mb"):  lambda v: v/(1024**2),
                ("bytes","gb"): lambda v: v/(1024**3),   ("deg","rad"):   lambda v: _math.radians(v),
                ("rad","deg"):  lambda v: _math.degrees(v),
                ("hours","min"):lambda v: v*60,          ("min","sec"):   lambda v: v*60,
                ("hours","sec"):lambda v: v*3600,
            }
            fn = conv.get((from_, to_))
            if fn: return round(fn(x), 6)
            raise CreamRuntimeError(f"convert: не знаю как {from_} → {to_}")
        env.set("convert", cream_convert)

        # ══════════════════════════════════════
        #  date(...)
        # ══════════════════════════════════════
        def cream_date(args):
            now = _datetime.datetime.now()
            if not args or args[0] == "now":
                return {"year": now.year, "month": now.month, "day": now.day,
                        "hour": now.hour, "minute": now.minute, "second": now.second}
            if args[0] == "timestamp": return int(now.timestamp())
            if args[0] == "today":     return now.strftime("%Y-%m-%d")
            if args[0] == "time":      return now.strftime("%H:%M:%S")
            if args[0] == "format":
                fmt = str(args[1]) if len(args) > 1 else "%Y-%m-%d"
                return now.strftime(fmt)
            return str(now)
        env.set("date", cream_date)

        # ══════════════════════════════════════
        #  file(path, op, ...)
        # ══════════════════════════════════════
        def cream_file(args):
            path = str(args[0])
            OPS = {"append","delete","exists","size","copy","move",
                   "rename","lines","json","csv","info","ext","name","dir"}
            if len(args) == 1:
                with open(path, 'r', encoding='utf-8') as f: return f.read()
            op = args[1]
            if not isinstance(op, str) or op not in OPS:
                with open(path, 'w', encoding='utf-8') as f: f.write(cs(op))
                return True
            if op == "append":
                with open(path, 'a', encoding='utf-8') as f: f.write(cs(args[2]))
                return True
            if op == "delete":
                if _os.path.exists(path): _os.remove(path)
                return True
            if op == "exists":  return _os.path.exists(path)
            if op == "size":    return _os.path.getsize(path) if _os.path.exists(path) else 0
            if op == "copy":    _shutil.copy2(path, str(args[2])); return True
            if op == "move":    _shutil.move(path, str(args[2])); return True
            if op == "rename":  _os.rename(path, str(args[2])); return True
            if op == "lines":
                with open(path, 'r', encoding='utf-8') as f:
                    return [l.rstrip('\n') for l in f.readlines()]
            if op == "json":
                if len(args) > 2:
                    with open(path, 'w', encoding='utf-8') as f:
                        _json.dump(args[2], f, ensure_ascii=False, indent=2)
                    return True
                with open(path, 'r', encoding='utf-8') as f: return _json.load(f)
            if op == "csv":
                if len(args) > 2:
                    with open(path, 'w', newline='', encoding='utf-8') as f:
                        writer = _csv.writer(f)
                        for row in args[2]: writer.writerow(row)
                    return True
                with open(path, 'r', encoding='utf-8') as f: return list(_csv.reader(f))
            if op == "ext":  return _os.path.splitext(path)[1]
            if op == "name": return _os.path.basename(path)
            if op == "dir":  return _os.path.dirname(path)
            if op == "info":
                stat = _os.stat(path)
                return {"size": stat.st_size, "name": _os.path.basename(path),
                        "ext": _os.path.splitext(path)[1], "dir": _os.path.dirname(path)}
            raise CreamRuntimeError(f"file: неизвестная операция '{op}'")
        env.set("file", cream_file)

        # ══════════════════════════════════════
        #  folder(path, op, ...)
        # ══════════════════════════════════════
        def cream_folder(args):
            path = str(args[0])
            if path == "current": return _os.getcwd()
            if path == "home":    return _os.path.expanduser("~")
            if len(args) == 1:
                return _os.listdir(path) if _os.path.isdir(path) else []
            op = args[1]
            if op == "create":  _os.makedirs(path, exist_ok=True); return True
            if op == "delete":  _shutil.rmtree(path, ignore_errors=True); return True
            if op == "exists":  return _os.path.isdir(path)
            if op == "copy":    _shutil.copytree(path, str(args[2])); return True
            if op == "move":    _shutil.move(path, str(args[2])); return True
            if op == "find":
                import glob as _glob
                return _glob.glob(_os.path.join(path, str(args[2])), recursive=True)
            if op == "files":
                return [f for f in _os.listdir(path)
                        if _os.path.isfile(_os.path.join(path, f))]
            if op == "folders":
                return [f for f in _os.listdir(path)
                        if _os.path.isdir(_os.path.join(path, f))]
            raise CreamRuntimeError(f"folder: неизвестная операция '{op}'")
        env.set("folder", cream_folder)

        # ══════════════════════════════════════
        #  sys_(op, ...)
        # ══════════════════════════════════════
        def cream_sys(args):
            import sys as _sys
            if not args: return _sys.platform
            op = str(args[0])
            if op == "os":       return _sys.platform
            if op == "args":     return _sys.argv[1:]
            if op == "exit":
                code = int(args[1]) if len(args) > 1 else 0
                _sys.exit(code)
            if op == "run":
                r = _subprocess.run(str(args[1]), shell=True, capture_output=True, text=True)
                return {"output": r.stdout, "error": r.stderr, "code": r.returncode}
            if op == "env":
                if len(args) > 2: _os.environ[str(args[1])] = str(args[2]); return True
                return _os.environ.get(str(args[1]), "")
            if op == "sleep":    _time_mod.sleep(float(args[1])); return None
            if op == "time":     return int(_time_mod.time())
            if op == "cwd":      return _os.getcwd()
            if op == "cd":       _os.chdir(str(args[1])); return True
            if op == "cpu":
                try: import multiprocessing; return multiprocessing.cpu_count()
                except: return 1
            raise CreamRuntimeError(f"sys: неизвестная операция '{op}'")
        env.set("sys_", cream_sys)
        env.set("sys",  cream_sys)

        # ══════════════════════════════════════
        #  encode(x, op, ...)
        # ══════════════════════════════════════
        def cream_encode(args):
            x = args[0]
            if len(args) < 2: return str(x)
            op   = str(args[1])
            mode = str(args[2]).lower() if len(args) > 2 else ""
            if op == "base64":
                if mode in ("de","decode"):
                    return _base64.b64decode(str(x)).decode('utf-8')
                return _base64.b64encode(str(x).encode()).decode()
            if op == "md5":    return _hashlib.md5(str(x).encode()).hexdigest()
            if op == "sha256": return _hashlib.sha256(str(x).encode()).hexdigest()
            if op == "sha1":   return _hashlib.sha1(str(x).encode()).hexdigest()
            if op == "url":
                from urllib.parse import quote, unquote
                if mode in ("de","decode"): return unquote(str(x))
                return quote(str(x))
            if op == "json":
                if mode in ("de","decode"): return _json.loads(str(x))
                return _json.dumps(x, ensure_ascii=False)
            if op == "hex":    return str(x).encode().hex()
            raise CreamRuntimeError(f"encode: неизвестная операция '{op}'")
        env.set("encode", cream_encode)

        # ══════════════════════════════════════
        #  str_(x, op, ...)
        # ══════════════════════════════════════
        def cream_str_fn(args):
            x = str(args[0])
            if len(args) == 1: return x
            op = str(args[1])
            if op == "upper":      return x.upper()
            if op == "lower":      return x.lower()
            if op == "title":      return x.title()
            if op == "capitalize": return x.capitalize()
            if op == "trim":
                if len(args) > 2:
                    s = str(args[2])
                    if s == "left":  return x.lstrip()
                    if s == "right": return x.rstrip()
                return x.strip()
            if op == "replace":    return x.replace(str(args[2]), str(args[3]) if len(args) > 3 else "")
            if op == "remove":     return x.replace(str(args[2]), "")
            if op == "split":
                sep = str(args[2]) if len(args) > 2 else " "
                return x.split(sep)
            if op == "join":       return x.join(cs(i) for i in args[2])
            if op == "contains":   return str(args[2]) in x
            if op == "starts":     return x.startswith(str(args[2]))
            if op == "ends":       return x.endswith(str(args[2]))
            if op == "count":      return x.count(str(args[2]))
            if op == "index":      return x.find(str(args[2]))
            if op == "slice":
                a = int(args[2]); b = int(args[3]) if len(args) > 3 else len(x)
                return x[a:b]
            if op == "repeat":     return x * int(args[2])
            if op == "reverse":    return x[::-1]
            if op == "length":     return len(x)
            if op == "words":      return x.split()
            if op == "lines":      return x.splitlines()
            if op == "chars":      return list(x)
            if op == "is_num":     return x.replace('.','',1).replace('-','',1).isdigit()
            if op == "is_alpha":   return x.isalpha()
            if op == "is_empty":   return len(x.strip()) == 0
            if op == "pad":
                n    = int(args[2])
                side = str(args[3]) if len(args) > 3 else "right"
                char = str(args[4]) if len(args) > 4 else " "
                if side == "left":  return x.rjust(n, char)
                if side == "both":  return x.center(n, char)
                return x.ljust(n, char)
            if op == "between":
                a, b = str(args[2]), str(args[3])
                start = x.find(a); end = x.find(b, start + len(a))
                if start == -1 or end == -1: return ""
                return x[start + len(a):end]
            if op == "match":      
                m = _re.search(str(args[2]), x)
                return m.group(0) if m else ""
            if op == "match_all":  return _re.findall(str(args[2]), x)
            raise CreamRuntimeError(f"str: неизвестная операция '{op}'")
        env.set("str_", cream_str_fn)
        env.set("str",  cream_str_fn)

        # ══════════════════════════════════════
        #  regex(pattern, text, op, ...)
        # ══════════════════════════════════════
        def cream_regex(args):
            pat = str(args[0]); text = str(args[1]) if len(args) > 1 else ""
            if len(args) == 2:
                m = _re.search(pat, text); return m.group(0) if m else ""
            op = str(args[2])
            if op == "all":     return _re.findall(pat, text)
            if op == "test":    return bool(_re.search(pat, text))
            if op == "replace":
                repl = str(args[3]) if len(args) > 3 else ""
                return _re.sub(pat, repl, text)
            if op == "split":   return _re.split(pat, text)
            if op == "groups":
                m = _re.search(pat, text)
                return list(m.groups()) if m else []
            if op == "count":   return len(_re.findall(pat, text))
            raise CreamRuntimeError(f"regex: неизвестная операция '{op}'")
        env.set("regex", cream_regex)

        # ══════════════════════════════════════
        #  text_(x, op, ...)
        # ══════════════════════════════════════
        def cream_text_fn(args):
            x = str(args[0])
            if len(args) == 1: return x
            op = str(args[1])
            if op == "clean":      return _re.sub(r'[^\w\s]', '', x)
            if op == "words":      return len(x.split())
            if op == "truncate":
                n = int(args[2]); suffix = str(args[3]) if len(args) > 3 else "..."
                return x[:n] + suffix if len(x) > n else x
            if op == "slug":
                s = _re.sub(r'[^\w\s-]', '', x.lower().strip())
                return _re.sub(r'[\s_-]+', '-', s).strip('-')
            if op == "palindrome":
                c = _re.sub(r'[^a-zA-Z0-9]', '', x.lower())
                return c == c[::-1]
            if op == "anagram":
                import re as re2
                a = sorted(re2.sub(r'\s', '', x.lower()))
                b = sorted(re2.sub(r'\s', '', str(args[2]).lower()))
                return a == b
            if op == "distance":
                a, b = x, str(args[2])
                dp = [[0]*(len(b)+1) for _ in range(len(a)+1)]
                for i in range(len(a)+1): dp[i][0] = i
                for j in range(len(b)+1): dp[0][j] = j
                for i in range(1, len(a)+1):
                    for j in range(1, len(b)+1):
                        cost = 0 if a[i-1]==b[j-1] else 1
                        dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
                return dp[len(a)][len(b)]
            if op == "similarity":
                a, b = x, str(args[2])
                if not a and not b: return 1.0
                if not a or not b:  return 0.0
                dp = [[0]*(len(b)+1) for _ in range(len(a)+1)]
                for i in range(len(a)+1): dp[i][0] = i
                for j in range(len(b)+1): dp[0][j] = j
                for i in range(1, len(a)+1):
                    for j in range(1, len(b)+1):
                        cost = 0 if a[i-1]==b[j-1] else 1
                        dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
                return round(1 - dp[len(a)][len(b)] / max(len(a), len(b)), 3)
            if op == "extract":
                what = str(args[2])
                if what == "emails":   return _re.findall(r'[\w.+-]+@[\w-]+\.[a-zA-Z]+', x)
                if what == "urls":     return _re.findall(r'https?://\S+', x)
                if what == "numbers":  return [float(n) if '.' in n else int(n)
                                               for n in _re.findall(r'-?\d+\.?\d*', x)]
                if what == "hashtags": return _re.findall(r'#\w+', x)
                if what == "mentions": return _re.findall(r'@\w+', x)
            raise CreamRuntimeError(f"text: неизвестная операция '{op}'")
        env.set("text_", cream_text_fn)

        # ══════════════════════════════════════
        #  print_(x, op, ...)  — цветной вывод
        # ══════════════════════════════════════
        COLORS = {
            "red":"\033[91m","green":"\033[92m","yellow":"\033[93m",
            "blue":"\033[94m","cyan":"\033[96m","white":"\033[97m",
            "gray":"\033[90m","reset":"\033[0m","bold":"\033[1m",
        }
        def cream_print(args):
            x = args[0] if args else ""
            if x == "line":
                n = int(args[1]) if len(args) > 1 else 40
                ch = str(args[2]) if len(args) > 2 else "─"
                print(ch * n); return None
            if x == "clear": print("\033[H\033[J", end=""); return None
            if len(args) == 1: print(cs(x)); return None
            op = str(args[1])
            if op == "color":
                c = COLORS.get(str(args[2]), "")
                print(f"{c}{cs(x)}{COLORS['reset']}")
            elif op == "bold":  print(f"\033[1m{cs(x)}\033[0m")
            elif op == "end":   print(cs(x), end=str(args[2]))
            else: print(cs(x))
            return None
        env.set("print_", cream_print)

        # ══════════════════════════════════════
        #  net(url, op, ...)
        # ══════════════════════════════════════
        def cream_net(args):
            from urllib import request as _req, parse as _parse, error as _uerr
            import json as _j
            if not args:
                raise CreamRuntimeError("net: нужен URL")
            url = str(args[0])

            if url == "ip":
                try:
                    with _req.urlopen("https://api.ipify.org", timeout=5) as r:
                        return r.read().decode()
                except: return "unknown"

            if url == "encode":
                params = args[1] if len(args) > 1 else {}
                if isinstance(params, dict): return _parse.urlencode(params)
                return _parse.quote(str(params))

            op = str(args[1]) if len(args) > 1 else "get"

            def do_request(method, data=None, headers=None, as_json=False):
                if data is not None:
                    if isinstance(data, dict):
                        if as_json:
                            body = _j.dumps(data).encode(); ct = "application/json"
                        else:
                            body = _parse.urlencode(data).encode(); ct = "application/x-www-form-urlencoded"
                    else:
                        body = str(data).encode(); ct = "text/plain"
                else:
                    body = None; ct = None
                req = _req.Request(url, data=body, method=method.upper())
                if ct: req.add_header("Content-Type", ct)
                req.add_header("User-Agent", "CreamLang/0.1")
                if headers and isinstance(headers, dict):
                    for k, v in headers.items(): req.add_header(str(k), str(v))
                try:
                    with _req.urlopen(req, timeout=10) as resp:
                        return resp.read().decode("utf-8", errors="replace")
                except _uerr.HTTPError as e:
                    raise CreamRuntimeError(f"net: HTTP {e.code} — {e.reason}")
                except _uerr.URLError as e:
                    raise CreamRuntimeError(f"net: ошибка — {e.reason}")

            if op == "get":     return do_request("GET")
            if op == "json":
                text = do_request("GET")
                try: return _j.loads(text)
                except: return text
            if op == "post":
                data = args[2] if len(args) > 2 else {}
                return do_request("POST", data=data)
            if op == "post_json":
                data = args[2] if len(args) > 2 else {}
                return do_request("POST", data=data, as_json=True)
            if op == "put":
                data = args[2] if len(args) > 2 else {}
                return do_request("PUT", data=data)
            if op == "delete":  return do_request("DELETE")
            if op == "head":
                req = _req.Request(url, method="HEAD")
                req.add_header("User-Agent", "CreamLang/0.1")
                try:
                    with _req.urlopen(req, timeout=10) as resp: return dict(resp.headers)
                except _uerr.HTTPError as e: raise CreamRuntimeError(f"net: HTTP {e.code}")
                except _uerr.URLError as e:  raise CreamRuntimeError(f"net: {e.reason}")
            if op == "status":
                req = _req.Request(url)
                req.add_header("User-Agent", "CreamLang/0.1")
                try:
                    with _req.urlopen(req, timeout=10) as resp: return resp.status
                except _uerr.HTTPError as e: return e.code
                except: return 0
            if op == "download":
                path = str(args[2]) if len(args) > 2 else "download"
                try: _req.urlretrieve(url, path); return True
                except Exception as e: raise CreamRuntimeError(f"net: {e}")
            if op == "headers":
                hdrs = args[2] if len(args) > 2 else {}
                return do_request("GET", headers=hdrs)
            raise CreamRuntimeError(f"net: неизвестная операция '{op}'")
        env.set("net", cream_net)

    def _cream_str(self, value):
        """Преобразует значение Cream в строку."""
        if value is None:       return "empty"
        if value is True:       return "yes"
        if value is False:      return "no"
        if isinstance(value, list):
            return "[" + ", ".join(self._cream_str(x) for x in value) + "]"
        if isinstance(value, dict):
            items = ", ".join(f"{k}: {self._cream_str(v)}" for k, v in value.items())
            return "{" + items + "}"
        if isinstance(value, float) and value == int(value):
            return str(int(value))
        return str(value)

    def _interpolate(self, s, env):
        """Интерполяция строк: "Hello, {name}" → "Hello, Ivan"."""
        def replace(m):
            var_name = m.group(1)
            try:    return self._cream_str(env.get(var_name))
            except: return m.group(0)
        return re.sub(r'\{(\w+)\}', replace, s)

    # ── выполнение блока ───────────────────

    def exec_block(self, stmts, env):
        for stmt in stmts:
            self.exec_stmt(stmt, env)

    # ── выполнение инструкции ──────────────

    def exec_stmt(self, node, env):

        if isinstance(node, Assign):
            value = self.eval_expr(node.value, env)
            env.set(node.name, value)

        elif isinstance(node, Say):
            value = self.eval_expr(node.value, env)
            print(self._cream_str(value))

        elif isinstance(node, Return):
            value = self.eval_expr(node.value, env)
            raise ReturnSignal(value)

        elif isinstance(node, If):
            if self.eval_expr(node.condition, env):
                local = Environment(env)
                self.exec_block(node.then_body, local)
            else:
                executed = False
                for cond, body in node.elseif_clauses:
                    if self.eval_expr(cond, env):
                        local = Environment(env)
                        self.exec_block(body, local)
                        executed = True
                        break
                if not executed and node.else_body:
                    local = Environment(env)
                    self.exec_block(node.else_body, local)

        elif isinstance(node, Repeat):
            count = self.eval_expr(node.count, env)
            for _ in range(int(count)):
                local = Environment(env)
                self.exec_block(node.body, local)

        elif isinstance(node, ForEach):
            iterable = self.eval_expr(node.iterable, env)
            for item in iterable:
                local = Environment(env)
                local.set(node.var, item)
                self.exec_block(node.body, local)

        elif isinstance(node, While):
            while self.eval_expr(node.condition, env):
                local = Environment(env)
                self.exec_block(node.body, local)

        elif isinstance(node, ActionDef):
            fn = CreamFunction(node.name, node.params, node.body, env)
            env.set(node.name, fn)

        elif isinstance(node, TaskDef):
            # task = action (async пока не реализован)
            fn = CreamFunction(node.name, node.params, node.body, env)
            env.set(node.name, fn)

        elif isinstance(node, StructDef):
            stype = CreamStructType(node.name, node.fields)
            env.set(node.name, stype)

        elif isinstance(node, TryCatch):
            try:
                local = Environment(env)
                self.exec_block(node.try_body, local)
            except CreamRuntimeError as e:
                local = Environment(env)
                local.set(node.error_var, {"message": str(e)})
                self.exec_block(node.catch_body, local)

        elif isinstance(node, Wait):
            # без async — просто вычисляем
            self.eval_expr(node.value, env)

        elif isinstance(node, Import):
            self._exec_import(node.path, env)

        else:
            # выражение как инструкция (например, вызов функции)
            self.eval_expr(node, env)

    # ── вычисление выражения ───────────────

    def eval_expr(self, node, env):

        if isinstance(node, NumberLiteral): return node.value
        if isinstance(node, BoolLiteral):   return node.value
        if isinstance(node, EmptyLiteral):  return None

        if isinstance(node, StringLiteral):
            return self._interpolate(node.value, env)

        if isinstance(node, Identifier):
            return env.get(node.name)

        if isinstance(node, ListLiteral):
            return [self.eval_expr(e, env) for e in node.elements]

        if isinstance(node, TableLiteral):
            return {k: self.eval_expr(v, env) for k, v in node.pairs}

        if isinstance(node, Lambda):
            return CreamLambda(node.param, node.body, env)

        if isinstance(node, UnaryOp):
            val = self.eval_expr(node.operand, env)
            if node.op == "not": return not val
            if node.op == "-":   return -val

        if isinstance(node, BinaryOp):
            return self.eval_binary(node, env)

        if isinstance(node, FieldAccess):
            obj = self.eval_expr(node.obj, env)
            if isinstance(obj, CreamStruct):
                if node.field in obj.fields:
                    return obj.fields[node.field]
                raise CreamRuntimeError(f"Поле '{node.field}' не найдено в {obj.type_name}")
            if isinstance(obj, dict):
                return obj.get(node.field)
            raise CreamRuntimeError(f"Нельзя получить поле у {type(obj).__name__}")

        if isinstance(node, IndexAccess):
            obj   = self.eval_expr(node.obj, env)
            index = self.eval_expr(node.index, env)
            try:
                return obj[int(index)]
            except (IndexError, KeyError, TypeError) as e:
                raise CreamRuntimeError(f"Ошибка индекса: {e}")

        if isinstance(node, Call):
            return self.eval_call(node, env)

        if isinstance(node, Pipeline):
            return self.eval_pipeline(node, env)

        if isinstance(node, Wait):
            return self.eval_expr(node.value, env)

        raise CreamRuntimeError(f"Неизвестный узел: {type(node).__name__}")

    # ── бинарные операции ──────────────────

    def eval_binary(self, node, env):
        left  = self.eval_expr(node.left,  env)
        right = self.eval_expr(node.right, env)
        op    = node.op

        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return self._cream_str(left) + self._cream_str(right)
            return left + right
        if op == "-":   return left - right
        if op == "*":   return left * right
        if op == "/":
            if right == 0: raise CreamRuntimeError("Деление на ноль")
            return left / right
        if op == "%":   return left % right
        if op == "==":  return left == right
        if op == "!=":  return left != right
        if op == ">":   return left > right
        if op == "<":   return left < right
        if op == ">=":  return left >= right
        if op == "<=":  return left <= right
        if op == "and": return left and right
        if op == "or":  return left or right

        raise CreamRuntimeError(f"Неизвестный оператор: {op}")

    # ── вызов функции ──────────────────────

    def eval_call(self, node, env):
        callee = self.eval_expr(node.callee, env)
        args   = [self.eval_expr(a, env) for a in node.args]

        # встроенная функция (lambda Python)
        if callable(callee) and not isinstance(callee, (CreamFunction, CreamLambda, CreamStructType)):
            return callee(args)

        # пользовательская функция (action)
        if isinstance(callee, CreamFunction):
            local = Environment(callee.closure)
            for i, (param_name, param_default) in enumerate(callee.params):
                if i < len(args):
                    local.set(param_name, args[i])
                elif param_default is not None:
                    local.set(param_name, self.eval_expr(param_default, env))
                else:
                    raise CreamRuntimeError(f"Не передан аргумент '{param_name}'")
            try:
                self.exec_block(callee.body, local)
                return None
            except ReturnSignal as r:
                return r.value

        # лямбда
        if isinstance(callee, CreamLambda):
            local = Environment(callee.closure)
            local.set(callee.param, args[0] if args else None)
            return self.eval_expr(callee.body, local)

        # конструктор структуры
        if isinstance(callee, CreamStructType):
            fields = {}
            for i, (fname, ftype, fdefault) in enumerate(callee.fields):
                if i < len(args):
                    fields[fname] = args[i]
                elif fdefault is not None:
                    fields[fname] = self.eval_expr(fdefault, env)
                else:
                    raise CreamRuntimeError(f"Не передано поле '{fname}'")
            return CreamStruct(callee.name, fields)

        raise CreamRuntimeError(f"'{callee}' не является функцией")

    # ── pipeline ───────────────────────────

    def eval_pipeline(self, node, env):
        value = self.eval_expr(node.value, env)

        for step in node.steps:
            # | sum, | sort, | reverse — без аргументов
            if isinstance(step, Identifier):
                name = step.name
                if name == "sum":     value = sum(value)
                elif name == "sort":  value = sorted(value)
                elif name == "reverse": value = list(reversed(value))
                elif name == "first": value = value[0] if value else None
                elif name == "last":  value = value[-1] if value else None
                elif name == "length": value = len(value)
                else:
                    fn = env.get(name)
                    value = self._apply_fn(fn, value, env)

            # | filter(fn), | map(fn), | sort(fn)
            elif isinstance(step, Call):
                fn_name = step.callee.name if isinstance(step.callee, Identifier) else None
                fn_args = [self.eval_expr(a, env) for a in step.args]
                fn      = fn_args[0] if fn_args else None

                if fn_name == "filter":
                    value = [x for x in value if self._apply_fn(fn, x, env)]
                elif fn_name == "map":
                    value = [self._apply_fn(fn, x, env) for x in value]
                elif fn_name == "sort":
                    value = sorted(value, key=lambda x: self._apply_fn(fn, x, env))
                elif fn_name == "reduce":
                    from functools import reduce
                    value = reduce(lambda a, b: self._apply_fn2(fn, a, b, env), value)
                else:
                    callee = self.eval_expr(step.callee, env)
                    value  = self._apply_fn(callee, value, env)
            else:
                step_val = self.eval_expr(step, env)
                value = self._apply_fn(step_val, value, env)

        return value

    def _apply_fn(self, fn, value, env):
        """Применяет функцию к одному значению."""
        if isinstance(fn, CreamLambda):
            local = Environment(fn.closure)
            local.set(fn.param, value)
            return self.eval_expr(fn.body, local)
        if isinstance(fn, CreamFunction):
            local = Environment(fn.closure)
            local.set(fn.params[0][0], value)
            try:
                self.exec_block(fn.body, local)
                return None
            except ReturnSignal as r:
                return r.value
        if callable(fn):
            return fn([value])
        raise CreamRuntimeError(f"Не является функцией: {fn}")

    def _apply_fn2(self, fn, a, b, env):
        """Применяет функцию к двум значениям (для reduce)."""
        if isinstance(fn, CreamLambda):
            # reduce-лямбда должна принимать два аргумента — упрощаем
            local = Environment(fn.closure)
            local.set(fn.param, a)
            return self.eval_expr(fn.body, local)
        raise CreamRuntimeError("reduce требует лямбду")

    # ── запуск программы ───────────────────

    def _exec_import(self, path, env):
        """
        import "file.cream"
        import "utils/helpers.cream"

        Загружает и выполняет внешний .cream файл.
        Все его переменные и функции становятся доступны
        в текущей области видимости.
        """
        import os as _os

        # Если путь относительный — ищем рядом с текущим файлом
        if not _os.path.isabs(path):
            # Пробуем рядом с запускаемым файлом
            base = getattr(self, '_base_dir', _os.getcwd())
            full_path = _os.path.join(base, path)
        else:
            full_path = path

        # Добавляем расширение если не указано
        if not full_path.endswith('.cream'):
            full_path += '.cream'

        if not _os.path.exists(full_path):
            raise CreamRuntimeError(f"import: файл не найден — '{full_path}'")

        # Защита от циклических импортов
        if not hasattr(self, '_imported'):
            self._imported = set()

        if full_path in self._imported:
            return  # уже импортировали — пропускаем
        self._imported.add(full_path)

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception as e:
            raise CreamRuntimeError(f"import: не удалось прочитать '{full_path}' — {e}")

        # Выполняем в текущей среде — всё становится доступно
        tokens = Lexer(source).tokenize()
        ast    = Parser(tokens).parse()
        self.exec_block(ast.body, env)

    def run(self, source, base_dir=None):
        import os as _os
        self._base_dir = base_dir or _os.getcwd()
        tokens = Lexer(source).tokenize()
        ast    = Parser(tokens).parse()
        self.exec_block(ast.body, self.global_env)


# ══════════════════════════════════════════
#  ЗАПУСК ФАЙЛА / REPL
# ══════════════════════════════════════════

def run_file(path):
    try:
        import os as _os
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
        interp = Interpreter()
        interp.run(source, base_dir=_os.path.dirname(_os.path.abspath(path)))
    except FileNotFoundError:
        print(f"❌ Файл не найден: {path}")
    except (LexerError, ParseError, CreamRuntimeError) as e:
        print(f"❌ {e}")

def repl():
    print("=" * 45)
    print("  Cream Language v0.1")
    print("  Type Cream code and press Enter.")
    print("  Type \'exit\' to quit.")
    print("=" * 45)
    print()
    interp = Interpreter()
    # Многострочный режим — если строка заканчивается на отступ
    buffer = []
    while True:
        try:
            prompt = "... " if buffer else "cream> "
            line = input(prompt)

            # выход
            if line.strip() in ("exit", "quit", "q"):
                print("Goodbye!")
                break

            # пустая строка — выполнить буфер если есть
            if not line.strip():
                if buffer:
                    code = "\n".join(buffer)
                    buffer = []
                    try:
                        interp.run(code)
                    except (LexerError, ParseError, CreamRuntimeError) as e:
                        print(f"❌ {e}")
                continue

            # если строка начинает блок (if/action/repeat и т.д.) — буферизуем
            stripped = line.strip()
            keywords_with_block = ("if ", "else", "or if", "action ", "task ",
                                   "repeat ", "while ", "for each", "try", "struct ")
            starts_block = any(stripped.startswith(kw) for kw in keywords_with_block)

            if starts_block or buffer:
                buffer.append(line)
            else:
                # однострочная команда — выполнить сразу
                try:
                    interp.run(line)
                except (LexerError, ParseError, CreamRuntimeError) as e:
                    print(f"❌ {e}")

        except (LexerError, ParseError, CreamRuntimeError) as e:
            print(f"❌ {e}")
            buffer = []
        except KeyboardInterrupt:
            if buffer:
                buffer = []
                print("\n(cancelled)")
            else:
                print("\nGoodbye!")
                break
        except EOFError:
            print("\nGoodbye!")
            break


# ══════════════════════════════════════════
#  ТЕСТ
# ══════════════════════════════════════════



import sys
import os
import re
import subprocess

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSplitter,
    QVBoxLayout, QHBoxLayout, QTextEdit, QPlainTextEdit,
    QToolBar, QStatusBar, QLabel, QPushButton,
    QFileDialog, QMessageBox, QFrame, QSizePolicy,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QRect, QSize
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QSyntaxHighlighter,
    QTextCharFormat, QTextCursor, QPainter, QAction,
    QKeySequence, QIcon, QPixmap,
)

# ══════════════════════════════════════════
#  ЦВЕТА
# ══════════════════════════════════════════

C = {
    "bg":      "#0F0F17",
    "bg2":     "#16161F",
    "bg3":     "#1E1E2E",
    "border":  "#2A2A3E",
    "text":    "#CDD6F4",
    "dim":     "#6C7086",
    "accent":  "#C17D3C",
    "accent2": "#FFB347",
    "green":   "#A6E3A1",
    "red":     "#F38BA8",
    "blue":    "#89B4FA",
    "purple":  "#CBA6F7",
    "yellow":  "#F9E2AF",
    "cyan":    "#89DCEB",
    "select":  "#313244",
    "line_bg": "#13131C",
}

# ══════════════════════════════════════════
#  ПОДСВЕТКА СИНТАКСИСА
# ══════════════════════════════════════════

class CreamHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        def rule(pattern, color, bold=False, italic=False):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))
            if bold:   fmt.setFontWeight(700)
            if italic: fmt.setFontItalic(True)
            self.rules.append((re.compile(pattern), fmt))

        rule(r'--[^\n]*',          C["dim"],    italic=True)
        rule(r'"[^"]*"',           C["green"])
        rule(r'\b(if|else|or if|for each|in|repeat|while|action|task|return|wait|together|try|on error|struct|import|say)\b', C["purple"], bold=True)
        rule(r'\b(yes|no|empty|PI|E|INF)\b', C["yellow"])
        rule(r'\b(math|num|rand|stats|convert|str_|text_|regex|list|table|file|folder|sys_|encode|net|date|print_|length|sum|min|max|abs|round|range|sort|reverse|first|last|join|split|upper|lower|trim|contains|number|bool|input)\b(?=\s*\()', C["cyan"])
        rule(r'\b-?\d+\.?\d*\b',   C["yellow"])
        rule(r'(→|->)',            C["accent"], bold=True)
        rule(r'\|',                C["accent"])
        rule(r'\{[^}]+\}',         C["accent2"])
        rule(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=\()', C["blue"])

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)

# ══════════════════════════════════════════
#  НУМЕРАЦИЯ СТРОК
# ══════════════════════════════════════════

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_width(), 0)

    def paintEvent(self, event):
        self.editor.paint_line_numbers(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_width(0)

    def line_number_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 16 + self.fontMetrics().horizontalAdvance('9') * digits

    def update_line_number_width(self, _=0):
        self.setViewportMargins(self.line_number_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_width(), cr.height()))

    def paint_line_numbers(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(C["line_bg"]))
        block = self.firstVisibleBlock()
        block_num = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QColor(C["dim"]))
                painter.setFont(self.font())
                painter.drawText(
                    0, top, self.line_number_area.width() - 6,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    str(block_num + 1)
                )
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_num += 1

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            self.textCursor().insertText("    ")
            return
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            line = self.textCursor().block().text()
            indent = " " * (len(line) - len(line.lstrip()))
            starters = ("if ","else","or if","for each","repeat ","while ","action ","task ","try","on error","struct ")
            if any(line.strip().startswith(k) for k in starters):
                indent += "    "
            super().keyPressEvent(event)
            self.textCursor().insertText(indent)
            return
        super().keyPressEvent(event)


# ══════════════════════════════════════════
#  ВСТРОЕННЫЙ ЗАПУСК CREAM
# ══════════════════════════════════════════


# ══════════════════════════════════════════
#  ОКНО ВЫВОДА (как в IDLE)
# ══════════════════════════════════════════

class RunOutputWindow(QWidget):
    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Cream — {filename}")
        self.resize(600, 400)
        self.setMinimumSize(400, 300)
        self.setStyleSheet(f"""
            QWidget {{
                background: {C['bg2']};
                color: {C['text']};
            }}
        """)

        # Иконка
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cream.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Заголовок
        header = QWidget()
        header.setFixedHeight(32)
        header.setStyleSheet(f"background: {C['bg3']}; border-bottom: 1px solid {C['border']};")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(12, 0, 8, 0)

        title = QLabel(f"▶  Running: {filename}")
        title.setStyleSheet(f"color: {C['dim']}; font-family: Consolas; font-size: 10px;")
        hl.addWidget(title)
        hl.addStretch()

        self.close_btn = QPushButton("✕ Close")
        self.close_btn.setFixedHeight(22)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C['dim']};
                border: none; font-family: Consolas; font-size: 10px; padding: 0 8px;
            }}
            QPushButton:hover {{ color: {C['red']}; }}
        """)
        self.close_btn.clicked.connect(self.close)
        hl.addWidget(self.close_btn)
        layout.addWidget(header)

        # Вывод
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 12))
        self.output.setStyleSheet(f"""
            QTextEdit {{
                background: {C['bg2']}; color: {C['text']};
                border: none; padding: 12px;
            }}
        """)
        layout.addWidget(self.output)

        # Статус снизу
        self.status_bar = QLabel("  Running...")
        self.status_bar.setFixedHeight(24)
        self.status_bar.setStyleSheet(f"""
            background: {C['bg3']}; color: {C['dim']};
            font-family: Consolas; font-size: 10px;
            border-top: 1px solid {C['border']};
            padding-left: 8px;
        """)
        layout.addWidget(self.status_bar)

    def append(self, text, tag="output"):
        colors = {
            "output":  C["text"],
            "error":   C["red"],
            "success": C["green"],
            "info":    C["dim"],
        }
        self.output.setTextColor(QColor(colors.get(tag, C["text"])))
        self.output.insertPlainText(text)
        self.output.ensureCursorVisible()

    def set_status(self, text, color=None):
        self.status_bar.setText(f"  {text}")
        if color:
            self.status_bar.setStyleSheet(f"""
                background: {C['bg3']}; color: {color};
                font-family: Consolas; font-size: 10px;
                border-top: 1px solid {C['border']};
                padding-left: 8px;
            """)

class BuiltinRunThread(QThread):
    output   = pyqtSignal(str, str)
    finished = pyqtSignal(int)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        import io
        import contextlib

        # Перехватываем print
        output_buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(output_buf):
                interp = Interpreter()
                with open(self.path, 'r', encoding='utf-8') as f:
                    source = f.read()
                interp.run(source)
            result = output_buf.getvalue()
            if result:
                self.output.emit(result, "output")
            self.finished.emit(0)
        except (LexerError, ParseError, CreamRuntimeError) as e:
            result = output_buf.getvalue()
            if result:
                self.output.emit(result, "output")
            self.output.emit(f"❌ {e}\n", "error")
            self.finished.emit(1)
        except Exception as e:
            result = output_buf.getvalue()
            if result:
                self.output.emit(result, "output")
            self.output.emit(f"❌ Unexpected error: {e}\n", "error")
            self.finished.emit(1)

    def stop(self):
        self.terminate()

# ══════════════════════════════════════════
#  ПОТОК ЗАПУСКА (внешний процесс, не используется)
# ══════════════════════════════════════════

class RunThread(QThread):
    output   = pyqtSignal(str, str)
    finished = pyqtSignal(int)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        self.process = None

    def run(self):
        try:
            self.process = subprocess.Popen(
                self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8", errors="replace",
            )
            stdout, stderr = self.process.communicate(timeout=30)
            if stdout: self.output.emit(stdout, "output")
            if stderr: self.output.emit(stderr, "error")
            self.finished.emit(self.process.returncode)
        except subprocess.TimeoutExpired:
            if self.process: self.process.kill()
            self.output.emit("\n⏱ Timeout!\n", "error")
            self.finished.emit(-1)
        except Exception as e:
            self.output.emit(f"\n❌ {e}\n", "error")
            self.finished.emit(-1)

    def stop(self):
        if self.process: self.process.kill()


# ══════════════════════════════════════════
#  СПЛЭШ-СКРИН
# ══════════════════════════════════════════

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SplashScreen
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(380, 420)

        # Центрировать на экране
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width()  - self.width())  // 2,
            (screen.height() - self.height()) // 2,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Фон
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {C['bg']};
                border-radius: 16px;
                border: 1px solid {C['border']};
            }}
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 50, 40, 40)
        container_layout.setSpacing(0)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Логотип
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cream.ico")
        if os.path.exists(icon_path):
            from PyQt6.QtGui import QPixmap
            pixmap = QPixmap(icon_path).scaled(
                160, 160,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(pixmap)
        else:
            self.logo_label.setText("🍦")
            self.logo_label.setStyleSheet("font-size: 80px;")
        container_layout.addWidget(self.logo_label)

        container_layout.addSpacing(28)

        # Название
        name_label = QLabel("Cream")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet(f"""
            color: {C['text']};
            font-family: Georgia, serif;
            font-size: 42px;
            font-weight: bold;
            font-style: italic;
            background: transparent;
            border: none;
        """)
        container_layout.addWidget(name_label)

        container_layout.addSpacing(6)

        # Подпись
        sub_label = QLabel("Programming Language IDE")
        sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_label.setStyleSheet(f"""
            color: {C['dim']};
            font-family: Consolas;
            font-size: 12px;
            letter-spacing: 2px;
            background: transparent;
            border: none;
        """)
        container_layout.addWidget(sub_label)

        container_layout.addSpacing(36)

        # Полоска загрузки
        self.progress_bar = QWidget()
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet(f"background: {C['border']}; border-radius: 2px; border: none;")
        container_layout.addWidget(self.progress_bar)

        self.progress_fill = QWidget(self.progress_bar)
        self.progress_fill.setFixedHeight(3)
        self.progress_fill.setStyleSheet(f"background: {C['accent']}; border-radius: 2px; border: none;")
        self.progress_fill.setFixedWidth(0)

        container_layout.addSpacing(12)

        # Версия
        ver_label = QLabel("v0.1  ©  Mauya Apps")
        ver_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ver_label.setStyleSheet(f"""
            color: {C['dim']};
            font-family: Consolas;
            font-size: 10px;
            background: transparent;
            border: none;
        """)
        container_layout.addWidget(ver_label)

        layout.addWidget(container)

        # Анимация прогресса
        self._progress = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self._animate)
        self._timer.start(18)

    def _animate(self):
        self._progress += 1
        bar_width = int((self.progress_bar.width() * self._progress) / 100)
        self.progress_fill.setFixedWidth(bar_width)
        if self._progress >= 100:
            self._timer.stop()

    def resizeEvent(self, event):
        super().resizeEvent(event)


# ══════════════════════════════════════════
#  ГЛАВНОЕ ОКНО
# ══════════════════════════════════════════

class CreamIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.modified     = False
        self.run_thread   = None
        self.cream_path   = self._find_cream()

        self.setWindowTitle("Cream IDE v0.1")
        self.resize(1200, 750)
        self._apply_theme()
        self._build_ui()
        self._build_menu()
        self._load_welcome()

    def _find_cream(self):
        return "builtin"  # интерпретатор встроен

    def _apply_theme(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ background:{C['bg']}; color:{C['text']}; }}
            QSplitter::handle {{ background:{C['border']}; }}
            QMenuBar {{ background:{C['bg2']}; color:{C['text']}; border-bottom:1px solid {C['border']}; padding:2px; }}
            QMenuBar::item:selected {{ background:{C['accent']}; color:{C['bg']}; border-radius:3px; }}
            QMenu {{ background:{C['bg3']}; color:{C['text']}; border:1px solid {C['border']}; }}
            QMenu::item:selected {{ background:{C['accent']}; color:{C['bg']}; }}
            QToolBar {{ background:{C['bg2']}; border-bottom:1px solid {C['border']}; spacing:4px; padding:4px 8px; }}
            QStatusBar {{ background:{C['bg3']}; color:{C['dim']}; font-family:Consolas; font-size:11px; border-top:1px solid {C['border']}; }}
            QPushButton {{ background:{C['bg3']}; color:{C['text']}; border:1px solid {C['border']}; border-radius:4px; padding:5px 14px; font-family:Consolas; font-size:11px; }}
            QPushButton:hover {{ background:{C['border']}; border-color:{C['accent']}; }}
            QPushButton#run_btn {{ background:{C['accent']}; color:{C['bg']}; border:none; font-weight:bold; }}
            QPushButton#run_btn:hover {{ background:{C['accent2']}; }}
            QPushButton#run_btn:disabled {{ background:{C['border']}; color:{C['dim']}; }}
            QScrollBar:vertical {{ background:{C['bg']}; width:10px; border:none; }}
            QScrollBar::handle:vertical {{ background:{C['border']}; border-radius:5px; min-height:20px; }}
            QScrollBar::handle:vertical:hover {{ background:{C['dim']}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}
            QScrollBar:horizontal {{ background:{C['bg']}; height:10px; border:none; }}
            QScrollBar::handle:horizontal {{ background:{C['border']}; border-radius:5px; }}
        """)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Тулбар
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        def tb_btn(text, slot, obj_name=None, shortcut=None):
            btn = QPushButton(text)
            if obj_name:  btn.setObjectName(obj_name)
            if shortcut:  btn.setShortcut(QKeySequence(shortcut))
            btn.clicked.connect(slot)
            toolbar.addWidget(btn)
            return btn

        tb_btn("⬜  New",  self._new_file,  shortcut="Ctrl+N")
        tb_btn("📂  Open", self._open_file, shortcut="Ctrl+O")
        tb_btn("💾  Save", self._save_file, shortcut="Ctrl+S")

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet(f"color:{C['border']}; margin:4px 6px;")
        toolbar.addWidget(sep)

        self.run_btn  = tb_btn("▶   Run",  self._run,  obj_name="run_btn", shortcut="F5")
        self.stop_btn = tb_btn("■   Stop", self._stop, shortcut="F6")

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        self.toolbar_status = QLabel("Ready")
        self.toolbar_status.setStyleSheet(f"color:{C['dim']}; font-family:Consolas; font-size:11px; padding-right:16px;")
        toolbar.addWidget(self.toolbar_status)

        # Сплиттер
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(4)
        layout.addWidget(splitter)

        # Редактор
        self.editor = CodeEditor()
        self.editor.setFont(QFont("Consolas", 12))
        self.editor.setStyleSheet(f"""
            QPlainTextEdit {{
                background:{C['bg']}; color:{C['text']};
                border:none; padding:8px;
                selection-background-color:{C['select']};
            }}
        """)
        self.highlighter = CreamHighlighter(self.editor.document())
        self.editor.document().contentsChanged.connect(self._on_modified)
        self.editor.cursorPositionChanged.connect(self._update_cursor_pos)
        splitter.addWidget(self.editor)

        # Консоль
        console_widget = QWidget()
        cl = QVBoxLayout(console_widget)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        ch = QWidget()
        ch.setFixedHeight(28)
        ch.setStyleSheet(f"background:{C['bg3']}; border-top:1px solid {C['border']};")
        chl = QHBoxLayout(ch)
        chl.setContentsMargins(12, 0, 8, 0)

        lbl = QLabel("Output")
        lbl.setStyleSheet(f"color:{C['dim']}; font-family:Consolas; font-size:10px;")
        chl.addWidget(lbl)
        chl.addStretch()

        clear_btn = QPushButton("✕ Clear")
        clear_btn.setFixedHeight(20)
        clear_btn.setStyleSheet(f"QPushButton{{background:transparent;color:{C['dim']};border:none;font-family:Consolas;font-size:10px;padding:0 8px;}}QPushButton:hover{{color:{C['text']};}}")
        clear_btn.clicked.connect(self._clear_output)
        chl.addWidget(clear_btn)
        cl.addWidget(ch)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 11))
        self.console.setStyleSheet(f"QTextEdit{{background:{C['bg2']};color:{C['text']};border:none;padding:8px 12px;}}")
        cl.addWidget(self.console)
        splitter.addWidget(console_widget)
        splitter.setSizes([520, 180])

        # Статусбар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        lang_label = QLabel(" Cream v0.1 ")
        lang_label.setStyleSheet(f"background:{C['accent']};color:{C['bg']};font-weight:bold;padding:0 8px;")
        self.status_bar.addWidget(lang_label)

        self.status_file = QLabel("untitled.cream")
        self.status_file.setStyleSheet(f"padding:0 12px;color:{C['dim']};")
        self.status_bar.addWidget(self.status_file)

        self.status_pos = QLabel("Ln 1, Col 1")
        self.status_pos.setStyleSheet(f"padding:0 12px;color:{C['dim']};")
        self.status_bar.addPermanentWidget(self.status_pos)

    def _build_menu(self):
        mb = self.menuBar()

        fm = mb.addMenu("File")
        fm.addAction(self._action("New",       "Ctrl+N",       self._new_file))
        fm.addAction(self._action("Open...",   "Ctrl+O",       self._open_file))
        fm.addAction(self._action("Save",      "Ctrl+S",       self._save_file))
        fm.addAction(self._action("Save As...", "Ctrl+Shift+S", self._save_as))
        fm.addSeparator()
        fm.addAction(self._action("Exit",      "Alt+F4",       self.close))

        rm = mb.addMenu("Run")
        rm.addAction(self._action("Run",          "F5", self._run))
        rm.addAction(self._action("Stop",         "F6", self._stop))
        rm.addAction(self._action("Clear Output", "",   self._clear_output))

    def _action(self, name, shortcut, slot):
        a = QAction(name, self)
        if shortcut: a.setShortcut(QKeySequence(shortcut))
        a.triggered.connect(slot)
        return a

    def _load_welcome(self):
        self.editor.setPlainText(
            '-- Welcome to Cream IDE! Press F5 to run.\n\n'
            'name = "World"\n'
            'say "Hello, {name}!"\n\n'
            'numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n'
            'result = numbers\n'
            '    | filter(x \u2192 x % 2 == 0)\n'
            '    | map(x \u2192 x * 2)\n'
            '    | sum\n'
            'say "Sum of evens: {result}"\n'
        )
        self.modified = False
        self._update_title()

    def _on_modified(self):
        if not self.modified:
            self.modified = True
            self._update_title()

    def _update_title(self):
        name = os.path.basename(self.current_file) if self.current_file else "untitled.cream"
        mark = " •" if self.modified else ""
        self.setWindowTitle(f"Cream IDE \u2014 {name}{mark}")
        self.status_file.setText(self.current_file or "untitled.cream")

    def _update_cursor_pos(self):
        c = self.editor.textCursor()
        self.status_pos.setText(f"Ln {c.blockNumber()+1}, Col {c.columnNumber()+1}")

    def _new_file(self):
        if self.modified:
            r = QMessageBox.question(self, "Unsaved", "Discard changes?")
            if r != QMessageBox.StandardButton.Yes: return
        self.editor.clear()
        self.current_file = None
        self.modified = False
        self._update_title()

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open", "", "Cream files (*.cream);;All files (*.*)")
        if not path: return
        with open(path, "r", encoding="utf-8") as f:
            self.editor.setPlainText(f.read())
        self.current_file = path
        self.modified = False
        self._update_title()

    def _save_file(self):
        if not self.current_file: return self._save_as()
        with open(self.current_file, "w", encoding="utf-8") as f:
            f.write(self.editor.toPlainText())
        self.modified = False
        self._update_title()
        self.toolbar_status.setText("Saved \u2713")
        QTimer.singleShot(2000, lambda: self.toolbar_status.setText("Ready"))

    def _save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Cream files (*.cream);;All files (*.*)")
        if not path: return
        self.current_file = path
        self._save_file()

    def _run(self):
        # Сохраняем код во временный файл
        if not self.current_file:
            tmp = os.path.join(os.path.expanduser("~"), "_cream_tmp.cream")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            run_path = tmp
            filename = "untitled.cream"
        else:
            self._save_file()
            run_path = self.current_file
            filename = os.path.basename(self.current_file)

        self.toolbar_status.setText("Running...")
        self.run_btn.setEnabled(False)

        # Открываем отдельное окно вывода
        self.output_window = RunOutputWindow(filename, parent=None)
        self.output_window.show()
        self.output_window.raise_()

        # Запускаем встроенный интерпретатор в отдельном потоке
        self.run_thread = BuiltinRunThread(run_path)
        self.run_thread.output.connect(self.output_window.append)
        self.run_thread.finished.connect(self._on_run_finished)
        self.run_thread.start()

    def _stop(self):
        if self.run_thread and self.run_thread.isRunning():
            self.run_thread.stop()
            self._print("\n■ Stopped\n", "error")
            self.toolbar_status.setText("Stopped")
            self.run_btn.setEnabled(True)

    def _on_run_finished(self, code):
        if hasattr(self, 'output_window') and self.output_window:
            if code == 0:
                self.output_window.append("\n✅ Done\n", "success")
                self.output_window.set_status("Done ✓", C["green"])
            else:
                self.output_window.set_status("Error", C["red"])
        self.toolbar_status.setText("Done ✓" if code == 0 else "Error")
        self.run_btn.setEnabled(True)

    def _clear_output(self):
        self.console.clear()

    def _print(self, text, tag="output"):
        colors = {"output": C["text"], "error": C["red"], "success": C["green"], "info": C["dim"]}
        self.console.setTextColor(QColor(colors.get(tag, C["text"])))
        self.console.insertPlainText(text)
        self.console.ensureCursorVisible()

    def closeEvent(self, event):
        if self.modified:
            r = QMessageBox.question(self, "Unsaved", "Save before exit?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
            if r == QMessageBox.StandardButton.Save: self._save_file()
            elif r == QMessageBox.StandardButton.Cancel: event.ignore(); return
        event.accept()


# ══════════════════════════════════════════
#  ЗАПУСК
# ══════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Cream IDE")
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window,        QColor(C["bg"]))
    palette.setColor(QPalette.ColorRole.WindowText,    QColor(C["text"]))
    palette.setColor(QPalette.ColorRole.Base,          QColor(C["bg"]))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(C["bg2"]))
    palette.setColor(QPalette.ColorRole.Text,          QColor(C["text"]))
    palette.setColor(QPalette.ColorRole.Button,        QColor(C["bg3"]))
    palette.setColor(QPalette.ColorRole.ButtonText,    QColor(C["text"]))
    palette.setColor(QPalette.ColorRole.Highlight,     QColor(C["accent"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(C["bg"]))
    app.setPalette(palette)

    window = CreamIDE()
    # Сплэш-скрин
    splash = SplashScreen()
    splash.show()
    app.processEvents()

    # Иконка окна
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cream.ico")
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))

    # Показать главное окно через 2 секунды
    QTimer.singleShot(2500, lambda: (splash.close(), window.show()))
    sys.exit(app.exec())
