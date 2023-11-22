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


def eval_program(node: Program, env: Environment, evaluate: EvalFunc) -> RuntimeValue:
    last_evaluated = NullValue()

    for statement in node.body:
        last_evaluated = evaluate(statement, env)

    return last_evaluated


def eval_variable_declaration(node: VariableDeclaration, env: Environment, evaluate: EvalFunc) -> RuntimeValue:
    if node.value is not None:
        value = evaluate(node.value, env)
    else:
        value = NullValue()
    return env.declare_variable(node.identifier, value, node.const)



