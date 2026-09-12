import hashlib as _hashlib_std
import sys as _sys_std

class TT:
    NUMBER   = "NUMBER";   STRING   = "STRING"
    BOOL     = "BOOL";     EMPTY    = "EMPTY"
    IDENT    = "IDENT";    KEYWORD  = "KEYWORD"
    PLUS     = "PLUS";     MINUS    = "MINUS"
    STAR     = "STAR";     SLASH    = "SLASH"
    PERCENT  = "PERCENT";  ARROW    = "ARROW"
    PIPE     = "PIPE";     DOT      = "DOT"
    QMARK    = "QMARK";    SPREAD   = "SPREAD"
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
    PLUS_ASSIGN   = "PLUS_ASSIGN"
    MINUS_ASSIGN  = "MINUS_ASSIGN"
    STAR_ASSIGN   = "STAR_ASSIGN"
    SLASH_ASSIGN  = "SLASH_ASSIGN"
    PERCENT_ASSIGN = "PERCENT_ASSIGN"

KEYWORDS = {
    "if", "else", "or if", "for each", "in",
    "repeat", "while", "action", "return",
    "task", "wait", "together", "try", "on error",
    "struct", "yes", "no", "empty",
    "and", "or", "not", "say",
    "page", "block", "card", "button", "text", "animation",
    "import", "match", "case", "assert",
    "break", "continue", "guard", "is",
}

AUG_ASSIGN_OPS = {
    TT.PLUS_ASSIGN:   "+",
    TT.MINUS_ASSIGN:  "-",
    TT.STAR_ASSIGN:   "*",
    TT.SLASH_ASSIGN:  "/",
    TT.PERCENT_ASSIGN:"%",
}

class ErrorCode:
    UNDEFINED_VAR    = "E001"
    TYPE_ERROR       = "E002"
    DIVISION_BY_ZERO = "E003"
    INDEX_ERROR      = "E004"
    ARITY_ERROR      = "E005"
    FIELD_NOT_FOUND  = "E006"
    FILE_NOT_FOUND   = "E007"
    UNKNOWN_OPERATOR = "E008"
    UNKNOWN_NODE     = "E009"
    IMPORT_ERROR     = "E010"
    UNKNOWN_BUILTIN  = "E011"
    NOT_CALLABLE     = "E012"
    PARSER_ERROR     = "E013"
    LEXER_ERROR      = "E014"
    ASSERT_ERROR     = "E015"
    PKG_ERROR        = "E016"
    TYPE_CHECK_ERROR = "E017"

_token_cache = {}
_ast_cache = {}
_CACHE_MAX = 64
_source_lines_cache = {}

def _cache_get(cache, key):
    return cache.get(key)

def _cache_set(cache, key, value):
    if len(cache) >= _CACHE_MAX:
        oldest = next(iter(cache))
        del cache[oldest]
    cache[key] = value

class Token:
    def __init__(self, type_, value, line=0, col=0):
        self.type = type_; self.value = value
        self.line = line;  self.col   = col
    def __repr__(self):
        return f"Token({self.type:<12}| {repr(self.value):<20}| line {self.line})"

class LexerError(Exception):
    def __init__(self, msg, line, col, source=None):
        self.line = line; self.col = col; self.source = source
        snippet = _format_snippet(source, line, col) if source else ""
        super().__init__(f"[Lexer Error] [{ErrorCode.LEXER_ERROR}] Line {line}, Col {col}: {msg}{snippet}")

def _format_snippet(source, line, col=0, context=2):
    if not source: return ""
    lines = source.split('\n')
    if line < 1 or line > len(lines): return ""
    start = max(0, line - 1 - context)
    end = min(len(lines), line + context)
    parts = []
    for i in range(start, end):
        marker = ">>>" if i == line - 1 else "   "
        parts.append(f"  {marker} {i+1:>3} | {lines[i]}")
        if i == line - 1 and col > 0:
            pointer = " " * (col + 9) + "^"
            parts.append(pointer)
    return "\n" + "\n".join(parts)

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

    def peek_str(self, n):
        if self.pos + n > len(self.source): return ""
        return self.source[self.pos:self.pos+n]

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
            raise LexerError("Незакрытая строка", self.line, col_start, self.source)
        self.advance()
        self.tokens.append(Token(TT.STRING, result, self.line, col_start))

    def read_multiline_string(self):
        col_start = self.col
        self.advance(); self.advance(); self.advance()
        result = ""
        while self.pos < len(self.source):
            if self.current() == '"' and self.peek_str(3) == '"""':
                self.advance(); self.advance(); self.advance()
                if result.startswith('\n'): result = result[1:]
                lines = result.split('\n')
                if len(lines) > 1:
                    min_indent = 999
                    for line in lines:
                        stripped = line.lstrip(' ')
                        if stripped: min_indent = min(min_indent, len(line) - len(stripped))
                    if min_indent < 999 and min_indent > 0:
                        result = '\n'.join(line[min_indent:] if len(line) >= min_indent else line for line in lines)
                self.tokens.append(Token(TT.STRING, result, self.line, col_start))
                return
            result += self.advance()
        raise LexerError("Незакрытая многострочная строка", self.line, col_start, self.source)

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
                else: self.pos, self.col, self.line = saved
        if word == "_":     self.tokens.append(Token(TT.IDENT, "_", self.line, col_start))
        elif word in ("yes", "no"):
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
            if not stripped or stripped.startswith('--'):
                if stripped and stripped.startswith('///'):
                    result.append(("DOC", stripped[3:].strip(), line_num))
                continue
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
        cache_key = _hashlib_std.md5(self.source.encode('utf-8')).hexdigest() if len(self.source) < 100000 else None
        if cache_key:
            cached = _cache_get(_token_cache, cache_key)
            if cached is not None: return cached
        _source_lines_cache[id(self.source)] = self.source
        lines = self.source.split('\n')
        pre = self.handle_indents(lines)
        all_tokens = []
        for item in pre:
            if isinstance(item, Token): all_tokens.append(item); continue
            kind, text, line_num = item
            if kind == "DOC":
                all_tokens.append(Token("DOC_COMMENT", text, line_num, 1))
                all_tokens.append(Token(TT.NEWLINE, '\n', line_num, len(text)))
                continue
            self.source = text; self.pos = 0
            self.line = line_num; self.col = 1; self.tokens = []
            self._tokenize_line()
            all_tokens.extend(self.tokens)
            all_tokens.append(Token(TT.NEWLINE, '\n', line_num, len(text)))
        all_tokens.append(Token(TT.EOF, None, self.line, self.col))
        if cache_key: _cache_set(_token_cache, cache_key, all_tokens)
        return all_tokens

    def _tokenize_line(self):
        while self.pos < len(self.source):
            ch = self.current()
            if ch in (' ', '\t'): self.skip_spaces()
            elif ch == '-' and self.peek() == '-': break
            elif ch == '"' and self.peek_str(3) == '"""': self.read_multiline_string()
            elif ch == '"': self.read_string()
            elif ch.isdigit(): self.read_number()
            elif ch.isalpha() or ch == '_': self.read_ident()
            elif ch == '\u2192': self.add(TT.ARROW, '\u2192'); self.advance()
            elif ch == '?' and self.peek() == '.':
                self.advance(); self.advance(); self.add(TT.QMARK, '?.')
            elif ch == '.' and self.peek() == '.' and self.peek(2) == '.':
                self.advance(); self.advance(); self.advance(); self.add(TT.SPREAD, '...')
            elif ch == '-' and self.peek() == '>':
                self.advance(); self.advance(); self.add(TT.ARROW, '->')
            elif ch == '+' and self.peek() == '=':
                self.advance(); self.advance(); self.add(TT.PLUS_ASSIGN, '+=')
            elif ch == '-' and self.peek() == '=':
                self.advance(); self.advance(); self.add(TT.MINUS_ASSIGN, '-=')
            elif ch == '*' and self.peek() == '=':
                self.advance(); self.advance(); self.add(TT.STAR_ASSIGN, '*=')
            elif ch == '/' and self.peek() == '=':
                self.advance(); self.advance(); self.add(TT.SLASH_ASSIGN, '/=')
            elif ch == '%' and self.peek() == '=':
                self.advance(); self.advance(); self.add(TT.PERCENT_ASSIGN, '%=')
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
            else: raise LexerError(f"Неизвестный символ: {repr(ch)}", self.line, self.col, self.source)

class Node:
    line = 0
    doc  = None

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
    def __init__(self, elements, spreads=None):
        self.elements = elements; self.spreads = spreads or []

class ListComprehension(Node):
    def __init__(self, expr, var, iterable, condition=None):
        self.expr = expr; self.var = var
        self.iterable = iterable; self.condition = condition

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
    def __init__(self, obj, field, optional=False):
        self.obj = obj; self.field = field; self.optional = optional

class IndexAccess(Node):
    def __init__(self, obj, index):
        self.obj = obj; self.index = index

class IsCheck(Node):
    def __init__(self, expr, type_name):
        self.expr = expr; self.type_name = type_name

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

class AugAssign(Node):
    def __init__(self, name, op, value):
        self.name = name; self.op = op; self.value = value

class MultiAssign(Node):
    def __init__(self, names, values):
        self.names = names; self.values = values

class MatchStmt(Node):
    def __init__(self, subject, cases):
        self.subject = subject; self.cases = cases

class CaseClause(Node):
    def __init__(self, pattern, is_wildcard, body):
        self.pattern = pattern; self.is_wildcard = is_wildcard; self.body = body

class AssertStmt(Node):
    def __init__(self, condition, message=None):
        self.condition = condition; self.message = message

class BreakSignal(Exception): pass

class ContinueSignal(Exception): pass

class Say(Node):
    def __init__(self, value): self.value = value

class Return(Node):
    def __init__(self, value): self.value = value

class If(Node):
    def __init__(self, condition, then_body, elseif_clauses, else_body):
        self.condition = condition; self.then_body = then_body
        self.elseif_clauses = elseif_clauses; self.else_body = else_body

class ForEach(Node):
    def __init__(self, var, iterable, body, index_var=None):
        self.var = var; self.iterable = iterable; self.body = body
        self.index_var = index_var

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
    def __init__(self, path): self.path = path

class GuardStmt(Node):
    def __init__(self, condition, else_body):
        self.condition = condition; self.else_body = else_body

class ParseError(Exception):
    def __init__(self, msg, token=None, source=None):
        self.line = token.line if token else 0
        self.source = source
        loc = f" (line {self.line})" if token else ""
        snippet = _format_snippet(source, self.line, token.col if token else 0) if source and token else ""
        super().__init__(f"[Parse Error] [{ErrorCode.PARSER_ERROR}]{loc}: {msg}{snippet}")

def _is_const(node):
    return isinstance(node, (NumberLiteral, StringLiteral, BoolLiteral, EmptyLiteral))

def _fold(node):
    if isinstance(node, BinaryOp) and _is_const(node.left) and _is_const(node.right):
        l = node.left.value; r = node.right.value; op = node.op
        try:
            if op == "+":
                if isinstance(l, str) or isinstance(r, str): return StringLiteral(str(l) + str(r))
                return NumberLiteral(l + r)
            if op == "-":  return NumberLiteral(l - r)
            if op == "*":  return NumberLiteral(l * r)
            if op == "/":
                if r == 0: return node
                return NumberLiteral(l / r)
            if op == "%":
                if r == 0: return node
                return NumberLiteral(l % r)
            if op == "==": return BoolLiteral(l == r)
            if op == "!=": return BoolLiteral(l != r)
            if op == ">":  return BoolLiteral(l > r)
            if op == "<":  return BoolLiteral(l < r)
            if op == ">=": return BoolLiteral(l >= r)
            if op == "<=": return BoolLiteral(l <= r)
            if op == "and": return BoolLiteral(l and r)
            if op == "or":  return BoolLiteral(l or r)
        except: pass
    if isinstance(node, UnaryOp) and _is_const(node.operand):
        v = node.operand.value
        try:
            if node.op == "not": return BoolLiteral(not v)
            if node.op == "-":   return NumberLiteral(-v)
        except: pass
    return node

class Parser:
    def __init__(self, tokens, source=None):
        self.tokens = tokens; self.pos = 0
        self._pending_doc = None; self.source = source

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

    def skip_doc_and_newlines(self):
        while self.current().type in (TT.NEWLINE, "DOC_COMMENT"):
            if self.current().type == "DOC_COMMENT": self._pending_doc = self.current().value
            self.advance()

    def expect(self, type_, value=None):
        tok = self.current()
        if tok.type != type_:
            raise ParseError(f"Ожидался {type_}, получен {tok.type} ({repr(tok.value)})", tok, self.source)
        if value is not None and tok.value != value:
            raise ParseError(f"Ожидалось {repr(value)}, получено {repr(tok.value)}", tok, self.source)
        return self.advance()

    def check(self, type_, value=None):
        tok = self.current()
        if tok.type != type_: return False
        if value is not None and tok.value != value: return False
        return True

    def check_keyword(self, kw):
        return self.current().type == TT.KEYWORD and self.current().value == kw

    def _mark(self, node, line):
        node.line = line
        if self._pending_doc:
            node.doc = self._pending_doc; self._pending_doc = None
        return node

    def parse_block(self):
        self.skip_newlines(); self.expect(TT.INDENT); stmts = []
        while not self.check(TT.DEDENT) and not self.check(TT.EOF):
            self.skip_newlines()
            if self.check(TT.DEDENT) or self.check(TT.EOF): break
            stmts.append(self.parse_statement()); self.skip_newlines()
        self.expect(TT.DEDENT); return stmts

    def parse_statement(self):
        self.skip_doc_and_newlines()
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
            if kw == "match":    return self.parse_match()
            if kw == "assert":   return self.parse_assert()
            if kw == "break":
                line = tok.line; self.advance(); self.skip_newlines()
                return self._mark(Say(None), line).__class__.__mro__
                # break/continue handled as signals
                self.advance(); self.skip_newlines()
                node = Say(None); node.__class__ = type('BreakNode', (Node,), {})
                node.line = tok.line; return node
            if kw == "continue":
                self.advance(); self.skip_newlines()
                node = Say(None); node.__class__ = type('ContinueNode', (Node,), {})
                node.line = tok.line; return node
            if kw == "guard":    return self.parse_guard()
        if tok.type == TT.IDENT and self.peek().type == TT.ASSIGN:
            saved_pos = self.pos; names = [self.advance().value]
            while self.check(TT.COMMA):
                self.advance(); names.append(self.expect(TT.IDENT).value)
            if len(names) == 1: self.pos = saved_pos; return self.parse_assign()
            return self.parse_multi_assign(names)
        if tok.type == TT.IDENT and self.peek().type in AUG_ASSIGN_OPS:
            return self.parse_aug_assign()
        expr = self.parse_expression(); self.skip_newlines(); return expr

    def parse_say(self):
        line = self.current().line; self.advance()
        value = self.parse_expression(); self.skip_newlines()
        return self._mark(Say(value), line)

    def parse_assign(self):
        line = self.current().line
        name = self.advance().value; self.advance()
        value = self.parse_pipeline(); self.skip_newlines()
        return self._mark(Assign(name, value), line)

    def parse_aug_assign(self):
        line = self.current().line
        name = self.advance().value; op = AUG_ASSIGN_OPS[self.advance().type]
        value = self.parse_pipeline(); self.skip_newlines()
        return self._mark(AugAssign(name, op, value), line)

    def parse_multi_assign(self, names):
        line = self.current().line; self.expect(TT.ASSIGN)
        values = [self.parse_expression()]
        while self.check(TT.COMMA): self.advance(); values.append(self.parse_expression())
        self.skip_newlines(); return self._mark(MultiAssign(names, values), line)

    def parse_return(self):
        line = self.current().line; self.advance()
        value = self.parse_expression(); self.skip_newlines()
        return self._mark(Return(value), line)

    def parse_wait_stmt(self):
        line = self.current().line; self.advance()
        value = self.parse_expression(); self.skip_newlines()
        return self._mark(Wait(value), line)

    def parse_if(self):
        line = self.current().line; self.advance()
        condition = self.parse_expression(); self.skip_newlines()
        then_body = self.parse_block()
        elseif_clauses = []; else_body = None
        while True:
            self.skip_newlines()
            if self.check_keyword("or if"):
                self.advance(); cond = self.parse_expression(); self.skip_newlines()
                body = self.parse_block(); elseif_clauses.append((cond, body))
            elif self.check_keyword("else"):
                self.advance(); self.skip_newlines()
                if self.check_keyword("if"):
                    self.advance(); cond = self.parse_expression(); self.skip_newlines()
                    body = self.parse_block(); elseif_clauses.append((cond, body))
                else: else_body = self.parse_block(); break
            else: break
        return self._mark(If(condition, then_body, elseif_clauses, else_body), line)

    def parse_for_each(self):
        line = self.current().line; self.advance()
        first_var = self.expect(TT.IDENT).value
        index_var = None
        if self.check(TT.COMMA):
            self.advance()
            index_var = first_var
            var = self.expect(TT.IDENT).value
        else:
            var = first_var
        self.expect(TT.KEYWORD, "in")
        iterable = self.parse_expression(); self.skip_newlines()
        body = self.parse_block()
        return self._mark(ForEach(var, iterable, body, index_var=index_var), line)

    def parse_repeat(self):
        line = self.current().line; self.advance()
        count = self.parse_expression(); self.skip_newlines()
        body = self.parse_block(); return self._mark(Repeat(count, body), line)

    def parse_while(self):
        line = self.current().line; self.advance()
        condition = self.parse_expression(); self.skip_newlines()
        body = self.parse_block(); return self._mark(While(condition, body), line)

    def parse_action(self):
        line = self.current().line; self.advance()
        name = self.expect(TT.IDENT).value; params = self.parse_params()
        self.skip_newlines(); body = self.parse_block()
        return self._mark(ActionDef(name, params, body), line)

    def parse_task(self):
        line = self.current().line; self.advance()
        name = self.expect(TT.IDENT).value; params = self.parse_params()
        self.skip_newlines(); body = self.parse_block()
        return self._mark(TaskDef(name, params, body), line)

    def parse_params(self):
        self.expect(TT.LPAREN); params = []
        while not self.check(TT.RPAREN):
            name = self.expect(TT.IDENT).value; default = None
            if self.check(TT.ASSIGN): self.advance(); default = self.parse_expression()
            params.append((name, default))
            if self.check(TT.COMMA): self.advance()
        self.expect(TT.RPAREN); return params

    def parse_try(self):
        line = self.current().line; self.advance(); self.skip_newlines()
        try_body = self.parse_block(); self.skip_newlines()
        self.expect(TT.KEYWORD, "on error")
        error_var = self.expect(TT.IDENT).value; self.skip_newlines()
        catch_body = self.parse_block()
        return self._mark(TryCatch(try_body, error_var, catch_body), line)

    def parse_struct(self):
        line = self.current().line; self.advance()
        name = self.expect(TT.IDENT).value; self.skip_newlines()
        self.expect(TT.INDENT); fields = []
        while not self.check(TT.DEDENT):
            self.skip_newlines()
            if self.check(TT.DEDENT): break
            fname = self.expect(TT.IDENT).value; self.expect(TT.COLON); tok = self.current()
            if tok.type in (TT.IDENT, TT.KEYWORD): ftype = self.advance().value
            else: raise ParseError(f"Ожидался тип поля", tok, self.source)
            default = None
            if self.check(TT.ASSIGN): self.advance(); default = self.parse_expression()
            fields.append((fname, ftype, default)); self.skip_newlines()
        self.expect(TT.DEDENT); return self._mark(StructDef(name, fields), line)

    def parse_match(self):
        line = self.current().line; self.advance()
        subject = self.parse_expression(); self.skip_newlines()
        self.expect(TT.INDENT); cases = []
        while not self.check(TT.DEDENT) and not self.check(TT.EOF):
            self.skip_newlines()
            if self.check(TT.DEDENT) or self.check(TT.EOF): break
            self.expect(TT.KEYWORD, "case"); tok = self.current()
            if tok.type == TT.IDENT and tok.value == "_":
                self.advance(); is_wildcard = True; pattern = None
            else: is_wildcard = False; pattern = self.parse_expression()
            self.skip_newlines(); body = self.parse_block()
            cases.append(CaseClause(pattern, is_wildcard, body))
            if is_wildcard: break
        self.expect(TT.DEDENT); return self._mark(MatchStmt(subject, cases), line)

    def parse_assert(self):
        line = self.current().line; self.advance()
        condition = self.parse_expression(); message = None
        if self.check(TT.COMMA): self.advance(); message = self.parse_expression()
        self.skip_newlines(); return self._mark(AssertStmt(condition, message), line)

    def parse_guard(self):
        line = self.current().line; self.advance()
        condition = self.parse_expression(); self.skip_newlines()
        self.expect(TT.INDENT); else_body = []
        while not self.check(TT.DEDENT) and not self.check(TT.EOF):
            self.skip_newlines()
            if self.check(TT.DEDENT) or self.check(TT.EOF): break
            else_body.append(self.parse_statement()); self.skip_newlines()
        self.expect(TT.DEDENT)
        return self._mark(GuardStmt(condition, else_body), line)

    def parse_expression(self): return self.parse_pipeline()

    def parse_pipeline(self):
        left = self.parse_is()
        if not self.check(TT.PIPE):
            if not (self.check(TT.NEWLINE) and self.peek().type == TT.PIPE): return left
        steps = []
        while True:
            if self.check(TT.NEWLINE) and self.peek().type == TT.PIPE: self.advance()
            if not self.check(TT.PIPE): break
            self.advance(); step = self.parse_call_or_ident(); steps.append(step)
        if not steps: return left
        return Pipeline(left, steps)

    def parse_is(self):
        left = self.parse_logical()
        if self.check_keyword("is"):
            self.advance()
            type_tok = self.expect(TT.IDENT)
            return IsCheck(left, type_tok.value)
        return left

    def parse_logical(self):
        left = self.parse_comparison()
        while self.current().type == TT.KEYWORD and self.current().value in ("and", "or"):
            op = self.advance().value; left = BinaryOp(left, op, self.parse_comparison())
        return _fold(left)

    def parse_comparison(self):
        left = self.parse_addition()
        cmp_types = {TT.EQ, TT.NEQ, TT.LT, TT.GT, TT.LTE, TT.GTE}
        while self.current().type in cmp_types:
            op = self.advance().value; left = BinaryOp(left, op, self.parse_addition())
        return _fold(left)

    def parse_addition(self):
        left = self.parse_multiply()
        while self.current().type in (TT.PLUS, TT.MINUS):
            op = self.advance().value; left = BinaryOp(left, op, self.parse_multiply())
        return _fold(left)

    def parse_multiply(self):
        left = self.parse_unary()
        while self.current().type in (TT.STAR, TT.SLASH, TT.PERCENT):
            op = self.advance().value; left = BinaryOp(left, op, self.parse_unary())
        return _fold(left)

    def parse_unary(self):
        if self.check_keyword("not"): self.advance(); return _fold(UnaryOp("not", self.parse_unary()))
        if self.check(TT.MINUS): self.advance(); return _fold(UnaryOp("-", self.parse_unary()))
        return self.parse_postfix()

    def parse_postfix(self):
        node = self.parse_primary()
        while True:
            if self.check(TT.DOT):
                self.advance(); node = FieldAccess(node, self.expect(TT.IDENT).value)
            elif self.check(TT.QMARK):
                self.advance(); node = FieldAccess(node, self.expect(TT.IDENT).value, optional=True)
            elif self.check(TT.LBRACKET):
                self.advance(); index = self.parse_expression()
                self.expect(TT.RBRACKET); node = IndexAccess(node, index)
            elif self.check(TT.LPAREN):
                node = Call(node, self.parse_args())
            else: break
        return node

    def parse_call_or_ident(self): return self.parse_postfix()

    def parse_args(self):
        self.expect(TT.LPAREN); args = []
        while not self.check(TT.RPAREN):
            if self.check(TT.IDENT) and self.peek().type == TT.ARROW:
                param = self.advance().value; self.advance()
                args.append(Lambda(param, self.parse_expression()))
            else: args.append(self.parse_expression())
            if self.check(TT.COMMA): self.advance()
        self.expect(TT.RPAREN); return args

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
            self.advance(); node = self.parse_expression(); self.expect(TT.RPAREN); return node
        if tok.type == TT.KEYWORD:
            if tok.value == "wait":   self.advance(); return Wait(self.parse_expression())
            if tok.value == "not":    self.advance(); return UnaryOp("not", self.parse_primary())
            self.advance()
            if self.check(TT.LPAREN): return Call(Identifier(tok.value), self.parse_args())
            return Identifier(tok.value)
        raise ParseError(f"Неожиданный токен: {tok.type} {repr(tok.value)}", tok, self.source)

    def parse_list(self):
        self.expect(TT.LBRACKET)
        if self.check(TT.RBRACKET): self.advance(); return ListLiteral([])
        elements = []; spreads = []; has_spread = False
        if self.check(TT.SPREAD):
            self.advance(); spreads.append(len(elements))
            elements.append(self.parse_expression()); has_spread = True
        else: elements.append(self.parse_expression())
        if not has_spread and self.check_keyword("for"):
            first = elements[0]; self.advance()
            var = self.expect(TT.IDENT).value
            self.expect(TT.KEYWORD, "in"); iterable = self.parse_expression()
            condition = None
            if self.check_keyword("if"): self.advance(); condition = self.parse_expression()
            self.expect(TT.RBRACKET)
            return ListComprehension(first, var, iterable, condition)
        while self.check(TT.COMMA):
            self.advance()
            if self.check(TT.RBRACKET): break
            if self.check(TT.SPREAD):
                self.advance(); spreads.append(len(elements))
                elements.append(self.parse_expression()); has_spread = True
            else: elements.append(self.parse_expression())
        self.expect(TT.RBRACKET)
        return ListLiteral(elements, spreads=spreads if has_spread else None)

    def parse_table(self):
        self.expect(TT.LBRACE); self.skip_newlines(); pairs = []
        while not self.check(TT.RBRACE):
            self.skip_newlines()
            key = self.expect(TT.IDENT).value; self.expect(TT.COLON)
            value = self.parse_expression()
            pairs.append((key, value)); self.skip_newlines()
            if self.check(TT.COMMA): self.advance()
            self.skip_newlines()
        self.expect(TT.RBRACE); return TableLiteral(pairs)

    def parse_import(self):
        line = self.current().line; self.advance()
        path = self.expect(TT.STRING).value; self.skip_newlines()
        return self._mark(Import(path), line)

    def parse(self):
        body = []; self.skip_newlines()
        while not self.check(TT.EOF):
            body.append(self.parse_statement()); self.skip_newlines()
        return Program(body)

class Environment:
    __slots__ = ('vars', 'parent')
    def __init__(self, parent=None):
        self.vars = {}; self.parent = parent

    def get(self, name):
        if name in self.vars: return self.vars[name]
        if self.parent: return self.parent.get(name)
        raise CreamRuntimeError(f"Переменная '{name}' не определена", code=ErrorCode.UNDEFINED_VAR)

    def set(self, name, value):
        self.vars[name] = value

    def assign(self, name, value):
        if name in self.vars: self.vars[name] = value
        elif self.parent: self.parent.assign(name, value)
        else: self.vars[name] = value

class CreamFunction:
    __slots__ = ('name', 'params', 'body', 'closure', 'doc')
    def __init__(self, name, params, body, closure, doc=None):
        self.name = name; self.params = params
        self.body = body; self.closure = closure; self.doc = doc
    def __repr__(self): return f"<action {self.name}>"

class CreamStruct:
    __slots__ = ('type_name', 'fields')
    def __init__(self, type_name, fields):
        self.type_name = type_name; self.fields = fields
    def __repr__(self):
        items = ", ".join(f"{k}={repr(v)}" for k, v in self.fields.items())
        return f"{self.type_name}({items})"

class CreamStructType:
    __slots__ = ('name', 'fields', 'doc')
    def __init__(self, name, fields, doc=None):
        self.name = name; self.fields = fields; self.doc = doc
    def __repr__(self): return f"<struct {self.name}>"

class CreamLambda:
    __slots__ = ('param', 'body', 'closure')
    def __init__(self, param, body, closure):
        self.param = param; self.body = body; self.closure = closure
    def __repr__(self): return f"<lambda {self.param}>"

class ReturnSignal(Exception):
    def __init__(self, value): self.value = value

class CreamRuntimeError(Exception):
    def __init__(self, msg, code=None, line=None, call_stack=None, source=None):
        self.code = code; self.line = line; self.source = source
        self.call_stack = call_stack or []
        parts = ["[Runtime Error]"]
        if code: parts.append(f"[{code}]")
        if line: parts.append(f"Line {line}:")
        parts.append(msg)
        full = " ".join(parts)
        if source and line:
            full += _format_snippet(source, line)
        if self.call_stack:
            chain = " -> ".join(str(s) for s in self.call_stack)
            full += f"\n  Call stack: {chain}"
        super().__init__(full)

class _Builtin:
    __slots__ = ('fn', 'name')
    def __init__(self, fn, name="builtin"):
        self.fn = fn; self.name = name
    def __call__(self, args): return self.fn(args)
    def __repr__(self): return f"<builtin {self.name}>"

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.call_stack = []
        self.docs = {}
        self._source = None
        self._profile_data = {}
        self._setup_builtins()

    def _pkg_dir(self):
        import os as _os
        d = _os.path.join(_os.path.expanduser("~"), ".cream", "packages")
        _os.makedirs(d, exist_ok=True)
        return d

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

        env = self.global_env; cs = self._cream_str; interp = self

        def _reg(name, doc_text): interp.docs[name] = doc_text

        _reg("say", "say value - Prints value to output")
        _reg("input", "input prompt - Reads user input")
        _reg("length", "length collection - Returns length")
        _reg("sum", "sum list - Returns sum")
        _reg("min", "min list - Returns minimum")
        _reg("max", "max list - Returns maximum")
        _reg("abs", "abs number - Absolute value")
        _reg("round", "round number, decimals=0 - Rounds")
        _reg("number", "number value - Convert to number")
        _reg("bool", "bool value - Convert to boolean")
        _reg("range", "range start, end - Number list")
        _reg("sort", "sort list - Sorted copy")
        _reg("reverse", "reverse list - Reversed copy")
        _reg("first", "first list - First element")
        _reg("last", "last list - Last element")
        _reg("join", "join list, sep=', ' - Join list")
        _reg("upper", "upper string - Uppercase")
        _reg("lower", "lower string - Lowercase")
        _reg("trim", "trim string - Trim whitespace")
        _reg("split", "split string, sep=' ' - Split")
        _reg("contains", "contains collection, item - Containment check")
        _reg("type", "type value - Returns type name")
        _reg("help", "help name? - Shows help")
        _reg("pkg", "pkg op, args... - Package manager")
        _reg("bench", "bench n, fn - Benchmark n iterations")
        _reg("time", "time fn - Time single call")
        _reg("math", "math x, op, args... - Math operations")
        _reg("num", "num x, op - Number operations")
        _reg("rand", "rand args... - Random")
        _reg("stats", "stats list, op? - Statistics")
        _reg("list", "list lst, op, args... - List ops")
        _reg("table", "table t, op, args... - Table ops")
        _reg("convert", "convert value, from, to - Units")
        _reg("date", "date op? - Date/time")
        _reg("file", "file path, op, args... - Files")
        _reg("folder", "folder path, op, args... - Folders")
        _reg("sys", "sys op, args... - System")
        _reg("encode", "encode value, op, mode? - Encoding")
        _reg("str_", "str_ value, op, args... - Strings")
        _reg("regex", "regex pattern, text, op? - Regex")
        _reg("text_", "text_ value, op, args... - Text")
        _reg("print_", "print_ value, op, args? - Print")
        _reg("net", "net url, op?, data? - HTTP")

        def cream_type(args):
            x = args[0]
            if x is None: return "empty"
            if isinstance(x, bool): return "bool"
            if isinstance(x, (int, float)): return "number"
            if isinstance(x, str): return "string"
            if isinstance(x, list): return "list"
            if isinstance(x, dict): return "table"
            if isinstance(x, CreamFunction): return "action"
            if isinstance(x, CreamLambda): return "lambda"
            if isinstance(x, CreamStruct): return "struct"
            if isinstance(x, CreamStructType): return "struct_type"
            if callable(x): return "builtin"
            return "unknown"
        env.set("type", _Builtin(cream_type, "type"))

        def cream_help(args):
            if not args:
                names = sorted(interp.docs.keys())
                print("Available builtins:")
                for n in names:
                    doc = interp.docs.get(n, ""); brief = doc.split(" - ")[1] if " - " in doc else doc
                    print(f"  {n:<14} {brief}")
                return None
            name = cs(args[0])
            if name in interp.docs: print(interp.docs[name]); return interp.docs[name]
            val = None
            try: val = env.get(name)
            except: pass
            if val and isinstance(val, CreamFunction) and val.doc: print(f"action {name}: {val.doc}"); return val.doc
            if val and isinstance(val, CreamStructType) and val.doc: print(f"struct {name}: {val.doc}"); return val.doc
            print(f"No documentation found for '{name}'"); return None
        env.set("help", _Builtin(cream_help, "help"))

        def cream_bench(args):
            import time as _t
            if len(args) < 2: raise CreamRuntimeError("bench: нужно bench(n, fn)", code=ErrorCode.ARITY_ERROR)
            n = int(args[0]); fn = args[1]; times = []
            for _ in range(n):
                start = _t.perf_counter()
                if isinstance(fn, CreamFunction):
                    local = Environment(fn.closure); interp.call_stack.append(fn.name)
                    try: interp.exec_block(fn.body, local)
                    except ReturnSignal: pass
                    finally: interp.call_stack.pop()
                elif isinstance(fn, CreamLambda):
                    local = Environment(fn.closure); interp.eval_expr(fn.body, local)
                elif callable(fn): fn([])
                elapsed = (_t.perf_counter() - start) * 1000; times.append(elapsed)
            avg = sum(times) / len(times); mn = min(times); mx = max(times)
            print(f"bench: {n} iterations, avg: {avg:.4f} ms, min: {mn:.4f} ms, max: {mx:.4f} ms")
            return {"avg": avg, "min": mn, "max": mx, "n": n}
        env.set("bench", _Builtin(cream_bench, "bench"))

        def cream_time_fn(args):
            import time as _t
            if not args: raise CreamRuntimeError("time: нужно time(fn)", code=ErrorCode.ARITY_ERROR)
            fn = args[0]; start = _t.perf_counter(); result = None
            if isinstance(fn, CreamFunction):
                local = Environment(fn.closure); interp.call_stack.append(fn.name)
                try: interp.exec_block(fn.body, local)
                except ReturnSignal as r: result = r.value
                finally: interp.call_stack.pop()
            elif isinstance(fn, CreamLambda):
                local = Environment(fn.closure); result = interp.eval_expr(fn.body, local)
            elif callable(fn): result = fn([])
            elapsed = (_t.perf_counter() - start) * 1000
            print(f"time: {elapsed:.4f} ms"); return elapsed
        env.set("time", _Builtin(cream_time_fn, "time"))

        def cream_pkg(args):
            if not args: raise CreamRuntimeError("pkg: нужна операция", code=ErrorCode.ARITY_ERROR)
            op = cs(args[0]); pkg_dir = interp._pkg_dir()
            if op == "list":
                pkgs = []
                if _os.path.isdir(pkg_dir):
                    for d in sorted(_os.listdir(pkg_dir)):
                        if _os.path.isdir(_os.path.join(pkg_dir, d)) or d.endswith('.cream'):
                            pkgs.append(d.replace('.cream', ''))
                if not pkgs: print("No packages installed")
                else:
                    print("Installed packages:")
                    for p in pkgs: print(f"  {p}")
                return pkgs
            if op == "install":
                if len(args) < 2: raise CreamRuntimeError("pkg install: нужно имя", code=ErrorCode.ARITY_ERROR)
                name = cs(args[1]); p = _os.path.join(pkg_dir, name + ".cream")
                if _os.path.exists(p): print(f"Package '{name}' already installed"); return True
                content = f"-- Package: {name}\n"
                if len(args) > 2 and _os.path.exists(cs(args[2])):
                    with open(cs(args[2]), 'r', encoding='utf-8') as f: content = f.read()
                with open(p, 'w', encoding='utf-8') as f: f.write(content)
                print(f"Installed package '{name}'"); return True
            if op == "remove":
                if len(args) < 2: raise CreamRuntimeError("pkg remove: нужно имя", code=ErrorCode.ARITY_ERROR)
                name = cs(args[1]); p = _os.path.join(pkg_dir, name + ".cream")
                if _os.path.exists(p): _os.remove(p); print(f"Removed package '{name}'"); return True
                print(f"Package '{name}' not found"); return False
            if op == "info":
                if len(args) < 2: raise CreamRuntimeError("pkg info: нужно имя", code=ErrorCode.ARITY_ERROR)
                name = cs(args[1]); p = _os.path.join(pkg_dir, name + ".cream")
                if not _os.path.exists(p): print(f"Package '{name}' not found"); return None
                size = _os.path.getsize(p)
                with open(p, 'r', encoding='utf-8') as f: lines = f.read().split('\n')
                print(f"Package: {name}, {size} bytes, {len(lines)} lines"); return {"name": name, "size": size}
            if op == "search":
                if len(args) < 2: raise CreamRuntimeError("pkg search: нужно слово", code=ErrorCode.ARITY_ERROR)
                keyword = cs(args[1]).lower(); found = []
                if _os.path.isdir(pkg_dir):
                    for d in _os.listdir(pkg_dir):
                        if keyword in d.lower(): found.append(d.replace('.cream', ''))
                if not found: print(f"No packages matching '{keyword}'")
                else:
                    print(f"Packages matching '{keyword}':")
                    for p in found: print(f"  {p}")
                return found
            raise CreamRuntimeError(f"pkg: неизвестная операция '{op}'", code=ErrorCode.PKG_ERROR)
        env.set("pkg", _Builtin(cream_pkg, "pkg"))

        env.set("say",     _Builtin(lambda args: print(cs(args[0])) or None, "say"))
        env.set("input",   _Builtin(lambda args: input(cs(args[0]) if args else ""), "input"))
        env.set("length",  _Builtin(lambda args: len(args[0]), "length"))
        env.set("sum",     _Builtin(lambda args: sum(args[0]) if isinstance(args[0], list) else args[0], "sum"))
        env.set("min",     _Builtin(lambda args: min(args[0]) if isinstance(args[0], list) else args[0], "min"))
        env.set("max",     _Builtin(lambda args: max(args[0]) if isinstance(args[0], list) else args[0], "max"))
        env.set("abs",     _Builtin(lambda args: abs(args[0]), "abs"))
        env.set("round",   _Builtin(lambda args: round(args[0], int(args[1]) if len(args) > 1 else 0), "round"))
        env.set("number",  _Builtin(lambda args: float(args[0]) if '.' in str(args[0]) else int(float(str(args[0]))), "number"))
        env.set("bool",    _Builtin(lambda args: bool(args[0]), "bool"))
        env.set("range",   _Builtin(lambda args: list(range(int(args[0]), int(args[1]))), "range"))
        env.set("sort",    _Builtin(lambda args: sorted(args[0]), "sort"))
        env.set("reverse", _Builtin(lambda args: list(reversed(args[0])), "reverse"))
        env.set("first",   _Builtin(lambda args: args[0][0] if args[0] else None, "first"))
        env.set("last",    _Builtin(lambda args: args[0][-1] if args[0] else None, "last"))
        env.set("join",    _Builtin(lambda args: (cs(args[1]) if len(args) > 1 else ", ").join(cs(x) for x in args[0]), "join"))
        env.set("upper",   _Builtin(lambda args: str(args[0]).upper(), "upper"))
        env.set("lower",   _Builtin(lambda args: str(args[0]).lower(), "lower"))
        env.set("trim",    _Builtin(lambda args: str(args[0]).strip(), "trim"))
        env.set("split",   _Builtin(lambda args: str(args[0]).split(str(args[1]) if len(args) > 1 else " "), "split"))
        env.set("contains",_Builtin(lambda args: args[1] in args[0], "contains"))
        env.set("PI", _math.pi); env.set("E", _math.e); env.set("INF", _math.inf)

        def cream_math(args):
            x = args[0]
            if len(args) == 1: return x
            op = args[1]
            if op == "sqrt": return _math.sqrt(x)
            if op == "pow":  return _math.pow(x, args[2])
            if op == "log":  return _math.log(x, args[2]) if len(args) > 2 else _math.log(x)
            if op == "log2": return _math.log2(x)
            if op == "log10": return _math.log10(x)
            if op == "sin":  return _math.sin(_math.radians(x))
            if op == "cos":  return _math.cos(_math.radians(x))
            if op == "tan":  return _math.tan(_math.radians(x))
            if op == "asin": return _math.degrees(_math.asin(x))
            if op == "acos": return _math.degrees(_math.acos(x))
            if op == "atan": return _math.degrees(_math.atan(x))
            if op == "floor": return _math.floor(x)
            if op == "ceil": return _math.ceil(x)
            if op == "round": return round(x, int(args[2]) if len(args) > 2 else 0)
            if op == "abs": return abs(x)
            if op == "factorial": return _math.factorial(int(x))
            if op == "gcd": return _math.gcd(int(x), int(args[2]))
            if op == "lcm":
                a, b = int(x), int(args[2]); return abs(a * b) // _math.gcd(a, b)
            if op == "prime":
                n = int(x)
                if n < 2: return False
                for i in range(2, int(_math.sqrt(n)) + 1):
                    if n % i == 0: return False
                return True
            if op == "digits": return [int(d) for d in str(abs(int(x)))]
            if op == "binary": return bin(int(x))[2:]
            if op == "hex":    return hex(int(x))[2:]
            if op == "octal":  return oct(int(x))[2:]
            if op == "clamp":  return max(args[2], min(args[3], x))
            if op == "sign":   return (1 if x > 0 else -1 if x < 0 else 0)
            if op == "percent": return (x / args[2]) * 100 if len(args) > 2 else x / 100
            raise CreamRuntimeError(f"math: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("math", _Builtin(cream_math, "math"))

        def cream_num(args):
            x = args[0]
            if len(args) == 1:
                try: return int(x) if '.' not in str(x) else float(x)
                except: return 0
            op = args[1]
            if op == "int": return int(float(x))
            if op == "float": return float(x)
            if op == "is":
                try: float(x); return True
                except: return False
            if op == "between": return args[2] <= x <= args[3]
            if op == "format": return f"{x:.{int(args[2])}f}"
            if op == "positive": return x > 0
            if op == "negative": return x < 0
            if op == "zero": return x == 0
            if op == "even": return int(x) % 2 == 0
            if op == "odd": return int(x) % 2 != 0
            raise CreamRuntimeError(f"num: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("num", _Builtin(cream_num, "num"))

        def cream_rand(args):
            if not args: return _random.random()
            if len(args) == 1:
                a = args[0]
                if isinstance(a, str):
                    if a == "uuid": import uuid; return str(uuid.uuid4())
                    if a == "coin": return _random.choice([True, False])
                    if a == "dice": return _random.randint(1, 6)
                if isinstance(a, (int, float)): return _random.randint(0, int(a))
                if isinstance(a, list): return _random.choice(a)
            if len(args) == 2:
                op = args[0]
                if op == "list": return _random.choice(args[1])
                if op == "shuffle": return _random.sample(args[1], len(args[1]))
                if op == "dice": return _random.randint(1, int(args[1]))
                if isinstance(op, (int, float)): return _random.randint(int(op), int(args[1]))
            if len(args) == 3 and args[0] == "sample":
                return _random.sample(args[1], int(args[2]))
            return _random.random()
        env.set("rand", _Builtin(cream_rand, "rand"))

        def cream_stats(args):
            lst = args[0]
            if not lst: return None
            if len(args) == 1:
                return {"mean": _statistics.mean(lst), "median": _statistics.median(lst),
                        "std": _statistics.stdev(lst) if len(lst) > 1 else 0,
                        "min": min(lst), "max": max(lst), "sum": sum(lst), "count": len(lst),
                        "range": max(lst) - min(lst)}
            op = args[1]
            if op == "mean": return _statistics.mean(lst)
            if op == "median": return _statistics.median(lst)
            if op == "mode": return _statistics.mode(lst)
            if op == "std": return _statistics.stdev(lst) if len(lst) > 1 else 0
            if op == "variance": return _statistics.variance(lst) if len(lst) > 1 else 0
            if op == "min": return min(lst)
            if op == "max": return max(lst)
            if op == "sum": return sum(lst)
            if op == "count": return len(lst)
            if op == "range": return max(lst) - min(lst)
            if op == "unique": return list(dict.fromkeys(lst))
            if op == "freq":
                freq = {}
                for x in lst: freq[x] = freq.get(x, 0) + 1
                return freq
            raise CreamRuntimeError(f"stats: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("stats", _Builtin(cream_stats, "stats"))

        def cream_list(args):
            lst = list(args[0])
            if len(args) == 1: return lst
            op = args[1]
            if op == "add": lst.append(args[2]); return lst
            if op == "remove":
                if args[2] in lst: lst.remove(args[2]); return lst
            if op == "pop":
                i = int(args[2]) if len(args) > 2 else -1; lst.pop(i); return lst
            if op == "insert": lst.insert(int(args[2]), args[3]); return lst
            if op == "has": return args[2] in lst
            if op == "index": return lst.index(args[2]) if args[2] in lst else -1
            if op == "count": return lst.count(args[2])
            if op == "slice": return lst[int(args[2]):int(args[3]) if len(args) > 3 else len(lst)]
            if op == "flat":
                result = []
                for item in lst:
                    if isinstance(item, list): result.extend(item)
                    else: result.append(item)
                return result
            if op == "zip": return [[a, b] for a, b in zip(lst, args[2])]
            if op == "chunk": return [lst[i:i+int(args[2])] for i in range(0, len(lst), int(args[2]))]
            if op == "unique": return list(dict.fromkeys(lst))
            if op == "concat": return lst + list(args[2])
            if op == "reverse": return list(reversed(lst))
            if op == "sort": return sorted(lst)
            if op == "shuffle": _random.shuffle(lst); return lst
            if op == "sum": return sum(lst)
            if op == "min": return min(lst)
            if op == "max": return max(lst)
            if op == "first": return lst[0] if lst else None
            if op == "last": return lst[-1] if lst else None
            if op == "empty": return len(lst) == 0
            if op == "fill": return [args[3] if len(args) > 3 else 0] * int(args[2])
            raise CreamRuntimeError(f"list: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("list", _Builtin(cream_list, "list"))

        def cream_table(args):
            t = dict(args[0]) if isinstance(args[0], dict) else {}
            if len(args) == 1: return t
            op = args[1]
            if op == "get": return t.get(args[2])
            if op == "set": t[args[2]] = args[3]; return t
            if op == "has": return args[2] in t
            if op == "delete": t.pop(args[2], None); return t
            if op == "keys": return list(t.keys())
            if op == "values": return list(t.values())
            if op == "merge": return {**t, **args[2]}
            if op == "size": return len(t)
            if op == "empty": return len(t) == 0
            if op == "to_list": return [[k, v] for k, v in t.items()]
            raise CreamRuntimeError(f"table: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("table", _Builtin(cream_table, "table"))

        def cream_convert(args):
            x = float(args[0])
            if len(args) < 3: return x
            from_, to_ = str(args[1]).lower(), str(args[2]).lower()
            conv = {
                ("km","miles"): lambda v: v*0.621371, ("miles","km"): lambda v: v*1.60934,
                ("m","ft"): lambda v: v*3.28084, ("ft","m"): lambda v: v/3.28084,
                ("kg","lbs"): lambda v: v*2.20462, ("lbs","kg"): lambda v: v/2.20462,
                ("kg","g"): lambda v: v*1000, ("g","kg"): lambda v: v/1000,
                ("c","f"): lambda v: v*9/5+32, ("f","c"): lambda v: (v-32)*5/9,
                ("c","k"): lambda v: v+273.15, ("k","c"): lambda v: v-273.15,
                ("bytes","kb"): lambda v: v/1024, ("kb","mb"): lambda v: v/1024,
                ("mb","gb"): lambda v: v/1024, ("bytes","mb"): lambda v: v/(1024**2),
                ("bytes","gb"): lambda v: v/(1024**3), ("deg","rad"): lambda v: _math.radians(v),
                ("rad","deg"): lambda v: _math.degrees(v),
                ("hours","min"): lambda v: v*60, ("min","sec"): lambda v: v*60, ("hours","sec"): lambda v: v*3600,
            }
            fn = conv.get((from_, to_))
            if fn: return round(fn(x), 6)
            raise CreamRuntimeError(f"convert: не знаю как {from_} -> {to_}", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("convert", _Builtin(cream_convert, "convert"))

        def cream_date(args):
            now = _datetime.datetime.now()
            if not args or args[0] == "now":
                return {"year": now.year, "month": now.month, "day": now.day,
                        "hour": now.hour, "minute": now.minute, "second": now.second}
            if args[0] == "timestamp": return int(now.timestamp())
            if args[0] == "today": return now.strftime("%Y-%m-%d")
            if args[0] == "time": return now.strftime("%H:%M:%S")
            if args[0] == "format": return now.strftime(str(args[1]) if len(args) > 1 else "%Y-%m-%d")
            return str(now)
        env.set("date", _Builtin(cream_date, "date"))

        def cream_file(args):
            path = str(args[0])
            OPS = {"append","delete","exists","size","copy","move","rename","lines","json","csv","info","ext","name","dir"}
            if len(args) == 1:
                with open(path, 'r', encoding='utf-8') as f: return f.read()
            op = args[1]
            if not isinstance(op, str) or op not in OPS:
                with open(path, 'w', encoding='utf-8') as f: f.write(cs(op)); return True
            if op == "append":
                with open(path, 'a', encoding='utf-8') as f: f.write(cs(args[2])); return True
            if op == "delete":
                if _os.path.exists(path): _os.remove(path); return True
            if op == "exists": return _os.path.exists(path)
            if op == "size": return _os.path.getsize(path) if _os.path.exists(path) else 0
            if op == "copy": _shutil.copy2(path, str(args[2])); return True
            if op == "move": _shutil.move(path, str(args[2])); return True
            if op == "rename": _os.rename(path, str(args[2])); return True
            if op == "lines":
                with open(path, 'r', encoding='utf-8') as f: return [l.rstrip('\n') for l in f.readlines()]
            if op == "json":
                if len(args) > 2:
                    with open(path, 'w', encoding='utf-8') as f: _json.dump(args[2], f, ensure_ascii=False, indent=2); return True
                with open(path, 'r', encoding='utf-8') as f: return _json.load(f)
            if op == "csv":
                if len(args) > 2:
                    with open(path, 'w', newline='', encoding='utf-8') as f:
                        writer = _csv.writer(f)
                        for row in args[2]: writer.writerow(row)
                    return True
                with open(path, 'r', encoding='utf-8') as f: return list(_csv.reader(f))
            if op == "ext": return _os.path.splitext(path)[1]
            if op == "name": return _os.path.basename(path)
            if op == "dir": return _os.path.dirname(path)
            if op == "info":
                stat = _os.stat(path)
                return {"size": stat.st_size, "name": _os.path.basename(path),
                        "ext": _os.path.splitext(path)[1], "dir": _os.path.dirname(path)}
            raise CreamRuntimeError(f"file: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("file", _Builtin(cream_file, "file"))

        def cream_folder(args):
            path = str(args[0])
            if path == "current": return _os.getcwd()
            if path == "home": return _os.path.expanduser("~")
            if len(args) == 1: return _os.listdir(path) if _os.path.isdir(path) else []
            op = args[1]
            if op == "create": _os.makedirs(path, exist_ok=True); return True
            if op == "delete": _shutil.rmtree(path, ignore_errors=True); return True
            if op == "exists": return _os.path.isdir(path)
            if op == "copy": _shutil.copytree(path, str(args[2])); return True
            if op == "move": _shutil.move(path, str(args[2])); return True
            if op == "find":
                import glob as _gl
                return _gl.glob(_os.path.join(path, str(args[2])), recursive=True)
            if op == "files": return [f for f in _os.listdir(path) if _os.path.isfile(_os.path.join(path, f))]
            if op == "folders": return [f for f in _os.listdir(path) if _os.path.isdir(_os.path.join(path, f))]
            raise CreamRuntimeError(f"folder: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("folder", _Builtin(cream_folder, "folder"))

        def cream_sys(args):
            import sys as _sys
            if not args: return _sys.platform
            op = str(args[0])
            if op == "os": return _sys.platform
            if op == "args": return _sys.argv[1:]
            if op == "exit": _sys.exit(int(args[1]) if len(args) > 1 else 0)
            if op == "run":
                r = _subprocess.run(str(args[1]), shell=True, capture_output=True, text=True)
                return {"output": r.stdout, "error": r.stderr, "code": r.returncode}
            if op == "env":
                if len(args) > 2: _os.environ[str(args[1])] = str(args[2]); return True
                return _os.environ.get(str(args[1]), "")
            if op == "sleep": _time_mod.sleep(float(args[1])); return None
            if op == "time": return int(_time_mod.time())
            if op == "cwd": return _os.getcwd()
            if op == "cd": _os.chdir(str(args[1])); return True
            if op == "cpu":
                try: import multiprocessing; return multiprocessing.cpu_count()
                except: return 1
            raise CreamRuntimeError(f"sys: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("sys_", _Builtin(cream_sys, "sys_"))
        env.set("sys",  _Builtin(cream_sys, "sys"))

        def cream_encode(args):
            x = args[0]
            if len(args) < 2: return str(x)
            op = str(args[1]); mode = str(args[2]).lower() if len(args) > 2 else ""
            if op == "base64":
                if mode in ("de","decode"): return _base64.b64decode(str(x)).decode('utf-8')
                return _base64.b64encode(str(x).encode()).decode()
            if op == "md5": return _hashlib.md5(str(x).encode()).hexdigest()
            if op == "sha256": return _hashlib.sha256(str(x).encode()).hexdigest()
            if op == "sha1": return _hashlib.sha1(str(x).encode()).hexdigest()
            if op == "url":
                from urllib.parse import quote, unquote
                if mode in ("de","decode"): return unquote(str(x))
                return quote(str(x))
            if op == "json":
                if mode in ("de","decode"): return _json.loads(str(x))
                return _json.dumps(x, ensure_ascii=False)
            if op == "hex": return str(x).encode().hex()
            raise CreamRuntimeError(f"encode: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("encode", _Builtin(cream_encode, "encode"))

        def cream_str_fn(args):
            x = str(args[0])
            if len(args) == 1: return x
            op = str(args[1])
            if op == "upper": return x.upper()
            if op == "lower": return x.lower()
            if op == "title": return x.title()
            if op == "capitalize": return x.capitalize()
            if op == "trim":
                if len(args) > 2:
                    s = str(args[2])
                    if s == "left": return x.lstrip()
                    if s == "right": return x.rstrip()
                return x.strip()
            if op == "replace": return x.replace(str(args[2]), str(args[3]) if len(args) > 3 else "")
            if op == "remove": return x.replace(str(args[2]), "")
            if op == "split": return x.split(str(args[2]) if len(args) > 2 else " ")
            if op == "join": return x.join(cs(i) for i in args[2])
            if op == "contains": return str(args[2]) in x
            if op == "starts": return x.startswith(str(args[2]))
            if op == "ends": return x.endswith(str(args[2]))
            if op == "count": return x.count(str(args[2]))
            if op == "index": return x.find(str(args[2]))
            if op == "slice": return x[int(args[2]):int(args[3]) if len(args) > 3 else len(x)]
            if op == "repeat": return x * int(args[2])
            if op == "reverse": return x[::-1]
            if op == "length": return len(x)
            if op == "words": return x.split()
            if op == "lines": return x.splitlines()
            if op == "chars": return list(x)
            if op == "is_num": return x.replace('.','',1).replace('-','',1).isdigit()
            if op == "is_alpha": return x.isalpha()
            if op == "is_empty": return len(x.strip()) == 0
            if op == "pad":
                n = int(args[2]); side = str(args[3]) if len(args) > 3 else "right"
                char = str(args[4]) if len(args) > 4 else " "
                if side == "left": return x.rjust(n, char)
                if side == "both": return x.center(n, char)
                return x.ljust(n, char)
            if op == "between":
                a, b = str(args[2]), str(args[3])
                start = x.find(a); end = x.find(b, start + len(a))
                if start == -1 or end == -1: return ""
                return x[start + len(a):end]
            if op == "match": m = _re.search(str(args[2]), x); return m.group(0) if m else ""
            if op == "match_all": return _re.findall(str(args[2]), x)
            raise CreamRuntimeError(f"str: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("str_", _Builtin(cream_str_fn, "str_"))
        env.set("str",  _Builtin(cream_str_fn, "str"))

        def cream_regex(args):
            pat = str(args[0]); text = str(args[1]) if len(args) > 1 else ""
            if len(args) == 2:
                m = _re.search(pat, text); return m.group(0) if m else ""
            op = str(args[2])
            if op == "all": return _re.findall(pat, text)
            if op == "test": return bool(_re.search(pat, text))
            if op == "replace": return _re.sub(pat, str(args[3]) if len(args) > 3 else "", text)
            if op == "split": return _re.split(pat, text)
            if op == "groups": m = _re.search(pat, text); return list(m.groups()) if m else []
            if op == "count": return len(_re.findall(pat, text))
            raise CreamRuntimeError(f"regex: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("regex", _Builtin(cream_regex, "regex"))

        def cream_text_fn(args):
            x = str(args[0])
            if len(args) == 1: return x
            op = str(args[1])
            if op == "clean": return _re.sub(r'[^\w\s]', '', x)
            if op == "words": return len(x.split())
            if op == "truncate":
                n = int(args[2]); suffix = str(args[3]) if len(args) > 3 else "..."
                return x[:n] + suffix if len(x) > n else x
            if op == "slug":
                s = _re.sub(r'[^\w\s-]', '', x.lower().strip())
                return _re.sub(r'[\s_-]+', '-', s).strip('-')
            if op == "palindrome":
                c = _re.sub(r'[^a-zA-Z0-9]', '', x.lower()); return c == c[::-1]
            if op == "anagram":
                import re as re2
                return sorted(re2.sub(r'\s', '', x.lower())) == sorted(re2.sub(r'\s', '', str(args[2]).lower()))
            if op == "distance":
                a, b = x, str(args[2])
                dp = [[0]*(len(b)+1) for _ in range(len(a)+1)]
                for i in range(len(a)+1): dp[i][0] = i
                for j in range(len(b)+1): dp[0][j] = j
                for i in range(1, len(a)+1):
                    for j in range(1, len(b)+1):
                        dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+(0 if a[i-1]==b[j-1] else 1))
                return dp[len(a)][len(b)]
            if op == "similarity":
                a, b = x, str(args[2])
                if not a and not b: return 1.0
                if not a or not b: return 0.0
                dp = [[0]*(len(b)+1) for _ in range(len(a)+1)]
                for i in range(len(a)+1): dp[i][0] = i
                for j in range(len(b)+1): dp[0][j] = j
                for i in range(1, len(a)+1):
                    for j in range(1, len(b)+1):
                        dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+(0 if a[i-1]==b[j-1] else 1))
                return round(1 - dp[len(a)][len(b)] / max(len(a), len(b)), 3)
            if op == "extract":
                what = str(args[2])
                if what == "emails": return _re.findall(r'[\w.+-]+@[\w-]+\.[a-zA-Z]+', x)
                if what == "urls": return _re.findall(r'https?://\S+', x)
                if what == "numbers": return [float(n) if '.' in n else int(n) for n in _re.findall(r'-?\d+\.?\d*', x)]
                if what == "hashtags": return _re.findall(r'#\w+', x)
                if what == "mentions": return _re.findall(r'@\w+', x)
            raise CreamRuntimeError(f"text: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("text_", _Builtin(cream_text_fn, "text_"))

        COLORS = {"red":"\033[91m","green":"\033[92m","yellow":"\033[93m",
                  "blue":"\033[94m","cyan":"\033[96m","white":"\033[97m",
                  "gray":"\033[90m","reset":"\033[0m","bold":"\033[1m"}
        def cream_print(args):
            x = args[0] if args else ""
            if x == "line":
                n = int(args[1]) if len(args) > 1 else 40
                ch = str(args[2]) if len(args) > 2 else "-"; print(ch * n); return None
            if x == "clear": print("\033[H\033[J", end=""); return None
            if len(args) == 1: print(cs(x)); return None
            op = str(args[1])
            if op == "color": c = COLORS.get(str(args[2]), ""); print(f"{c}{cs(x)}{COLORS['reset']}")
            elif op == "bold": print(f"\033[1m{cs(x)}\033[0m")
            elif op == "end": print(cs(x), end=str(args[2]))
            else: print(cs(x))
            return None
        env.set("print_", _Builtin(cream_print, "print_"))

        def cream_net(args):
            from urllib import request as _req, parse as _parse, error as _uerr
            import json as _j
            if not args: raise CreamRuntimeError("net: нужен URL", code=ErrorCode.ARITY_ERROR)
            url = str(args[0])
            if url == "ip":
                try:
                    with _req.urlopen("https://api.ipify.org", timeout=5) as r: return r.read().decode()
                except: return "unknown"
            if url == "encode":
                params = args[1] if len(args) > 1 else {}
                if isinstance(params, dict): return _parse.urlencode(params)
                return _parse.quote(str(params))
            op = str(args[1]) if len(args) > 1 else "get"

            def do_request(method, data=None, headers=None, as_json=False):
                if data is not None:
                    if isinstance(data, dict):
                        if as_json: body = _j.dumps(data).encode(); ct = "application/json"
                        else: body = _parse.urlencode(data).encode(); ct = "application/x-www-form-urlencoded"
                    else: body = str(data).encode(); ct = "text/plain"
                else: body = None; ct = None
                req = _req.Request(url, data=body, method=method.upper())
                if ct: req.add_header("Content-Type", ct)
                req.add_header("User-Agent", "CreamLang/0.1")
                if headers and isinstance(headers, dict):
                    for k, v in headers.items(): req.add_header(str(k), str(v))
                try:
                    with _req.urlopen(req, timeout=10) as resp: return resp.read().decode("utf-8", errors="replace")
                except _uerr.HTTPError as e: raise CreamRuntimeError(f"net: HTTP {e.code} - {e.reason}", code=ErrorCode.FILE_NOT_FOUND)
                except _uerr.URLError as e: raise CreamRuntimeError(f"net: error - {e.reason}", code=ErrorCode.FILE_NOT_FOUND)

            if op == "get": return do_request("GET")
            if op == "json":
                text = do_request("GET")
                try: return _j.loads(text)
                except: return text
            if op == "post": return do_request("POST", data=args[2] if len(args) > 2 else {})
            if op == "post_json": return do_request("POST", data=args[2] if len(args) > 2 else {}, as_json=True)
            if op == "put": return do_request("PUT", data=args[2] if len(args) > 2 else {})
            if op == "delete": return do_request("DELETE")
            if op == "head":
                req = _req.Request(url, method="HEAD"); req.add_header("User-Agent", "CreamLang/0.1")
                try:
                    with _req.urlopen(req, timeout=10) as resp: return dict(resp.headers)
                except _uerr.HTTPError as e: raise CreamRuntimeError(f"net: HTTP {e.code}", code=ErrorCode.FILE_NOT_FOUND)
                except _uerr.URLError as e: raise CreamRuntimeError(f"net: {e.reason}", code=ErrorCode.FILE_NOT_FOUND)
            if op == "status":
                req = _req.Request(url); req.add_header("User-Agent", "CreamLang/0.1")
                try:
                    with _req.urlopen(req, timeout=10) as resp: return resp.status
                except _uerr.HTTPError as e: return e.code
                except: return 0
            if op == "download":
                path = str(args[2]) if len(args) > 2 else "download"
                try: _req.urlretrieve(url, path); return True
                except Exception as e: raise CreamRuntimeError(f"net: {e}", code=ErrorCode.FILE_NOT_FOUND)
            if op == "headers": return do_request("GET", headers=args[2] if len(args) > 2 else {})
            raise CreamRuntimeError(f"net: неизвестная операция '{op}'", code=ErrorCode.UNKNOWN_BUILTIN)
        env.set("net", _Builtin(cream_net, "net"))

    def _cream_str(self, value):
        if value is None: return "empty"
        if value is True: return "yes"
        if value is False: return "no"
        if isinstance(value, list):
            return "[" + ", ".join(self._cream_str(x) for x in value) + "]"
        if isinstance(value, dict):
            items = ", ".join(f"{k}: {self._cream_str(v)}" for k, v in value.items())
            return "{" + items + "}"
        if isinstance(value, float) and value == int(value): return str(int(value))
        return str(value)

    def _interpolate(self, s, env):
        import re as _re_local
        def replace(m):
            var_name = m.group(1)
            try: return self._cream_str(env.get(var_name))
            except: return m.group(0)
        return _re_local.sub(r'\{(\w+)\}', replace, s)

    def _enrich_error(self, e, node):
        if not e.line and hasattr(node, 'line') and node.line: e.line = node.line
        if not e.call_stack and self.call_stack: e.call_stack = list(self.call_stack)
        if not e.source and self._source: e.source = self._source
        return e

    def _collect_docs(self, node):
        if hasattr(node, 'doc') and node.doc:
            name = None
            if isinstance(node, (ActionDef, TaskDef)): name = node.name
            elif isinstance(node, StructDef): name = node.name
            if name: self.docs[name] = node.doc

    def _check_type(self, value, type_name):
        TN = type_name.lower()
        if TN == "number":   return isinstance(value, (int, float)) and not isinstance(value, bool)
        if TN == "string":   return isinstance(value, str)
        if TN == "bool":     return isinstance(value, bool)
        if TN == "empty":    return value is None
        if TN == "list":     return isinstance(value, list)
        if TN == "table":    return isinstance(value, dict)
        if TN == "action":   return isinstance(value, CreamFunction)
        if TN == "lambda":   return isinstance(value, CreamLambda)
        if TN == "struct":   return isinstance(value, CreamStruct)
        if TN == "function": return isinstance(value, (CreamFunction, CreamLambda)) or callable(value)
        return False

    def exec_block(self, stmts, env):
        for stmt in stmts:
            self.exec_stmt(stmt, env)

    def exec_stmt(self, node, env):
        try:
            self._exec_stmt_core(node, env)
        except (BreakSignal, ContinueSignal, ReturnSignal):
            raise
        except CreamRuntimeError as e:
            self._enrich_error(e, node); raise

    def _exec_stmt_core(self, node, env):
        if isinstance(node, Assign):
            env.set(node.name, self.eval_expr(node.value, env))

        elif isinstance(node, AugAssign):
            current = env.get(node.name); right = self.eval_expr(node.value, env); op = node.op
            if op == "+":
                if isinstance(current, str) or isinstance(right, str): current = self._cream_str(current) + self._cream_str(right)
                else: current = current + right
            elif op == "-": current = current - right
            elif op == "*": current = current * right
            elif op == "/":
                if right == 0: raise CreamRuntimeError("Деление на ноль", code=ErrorCode.DIVISION_BY_ZERO)
                current = current / right
            elif op == "%": current = current % right
            env.assign(node.name, current)

        elif isinstance(node, MultiAssign):
            values = [self.eval_expr(v, env) for v in node.values]
            if len(values) == 1 and isinstance(values[0], list): values = values[0]
            for i, name in enumerate(node.names):
                env.set(name, values[i] if i < len(values) else None)

        elif isinstance(node, MatchStmt):
            subject = self.eval_expr(node.subject, env)
            for case in node.cases:
                if case.is_wildcard:
                    try: self.exec_block(case.body, Environment(env))
                    except BreakSignal: pass
                    break
                if subject == self.eval_expr(case.pattern, env):
                    try: self.exec_block(case.body, Environment(env))
                    except BreakSignal: pass
                    break

        elif isinstance(node, AssertStmt):
            cond = self.eval_expr(node.condition, env)
            if not cond:
                msg = "Assert failed"
                if node.message: msg = self._cream_str(self.eval_expr(node.message, env))
                raise CreamRuntimeError(msg, code=ErrorCode.ASSERT_ERROR, line=node.line, source=self._source)

        elif isinstance(node, GuardStmt):
            cond = self.eval_expr(node.condition, env)
            if not cond:
                self.exec_block(node.else_body, Environment(env))
                raise ContinueSignal()

        elif isinstance(node, Say):
            print(self._cream_str(self.eval_expr(node.value, env)))

        elif isinstance(node, Return):
            raise ReturnSignal(self.eval_expr(node.value, env))

        elif isinstance(node, If):
            if self.eval_expr(node.condition, env):
                self.exec_block(node.then_body, Environment(env))
            else:
                executed = False
                for cond, body in node.elseif_clauses:
                    if self.eval_expr(cond, env):
                        self.exec_block(body, Environment(env)); executed = True; break
                if not executed and node.else_body:
                    self.exec_block(node.else_body, Environment(env))

        elif isinstance(node, Repeat):
            count = int(self.eval_expr(node.count, env))
            for _ in range(count):
                try: self.exec_block(node.body, Environment(env))
                except BreakSignal: break
                except ContinueSignal: continue

        elif isinstance(node, ForEach):
            iterable = self.eval_expr(node.iterable, env)
            for idx, item in enumerate(iterable):
                local = Environment(env); local.set(node.var, item)
                if node.index_var: local.set(node.index_var, idx)
                try: self.exec_block(node.body, local)
                except BreakSignal: break
                except ContinueSignal: continue

        elif isinstance(node, While):
            while self.eval_expr(node.condition, env):
                try: self.exec_block(node.body, Environment(env))
                except BreakSignal: break
                except ContinueSignal: continue

        elif isinstance(node, ActionDef):
            self._collect_docs(node)
            env.set(node.name, CreamFunction(node.name, node.params, node.body, env, doc=node.doc))

        elif isinstance(node, TaskDef):
            self._collect_docs(node)
            env.set(node.name, CreamFunction(node.name, node.params, node.body, env, doc=node.doc))

        elif isinstance(node, StructDef):
            self._collect_docs(node)
            env.set(node.name, CreamStructType(node.name, node.fields, doc=node.doc))

        elif isinstance(node, TryCatch):
            try:
                self.exec_block(node.try_body, Environment(env))
            except CreamRuntimeError as e:
                local = Environment(env)
                local.set(node.error_var, {"message": str(e), "code": e.code or "", "line": e.line or 0})
                self.exec_block(node.catch_body, local)

        elif isinstance(node, Wait):
            self.eval_expr(node.value, env)

        elif isinstance(node, Import):
            self._exec_import(node.path, env)

        else:
            self.eval_expr(node, env)

    def eval_expr(self, node, env):
        try:
            return self._eval_expr_core(node, env)
        except CreamRuntimeError as e:
            self._enrich_error(e, node); raise

    def _eval_expr_core(self, node, env):
        if isinstance(node, NumberLiteral): return node.value
        if isinstance(node, BoolLiteral): return node.value
        if isinstance(node, EmptyLiteral): return None
        if isinstance(node, StringLiteral): return self._interpolate(node.value, env)
        if isinstance(node, Identifier): return env.get(node.name)
        if isinstance(node, ListLiteral):
            if node.spreads:
                result = []
                for i, elem in enumerate(node.elements):
                    if i in node.spreads:
                        val = self.eval_expr(elem, env)
                        if isinstance(val, list): result.extend(val)
                        else: result.append(val)
                    else: result.append(self.eval_expr(elem, env))
                return result
            return [self.eval_expr(e, env) for e in node.elements]
        if isinstance(node, ListComprehension):
            iterable = self.eval_expr(node.iterable, env); result = []
            for item in iterable:
                local = Environment(env); local.set(node.var, item)
                if node.condition and not self.eval_expr(node.condition, local): continue
                result.append(self.eval_expr(node.expr, local))
            return result
        if isinstance(node, TableLiteral):
            return {k: self.eval_expr(v, env) for k, v in node.pairs}
        if isinstance(node, Lambda): return CreamLambda(node.param, node.body, env)
        if isinstance(node, IsCheck):
            val = self.eval_expr(node.expr, env); return self._check_type(val, node.type_name)
        if isinstance(node, UnaryOp):
            val = self.eval_expr(node.operand, env)
            if node.op == "not": return not val
            if node.op == "-": return -val
        if isinstance(node, BinaryOp): return self.eval_binary(node, env)
        if isinstance(node, FieldAccess):
            obj = self.eval_expr(node.obj, env)
            if node.optional and obj is None: return None
            if isinstance(obj, CreamStruct):
                if node.field in obj.fields: return obj.fields[node.field]
                if node.optional: return None
                raise CreamRuntimeError(f"Поле '{node.field}' не найдено в {obj.type_name}", code=ErrorCode.FIELD_NOT_FOUND)
            if isinstance(obj, dict):
                val = obj.get(node.field)
                if val is None and node.field not in obj:
                    if node.optional: return None
                return val
            if node.optional: return None
            raise CreamRuntimeError(f"Нельзя получить поле у {type(obj).__name__}", code=ErrorCode.TYPE_ERROR)
        if isinstance(node, IndexAccess):
            obj = self.eval_expr(node.obj, env); index = self.eval_expr(node.index, env)
            try: return obj[int(index)]
            except (IndexError, KeyError, TypeError) as e:
                raise CreamRuntimeError(f"Ошибка индекса: {e}", code=ErrorCode.INDEX_ERROR)
        if isinstance(node, Call): return self.eval_call(node, env)
        if isinstance(node, Pipeline): return self.eval_pipeline(node, env)
        if isinstance(node, Wait): return self.eval_expr(node.value, env)
        raise CreamRuntimeError(f"Неизвестный узел: {type(node).__name__}", code=ErrorCode.UNKNOWN_NODE)

    def eval_binary(self, node, env):
        op = node.op
        if op == "and":
            left = self.eval_expr(node.left, env)
            return left and self.eval_expr(node.right, env) if left else left
        if op == "or":
            left = self.eval_expr(node.left, env)
            return left if left else self.eval_expr(node.right, env)
        left = self.eval_expr(node.left, env); right = self.eval_expr(node.right, env)
        if op == "+":
            if isinstance(left, str) or isinstance(right, str): return self._cream_str(left) + self._cream_str(right)
            return left + right
        if op == "-": return left - right
        if op == "*": return left * right
        if op == "/":
            if right == 0: raise CreamRuntimeError("Деление на ноль", code=ErrorCode.DIVISION_BY_ZERO)
            return left / right
        if op == "%":
            if right == 0: raise CreamRuntimeError("Деление на ноль", code=ErrorCode.DIVISION_BY_ZERO)
            return left % right
        if op == "==": return left == right
        if op == "!=": return left != right
        if op == ">":  return left > right
        if op == "<":  return left < right
        if op == ">=": return left >= right
        if op == "<=": return left <= right
        raise CreamRuntimeError(f"Неизвестный оператор: {op}", code=ErrorCode.UNKNOWN_OPERATOR)

    def eval_call(self, node, env):
        callee = self.eval_expr(node.callee, env)
        args = [self.eval_expr(a, env) for a in node.args]
        if isinstance(callee, _Builtin): return callee.fn(args)
        if callable(callee) and not isinstance(callee, (CreamFunction, CreamLambda, CreamStructType)):
            return callee(args)
        if isinstance(callee, CreamFunction):
            self.call_stack.append(callee.name); local = Environment(callee.closure)
            for i, (param_name, param_default) in enumerate(callee.params):
                if i < len(args): local.set(param_name, args[i])
                elif param_default is not None: local.set(param_name, self.eval_expr(param_default, env))
                else: self.call_stack.pop()
                raise CreamRuntimeError(f"Не передан аргумент '{param_name}' в {callee.name}()", code=ErrorCode.ARITY_ERROR)
            try:
                is_tail = (len(callee.body) == 1 and isinstance(callee.body[0], Return)
                           and isinstance(callee.body[0].value, Call))
                if is_tail:
                    result = None
                    while True:
                        try: self.exec_block(callee.body, local); break
                        except ReturnSignal as r:
                            ret_node = callee.body[0].value
                            if isinstance(ret_node, Call):
                                new_callee = self.eval_expr(ret_node.callee, local)
                                if isinstance(new_callee, CreamFunction) and new_callee.name == callee.name:
                                    local = Environment(new_callee.closure)
                                    new_args = [self.eval_expr(a, local) for a in ret_node.args]
                                    for j, (pn, pd) in enumerate(new_callee.params):
                                        if j < len(new_args): local.set(pn, new_args[j])
                                        elif pd is not None: local.set(pn, self.eval_expr(pd, local))
                                    continue
                            result = r.value; break
                    self.call_stack.pop(); return result
                else:
                    self.exec_block(callee.body, local)
                    self.call_stack.pop(); return None
            except ReturnSignal as r:
                self.call_stack.pop(); return r.value
            except CreamRuntimeError as e:
                self.call_stack.pop()
                if not e.call_stack: e.call_stack = list(self.call_stack)
                raise
        if isinstance(callee, CreamLambda):
            local = Environment(callee.closure); local.set(callee.param, args[0] if args else None)
            return self.eval_expr(callee.body, local)
        if isinstance(callee, CreamStructType):
            fields = {}
            for i, (fname, ftype, fdefault) in enumerate(callee.fields):
                if i < len(args): fields[fname] = args[i]
                elif fdefault is not None: fields[fname] = self.eval_expr(fdefault, env)
                else: raise CreamRuntimeError(f"Не передано поле '{fname}'", code=ErrorCode.ARITY_ERROR)
            return CreamStruct(callee.name, fields)
        raise CreamRuntimeError(f"'{callee}' не является функцией", code=ErrorCode.NOT_CALLABLE)

    def eval_pipeline(self, node, env):
        value = self.eval_expr(node.value, env)
        for step in node.steps:
            if isinstance(step, Identifier):
                name = step.name
                if name == "sum": value = sum(value)
                elif name == "sort": value = sorted(value)
                elif name == "reverse": value = list(reversed(value))
                elif name == "first": value = value[0] if value else None
                elif name == "last": value = value[-1] if value else None
                elif name == "length": value = len(value)
                else: value = self._apply_fn(env.get(name), value, env)
            elif isinstance(step, Call):
                fn_name = step.callee.name if isinstance(step.callee, Identifier) else None
                fn_args = [self.eval_expr(a, env) for a in step.args]; fn = fn_args[0] if fn_args else None
                if fn_name == "filter": value = [x for x in value if self._apply_fn(fn, x, env)]
                elif fn_name == "map": value = [self._apply_fn(fn, x, env) for x in value]
                elif fn_name == "sort": value = sorted(value, key=lambda x: self._apply_fn(fn, x, env))
                elif fn_name == "reduce":
                    from functools import reduce
                    value = reduce(lambda a, b: self._apply_fn2(fn, a, b, env), value)
                else: value = self._apply_fn(self.eval_expr(step.callee, env), value, env)
            else: value = self._apply_fn(self.eval_expr(step, env), value, env)
        return value

    def _apply_fn(self, fn, value, env):
        if isinstance(fn, CreamLambda):
            local = Environment(fn.closure); local.set(fn.param, value)
            return self.eval_expr(fn.body, local)
        if isinstance(fn, CreamFunction):
            local = Environment(fn.closure); local.set(fn.params[0][0], value)
            try: self.exec_block(fn.body, local); return None
            except ReturnSignal as r: return r.value
        if isinstance(fn, _Builtin): return fn.fn([value])
        if callable(fn): return fn([value])
        raise CreamRuntimeError(f"Не является функцией: {fn}", code=ErrorCode.NOT_CALLABLE)

    def _apply_fn2(self, fn, a, b, env):
        if isinstance(fn, CreamLambda):
            local = Environment(fn.closure); local.set(fn.param, a)
            return self.eval_expr(fn.body, local)
        if isinstance(fn, CreamFunction):
            local = Environment(fn.closure)
            if len(fn.params) >= 2: local.set(fn.params[0][0], a); local.set(fn.params[1][0], b)
            elif len(fn.params) == 1: local.set(fn.params[0][0], a)
            try: self.exec_block(fn.body, local); return None
            except ReturnSignal as r: return r.value
        raise CreamRuntimeError("reduce требует лямбду или action с 2 параметрами", code=ErrorCode.TYPE_ERROR)

    def _exec_import(self, path, env):
        import os as _os
        if not _os.path.isabs(path):
            base = getattr(self, '_base_dir', _os.getcwd())
            full_path = _os.path.join(base, path)
        else: full_path = path
        if not full_path.endswith('.cream'): full_path += '.cream'
        if not _os.path.exists(full_path):
            pkg_path = _os.path.join(self._pkg_dir(), _os.path.basename(full_path))
            if _os.path.exists(pkg_path): full_path = pkg_path
            else: raise CreamRuntimeError(f"import: файл не найден - '{full_path}'", code=ErrorCode.FILE_NOT_FOUND)
        if not hasattr(self, '_imported'): self._imported = set()
        if full_path in self._imported: return
        self._imported.add(full_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f: source = f.read()
        except Exception as e:
            raise CreamRuntimeError(f"import: не удалось прочитать '{full_path}' - {e}", code=ErrorCode.IMPORT_ERROR)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens, source=source).parse()
        self.exec_block(ast.body, env)

    def run(self, source, base_dir=None):
        import os as _os
        self._base_dir = base_dir or _os.getcwd()
        self._source = source
        cache_key = _hashlib_std.md5(source.encode('utf-8')).hexdigest() if len(source) < 100000 else None
        if cache_key:
            cached_ast = _cache_get(_ast_cache, cache_key)
            if cached_ast:
                try: self.exec_block(cached_ast.body, self.global_env)
                except (BreakSignal, ContinueSignal): pass
                return
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens, source=source).parse()
        if cache_key: _cache_set(_ast_cache, cache_key, ast)
        try: self.exec_block(ast.body, self.global_env)
        except (BreakSignal, ContinueSignal): pass

    def generate_docs(self, source):
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens, source=source).parse()
        output = []; current_doc = None
        for node in ast.body:
            if hasattr(node, 'doc') and node.doc: current_doc = node.doc
            if isinstance(node, (ActionDef, TaskDef)):
                params = ", ".join(p[0] for p in node.params)
                kind = "action" if isinstance(node, ActionDef) else "task"
                entry = f"## {kind} {node.name}({params})"
                if current_doc: entry += f"\n\n{current_doc}"
                output.append(entry); current_doc = None
            elif isinstance(node, StructDef):
                fields = "\n".join(f"  - {f[0]}: {f[1]}" for f in node.fields)
                entry = f"## struct {node.name}"
                if current_doc: entry += f"\n\n{current_doc}\n\n{fields}"
                else: entry += f"\n\n{fields}"
                output.append(entry); current_doc = None
            else: current_doc = None
        return "\n\n".join(output)

def run_file(path):
    try:
        import os as _os
        with open(path, 'r', encoding='utf-8') as f: source = f.read()
        interp = Interpreter()
        interp.run(source, base_dir=_os.path.dirname(_os.path.abspath(path)))
    except FileNotFoundError: print(f"File not found: {path}")
    except (LexerError, ParseError, CreamRuntimeError) as e: print(f"{e}")

def run_doc(path):
    import os as _os
    try:
        with open(path, 'r', encoding='utf-8') as f: source = f.read()
        interp = Interpreter()
        docs = interp.generate_docs(source)
        if not docs: print("No documentation found."); return
        out_path = path.replace('.cream', '_docs.md')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(f"# Documentation: {_os.path.basename(path)}\n\n{docs}\n")
        print(f"Documentation generated: {out_path}\n{docs}")
    except FileNotFoundError: print(f"File not found: {path}")
    except Exception as e: print(f"Error: {e}")

def run_test(path):
    import io, contextlib
    try:
        with open(path, 'r', encoding='utf-8') as f: source = f.read()
        interp = Interpreter(); output_buf = io.StringIO()
        with contextlib.redirect_stdout(output_buf): interp.run(source)
        result = output_buf.getvalue()
        if result: print(result)
        print(f"All tests in {path} passed.")
    except FileNotFoundError: print(f"File not found: {path}")
    except CreamRuntimeError as e: print(f"Test failed: {e}")
    except Exception as e: print(f"Error: {e}")

def run_benchmark(path):
    import time as _t
    try:
        with open(path, 'r', encoding='utf-8') as f: source = f.read()
        times = []
        for i in range(5):
            interp = Interpreter(); start = _t.perf_counter()
            interp.run(source); elapsed = (_t.perf_counter() - start) * 1000
            times.append(elapsed); print(f"  Run {i+1}: {elapsed:.4f} ms")
        avg = sum(times) / len(times); mn = min(times); mx = max(times)
        print(f"\n  avg: {avg:.4f} ms | min: {mn:.4f} ms | max: {mx:.4f} ms")
    except FileNotFoundError: print(f"File not found: {path}")
    except Exception as e: print(f"Error: {e}")

def _get_history_path():
    import os as _os
    d = _os.path.join(_os.path.expanduser("~"), ".cream")
    _os.makedirs(d, exist_ok=True)
    return _os.path.join(d, "history")

def _load_history(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f.readlines()[-1000:]]
    except: return []

def _save_history(path, history):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for line in history[-1000:]: f.write(line + '\n')
    except: pass

def repl():
    print("=" * 45)
    print("  Cream Language v0.1")
    print("  Type Cream code and press Enter.")
    print("  Type 'exit' to quit. 'help' for docs.")
    print("=" * 45)
    print()
    interp = Interpreter(); buffer = []
    hist_path = _get_history_path(); history = _load_history(hist_path)
    while True:
        try:
            prompt = "... " if buffer else "cream> "
            line = input(prompt)
            history.append(line)
            if line.strip() in ("exit", "quit", "q"):
                _save_history(hist_path, history); print("Goodbye!"); break
            if not line.strip():
                if buffer:
                    code = "\n".join(buffer); buffer = []
                    try: interp.run(code)
                    except (LexerError, ParseError, CreamRuntimeError) as e: print(f"{e}")
                continue
            stripped = line.strip()
            keywords_with_block = ("if ", "else", "or if", "action ", "task ",
                                   "repeat ", "while ", "for each", "try", "struct ", "match ", "guard ")
            starts_block = any(stripped.startswith(kw) for kw in keywords_with_block)
            if starts_block or buffer: buffer.append(line)
            else:
                try: interp.run(line)
                except (LexerError, ParseError, CreamRuntimeError) as e: print(f"{e}")
        except (LexerError, ParseError, CreamRuntimeError) as e:
            print(f"{e}"); buffer = []
        except KeyboardInterrupt:
            if buffer: buffer = []; print("\n(cancelled)")
            else: _save_history(hist_path, history); print("\nGoodbye!"); break
        except (EOFError, OSError):
            _save_history(hist_path, history); print("\nGoodbye!"); break

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "doc" and len(sys.argv) > 2: run_doc(sys.argv[2])
        elif cmd == "test" and len(sys.argv) > 2: run_test(sys.argv[2])
        elif cmd == "benchmark" and len(sys.argv) > 2: run_benchmark(sys.argv[2])
        elif cmd == "help":
            interp = Interpreter(); interp.global_env.get("help").fn([])
        else: run_file(cmd)
        sys.exit()
    repl()
