import re
from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    Name = auto()
    Indent = auto()
    Number = auto()
    Operator = auto()
    String = auto()
    NewLine = auto()
    EndMarker = auto()

    def __repr__(self) -> str:
        return self.name


@dataclass
class TokenInfo:
    type: TokenType
    string: str
    start: tuple[int, int]
    end: tuple[int, int]
    line: str


def _startswith_keyword(txt: str) -> str:
    for keyword in {
        "為每個",  # for
        "存在於",  # in
        "或若",  # elif
        "不然",  # else
        "每當",  # while
        "引用",  # import
        "令",  # let
        "為",  # assignment
        "是",  # true
        "否",  # false
        "若",  # if
        "或",  # else
    }:
        if txt.startswith(keyword):
            return keyword
    return ""


def _startswith_operator(txt: str) -> bool:
    for op in {
        "：",  # :
        "（",  # (
        "）",  # )
        "《",  # [
        "》",  # ]
        "，",  # dot notation
        "。",  # ; notation
        "等於",
        "不等於",
        "大於",
        "大於等於",
        "小於",
        "小於等於",
    }:
        if txt.startswith(op):
            return True
    return False


def _startswith_spaces(txt: str) -> str:
    if m := re.match(r"^\s+", txt):
        return m.group(0)
    return ""


def _is_number_string(txt: str) -> bool:
    try:
        # TODO: use a safer eval function
        eval(txt)
        return True
    except:
        return False


class State(Enum):
    CheckIndent = auto()
    GetChar = auto()
    GetString = auto()
    AppendToken = auto()
    ClearBuffer = auto()


def _tokenize_line(lineno: int, line: str):
    tokens = []
    col = 0
    txt = ""

    in_string = False
    state = State.CheckIndent
    while True:
        match state:
            case State.CheckIndent:
                if indent := _startswith_spaces(line):
                    tokens.append(
                        TokenInfo(
                            TokenType.Indent,
                            indent,
                            (lineno, col),
                            (lineno, col + len(indent)),
                            line,
                        )
                    )
                    col += len(indent)
                state = State.GetChar
            case State.GetChar:
                if col >= len(line):
                    break
                txt += line[col]
                col += 1
                state = State.AppendToken
            case State.AppendToken:
                if in_string:
                    if txt.endswith("」"):
                        tokens.append(
                            TokenInfo(
                                TokenType.String,
                                txt,
                                (lineno, col - len(txt)),
                                (lineno, col),
                                line,
                            )
                        )
                        in_string = False
                        state = State.ClearBuffer
                    else:
                        state = State.GetChar
                elif txt.startswith("「"):
                    in_string = True
                    state = State.GetChar
                elif longest := _startswith_keyword(line[col - len(txt) :]):
                    col += len(longest) - len(txt)
                    tokens.append(
                        TokenInfo(
                            TokenType.Name,
                            longest,
                            (lineno, col - len(longest)),
                            (lineno, col),
                            line,
                        )
                    )
                    state = State.ClearBuffer
                elif _startswith_operator(txt):
                    tokens.append(
                        TokenInfo(
                            TokenType.Operator,
                            txt,
                            (lineno, col - len(txt)),
                            (lineno, col),
                            line,
                        )
                    )
                    state = State.ClearBuffer
                elif txt == "\n":
                    tokens.append(
                        TokenInfo(
                            TokenType.NewLine,
                            txt,
                            (lineno, col - len(txt)),
                            (lineno, col),
                            line,
                        )
                    )
                    state = State.ClearBuffer
                elif (
                    col >= len(line) - 1
                    or _startswith_keyword(line[col:])
                    or _startswith_operator(line[col:])
                ):
                    if _is_number_string(txt):
                        tokens.append(
                            TokenInfo(
                                TokenType.Number,
                                txt,
                                (lineno, col - len(txt)),
                                (lineno, col),
                                line,
                            )
                        )
                    else:
                        clean_txt = txt.rstrip()
                        tokens.append(
                            TokenInfo(
                                TokenType.Name,
                                clean_txt,
                                (lineno, col - len(txt)),
                                (lineno, col - len(txt) + len(clean_txt)),
                                line,
                            )
                        )
                    state = State.ClearBuffer
                elif _startswith_spaces(txt):
                    state = State.ClearBuffer
                else:
                    state = State.GetChar
            case State.ClearBuffer:
                txt = ""
                state = State.GetChar
    return tokens


if __name__ == "__main__":
    tokens = []
    with open("chpy.ch") as fs:
        for line_no, line in enumerate(fs.readlines()):
            tokens += _tokenize_line(line_no, line)

    print(tokens)
