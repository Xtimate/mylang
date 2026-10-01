import sys
from errors import LangError
from lexer import lex
from parser import Parser
from codegen import generate

def main():
    if len(sys.argv) != 2:
        print("usage: main.py <file.lang>", file=sys.stderr)
        sys.exit(2)

    path = sys.argv[1]
    with open(path) as f:
        src = f.read()

    try:
        tokens = lex(src)
        program = Parser(tokens).parse_program()
        c_code = generate(program)
    except LangError as e:
        print(f"error: {path}:{e.line}:{e.col}: {e.message}", file=sys.stderr)
        lines = src.split("\n")
        if 1 <= e.line <= len(lines):
            print("  " + lines[e.line - 1], file=sys.stderr)
            print("  " + " " * (e.col - 1) + "^", file=sys.stderr)
        sys.exit(1)

    print(c_code)

main()
