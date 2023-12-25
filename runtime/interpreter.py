from frontend.chast import AssignmentExpr
from frontend.chast import BinaryExpr
from frontend.chast import CallExpr
from frontend.chast import Identifier
from frontend.chast import NumberLiteral
from frontend.chast import ObjectLiteral
from frontend.chast import Program
from frontend.chast import Statement
from frontend.chast import VariableDeclaration
from runtime.environment import Environment
from runtime.eval import expressions
from runtime.eval import statements

from .values import NullValue
from .values import NumberValue
from .values import RuntimeValue


def evaluate(node: Statement, env: Environment) -> RuntimeValue:
    match node:
        case NumberLiteral():
            return NumberValue(node.value)
        case Identifier():
            return expressions.eval_identifier(node, env)
        case ObjectLiteral():
            return expressions.eval_object_expr(node, env, evaluate)
        case CallExpr():
            return expressions.eval_call_expr(node, env, evaluate)
        case AssignmentExpr():
            return expressions.eval_assignment(node, env, evaluate)
        case BinaryExpr():
            return expressions.eval_binary_expr(node, env, evaluate)
        case Program():
            return statements.eval_program(node, env, evaluate)
        case VariableDeclaration():
            return statements.eval_variable_declaration(node, env, evaluate)
        case _:
            raise NotImplementedError(f"evaluate {node=}")

