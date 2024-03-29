from app.Node import Program, Block
from app.Visitor import Visitor


class Symbol:
    def __init__(self, id_, type_, scope, is_array):
        self.id_ = id_
        self.type_ = type_
        self.scope = scope
        self.is_array = is_array

    def __str__(self):
        return "<{} {} {}>".format(self.id_, self.type_, self.scope)

    def copy(self):
        return Symbol(self.id_, self.type_, self.scope, self.is_array)


class Symbols:
    def __init__(self):
        self.symbols = {}

    def put(self, id_, type_, scope, is_array):
        self.symbols[id_] = Symbol(id_, type_, scope, is_array)

    def get(self, id_):
        return self.symbols[id_]

    def contains(self, id_):
        return id_ in self.symbols

    def remove(self, id_):
        del self.symbols[id_]

    def __len__(self):
        return len(self.symbols)

    def __str__(self):
        out = ""
        for _, value in self.symbols.items():
            if len(out) > 0:
                out += "\n"
            out += str(value)
        return out

    def __iter__(self):
        return iter(self.symbols.values())

    def __next__(self):
        return next(self.symbols.values())


class Symbolizer(Visitor):
    def __init__(self, ast):
        self.ast = ast

    def visit_Program(self, parent, node):
        node.symbols = Symbols()
        for n in node.nodes:
            self.visit(node, n)

    def visit_Decl(self, parent, node):
        parent.symbols.put(node.id_.value, node.type_.value, id(parent), False)

    def visit_ArrayDecl(self, parent, node):
        # node.symbols = Symbols()
        # setattr(node, 'symbols', Symbols())
        parent.symbols.put(node.id_.value, node.type_.value, id(parent), True)

    def visit_StringDecl(self, parent, node):
        # node.symbols = Symbols()
        parent.symbols.put(node.id_.value, node.type_.value, id(parent), False)

    def visit_ArrayElem(self, parent, node):
        pass

    def visit_Assign(self, parent, node):
        pass

    def visit_If(self, parent, node):
        node.symbols = Symbols()
        for s in parent.symbols:
            node.symbols.put(s.id_, s.type_, id(parent), s.is_array)
        self.visit(node, node.true)
        if node.elseifs is not None:
            for elseif in node.elseifs:
                self.visit(node, elseif.true)
        if node.false is not None:
            self.visit(node, node.false)

    def visit_ElseIf(self, parent, node):
        node.symbols = Symbols()
        for s in parent.symbols:
            node.symbols.put(s.id_, s.type_, id(parent), s.is_array)
        self.visit(node, node.true)

    def visit_Else(self, parent, node):
        node.symbols = Symbols()
        self.visit(node, node.block)
        for s in parent.symbols:
            node.symbols.put(s.id_, s.type_, id(parent), s.is_array)
        self.visit(node, node.block)

    def visit_While(self, parent, node):
        node.symbols = Symbols()
        for s in parent.symbols:
            node.symbols.put(s.id_, s.type_, id(parent), s.is_array)
        self.visit(node, node.block)

    def visit_RepeatUntil(self, parent, node):
        node.symbols = Symbols()
        for s in parent.symbols:
            node.symbols.put(s.id_, s.type_, id(parent), s.is_array)
        self.visit(node, node.block)

    def visit_For(self, parent, node):
        node.symbols = Symbols()
        for s in parent.symbols:
            node.symbols.put(s.id_, s.type_, id(parent), s.is_array)
        self.visit(node, node.block)

    def visit_FuncImpl(self, parent, node):
        node.symbols = Symbols()
        parent.symbols.put(node.id_.value, node.type_.value, id(parent), False)
        self.visit(node, node.block)
        self.visit(node, node.params)
        self.visit(node, node.local_variables)

    def visit_ProcImpl(self, parent, node):
        node.symbols = Symbols()
        parent.symbols.put(node.id_.value, None, id(parent), False)
        self.visit(node, node.block)
        self.visit(node, node.params)
        self.visit(node, node.local_variables)

    def visit_FuncCall(self, parent, node):
        pass

    def visit_ProcCall(self, parent, node):
        pass

    def visit_Block(self, parent, node):
        node.symbols = Symbols()
        for s in parent.symbols:
            node.symbols.put(s.id_, s.type_, id(parent), s.is_array)
        # setattr(node, 'symbols', Symbols())
        for n in node.nodes:
            self.visit(node, n)
        for s in node.symbols:
            parent.symbols.put(s.id_, s.type_, id(parent), s.is_array)

    def visit_Params(self, parent, node):
        node.symbols = Symbols()
        for p in node.params:
            self.visit(node, p)
            self.visit(parent.block, p)
        for s in node.symbols:
            parent.symbols.put(s.id_, s.type_, id(parent), s.is_array)

    def visit_LocalVars(self, parent, node):
        node.symbols = Symbols()
        for lv in node.local_variables:
            self.visit(node, lv)
            # if type(parent) is not Program:
            #     self.visit(parent.block, lv)
            # else:
            #     for n in parent.nodes:
            #         if type(n) is Block:
            #             self.visit(node, lv)
        for s in node.symbols:
            parent.symbols.put(s.id_, s.type_, id(parent), s.is_array)

    def visit_Args(self, parent, node):
        pass

    def visit_WriteArg(self, parent, node):
        pass

    def visit_Elems(self, parent, node):
        pass

    def visit_Break(self, parent, node):
        pass

    def visit_Continue(self, parent, node):
        pass

    def visit_Return(self, parent, node):
        pass

    def visit_Exit(self, parent, node):
        pass

    def visit_Type(self, parent, node):
        pass

    def visit_Int(self, parent, node):
        pass

    def visit_Real(self, parent, node):
        pass

    def visit_Char(self, parent, node):
        pass

    def visit_String(self, parent, node):
        pass

    def visit_Bool(self, parent, node):
        pass

    def visit_Id(self, parent, node):
        pass

    def visit_BinOp(self, parent, node):
        pass

    def visit_UnOp(self, parent, node):
        pass

    def visit_NoneType(self, parent, node):
        pass

    def symbolize(self):
        self.visit(None, self.ast)
