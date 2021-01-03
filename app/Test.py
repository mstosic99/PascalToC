from os import getcwd

from IPython.core.display import Image

import os

from app.Generator import Generator
from app.Symbolizer import Symbolizer

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

from app.Grapher import Grapher
from app.Lexer import Lexer
from app.Parser import Parser

test_id = 1
# path = f'{getcwd()}/data/pas/test{test_id}.pas'
path = f'{getcwd()}/data/pas2/{test_id}/src.pas'

with open(path, 'r') as source:

    text = source.read()
    lexer = Lexer(text)
    tokens = lexer.lex()

    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)

    symbolizer = Symbolizer(ast)
    symbolizer.symbolize()

    grapher = Grapher(ast)
    img = grapher.graph()

    generator = Generator(ast)
    code = generator.generate('main.c')

Image(img)
