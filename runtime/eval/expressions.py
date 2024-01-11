from collections import OrderedDict
from typing import Callable

from frontend.chast import AssignmentExpr
from frontend.chast import BinaryExpr
from frontend.chast import CallExpr
from frontend.chast import Identifier
from frontend.chast import NumberLiteral
from frontend.chast import ObjectLiteral
from frontend.chast import Program
from frontend.chast import Statement
from frontend.chast import VariableDeclaration
from runtime.environment import BooleanValue
from runtime.environment import DictionaryValue
from runtime.environment import Environment
from runtime.environment import FunctionValue
from runtime.environment import NativeFnValue
from runtime.environment import NullValue
from runtime.environment import NumberValue
from runtime.environment import RuntimeValue

EvalFunc = Callable[[Statement, Environment], RuntimeValue]


def _eval_binary_expr(lhs: int | float, rhs: int | float, operator: str) -> RuntimeValue:
    match operator:
        case "+":
            return NumberValue(lhs + rhs)
        case "-":
            return NumberValue(lhs - rhs)
        case "*":
            return NumberValue(lhs * rhs)
        case "/":
            if rhs == 0:
                raise ZeroDivisionError()
            return NumberValue(lhs / rhs)
        case "%":
            return NumberValue(lhs % rhs)
        case "<<":
            if isinstance(lhs, float) or isinstance(rhs, float):
                raise NotImplementedError("float left shift")
            return NumberValue(lhs << rhs)
        case ">>":
            if isinstance(lhs, float) or isinstance(rhs, float):
                raise NotImplementedError("float right shift")
            return NumberValue(lhs >> rhs)
        case "^":
            if isinstance(lhs, float) or isinstance(rhs, float):
                raise NotImplementedError("float xor")
            return NumberValue(lhs ^ rhs)
        case "!=":
            return BooleanValue(lhs != rhs)
        case "==":
            return BooleanValue(lhs == rhs)
        case ">":
            return BooleanValue(lhs > rhs)
        case ">=":
            return BooleanValue(lhs >= rhs)
        case "<":
            return BooleanValue(lhs < rhs)
        case "<=":
            return BooleanValue(lhs <= rhs)
        case _:
            raise NotImplementedError(f"_eval_numeric_expr {operator=}")


def eval_binary_expr(node: BinaryExpr, env: Environment, evaluate: EvalFunc) -> RuntimeValue:
    lhs = evaluate(node.left, env)
    rhs = evaluate(node.right, env)

    lhs_val = getattr(lhs, "value", None)
    rhs_val = getattr(rhs, "value", None)
    if lhs_val is None or rhs_val is None:
        # TODO: mix type operation
        return NullValue()

    return _eval_binary_expr(lhs_val, rhs_val, node.operator)


def eval_identifier(node: Identifier, env: Environment) -> RuntimeValue:
    return env.lookup_variable(node.symbol)


def eval_assignment(node: AssignmentExpr, env: Environment, evaluate: EvalFunc) -> RuntimeValue:
    if type(node.assigne) is not Identifier:
        raise NotImplementedError(f"trying to assign to {type(node.assigne)=}")

    value = evaluate(node.value, env)
    return env.assign_variable(node.assigne.symbol, value)


def eval_object_expr(obj: ObjectLiteral, env: Environment, evaluate: EvalFunc) -> RuntimeValue:
    properties = {}

    for prop in obj.properties:
        if prop.value is None:
            properties[prop.key] = env.lookup_variable(prop.key)
        else:
            properties[prop.key] = evaluate(prop.value, env)

    return DictionaryValue(properties=properties)


def eval_call_expr(expr: CallExpr, env: Environment, evaluate: EvalFunc) -> RuntimeValue:
    args = [evaluate(x, env) for x in expr.args]
    fn = evaluate(expr.caller, env)

    if type(fn) is NativeFnValue:
        # TODO: support keyward arguments
        return fn.call(*args)
    elif type(fn) is FunctionValue:
        scope = Environment(fn.declaration_env)

        # create variables for function parameters
        # TODO: check the bounds of args, verity arity of function
        for varname, arg in zip(fn.parameters, args):
            scope.declare_variable(varname, arg, False)

        result = NullValue()
        for statement in fn.body:
            # evaluate statement line by line
            result = evaluate(statement, scope)

        return result
    else:
        raise NotImplementedError(f"can not call {fn=}")

