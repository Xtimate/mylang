from errors import LangError
from nodes import Num, Str, Var, BinOp, Let, Print

def describe(tok):
    if tok.kind == "EOF":     return "end of file"
    if tok.kind == "NEWLINE": return "end of line"
    return repr(tok.text)

class Parser:
    def __init__(self, tokens):
        self.toks = tokens
        self.pos = 0

    def peek(self):
        return self.toks[self.pos]

    def advance(self):
        tok = self.toks[self.pos]
        self.pos += 1
        return tok

    def expect(self, kind):
        tok = self.peek()
        if tok.kind != kind:
            what = {"ID": "a name"}.get(kind, repr(kind))
            raise LangError(f"expected {what} but found {describe(tok)}", tok.line, tok.col)
        return self.advance()

    def parse_program(self):
        stmts = []
        while self.peek().kind != "EOF":
            if self.peek().kind == "NEWLINE":
                self.advance()
                continue
            stmts.append(self.statement())
            tok = self.peek()
            if tok.kind not in ("NEWLINE", "EOF"):
                raise LangError(f"unexpected {describe(tok)} after statement", tok.line, tok.col)
        return stmts

    def statement(self):
        tok = self.peek()
        match tok.kind:
            case "let":
                self.advance()
                name = self.expect("ID")
                self.expect("=")
                return Let(name.text, self.expr(), name.line)
            case "print":
                self.advance()
                self.expect("(")
                value = self.expr()
                self.expect(")")
                return Print(value)
            case _:
                raise LangError(f"expected a statement but found {describe(tok)}", tok.line, tok.col)

    def expr(self):
        node = self.term()
        while self.peek().kind in ("+", "-"):
            op = self.advance()
            node = BinOp(op.kind, node, self.term())
        return node

    def term(self):
        node = self.atom()
        while self.peek().kind in ("*", "/"):
            op = self.advance()
            node = BinOp(op.kind, node, self.atom())
        return node

    def atom(self):
        tok = self.peek()
        match tok.kind:
            case "NUM":
                self.advance()
                return Num(int(tok.text))
            case "STR":
                self.advance()
                return Str(tok.text[1:-1])
            case "ID":
                self.advance()
                return Var(tok.text, tok.line, tok.col)
            case "(":
                self.advance()
                node = self.expr()
                self.expect(")")
                return node
            case _:
                raise LangError(f"expected a value but found {describe(tok)}", tok.line, tok.col)
