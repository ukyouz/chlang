import sys
from pprint import pprint

from frontend.lexer import tokenize
from frontend.parser import Parser
from runtime import interpreter
from runtime import values
from runtime.environment import Environment
from runtime.values import BooleanValue
from runtime.values import NullValue
from runtime.values import NumberValue

parser = Parser()
env = Environment()
env.declare_variable("x", NumberValue(5))
env.declare_variable("True", BooleanValue(True))
env.declare_variable("False", BooleanValue(False))
env.declare_variable("是", BooleanValue(True))
env.declare_variable("否", BooleanValue(False))
env.declare_variable("Null", NullValue())
env.declare_variable("空", NullValue())

s = sys.argv[1] if len(sys.argv) > 1 else "let x"

pprint(tokenize(s))
print("-----------")

program = parser.produce_ast(s)
pprint(program)

print("-----------")
result = interpreter.evaluate(program, env)
pprint(result)

