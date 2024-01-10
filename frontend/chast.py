from dataclasses import dataclass
from dataclasses import field


# ====================================
@dataclass
class Statement:
    ...


@dataclass
class Expression(Statement):
    ...


# ====================================

"""
Statements
  no actual computed value,
  can not chain with other statements
"""

@dataclass
class Program(Statement):
    body: list[Statement] = field(default_factory=list)


@dataclass
class VariableDeclaration(Statement):
    identifier: str
    value: Expression | None
    const: bool


@dataclass
class FunctionDeclaration(Statement):
    name: str
    params: list[str]
    body: list[Statement]


@dataclass
class IfStatement(Statement):
    test: Expression
    consequent: list[Statement]
    alternate: list[Statement]


"""
Expressions
    can be evaluated to a value,
    can be chained with other expressions
"""


@dataclass
class AssignmentExpr(Expression):
    assigne: Expression
    value: Expression


@dataclass
class CallExpr(Expression):
    caller: Expression
    args: list[Expression]


@dataclass
class MemberExpr(Expression):
    obj: Expression
    prop: Expression
    computed: bool


""" Literals """


@dataclass
class BinaryExpr(Expression):
    left: Expression
    right: Expression
    operator: str


@dataclass
class LogicalExpr(Expression):
    left: Expression
    right: Expression
    operator: str


@dataclass
class Identifier(Expression):
    symbol: str


@dataclass
class Property(Expression):
    key: str
    value: Expression | None


@dataclass
class ObjectLiteral(Expression):
    properties: list[Property]


@dataclass
class NumberLiteral(Expression):
    value: int | float


@dataclass
class StringLiteral(Expression):
    value: str
