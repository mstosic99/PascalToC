from os import getcwd

from IPython.core.display import Image

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

from app.Grapher import Grapher
from app.Lexer import Lexer
from app.Parser import Parser

test_id = 10
path = f'{getcwd()}/data/pas/test{test_id}.pas'

with open(path, 'r') as source:

    text = source.read()
    lexer = Lexer(text)
    tokens = lexer.lex()

    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)

    grapher = Grapher(ast)
    img = grapher.graph()

Image(img)
