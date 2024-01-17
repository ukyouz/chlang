# chlang

A programming compatible with Chinese.

This is a demo project for possiblility of coding in Chinese, so just implement in python for convenient.

An issue for other Chinese programming languages is that they sitll use English characters for syntax, so in this project, fullwidth characters and some Chinese forms are also considered as a syntax, so you don't need to switch IME that much often.

## Design Principle

### Indentations

Python use indentations as function block, and I am really up for this idea. It also looks like Chinese paragraph style.

### Syntax

To let syntax seems like Chinese sentense, there are some special considerations.

#### Variable Declaration

```
令 變數A 為 123
```

For lexer to work, you actually need to add spaces around keyword and variable.

####  String

The following syntaxes are all strings.

```
"you can use double quote"
'also single quote.'
「為了對應中文語法，也可以使用引號。」
```

####  Function

```
定義 加加函式（參數1、參數2）：
    輸出（參數1、參數2）

    參數1+參數2
```

參數的間隔使用頓號 `、` 表示並列。目前實作會返回最後一行表達式的值。也許之後會加入返回關鍵字。

####  If-Elif-Else

```
若 foo：
    輸出（「foo為真」）
或若 boo：
    輸出（「boo為真」）
或者：
    輸出（「以上皆非。」）
```

####  Chinese Operators

*Binary Operations*

- `加 減 乘 除 餘` 等同於
- `+ -  *  / %`

- `且  或` 等同於
- `and or`

*Compare*

- `等於 不等於 大於 大於等於 小於 小於等於` 等同於
- `==  !=    >   >=      <   <=`


## Usage

A sample content of `testfile.ch`.

```
定義 加法器（位移、要輸出）：

    定義 add(甲、乙) ：
        令 結果 為 甲 加 乙 加 位移
        若 要輸出：
            輸出（結果）

    add

令 加十三 為 加法器（13、是）

輸出（加十三（1、4））
```

```bash
$ python3 main.py testfile.ch
[
    Token(type=Fn, value='定義', raw='定義'),
    Token(type=Identifier, value='adder', raw='adder'),
    Token(type=OpenParen, value='(', raw='（'),
    Token(type=Identifier, value='位移', raw='位移'),
    Token(type=Comma, value=',', raw='、'),
    Token(type=Identifier, value='要輸出', raw='要輸出'),
    Token(type=CloseParen, value=')', raw='）'),
...
    Token(type=OpenParen, value='(', raw='（'),
    Token(type=Number, value='1', raw='1'),
    Token(type=Comma, value=',', raw='、'),
    Token(type=Number, value='4', raw='4'),
    Token(type=CloseParen, value=')', raw='）'),
    Token(type=CloseParen, value=')', raw='）'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=EOF, value='<EOF>', raw='')
]
-----------
Program(
    body=[
        FunctionDeclaration(
            name='adder',
            params=['位移', '要輸出'],
            body=[
                FunctionDeclaration(
                    name='add',
                    params=['甲', '乙'],
                    body=[
...
                        IfStatement(
                            test=Identifier(symbol='要輸出'),
                            consequent=[CallExpr(caller=Identifier(symbol='輸出'), args=[Identifier(symbol='結果')])],
                            alternate=[]
                        )
                    ]
                ),
                Identifier(symbol='add')
            ]
        ),
        VariableDeclaration(
            identifier='加十三',
            value=CallExpr(caller=Identifier(symbol='adder'), args=[NumberLiteral(value=13), Identifier(symbol='是')]),
            const=False
        ),
        CallExpr(
            caller=Identifier(symbol='輸出'),
            args=[CallExpr(caller=Identifier(symbol='加十三'), args=[NumberLiteral(value=1), NumberLiteral(value=4)])]
        )
    ]
)
-----------
NumberValue(value=18)  <- output of 輸出（加十三（1、4））
NullValue()  <- return value of 輸出, default return Null
NullValue()  <- return value of the program, which is the last expression.
```

## Output

For better debug usage, currently print out all token list and syntax tree.


## References

- [Youtube Playlist: Build a Custom Scripting Language In Typescript - Introduction to Interpreters & Compilers](https://www.youtube.com/playlist?list=PL_2VhOvlMk4UHGqYCLWc6GO8FaPl8fQTh)
