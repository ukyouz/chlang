from frontend.chast import BinaryExpr
from frontend.chast import NullLiteral
from frontend.chast import NumberLiteral
from frontend.chast import Program
from frontend.chast import Statement

from .values import NullValue
from .values import NumberValue
from .values import RuntimeValue


def _eval_program(node: Program) -> RuntimeValue:
    last_evaluated = NullValue()

    for statement in node.body:
        last_evaluated = evaluate(statement)

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


def _eval_binary_expr(node: BinaryExpr) -> RuntimeValue:
    lhs = evaluate(node.left)
    rhs = evaluate(node.right)

    if not isinstance(lhs, NumberValue) or not isinstance(rhs, NumberValue):
        # TODO: mix type operation
        return NullValue()

    return _eval_numeric_expr(lhs, rhs, node.operator)


def evaluate(node: Statement) -> RuntimeValue:
    match node:
        case NumberLiteral():
            return NumberValue(node.value)
        case BinaryExpr():
            return _eval_binary_expr(node)
        case Program():
            return _eval_program(node)
        case NullLiteral():
            return NullValue()
        case _:
            raise NotImplementedError(f"evaluate {node=}")



