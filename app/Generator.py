from app.Node import LocalVars, ProcImpl, WriteArg, Program
from app.Visitor import Visitor
import re


class Generator(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.c = ""
        self.level = 0

    def append(self, text):
        self.c += str(text)

    def newline(self):
        self.append('\n\r')

    def indent(self):
        for i in range(self.level):
            self.append('\t')

    def visit_Program(self, parent, node):

        for n in node.nodes:
            if type(n) is LocalVars:
                self.visit(node, n)

        for n in node.nodes:
            if type(n) is not LocalVars:
                self.visit(node, n)

        # self.append('if __name__ == "__main__":')
        # self.newline()
        # self.level += 1
        # self.indent()
        # self.append('main()')
        # self.newline()
        # self.level -= 1

    def visit_Decl(self, parent, node):
        self.visit(node, node.type_)
        self.visit(node, node.id_)
        self.append(';')

    def visit_ArrayDecl(self, parent, node):
        self.visit(node, node.type_)
        self.visit(node, node.id_)
        self.append('[')
        self.append(node.to_.value - node.from_.value + 1)
        self.append(']')
        if node.elems is not None:
            self.append(' =  {')
            self.visit(node, node.elems)
            self.append('}')
        self.append(';')

    def visit_StringDecl(self, parent, node):
        self.visit(node, node.type_)
        self.visit(node, node.id_)
        self.append('[')
        self.visit(node, node.size)
        self.append(']')
        self.append(';')

    def visit_ArrayElem(self, parent, node):
        self.visit(node, node.id_)
        self.append('[')
        self.visit(node, node.index)
        self.append(']')

    def visit_Assign(self, parent, node):
        self.visit(node, node.id_)
        self.append(' = ')
        self.visit(node, node.expr)
        self.append(';')

    def visit_If(self, parent, node):
        self.append('if (')
        self.visit(node, node.cond)
        self.append(') {')
        self.newline()
        self.indent()
        self.visit(node, node.true)
        self.newline()
        self.append('}')
        self.newline()
        if node.elseifs is not None:
            for elseif in node.elseifs:
                self.visit(node, elseif)
        if node.false is not None:
            self.visit(node, node.false)

    def visit_ElseIf(self, parent, node):
        self.indent()
        self.append('else if (')
        self.visit(node, node.cond)
        self.append(')  {')
        self.visit(node, node.true)
        self.newline()
        self.append('}')
        self.newline()

    def visit_Else(self, parent, node):
        self.indent()
        self.append('else {')
        self.visit(node, node.block)
        self.newline()
        self.append('}')
        self.newline()

    def visit_While(self, parent, node):
        self.append('while (')
        self.visit(node, node.cond)
        self.append(') {')
        self.newline()
        self.visit(node, node.block)
        self.newline()
        self.append('}')
        self.newline()

    def visit_RepeatUntil(self, parent, node):
        self.append('do {')
        self.newline()
        self.visit(node, node.block)
        self.newline()
        self.append('}')
        self.append('while (')
        self.visit(node, node.cond)
        self.append(');')
        self.newline()

    def visit_For(self, parent, node):
        self.newline()
        self.visit(node, node.init)
        self.append(';')
        self.newline()
        self.indent()
        self.append('while (')
        self.visit(node, node.cond)
        self.append(') {')
        self.newline()
        self.visit(node, node.block)
        self.newline()
        self.level += 1
        self.indent()
        self.visit(node, node.step)
        self.append(';')
        self.newline()
        self.append('}')
        self.level -= 1
        self.newline()

    def visit_FuncImpl(self, parent, node):
        self.visit(node, node.type_)
        self.append(node.id_.value)
        self.append('(')
        self.visit(node, node.params)
        self.append(') {')
        self.newline()
        self.visit(node, node.local_variables)
        self.newline()
        self.visit(node, node.block)
        self.newline()
        self.append('}')
        self.newline()

    def visit_FuncCall(self, parent, node):
        func = node.id_.value
        self.append(func)
        self.append('(')
        self.visit(node, node.args)
        self.append(')')

    def visit_ProcImpl(self, parent, node):
        self.append('void ')
        self.append(node.id_.value)
        self.append('(')
        self.visit(node, node.params)
        self.append(') {')
        self.newline()
        self.visit(node, node.local_variables)
        self.newline()
        self.visit(node, node.block)
        self.newline()
        self.append('}')
        self.newline()

    def visit_ProcCall(self, parent, node):
        proc = node.id_.value
        args = node.args.args
        symbols = parent.symbols
        if proc == 'write':
            self.append('printf("')
            for i, n in enumerate(args[0:]):
                if i > 0:
                    self.append(' ')
                self.append('%d')
                # if symbols.get(n.value).type_ == 'char':
                #     self.append('%c')
                # elif symbols.get(n.value).type_ == 'integer' or symbols.get(n.value).type_ == 'boolean':
                #     self.append('%d')
                # elif symbols.get(n.value).type_ == 'string':
                #     self.append('%s')
                # elif symbols.get(n.value).type_ == 'float' or symbols.get(n.value).type_ == 'double':
                #     if type(n) is WriteArg and n.total_characters is not None and n.places_after_dot is not None:
                #         self.append('%{}.{}f'.format(n.total_characters.value, n.places_after_dot.value))
                #     elif type(n) is WriteArg and n.total_characters is not None and n.places_after_dot is None:
                #         self.append('%{}f'.format(n.total_characters))
                #     elif type(n) is WriteArg and n.total_characters is None and n.places_after_dot is not None:
                #         self.append('%.{}f'.format(n.places_after_dot))
                #     else:
                #         self.append('%f')
            self.append('"')
            if len(args) > 0:
                self.append(', ')
            self.visit(node, node.args)
            self.append(')')
        elif proc == 'readln':
            self.append('scanf("')
            for i, n in enumerate(args[0:]):
                self.append('%d')
            #     if symbols.get(n.value).type_ == 'char':
            #         self.append('%c')
            #     elif symbols.get(n.value).type_ == 'integer' or symbols.get(n.value).type_ == 'boolean':
            #         self.append('%d')
            #     elif symbols.get(n.value).type_ == 'string':
            #         self.append('%s')
            #     elif symbols.get(n.value).type_ == 'float' or symbols.get(n.value).type_ == 'double':
            #         self.append('%f')
            self.append('"')
            if len(args) > 0:
                self.append(', ')
            self.visit(node, node.args)
            self.append(')')
        elif proc == 'strlen':
            self.append('len(')
            self.visit(node, node.args)
            self.append(')')
        elif proc == 'strcat':
            self.visit(node.args, args[0])
            self.append(' += ')
            self.visit(node.args, args[1])
            self.newline()
            self.indent()
        else:
            self.append(proc)
            self.append('(')
            self.visit(node, node.args)
            self.append(')')
        self.append(';')
        self.newline()

    def visit_Block(self, parent, node):
        if type(parent) is Program:
            self.newline()
            self.append('void main() {')
            self.newline()
        self.level += 1
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.newline()
        self.level -= 1
        if type(parent) is Program:
            self.newline()
            self.indent()
            self.append('}')
            self.newline()

    def visit_Params(self, parent, node):
        for i, p in enumerate(node.params):
            if i > 0:
                self.append(', ')
            self.visit(p, p.id_)

    def visit_LocalVars(self, parent, node):
        pass  # TODO

    def visit_Args(self, parent, node):
        for i, a in enumerate(node.args):
            if i > 0:
                self.append(', ')
            if parent.id_.value == 'readln':
                self.append('&(')
                self.visit(node, a)
                self.append(')')
                continue
            self.visit(node, a)

    def visit_WriteArg(self, parent, node):
        self.visit(node, node.expr)

    def visit_Elems(self, parent, node):
        for i, e in enumerate(node.elems):
            if i > 0:
                self.append(', ')
            self.visit(node, e)

    def visit_Break(self, parent, node):
        self.append('break;')

    def visit_Continue(self, parent, node):
        self.append('continue;')

    def visit_Return(self, parent, node):
        pass

    def visit_Exit(self, parent, node):
        self.append('return')
        if node.expr is not None:
            self.append(' ')
            self.visit(node, node.expr)
        self.append(';')

    def visit_Type(self, parent, node):
        if node.value == 'integer' or node.value == 'boolean':
            self.append('int ')
        elif node.value == 'string' or node.value == 'char':
            self.append('char ')
        elif node.value == 'real':
            self.append('float ')

    def visit_Int(self, parent, node):
        self.append(node.value)

    def visit_Real(self, parent, node):
        self.append(node.value)

    def visit_Char(self, parent, node):
        self.append(ord(node.value))

    def visit_String(self, parent, node):
        self.append(node.value)

    def visit_Bool(self, parent, node):
        if node.value == 'true':
            self.append(1)
        elif node.vale == 'false':
            self.append(0)

    def visit_Id(self, parent, node):
        self.append(node.value)

    def visit_BinOp(self, parent, node):
        self.visit(node, node.first)
        if node.symbol == 'and':
            self.append(' && ')
        elif node.symbol == 'or':
            self.append(' || ')
        elif node.symbol == 'div':
            self.append(' / ')
        elif node.symbol == 'mod':
            self.append(' % ')
        else:
            self.append(node.symbol)
        self.visit(node, node.second)

    def visit_UnOp(self, parent, node):
        if node.symbol == 'not':
            self.append(' !')
        elif node.symbol != '&':
            self.append(node.symbol)
        self.visit(node, node.first)

    def visit_NoneType(self, parent, node):
        pass  # TODO

    def generate(self, path):
        self.visit(None, self.ast)
        self.c = re.sub('\n\s*\n', '\n', self.c)
        with open(path, 'w') as source:
            source.write(self.c)
        return path
