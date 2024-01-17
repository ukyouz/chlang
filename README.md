# chlang

A programming compatible with Chinese.

This is a demo project for possiblility of coding in Chinese, so just implement in python for convenient.

## usage

A sample content of `testfile.ch`.

```
定義 adder（位移、要輸出）：

    定義 add(甲、乙) ：
        令 結果 為 甲 + 乙 + 位移
        若 要輸出：
            輸出（結果）

    add

令 加十三 為 adder（13、是）

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
    Token(type=Colon, value=':', raw='：'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=Indent, value='    ', raw='    '),
    Token(type=Fn, value='定義', raw='定義'),
    Token(type=Identifier, value='add', raw='add'),
    Token(type=OpenParen, value='(', raw='('),
    Token(type=Identifier, value='甲', raw='甲'),
    Token(type=Comma, value=',', raw='、'),
    Token(type=Identifier, value='乙', raw='乙'),
    Token(type=CloseParen, value=')', raw=')'),
    Token(type=Colon, value=':', raw='：'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=Indent, value='        ', raw='        '),
    Token(type=Let, value='令', raw='令'),
    Token(type=Identifier, value='結果', raw='結果'),
    Token(type=Equals, value='=', raw='為'),
    Token(type=Identifier, value='甲', raw='甲'),
    Token(type=BinaryOp, value='+', raw='+'),
    Token(type=Identifier, value='乙', raw='乙'),
    Token(type=BinaryOp, value='+', raw='+'),
    Token(type=Identifier, value='位移', raw='位移'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=Indent, value='        ', raw='        '),
    Token(type=If, value='若', raw='若'),
    Token(type=Identifier, value='要輸出', raw='要輸出'),
    Token(type=Colon, value=':', raw='：'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=Indent, value='            ', raw='            '),
    Token(type=Identifier, value='輸出', raw='輸出'),
    Token(type=OpenParen, value='(', raw='（'),
    Token(type=Identifier, value='結果', raw='結果'),
    Token(type=CloseParen, value=')', raw='）'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=Indent, value='    ', raw='    '),
    Token(type=Identifier, value='add', raw='add'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=Let, value='令', raw='令'),
    Token(type=Identifier, value='加十三', raw='加十三'),
    Token(type=Equals, value='=', raw='為'),
    Token(type=Identifier, value='adder', raw='adder'),
    Token(type=OpenParen, value='(', raw='（'),
    Token(type=Number, value='13', raw='13'),
    Token(type=Comma, value=',', raw='、'),
    Token(type=Identifier, value='是', raw='是'),
    Token(type=CloseParen, value=')', raw='）'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=NewLine, value='\n', raw='\n'),
    Token(type=Identifier, value='輸出', raw='輸出'),
    Token(type=OpenParen, value='(', raw='（'),
    Token(type=Identifier, value='加十三', raw='加十三'),
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
                        VariableDeclaration(
                            identifier='結果',
                            value=BinaryExpr(
                                left=BinaryExpr(
                                    left=Identifier(symbol='甲'),
                                    right=Identifier(symbol='乙'),
                                    operator='+'
                                ),
                                right=Identifier(symbol='位移'),
                                operator='+'
                            ),
                            const=False
                        ),
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
NumberValue(value=18)
NullValue()
NullValue()
```

## Output

For better debug usage, currently print out all token list and syntax tree.
