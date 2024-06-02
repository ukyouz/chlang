import re
from contextlib import suppress
from dataclasses import dataclass
from enum import Enum
from enum import auto


class TokenType(Enum):
    # Literal Types
    Identifier = auto()
    Number = auto()
    String = auto()

    Indent = auto()
    NewLine = auto()

    # keywords
    Let = auto()
    Const = auto()
    Fn = auto()
    If = auto()
    Elif = auto()
    Else = auto()
    While = auto()

    # Grouping * Operators
    BinaryOp = auto()
    LogicalOp = auto()
    UnaryOp = auto()
    Equals = auto()
    Dot = auto()
    Comma = auto()
    Colon = auto()
    Semicolon = auto()
    OpenParen = auto()
    CloseParen = auto()
    OpenBracket = auto()
    CloseBracket = auto()
    OpenBrace = auto()
    CloseBrace = auto()

    EOF = auto()

    def __repr__(self) -> str:
        return self.name


@dataclass
class Token:
    type: TokenType
    value: str
    ## TODO
    # start: tuple[int, int]
    # end: tuple[int, int]
    raw: str


def _is_skippable(char: str) -> bool:
    return char in "\r"


def _is_quote(char: str) -> bool:
    return char in "'\"“”「」"

def _get_close_quote(char: str) -> str:
    if char == '"':
        return '"'
    elif char == "'":
        return "'"
    elif char == "“":
        return "”"
    elif char == "「":
        return "」"
    else:
        raise ValueError(f"Invalid quote: {char}")


def halve_fullwidth_chars(txt: str):
    src = "？！（）《》【】＋－＊／％＝＜＞"
    dst = "?!()[]{}+-*/%=<>"
    for s, d in zip(src, dst):
        txt = txt.replace(s, d)
    return txt


NORMALIZED_OPS = {
    "且": "and",
    "或": "or",
    "非": "not",
    "等於": "==",
    "不等於": "!=",
    "大於等於": ">=",
    "大於": ">",
    "小於等於": "<=",
    "小於": "<",
}

OTHER_BINARY_OPS = {
    "and": TokenType.LogicalOp,
    "or": TokenType.LogicalOp,
    "not": TokenType.UnaryOp,
    "<<": TokenType.BinaryOp,
    ">>": TokenType.BinaryOp,
    "==": TokenType.BinaryOp,
    "!=": TokenType.BinaryOp,
    ">": TokenType.BinaryOp,
    ">=": TokenType.BinaryOp,
    "<": TokenType.BinaryOp,
    "<=": TokenType.BinaryOp,
    "^": TokenType.BinaryOp,
}

def _has_operator_cnt(text: str) -> int:
    text = halve_fullwidth_chars(text)
    for op in OTHER_BINARY_OPS.keys():
        if text == op:
            return len(op)
    for op in NORMALIZED_OPS.keys():
        if text == op:
            return len(op)
    return 0


KEYWORDS_TOKENS = {
    "令": TokenType.Let,
    "let": TokenType.Let,
    "常數": TokenType.Const,
    "const": TokenType.Const,
    "def": TokenType.Fn,
    "定義": TokenType.Fn,
    "if": TokenType.If,
    "若": TokenType.If,
    "elif": TokenType.Elif,
    "或若": TokenType.Elif,
    "else": TokenType.Else,
    "不然": TokenType.Else,
    "while": TokenType.While,
    "每當": TokenType.While,
}


def _get_soft_token(text: str) -> tuple[TokenType | None, str]:
    # since chinnese may also be part of identifier,
    # so tokenize it lazily
    match text:
        case "加":
            return TokenType.BinaryOp, "+"
        case "減":
            return TokenType.BinaryOp, "-"
        case "乘" | "乘以":
            return TokenType.BinaryOp, "*"
        case "除" | "除以":
            return TokenType.BinaryOp, "/"
        case "餘" | "取餘":
            return TokenType.BinaryOp, "%"
        case "為":
            return TokenType.Equals, "="
        case _:
            return None, ""


def tokenize(src_code: str) -> list[Token]:
    src = src_code

    tokens = []
    while src != "":
        # take care of fullwidth characters too
        match src[0]:
            case "(" | "（":
                tokens.append(Token(TokenType.OpenParen, "(", src[0]))
                src = src[1:]
            case ")" | "）":
                tokens.append(Token(TokenType.CloseParen, ")", src[0]))
                src = src[1:]
            case "[" | "《":
                tokens.append(Token(TokenType.OpenBracket, "[", src[0]))
                src = src[1:]
            case "]" | "》":
                tokens.append(Token(TokenType.CloseBracket, "]", src[0]))
                src = src[1:]
            case "{" | "【":
                tokens.append(Token(TokenType.OpenBrace, "{", src[0]))
                src = src[1:]
            case "}" | "】":
                tokens.append(Token(TokenType.CloseBrace, "}", src[0]))
                src = src[1:]
            case "+" | "＋":
                tokens.append(Token(TokenType.BinaryOp, "+", src[0]))
                src = src[1:]
            case "-" | "－":
                tokens.append(Token(TokenType.BinaryOp, "-", src[0]))
                src = src[1:]
            case "*" | "＊":
                tokens.append(Token(TokenType.BinaryOp, "*", src[0]))
                src = src[1:]
            case "/" | "／":
                tokens.append(Token(TokenType.BinaryOp, "/", src[0]))
                src = src[1:]
            case "%" | "％":
                tokens.append(Token(TokenType.BinaryOp, "%", src[0]))
                src = src[1:]
            case "=" | "＝":
                tokens.append(Token(TokenType.Equals, "=", src[0]))
                src = src[1:]
            case "." | "，":
                tokens.append(Token(TokenType.Dot, ".", src[0]))
                src = src[1:]
            case "," | "、":
                tokens.append(Token(TokenType.Comma, ",", src[0]))
                src = src[1:]
            case ":" | "：":
                tokens.append(Token(TokenType.Colon, ":", src[0]))
                src = src[1:]
            case ";" | "；":
                tokens.append(Token(TokenType.Semicolon, ";", src[0]))
                src = src[1:]
            case " " | "\t" | "　":
                if tokens[-1].type == TokenType.Indent:
                    raise SyntaxError("IndentationError: mixing tabs and spaces in indentation")
                if tokens[-1].type == TokenType.NewLine:
                    indent = ""
                    pos = 0
                    while src[pos] == src[0]:
                        indent += " "
                        pos += 1
                    tokens.append(Token(TokenType.Indent, indent, src[:pos]))
                    src = src[pos:]
                else:
                    src = src[1:]
            case "\r":
                with suppress(IndexError):
                    if src[1] == "\n":
                        tokens.append(Token(TokenType.NewLine, "\n", "\n"))
                        src = src[2:]
                    else:
                        src = src[1:]
            case "\n":
                tokens.append(Token(TokenType.NewLine, "\n", "\n"))
                src = src[1:]
            case _:
                if src[0].isnumeric():
                    char_cnt = 0
                    while char_cnt < len(src) and src[char_cnt].isnumeric():
                        char_cnt += 1
                    num, src = src[:char_cnt], src[char_cnt:]
                    if src.startswith("."):
                        char_cnt = 1
                        while char_cnt < len(src) and src[char_cnt].isnumeric():
                            char_cnt += 1
                        num += src[:char_cnt]
                        src = src[char_cnt:]
                    tokens.append(Token(TokenType.Number, num, num))
                elif src[0].isalpha():
                    char_cnt = 0
                    src_len = len(src)
                    while char_cnt < src_len:
                        if char_cnt > 0:
                            if not (src[char_cnt].isnumeric() or src[char_cnt].isalpha()):
                                break
                        elif not src[char_cnt].isalpha():
                            break
                        char_cnt += 1
                    alpha, src = src[:char_cnt], src[char_cnt:]

                    t, normailzed = _get_soft_token(alpha)
                    if t is not None:
                        tokens.append(Token(t, normailzed, alpha))
                    elif _has_operator_cnt(alpha):
                        op = NORMALIZED_OPS.get(alpha, alpha)
                        tokens.append(Token(OTHER_BINARY_OPS[op], op, alpha))
                    else:
                        t = KEYWORDS_TOKENS.get(alpha, TokenType.Identifier)
                        tokens.append(Token(t, alpha, alpha))
                elif _is_skippable(src[0]):
                    src = src[1:]
                elif _is_quote(src[0]):
                    quote = src[0]
                    close_quote = _get_close_quote(quote)
                    char_cnt = 1
                    src_len = len(src)
                    while char_cnt < src_len:
                        if src[char_cnt] == close_quote:
                            break
                        char_cnt += 1
                    if char_cnt == src_len:
                        raise SyntaxError("SyntaxError: unterminated string")
                    string, src = src[1:char_cnt], src[char_cnt+1:]
                    tokens.append(Token(TokenType.String, string, string))
                else:
                    raise NotImplementedError(f"Unknown token: {src[0]}")
    tokens.append(Token(TokenType.EOF, "<EOF>", ""))

    return tokens

if __name__ == "__main__":
    from pprint import pprint
    tokens = tokenize("令 x = 一二三 加 2 乘（3）")
    pprint(tokens)

    tokens = tokenize("令 數字 為 1 + 2")
    pprint(tokens)

