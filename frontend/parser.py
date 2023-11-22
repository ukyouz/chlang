from .chast import BinaryExpr
from .chast import Expression
from .chast import Identifier
from .chast import NumberLiteral
from .chast import Program
from .chast import Statement
from .chast import VariableDeclaration
from .lexer import Token
from .lexer import TokenType
from .lexer import tokenize


class ParserError(Exception):
    ...


class Parser:
    tokens: list[Token] = []

    def at_the_end(self) -> bool:
        return self.tokens[0].type == TokenType.EOF

    def produce_ast(self, source_code: str) -> Program:
        self.tokens = tokenize(source_code)

        statements = []
        while not self.at_the_end():
            statement = self._parse_statement()
            statements.append(statement)

        return Program(body=statements)

    def at(self) -> Token:
        return self.tokens[0]

    def eat(self) -> Token:
        return self.tokens.pop(0)

    def expect(self, type: TokenType, err: str):
        prev = self.at()
        if prev.type != type:
            raise ParserError("{} Expect type {!r}, got token {!r}".format(err, type, prev))

    """
    orders of prescedence
    - assignment expression
    - member expression
    - function call
    - logical expression: and, or
    - comparison expression
    - additive expression
    - multiplicative expression
    - unary expression
    - primary expression
    """

    def _parse_statement(self) -> Statement:
        # skip to parse expression
        match self.at().type:
            case TokenType.Const:
                return self._parse_variable_declaration(True)
            case TokenType.Let:
                return self._parse_variable_declaration(False)
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

    def _parse_expression(self) -> Expression:
        return self._parse_additive_expression()

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
        left = self._parse_primary_expression()

        while self.at().value in {"*", "/", "%"}:
            operator = self.eat()
            right = self._parse_primary_expression()
            left = BinaryExpr(
                left=left,
                right=right,
                operator=operator.value,
            )

        return left

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
