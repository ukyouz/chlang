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

""" Statements """

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
    body: [Statement]


""" Expressions """


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


