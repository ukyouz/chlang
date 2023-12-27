import re
import sys
from argparse import ArgumentParser
from collections import defaultdict

try:
    from rich import inspect
    from rich import print
except ImportError:
    pass
from frontend.lexer import tokenize
from frontend.parser import Parser
from runtime import interpreter
from runtime.environment import create_global_env

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("file", nargs="?", default="test.ch")
    argparser.add_argument("--cmd", "-c", help="program passed in as string (terminates option list)")
    args = argparser.parse_args()

    parser = Parser()
    env = create_global_env()

    if args.cmd:
        src = args.cmd
    else:
        file = sys.argv[1] if len(sys.argv) > 1 else "test.ch"
        with open(file) as fs:
            src = fs.read()

    print(tokenize(src))
    print("-----------")

    program = parser.produce_ast(src)
    print(program)

    print("-----------")
    result = interpreter.evaluate(program, env)
    print(result)

