from frontend.chast import AssignmentExpr
from frontend.chast import BinaryExpr
from frontend.chast import CallExpr
from frontend.chast import FunctionDeclaration
from frontend.chast import Identifier
from frontend.chast import IfStatement
from frontend.chast import LogicalExpr
from frontend.chast import NumberLiteral
from frontend.chast import ObjectLiteral
from frontend.chast import Program
from frontend.chast import Statement
from frontend.chast import StringLiteral
from frontend.chast import VariableDeclaration
from frontend.chast import WhileStatement
from runtime.environment import Environment
from runtime.environment import NullValue
from runtime.environment import NumberValue
from runtime.environment import RuntimeValue
from runtime.environment import StringValue
from runtime.eval import expressions
from runtime.eval import statements


def evaluate(node: Statement, env: Environment) -> RuntimeValue:
    match node:
        case NumberLiteral():
            return NumberValue(node.value)
        case StringLiteral():
            return StringValue(node.value)
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
        case LogicalExpr():
            return expressions.eval_logical_expr(node, env, evaluate)
        case Program():
            return statements.eval_program(node, env, evaluate)
        case VariableDeclaration():
            return statements.eval_variable_declaration(node, env, evaluate)
        case FunctionDeclaration():
            return statements.eval_function_declaration(node, env)
        case IfStatement():
            return statements.eval_if_statement(node, env, evaluate)
        case WhileStatement():
            return statements.eval_while_statement(node, env, evaluate)
        case _:
            raise NotImplementedError(f"evaluate {node=}")

