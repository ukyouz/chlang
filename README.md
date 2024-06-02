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
定義 遊戲（目標值、最大嘗試次數）：
    令 執行中 為 是
    令 猜測次數 為 0
    每當 執行中：
        令 使用者輸入 為 整數（輸入（「請輸入一個數字：」））
        若 使用者輸入 等於 目標值：
            輸出（「賓果！」）
            執行中 為 否
        或若 使用者輸入 小於 目標值：
            輸出（「GG，猜太小了！」）
            猜測次數 為 猜測次數 加 1
        不然：
            輸出（「GG，猜太大了！」）
            猜測次數 為 猜測次數 加 1
        若 猜測次數 大於等於 最大嘗試次數：
            輸出（「QQ，你錯太多次了！」）
            執行中 為 否
    猜測次數

令 答案 為 123
令 錯誤次數 為 遊戲（答案、5）
輸出（錯誤次數）
輸出（「程式結束。」）
```

```bash
$ python3 main.py testfile.ch
[
    Token(type=Fn, value='定義', raw='定義'),
    Token(type=Identifier, value='遊戲', raw='遊戲'),
    Token(type=OpenParen, value='(', raw='（'),
    Token(type=Identifier, value='目標值', raw='目標值'),
    Token(type=Comma, value=',', raw='、'),
    Token(type=Identifier, value='最大嘗試次數', raw='最大嘗試次數'),
...
    Token(type=Identifier, value='輸出', raw='輸出'),
    Token(type=OpenParen, value='(', raw='（'),
    Token(type=String, value='程式結束。', raw='程式結束。'),
    Token(type=CloseParen, value=')', raw='）'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=EOF, value='<EOF>', raw='')
]
-----------
Program(
    body=[
        FunctionDeclaration(
            name='遊戲',
            params=['目標值', '最大嘗試次數'],
            body=[
                VariableDeclaration(identifier='執行中', value=Identifier(symbol='是'), const=False),
                VariableDeclaration(identifier='猜測次數', value=NumberLiteral(value=0), const=False),
                WhileStatement(
                    test=Identifier(symbol='執行中'),
                    body=[
...
                    ]
                ),
                Identifier(symbol='猜測次數')
            ]
        ),
        VariableDeclaration(identifier='答案', value=NumberLiteral(value=123), const=False),
        VariableDeclaration(
            identifier='錯誤次數',
            value=CallExpr(caller=Identifier(symbol='遊戲'), args=[Identifier(symbol='答案'), NumberLiteral(value=5)]),
            const=False
        ),
        CallExpr(caller=Identifier(symbol='輸出'), args=[Identifier(symbol='錯誤次數')]),
        CallExpr(caller=Identifier(symbol='輸出'), args=[StringLiteral(value='程式結束。')])
    ]
)
-----------
StringValue(value='請輸入一個數字：')12
StringValue(value='GG，猜太小了！')
StringValue(value='請輸入一個數字：')123
StringValue(value='賓果！')
NumberValue(value=1)
StringValue(value='程式結束。')
NullValue()  <- return value of the program, which is the last expression.
```

## Output

For better debug usage, currently print out all token list and syntax tree.


## References

- [Youtube Playlist: Build a Custom Scripting Language In Typescript - Introduction to Interpreters & Compilers](https://www.youtube.com/playlist?list=PL_2VhOvlMk4UHGqYCLWc6GO8FaPl8fQTh)
