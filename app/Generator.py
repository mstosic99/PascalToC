from app.Node import LocalVars, ProcImpl, Id, WriteArg, Program, FuncCall, BinOp, UnOp, String, Int, Char, Bool, Real, \
    ArrayElem
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
        self.append(' - 1')
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
        self.append('while (!')
        self.visit(node, node.cond)
        self.append(');')
        self.newline()

    def visit_For(self, parent, node):
        self.newline()
        self.append('for (')
        self.visit(node, node.init)
        if node.is_to:
            self.append(node.init.id_.value + ' <= ')
            self.visit(node, node.goal)
        else:
            self.append(str(node.init.id_.value) + ' >= ')
            self.visit(node, node.goal)
        self.append(';')
        if node.is_to:
            self.append(str(node.init.id_.value) + ' = ' + str(node.init.id_.value) + ' + 1')
        else:
            self.append(str(node.init.id_.value) + ' = ' + str(node.init.id_.value) + ' - 1')
        self.append(') {')
        self.newline()
        self.indent()
        self.visit(node, node.block)
        self.newline()
        self.level += 1
        self.indent()

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
        if func == 'length':
            self.append('strlen(')
            self.visit(node, node.args)
            self.append(')')
        elif func not in ('ord', 'chr'):
            self.append(func)
            self.append('(')
            self.visit(node, node.args)
            self.append(')')
        else:
            self.visit(node, node.args)

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
        if proc in ('write', 'writeln'):
            if proc == 'writeln' and len(args) == 0:
                self.append(r'printf("\n")')
                self.append(';')
                self.newline()
                return
            self.append('printf("')
            if len(args) == 1 and type(args[0]) in (String, Char):
                self.append(args[0].value + '");')
                self.newline()
                return
            if len(args) == 1 and type(args[0].expr) in (String, Char):
                self.append(args[0].expr.value + '");')
                self.newline()
                return
            for i, n in enumerate(args[0:]):
                temp = n
                if type(n) == WriteArg and type(n.expr) in (BinOp, UnOp):
                    temp = n.expr.first
                elif type(n) == WriteArg and type(n.expr) in (String, Int, Char, Bool, Real, Id):
                    temp = n.expr
                elif type(n) == WriteArg and type(n.expr) is FuncCall:
                    temp = n.expr.id_
                    if n.expr.id_.value in ('chr', 'ord'):
                        self.append('%c')
                elif type(n) == WriteArg and type(n.expr) is ArrayElem:
                    temp = n.expr.id_
                else:
                    continue
                if i > 0:
                    self.append(' ')
                if symbols.contains(temp.value):
                    if symbols.get(temp.value).type_ == 'char':
                        self.append('%c')
                    # elif symbols.get(temp.value).type_ == 'integer' and temp.value in ('niz', 'c', 'b', 'a'):
                    elif symbols.get(temp.value).type_ == 'integer' and symbols.get(temp.value).is_array:
                        self.append('%d ')
                    elif symbols.get(temp.value).type_ == 'integer' or symbols.get(temp.value).type_ == 'boolean':
                        self.append('%d')
                    elif symbols.get(temp.value).type_ == 'string':
                        self.append('%s')
                    elif symbols.get(temp.value).type_ == 'real':
                        if type(n) is WriteArg and n.total_characters is not None and n.places_after_dot is not None:
                            self.append('%{}.{}f'.format(n.total_characters.value, n.places_after_dot.value))
                        elif type(n) is WriteArg and n.total_characters is not None and n.places_after_dot is None:
                            self.append('%{}f'.format(n.total_characters))
                        elif type(n) is WriteArg and n.total_characters is None and n.places_after_dot is not None:
                            self.append('%.{}f'.format(n.places_after_dot))
                        else:
                            self.append('%f')
            if proc == 'writeln':
                self.append(r'\n')
            self.append('"')
            if len(args) > 0:
                self.append(', ')
            self.visit(node, node.args)
            self.append(')')
        elif proc in ('readln', 'read'):
            self.append('scanf("')
            for i, n in enumerate(args[0:]):
                temp = n
                if type(n) is ArrayElem:
                    temp = n.id_
                if symbols.get(temp.value).type_ == 'char':
                    self.append('%c')
                elif symbols.get(temp.value).type_ == 'integer' or symbols.get(temp.value).type_ == 'boolean':
                    self.append('%d')
                elif symbols.get(temp.value).type_ == 'string':
                    self.append('%s')
                elif symbols.get(temp.value).type_ == 'real':
                    self.append('%f')
            self.append('"')
            if len(args) > 0:
                self.append(', ')
            self.visit(node, node.args)
            self.append(')')
        elif proc == 'inc':
            self.visit(node.args, args[0])
            self.append(' += 1')
        elif proc == 'insert':
            if type(args[1]) is Id:
                self.visit(node.args, args[1])
            else:
                self.visit(args[1], args[1].expr)
            self.append('[')
            if type(args[2]) is Id:
                self.visit(node.args, args[2])
            else:
                self.visit(args[2], args[2].expr)
            self.append('-1] = ')
            self.visit(node.args, args[0])
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
            self.visit(p, p.type_)
            self.visit(p, p.id_)

    def visit_LocalVars(self, parent, node):
        for n in node.local_variables:
            self.visit(node, n)
            self.newline()

    def visit_Args(self, parent, node):
        for i, a in enumerate(node.args):
            if parent.id_.value == 'write' and type(a) is not WriteArg:
                continue
            if i > 0:
                self.append(', ')
            if parent.id_.value in ('readln', 'read'):
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
        elif node.value == 'false':
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
        elif node.symbol == '=':
            self.append(' == ')
        elif node.symbol == '<>':
            self.append(' != ')
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
