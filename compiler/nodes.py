from dataclasses import dataclass

@dataclass
class Num:
    value: int

@dataclass
class Var:
    name: str
    line: int
    col: int

@dataclass
class BinOp:
    op: str
    left: object
    right: object

@dataclass
class Let:
    name: str
    value: object
    line: int

@dataclass
class Print:
    value: object
