from os import getcwd

from app.Lexer import Lexer

test_id = 8
path = f'{getcwd()}/data/pas/test{test_id}.pas'

with open(path, 'r') as source:

    text = source.read()
    lexer = Lexer(text)
    tokens = lexer.lex()

    for t in tokens:
        print(t)
