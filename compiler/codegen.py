from errors import LangError
from nodes import Num, Str, Var, BinOp, Let, Assign, Print, If, While

RT_FUNCS = {
    "+": "rt_add", "-": "rt_sub", "*": "rt_mul", "/": "rt_div",
    "<": "rt_lt", ">": "rt_gt", "<=": "rt_le", ">=": "rt_ge",
    "==": "rt_eq", "!=": "rt_ne",
}

def c_string(s):
    return '"' + s.replace("\\", "\\\\") + '"'

class CodeGen:
    def __init__(self):
        self.scopes = []
        self.lines = []
        self.indent = 0
        self.counter = 0

    def emit(self, text):
        self.lines.append("    " * self.indent + text)

    def lookup(self, node):
        for scope in reversed(self.scopes):
            if node.name in scope["names"]:
                return scope["names"][node.name]
        raise LangError(f"undefined variable '{node.name}'", node.line, node.col)

    def declare(self, name):
        cname = f"v_{name}_{self.counter}"
        self.counter += 1
        self.scopes[-1]["names"][name] = cname
        self.scopes[-1]["owned"].append(cname)
        return cname

    def use(self, node):
        return f'rt_use(&{self.lookup(node)}, "{node.name}")'

    def move(self, node):
        return f'rt_move(&{self.lookup(node)}, "{node.name}")'

    def value_of(self, node):
        return self.move(node) if isinstance(node, Var) else self.expr(node)

    def expr(self, node):
        match node:
            case Num(value=v):
                return f"rt_int({v})"
            case Str(value=s):
                return f"rt_str({c_string(s)})"
            case Var():
                return self.use(node)
            case BinOp(op=op, left=left, right=right):
                return f"{RT_FUNCS[op]}({self.expr(left)}, {self.expr(right)})"
            case _:
                raise AssertionError(f"unknown expression node {node}")

    def body(self, stmts):
        self.scopes.append({"names": {}, "owned": []})
        self.indent += 1
        for s in stmts:
            self.stmt(s)
        scope = self.scopes.pop()
        for cname in reversed(scope["owned"]):
            self.emit(f"rt_drop(&{cname});")
        self.indent -= 1

    def stmt(self, node):
        match node:
            case Let(name=name, value=value):
                code = self.value_of(value)
                cname = self.declare(name)
                self.emit(f"Value {cname} = {code};")
            case Assign(name=name, value=value):
                cname = self.lookup(node)
                code = self.value_of(value)
                self.emit(f"{{ Value t = {code}; rt_drop(&{cname}); {cname} = t; }}")
            case Print(value=value):
                if isinstance(value, Var):
                    self.emit(f"rt_print({self.use(value)});")
                else:
                    self.emit(f"{{ Value t = {self.expr(value)}; rt_print(t); rt_drop(&t); }}")
            case If(cond=cond, then=then, els=els):
                self.emit(f"if (rt_truthy({self.expr(cond)})) {{")
                self.body(then)
                if els is not None:
                    self.emit("} else {")
                    self.body(els)
                self.emit("}")
            case While(cond=cond, body=body):
                self.emit(f"while (rt_truthy({self.expr(cond)})) {{")
                self.body(body)
                self.emit("}")
            case _:
                raise AssertionError(f"unknown statement node {node}")

def generate(program):
    gen = CodeGen()
    gen.body(program)
    body = "\n".join(gen.lines)
    header = '#include "rt.h"'
    return header + "\n\nint main(void) {\n" + body + "\n    return 0;\n}\n"
