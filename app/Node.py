from threading import local


class Node:
    pass


class Program(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Decl(Node):
    def __init__(self, type_, id_):
        self.type_ = type_
        self.id_ = id_


class ArrayDecl(Node):
    def __init__(self, type_, id_, from_, to_, elems):
        self.type_ = type_
        self.id_ = id_
        self.from_ = from_
        self.to_ = to_
        self.elems = elems


class ArrayElem(Node):
    def __init__(self, id_, index):
        self.id_ = id_
        self.index = index


class StringDecl(Node):
    def __init__(self, type_, id_, size):
        self.type_ = type_
        self.id_ = id_
        self.size = size


class Assign(Node):
    def __init__(self, id_, expr):
        self.id_ = id_
        self.expr = expr


class If(Node):
    def __init__(self, cond, true, elseifs, false):
        self.cond = cond
        self.true = true
        self.elseifs = elseifs
        self.false = false


class ElseIf(Node):
    def __init__(self, cond, true):
        self.cond = cond
        self.true = true


class Else(Node):
    def __init__(self, block):
        self.block = block


class While(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class RepeatUntil(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class For(Node):
    def __init__(self, init, goal, block, is_to):
        self.init = init
        self.goal = goal
        self.block = block
        self.is_to = is_to


class FuncImpl(Node):
    def __init__(self, type_, id_, params, block, local_variables):
        self.type_ = type_
        self.id_ = id_
        self.params = params
        self.block = block
        self.local_variables = local_variables


class FuncCall(Node):
    def __init__(self, id_, args):
        self.id_ = id_
        self.args = args


class ProcImpl(Node):
    def __init__(self, id_, params, block, local_variables):
        self.id_ = id_
        self.params = params
        self.block = block
        self.local_variables = local_variables


class ProcCall(Node):
    def __init__(self, id_, args):
        self.id_ = id_
        self.args = args


class Block(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Params(Node):
    def __init__(self, params):
        self.params = params


class LocalVars(Node):
    def __init__(self, local_variables):
        self.local_variables = local_variables


class Args(Node):
    def __init__(self, args):
        self.args = args


class WriteArg(Node):
    def __init__(self, expr, total_characters, places_after_dot):
        self.expr = expr
        self.total_characters = total_characters
        self.places_after_dot = places_after_dot


class Elems(Node):
    def __init__(self, elems):
        self.elems = elems


class Break(Node):
    pass


class Continue(Node):
    pass


class Exit(Node):
    def __init__(self, expr):
        self.expr = expr


class Type(Node):
    def __init__(self, value):
        self.value = value


class Int(Node):
    def __init__(self, value):
        self.value = value


class Real(Node):
    def __init__(self, value):
        self.value = value


class Char(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Id(Node):
    def __init__(self, value):
        self.value = value


class Bool(Node):
    def __init__(self, value):
        self.value = value


class BinOp(Node):
    def __init__(self, symbol, first, second):
        self.symbol = symbol
        self.first = first
        self.second = second


class UnOp(Node):
    def __init__(self, symbol, first):
        self.symbol = symbol
        self.first = first
