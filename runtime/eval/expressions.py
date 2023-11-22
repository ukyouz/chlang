from typing import Callable

from frontend.chast import BinaryExpr
from frontend.chast import Identifier
from frontend.chast import NumberLiteral
from frontend.chast import Program
from frontend.chast import Statement
from frontend.chast import VariableDeclaration
from runtime.environment import Environment
from runtime.values import NullValue
from runtime.values import NumberValue
from runtime.values import RuntimeValue

EvalFunc = Callable[[Statement, Environment], RuntimeValue]


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


def eval_binary_expr(node: BinaryExpr, env: Environment, evaluate: EvalFunc) -> RuntimeValue:
    lhs = evaluate(node.left, env)
    rhs = evaluate(node.right, env)

    if not isinstance(lhs, NumberValue) or not isinstance(rhs, NumberValue):
        # TODO: mix type operation
        return NullValue()

    return _eval_numeric_expr(lhs, rhs, node.operator)


def eval_identifier(node: Identifier, env: Environment) -> RuntimeValue:
    return env.lookup_variable(node.symbol)


