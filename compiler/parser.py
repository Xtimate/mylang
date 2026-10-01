from errors import LangError
from nodes import Num, Var, BinOp, Let, Print

def describe(tok):
    if tok.kind == "EOF": return "end of file"
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
            raise LangError(f"expected {what} but got {describe(tok)}", tok.line, tok.col)
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
        if tok.kind == "let":
            self.advance()
            name = self.expect("ID")
            self.expect("=")
            return Let(name.text, self.expr(), name.line)
        if tok.kind == "print":
            self.advance()
            self.expect("(")
            value = self.expr()
            self.expect(")")
            return Print(value)
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
        if tok.kind == "NUM":
            self.advance()
            return Num(int(tok.text))
        if tok.kind == "ID":
            self.advance()
            return Var(tok.text, tok.line, tok.col)
        if tok.kind == "(":
            self.advance()
            node = self.expr()
            self.expect(")")
            return node
        raise LangError(f"expected a value but found {describe(tok)}", tok.line, tok.col)
