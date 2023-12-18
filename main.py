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
env.declare_variable("True", BooleanValue(True), True)
env.declare_variable("False", BooleanValue(False), True)
env.declare_variable("是", BooleanValue(True), True)
env.declare_variable("否", BooleanValue(False), True)
env.declare_variable("Null", NullValue(), True)
env.declare_variable("空", NullValue(), True)

s = sys.argv[1] if len(sys.argv) > 1 else "let y=8+9; y=y*6"

pprint(tokenize(s))
print("-----------")

program = parser.produce_ast(s)
pprint(program)

print("-----------")
result = interpreter.evaluate(program, env)
pprint(result)

