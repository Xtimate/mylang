from errors import LangError
from nodes import Num, Var, BinOp, Let, Print

RT_FUNCS = {"+": "rt_add", "-": "rt_sub", "*": "rt_mul", "/": "rt_div"}

class CodeGen:
    def __init__(self):
        self.declared = set()
        self.lines = []

    def expr(self, node):
        match node:
            case Num(value=v):
                return f"rt_int({v})"
            case Var(name=n, line=l, col=c):
                if n not in self.declared:
                    raise LangError(f"undefined variable '{n}'", l, c)
                return f"v_{n}"
            case BinOp(op=op, left=left, right=right):
                return f"{RT_FUNCS[op]}({self.expr(left)}, {self.expr(right)})"
            case _:
                raise AssertionError(f"unknown expression node {node}")

    def stmt(self, node):
        if isinstance(node, Let):
            value = self.expr(node.value)
            if node.name in self.declared:
                self.lines.append(f"    v_{node.name} = {value};")
            else:
                self.declared.add(node.name)
                self.lines.append(f"    Value v_{node.name} = {value};")
        elif isinstance(node, Print):
            self.lines.append(f"    rt_print({self.expr(node.value)});")
        else:
            raise AssertionError(f"unknown statement node {node}")

def generate(program):
    gen = CodeGen()
    for s in program:
        gen.stmt(s)
    body = "\n".join(gen.lines)
    return f'#include "rt.h"\n\nint main(void) {{\n{body}\n    return 0;\n}}\n'
