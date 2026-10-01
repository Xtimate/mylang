from errors import LangError
from nodes import Num, Str, Var, BinOp, Let, Print

RT_FUNCS = {"+": "rt_add", "-": "rt_sub", "*": "rt_mul", "/": "rt_div"}

def c_string(s):
    return '"' + s.replace("\\", "\\\\") + '"'

class CodeGen:
    def __init__(self):
        self.declared = {}
        self.lines = []

    def check_declared(self, node):
        if node.name not in self.declared:
            raise LangError(f"undefined variable '{node.name}'", node.line, node.col)

    def use(self, node):
        self.check_declared(node)
        return f'rt_use(&v_{node.name}, "{node.name}")'

    def move(self, node):
        self.check_declared(node)
        return f'rt_move(&v_{node.name}, "{node.name}")'

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

    def stmt(self, node):
        match node:
            case Let(name=name, value=value):
                code = self.move(value) if isinstance(value, Var) else self.expr(value)
                if name in self.declared:
                    self.lines.append(f"    {{ Value t = {code}; rt_drop(&v_{name}); v_{name} = t; }}")
                else:
                    self.declared[name] = True
                    self.lines.append(f"    Value v_{name} = {code};")
            case Print(value=value):
                if isinstance(value, Var):
                    self.lines.append(f"    rt_print({self.use(value)});")
                else:
                    self.lines.append(f"    {{ Value t = {self.expr(value)}; rt_print(t); rt_drop(&t); }}")
            case _:
                raise AssertionError(f"unknown statement node {node}")

def generate(program):
    gen = CodeGen()
    for s in program:
        gen.stmt(s)
    for name in reversed(list(gen.declared)):
        gen.lines.append(f"    rt_drop(&v_{name});")
    body = "\n".join(gen.lines)
    header = '#include "rt.h"'
    return header + "\n\nint main(void) {\n" + body + "\n    return 0;\n}\n"
