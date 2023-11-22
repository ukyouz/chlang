from dataclasses import dataclass
from dataclasses import field


@dataclass
class Statement:
    ...


@dataclass
class Program(Statement):
    body: list[Statement] = field(default_factory=list)


@dataclass
class Expression(Statement):
    ...


@dataclass
class BinaryExpr(Expression):
    left: Expression
    right: Expression
    operator: str


@dataclass
class Identifier(Expression):
    symbol: str


@dataclass
class NumberLiteral(Expression):
    value: int | float


