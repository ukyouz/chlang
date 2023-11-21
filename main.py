from pprint import pprint
from frontend.parser import Parser


def main():
    parser = Parser()

    while True:
        try:
            s = input('>> ')
        except EOFError:
            break
        if not s:
            continue

        program = parser.produce_ast(s)
        pprint(program)


if __name__ == '__main__':
    import sys
    parser = Parser()
    s = sys.argv[1] if len(sys.argv) > 1 else "((4))"
    program = parser.produce_ast(s)
    pprint(program)

