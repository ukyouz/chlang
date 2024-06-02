from typing import Callable

from frontend.chast import FunctionDeclaration
from frontend.chast import IfStatement
from frontend.chast import Program
from frontend.chast import Statement
from frontend.chast import VariableDeclaration
from frontend.chast import WhileStatement
from runtime.environment import BooleanValue
from runtime.environment import DictionaryValue
from runtime.environment import Environment
from runtime.environment import FunctionValue
from runtime.environment import NullValue
from runtime.environment import NumberValue
from runtime.environment import RuntimeValue
from runtime.environment import StringValue

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


def eval_function_declaration(node: FunctionDeclaration, env: Environment) -> RuntimeValue:
    fn = FunctionValue(
        name = node.name,
        parameters = node.params,
        declaration_env = env,
        body = node.body,
    )

    return env.declare_variable(node.name, fn, True)


def eval_if_statement(node: IfStatement, env: Environment, evaluate: EvalFunc) -> RuntimeValue:
    runtime_true = evaluate(node.test, env)
    match runtime_true:
        case NumberValue(0) | NullValue() | BooleanValue(False):
            true = False
        case StringValue("") | DictionaryValue({}):
            true = False
        case _:
            true = True
    body = node.consequent if true else node.alternate

    last_evaluated = NullValue()
    for statement in body:
        last_evaluated = evaluate(statement, env)

    return last_evaluated


def eval_while_statement(node: WhileStatement, env: Environment, evaluate: EvalFunc) -> RuntimeValue:
    last_evaluated = NullValue()

    while evaluate(node.test, env).value:
        for statement in node.body:
            last_evaluated = evaluate(statement, env)

    return last_evaluated
