from frontend.chast import BinaryExpr
from frontend.chast import Identifier
from frontend.chast import NumberLiteral
from frontend.chast import Program
from frontend.chast import Statement
from runtime.environment import Environment

from .values import NullValue
from .values import NumberValue
from .values import RuntimeValue


def _eval_program(node: Program, env: Environment) -> RuntimeValue:
    last_evaluated = NullValue()

    for statement in node.body:
        last_evaluated = evaluate(statement, env)

    return last_evaluated


def _eval_numeric_expr(lhs: NumberValue, rhs: NumberValue, operator: str) -> RuntimeValue:
    match operator:
        case "+":
            return NumberValue(lhs.value + rhs.value)
        case "-":
            return NumberValue(lhs.value - rhs.value)
        case "*":
            return NumberValue(lhs.value * rhs.value)
        case "/":
            # TODO: divide by zero check
            return NumberValue(lhs.value / rhs.value)
        case "%":
            return NumberValue(lhs.value % rhs.value)
        case _:
            raise NotImplementedError(f"_eval_numeric_expr {operator=}")


def _eval_binary_expr(node: BinaryExpr, env: Environment) -> RuntimeValue:
    lhs = evaluate(node.left, env)
    rhs = evaluate(node.right, env)

    if not isinstance(lhs, NumberValue) or not isinstance(rhs, NumberValue):
        # TODO: mix type operation
        return NullValue()

    return _eval_numeric_expr(lhs, rhs, node.operator)


def _eval_identifier(node: Identifier, env: Environment) -> RuntimeValue:
    return env.lookup_variable(node.symbol)


def evaluate(node: Statement, env: Environment) -> RuntimeValue:
    match node:
        case NumberLiteral():
            return NumberValue(node.value)
        case Identifier():
            return _eval_identifier(node, env)
        case BinaryExpr():
            return _eval_binary_expr(node, env)
        case Program():
            return _eval_program(node, env)
        case _:
            raise NotImplementedError(f"evaluate {node=}")

