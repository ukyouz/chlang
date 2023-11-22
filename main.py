import sys
from pprint import pprint

from frontend.parser import Parser
from runtime import interpreter
from runtime import values

parser = Parser()
s = sys.argv[1] if len(sys.argv) > 1 else "((4))"
program = parser.produce_ast(s)
pprint(program)

print("-----------")
result = interpreter.evaluate(program)
pprint(result)

