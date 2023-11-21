import re
from dataclasses import dataclass
from enum import Enum
from enum import auto


class TokenType(Enum):
    # Literal Types
    Identifier = auto()
    Number = auto()

    # keywords
    Let = auto()

    # Grouping * Operators
    BinaryOp = auto()
    Equals = auto()
    OpenParen = auto()
    CloseParen = auto()

    EOF = auto()

    def __repr__(self) -> str:
        return self.name

    @staticmethod
    def find_special_type(keyword: str):
        maps = {
            "令": TokenType.Let,
            "為": TokenType.Equals,
            "取餘": TokenType.BinaryOp,
        }
        return maps.get(keyword, None)


@dataclass
class Token:
    type: TokenType
    value: str
    ## TODO
    # start: tuple[int, int]
    # end: tuple[int, int]
    # line: str


def _is_skippable(char: str) -> bool:
    return char in " \n\r\t"


def tokenize(src_code: str) -> list[Token]:
    src = src_code

    tokens = []
    while src != "":
        # take care of fullwidth characters too
        match src[0]:
            case "(" | "（":
                tokens.append(Token(TokenType.OpenParen, src[0]))
                src = src[1:]
            case ")" | "）":
                tokens.append(Token(TokenType.CloseParen, src[0]))
                src = src[1:]
            case "+" | "-" | "*" | "/" | "%":
                tokens.append(Token(TokenType.BinaryOp, src[0]))
                src = src[1:]
            case "＋" | "－" | "＊" | "／" | "％":
                tokens.append(Token(TokenType.BinaryOp, src[0]))
                src = src[1:]
            case "加" | "減" | "乘" | "除":
                tokens.append(Token(TokenType.BinaryOp, src[0]))
                src = src[1:]
            case "=" | "＝":
                tokens.append(Token(TokenType.Equals, src[0]))
                src = src[1:]
            case _:
                if src[0].isnumeric():
                    char_cnt = 0
                    src_len = len(src)
                    while char_cnt < src_len and src[char_cnt].isnumeric():
                        char_cnt += 1
                    num, src = src[:char_cnt], src[char_cnt:]
                    tokens.append(Token(TokenType.Number, num))
                elif src[0].isalpha():
                    char_cnt = 0
                    src_len = len(src)
                    while char_cnt < src_len and src[char_cnt].isalpha():
                        char_cnt += 1
                    alpha, src = src[:char_cnt], src[char_cnt:]

                    t = TokenType.find_special_type(alpha) or TokenType.Identifier
                    tokens.append(Token(t, alpha))
                elif _is_skippable(src[0]):
                    src = src[1:]
                else:
                    raise NotImplementedError(f"Unknown token: {src[0]}")
    tokens.append(Token(TokenType.EOF, "<EOF>"))

    return tokens

if __name__ == "__main__":
    from pprint import pprint
    tokens = tokenize("令 x = 1 + 2")
    pprint(tokens)

    tokens = tokenize("令 數字 為 1 + 2")
    pprint(tokens)

