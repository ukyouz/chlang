from .chast import AssignmentExpr
from .chast import BinaryExpr
from .chast import CallExpr
from .chast import Expression
from .chast import FunctionDeclaration
from .chast import Identifier
from .chast import MemberExpr
from .chast import NumberLiteral
from .chast import ObjectLiteral
from .chast import Program
from .chast import Property
from .chast import Statement
from .chast import VariableDeclaration
from .lexer import Token
from .lexer import TokenType
from .lexer import tokenize


class ParserError(Exception):
    ...


class Parser:
    tokens: list[Token] = []
    indents: list[str] = []

    def at_the_end(self) -> bool:
        return self.tokens[0].type == TokenType.EOF

    def produce_ast(self, source_code: str) -> Program:
        self.tokens = tokenize(source_code)

        statements = []
        self._ignore_whitespaces()
        while not self.at_the_end():
            statement = self._parse_statement()
            statements.append(statement)
            self._ignore_whitespaces()

        return Program(body=statements)

    def at(self) -> Token:
        return self.tokens[0]

    def eat(self) -> Token:
        return self.tokens.pop(0)

    def expect(self, token_type: TokenType, err: str):
        prev = self.at()
        if prev.type != token_type:
            raise ParserError("{} Expect type {!r}, got token {!r}".format(err, token_type, prev))

    def _ignore_whitespaces(self):
        while self.at().type in {TokenType.NewLine, TokenType.Indent}:
            self.eat()  # ignore newlines and spaces

    """
    orders of prescedence
    - assignment expression
    - object
    - logical expression: and, or
    - comparison expression
    - additive expression
    - multiplicative expression
    - unary expression
    - function call
    - member expression
    - primary expression
    """

    def _parse_statement(self) -> Statement:
        # skip to parse expression
        match self.at().type:
            case TokenType.Const:
                return self._parse_variable_declaration(True)
            case TokenType.Let:
                return self._parse_variable_declaration(False)
            case TokenType.Fn:
                return self._parse_function_declaration()
            case _:
                return self._parse_expression()

    def _parse_variable_declaration(self, is_const: bool) -> Statement:
        # let IDENT;
        # let IDENT = EXPRESSION;
        self.eat()  # eat "let"
        self.expect(
            TokenType.Identifier,
            "Expect an identifier following let keyword."
        )
        ident = self.eat().value

        if self.at().type in {TokenType.Semicolon, TokenType.NewLine, TokenType.EOF}:
            if is_const:
                raise ParserError("Expect a value for const variable.")
            # let IDENT
            # let IDENT;
            # let IDENT\n
            if not self.at_the_end():
                if self.at().type not in {TokenType.Semicolon, TokenType.NewLine}:
                    self.expect(
                        TokenType.NewLine,
                        "Expect a newline or semicolon after variable declaration."
                    )
                self.eat()
            return VariableDeclaration(ident, value=None, const=is_const)
        else:
            # let IDENT = EXPRESSION
            # let IDENT = EXPRESSION;
            self.eat() # eat "="
            value = self._parse_expression()
            if not self.at_the_end():
                if self.at().type not in {TokenType.Semicolon, TokenType.NewLine}:
                    self.expect(
                        TokenType.NewLine,
                        "Expect a newline or semicolon after variable declaration."
                    )
                self.eat() # eat a newline or semicolon
            return VariableDeclaration(ident, value=value, const=is_const)

    def _check_indent_level(self, new_scope=False) -> int:
        """
        return True if the indent continues
        return False if the indent ends, and goes up a level
        """
        while not self.at_the_end() and self.at().type is TokenType.NewLine:
            self.eat()  # eat newline
        if self.at().type is not TokenType.Indent:
            if new_scope:
                raise SyntaxError("Expect an indent after `:`")
            if self.indents:
                self.indents.pop()
                return -1
            return 0

        indent = self.at().value
        if new_scope:
            self.indents.append(indent)
            return 1
        if self.indents:
            if indent == self.indents[-1]:
                return 0
            elif len(self.indents) >= 2 and indent == self.indents[-2]:
                self.indents.pop()
                return -1
            raise SyntaxError("Indentation mismatch")
        else:
            raise SyntaxError("Unexpected indent.")

    def _parse_function_declaration(self) -> Statement:
        self.eat()  # eat "def"
        self.expect(
            TokenType.Identifier,
            "Expect an identifier following `def` keyword."
        )
        name = self.eat().value
        args = self._parse_args()
        params = []
        for arg in args:
            if type(arg) != Identifier:
                raise ParserError("Expect an identifier as function parameter.")
            params.append(arg.symbol)

        self.expect(
            TokenType.Colon,
            "Expect a `:` after function parameters."
        )
        self.eat()  # eat ":"
        assert self._check_indent_level(new_scope=True) == 1

        body = []

        while not self.at_the_end():
            self.expect(
                TokenType.Indent,
                "Expect an indent after `:`"
            )
            self.eat()  # eat indent
            statement = self._parse_statement()
            body.append(statement)
            if self._check_indent_level() == -1:
                break

        return FunctionDeclaration(name=name, params=params, body=body)

    def _parse_expression(self) -> Expression:
        return self._parser_assignment_expression()

    def _parser_assignment_expression(self) -> Expression:
        left = self._parse_object_expression()

        if (self.at().type == TokenType.Equals):
            self.eat()  # "="
            value = self._parse_expression()
            return AssignmentExpr(
                assigne=left,
                value=value,
            )

        return left

    def _parse_object_expression(self) -> Expression:
        if self.at().type is not TokenType.OpenBrace:
            return self._parse_additive_expression()

        self.eat()  # eat "{"
        self._ignore_whitespaces()

        properties = []
        while not self.at_the_end() and self.at().type is not TokenType.CloseBrace:

            self.expect(
                TokenType.Identifier,
                "Expect an identifier as property name."
            )
            key = self.eat().value
            if self.at().type is TokenType.Comma:
                # { prop1, prop2, }, allow shorthand
                self.eat()   # advance past comma
                properties.append(Property(key=key, value=None))
            elif self.at().type is TokenType.CloseBrace:
                # { prop1 }, allow shorthand
                properties.append(Property(key=key, value=None))
            else:
                # { prop1: value1, prop2: value2 }
                self.expect(
                    TokenType.Colon,
                    "Expect a colon after property name."
                )
                self.eat()
                value = self._parse_expression()
                properties.append(Property(key=key, value=value))

                self._ignore_whitespaces()

                if self.at().type is not TokenType.CloseBrace:
                    self.expect(
                        TokenType.Comma,
                        "Expect a comma after property."
                    )
                    self.eat()

            self._ignore_whitespaces()

        self.expect(
            TokenType.CloseBrace,
            "Expect a closing brace after object expression."
        )
        self.eat()
        return ObjectLiteral(properties=properties)

    # (10 + 5) - 1
    def _parse_additive_expression(self) -> Expression:
        left = self._parse_multiplicative_expression()

        while self.at().value in {"+", "-"}:
            operator = self.eat()
            right = self._parse_multiplicative_expression()
            left = BinaryExpr(
                left=left,
                right=right,
                operator=operator.value,
            )

        return left

    def _parse_multiplicative_expression(self) -> Expression:
        left = self._parse_call_member_expression()

        while self.at().value in {"*", "/", "%"}:
            operator = self.eat()
            right = self._parse_call_member_expression()
            left = BinaryExpr(
                left=left,
                right=right,
                operator=operator.value,
            )

        return left

    def _parse_call_member_expression(self) -> Expression:
        # foo.x()
        member = self._parse_member_expression()

        if self.at().type is TokenType.OpenParen:
            return self._parse_call_expression(member)

        return member

    def _parse_call_expression(self, caller: Expression) -> Expression:
        call_expr = CallExpr(caller=caller, args=self._parse_args())

        if self.at() == TokenType.OpenParen:
            # foo.x()()
            call_expr = self._parse_call_expression(call_expr)

        return call_expr

    def _parse_args(self) -> list[Expression]:
        self.expect(
            TokenType.OpenParen,
            "Expect a opening parenthesis after function call."
        )
        self.eat()
        if self.at().type is TokenType.CloseParen:
            args = []
        else:
            args = self. _parse_arguments_list()
        self.expect(
            TokenType.CloseParen,
            "Expect a closing parenthesis after function call."
        )
        self.eat()
        return args

    def _parse_arguments_list(self) -> list[Expression]:
        args = [self._parser_assignment_expression()]

        while self.at().type is TokenType.Comma:
            self.eat()
            args.append(self._parser_assignment_expression())

        return args

    def _parse_member_expression(self) -> Expression:
        obj = self._parse_primary_expression()

        while self.at().type in {TokenType.Dot, TokenType.OpenBracket}:
            operator = self.eat()

            if operator.type is TokenType.Dot:
                # non-computed values, aka obj.expr
                computed = False
                property = self._parse_primary_expression()

                if not isinstance(property, Identifier):
                    raise SyntaxError("Expect an identifier after '.'")
            else:
                computed = True
                property = self._parse_expression()
                self.expect(
                    TokenType.CloseBracket,
                    "Missing closing bracket after computed property."
                )
                self.eat()

            obj = MemberExpr(
                obj=obj,
                prop=property,
                computed=computed,
            )

        return obj

    def _parse_primary_expression(self) -> Expression:
        tk = self.at().type

        match tk:
            case TokenType.Identifier:
                return Identifier(symbol=self.eat().value)
            case TokenType.Number:
                if "." in self.at().value:
                    return NumberLiteral(value=float(self.eat().value))
                else:
                    return NumberLiteral(value=int(self.eat().value))
            case TokenType.OpenParen:
                self.eat()  # eat "("
                value = self._parse_expression()
                self.expect(
                    TokenType.CloseParen,
                    "Unexpected token: expected ')'"
                )
                self.eat()
                return value
            case _:
                raise NotImplementedError(f"Unhandle token: {self.at()}")


if __name__ == "__main__":
    parser = Parser()
    ast = parser.produce_ast("a + 1")
    print(ast)
