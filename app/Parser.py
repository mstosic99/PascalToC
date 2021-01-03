import pickle
from functools import wraps

from app.Class import Class
from app.Node import Id, Program, FuncCall, ArrayElem, Assign, ArrayDecl, FuncImpl, Decl, If, While, For, Block, Params, \
    Args, Elems, Break, Continue, Type, Int, Char, String, UnOp, BinOp, ProcImpl, LocalVars, Exit, RepeatUntil, Real, \
    StringDecl, ProcCall, Bool, ElseIf, Else, WriteArg


class Parser:
    is_write = False

    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = tokens.pop(0)
        self.prev = None

    def restorable(call):
        @wraps(call)
        def wrapper(self, *args, **kwargs):
            state = pickle.dumps(self.__dict__)
            result = call(self, *args, **kwargs)
            self.__dict__ = pickle.loads(state)
            return result

        return wrapper

    def eat(self, class_):
        if self.curr.class_ == class_:
            self.prev = self.curr
            self.curr = self.tokens.pop(0)
        else:
            self.die_type(class_.name, self.curr.class_.name)

    def program(self):
        nodes = []
        while self.curr.class_ != Class.EOF:
            if self.curr.class_ == Class.VAR:
                nodes.append(self.variables())
            elif self.curr.class_ == Class.FUNCTION:
                nodes.append(self.function())
            elif self.curr.class_ == Class.PROCEDURE:
                nodes.append(self.procedure())
            elif self.curr.class_ == Class.BEGIN:
                nodes.append(self.block())
                self.eat(Class.DOT)
            else:
                self.die_deriv(self.program.__name__)
        return Program(nodes)

    def variables(self):
        self.eat(Class.VAR)
        variables = []
        while self.curr.class_ != Class.BEGIN:
            ids = []
            while self.curr.class_ != Class.COLON:
                if len(ids) > 0:
                    self.eat(Class.COMMA)
                ids.append(Id(self.curr.lexeme))
                self.eat(Class.ID)
            self.eat(Class.COLON)
            if self.curr.class_ != Class.ARRAY:
                type_ = self.type_()
                if type_.value != 'string':
                    for id_ in ids:
                        variables.append(Decl(type_, id_))
                else:
                    size = Int(255)
                    if self.curr.class_ == Class.LBRACKET:
                        self.eat(Class.LBRACKET)
                        size = self.expr()
                        self.eat(Class.RBRACKET)
                    for id_ in ids:
                        variables.append(StringDecl(type_, id_, size))

            else:
                self.eat(Class.ARRAY)
                self.eat(Class.LBRACKET)
                from_ = Int(self.curr.lexeme)
                self.eat(Class.INT)
                self.eat(Class.DDOT)
                to_ = Int(self.curr.lexeme)
                self.eat(Class.INT)
                self.eat(Class.RBRACKET)
                self.eat(Class.OF)
                type_ = self.type_()
                elems = None
                if self.curr.class_ == Class.EQ:
                    self.eat(Class.EQ)
                    self.eat(Class.LPAREN)
                    elems = self.elems()
                    self.eat(Class.RPAREN)
                for e in ids:
                    variables.append(ArrayDecl(type_, e, from_, to_, elems))
            self.eat(Class.SEMICOLON)
        return LocalVars(variables)

    def function(self):
        self.eat(Class.FUNCTION)
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        self.eat(Class.LPAREN)
        params = self.params()
        self.eat(Class.RPAREN)
        self.eat(Class.COLON)
        type_ = Type(self.curr.lexeme)
        self.eat(Class.TYPE)
        self.eat(Class.SEMICOLON)
        local_variables = None
        if self.curr.class_ == Class.VAR:
            local_variables = self.variables()
        block = self.block()
        self.eat(Class.SEMICOLON)
        return FuncImpl(type_, id_, params, block, local_variables)

    def procedure(self):
        self.eat(Class.PROCEDURE)
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        self.eat(Class.LPAREN)
        params = self.params()
        self.eat(Class.RPAREN)
        self.eat(Class.SEMICOLON)
        local_variables = None
        if self.curr.class_ == Class.VAR:
            local_variables = self.variables()
        block = self.block()
        self.eat(Class.SEMICOLON)
        return ProcImpl(id_, params, block, local_variables)

    def id_(self):
        is_proc_call = self.prev.class_ == Class.SEMICOLON or self.prev.class_ == Class.BEGIN
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        is_proc_call = is_proc_call and self.curr.class_ == Class.LPAREN
        if self.curr.class_ == Class.LPAREN and self.is_func_call():
            self.is_write = False
            if self.prev.lexeme == 'write' or self.prev.lexeme == 'writeln':
                self.is_write = True
            self.eat(Class.LPAREN)
            args = self.args()
            self.eat(Class.RPAREN)
            self.is_write = True
            if is_proc_call:
                return ProcCall(id_, args)
            else:
                return FuncCall(id_, args)
        elif self.curr.class_ == Class.LBRACKET:
            self.eat(Class.LBRACKET)
            index = self.expr()
            self.eat(Class.RBRACKET)
            id_ = ArrayElem(id_, index)
        if self.curr.class_ == Class.ASSIGN:
            self.eat(Class.ASSIGN)
            logic = self.logic()
            return Assign(id_, logic)
        else:
            return id_

    def if_(self):
        self.eat(Class.IF)
        cond = self.logic()
        self.eat(Class.THEN)
        true = self.block()
        false = None
        elseifs = []
        while self.curr.class_ == Class.ELSE or self.curr.class_ == Class.ELSEIF:
            if self.curr.class_ == Class.ELSEIF:
                elseif = ElseIf(None, None)
                self.eat(Class.ELSEIF)
                elseif.cond = self.logic()
                self.eat(Class.THEN)
                elseif.true = self.block()
                elseifs.append(elseif)
            elif self.curr.class_ == Class.ELSE:
                self.eat(Class.ELSE)
                false = Else(self.block())

        self.eat(Class.SEMICOLON)
        return If(cond, true, elseifs, false)

    def while_(self):
        self.eat(Class.WHILE)
        cond = self.logic()
        self.eat(Class.DO)
        block = self.block()
        self.eat(Class.SEMICOLON)
        return While(cond, block)

    def for_(self):
        self.eat(Class.FOR)
        init = self.id_()
        is_to = None
        if self.curr.lexeme == 'to':
            self.eat(Class.TO)
            is_to = True
        elif self.curr.lexeme == 'downto':
            self.eat(Class.DOWNTO)
            is_to = False
        goal = self.expr()
        self.eat(Class.DO)
        block = self.block()
        self.eat(Class.SEMICOLON)
        return For(init, goal, block, is_to)

    def repeat_until(self):
        self.eat(Class.REPEAT)
        block = self.block_repeat_until()
        self.eat(Class.UNTIL)
        cond = self.logic()
        self.eat(Class.SEMICOLON)
        return RepeatUntil(cond, block)

    def block(self):
        nodes = []
        self.eat(Class.BEGIN)
        while self.curr.class_ != Class.END:
            if self.curr.class_ == Class.IF:
                nodes.append(self.if_())
            elif self.curr.class_ == Class.WHILE:
                nodes.append(self.while_())
            elif self.curr.class_ == Class.REPEAT:
                nodes.append(self.repeat_until())
            elif self.curr.class_ == Class.FOR:
                nodes.append(self.for_())
            elif self.curr.class_ == Class.BREAK:
                nodes.append(self.break_())
            elif self.curr.class_ == Class.CONTINUE:
                nodes.append(self.continue_())
            elif self.curr.class_ == Class.EXIT:
                nodes.append(self.exit_())
            elif self.curr.class_ == Class.ID:
                nodes.append(self.id_())
                self.eat(Class.SEMICOLON)
            else:
                self.die_deriv(self.block.__name__)
        self.eat(Class.END)
        return Block(nodes)

    def block_repeat_until(self):
        nodes = []
        while self.curr.class_ != Class.UNTIL:
            if self.curr.class_ == Class.IF:
                nodes.append(self.if_())
            elif self.curr.class_ == Class.WHILE:
                nodes.append(self.while_())
            elif self.curr.class_ == Class.REPEAT:
                nodes.append(self.repeat_until())
            elif self.curr.class_ == Class.FOR:
                nodes.append(self.for_())
            elif self.curr.class_ == Class.BREAK:
                nodes.append(self.break_())
            elif self.curr.class_ == Class.CONTINUE:
                nodes.append(self.continue_())
            elif self.curr.class_ == Class.EXIT:
                nodes.append(self.exit_())
            elif self.curr.class_ == Class.ID:
                nodes.append(self.id_())
                self.eat(Class.SEMICOLON)
            else:
                self.die_deriv(self.block.__name__)
        return Block(nodes)

    def params(self):
        params = []
        while self.curr.class_ != Class.RPAREN:
            ids = []
            if self.curr.class_ == Class.SEMICOLON:
                self.eat(Class.SEMICOLON)
            while self.curr.class_ != Class.COLON:
                if len(ids) > 0:
                    self.eat(Class.COMMA)
                ids.append(Id(self.curr.lexeme))
                self.eat(Class.ID)
            self.eat(Class.COLON)
            type_ = self.type_()
            for id_ in ids:
                params.append(Decl(type_, id_))
        return Params(params)

    def handle_write(self, args):
        total_characters = None
        places_after_dot = None
        a = self.curr.class_ == Class.LPAREN
        if self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
        expr = self.expr()
        if self.curr.class_ == Class.RPAREN and a:
            self.eat(Class.RPAREN)
        if type(expr) == Char:
            args.append(Char(expr.value))
            return
        if self.curr.class_ == Class.COLON:
            self.eat(Class.COLON)
            total_characters = Int(self.curr.lexeme)
            self.eat(Class.INT)
        if self.curr.class_ == Class.COLON:
            self.eat(Class.COLON)
            places_after_dot = Int(self.curr.lexeme)
            self.eat(Class.INT)
        args.append(WriteArg(expr, total_characters, places_after_dot))

    def args(self):
        args = []
        while self.curr.class_ != Class.RPAREN:
            if len(args) > 0:
                self.eat(Class.COMMA)
            if self.is_write:
                self.handle_write(args)
                continue
            args.append(self.expr())
        return Args(args)

    def elems(self):
        elems = []
        while self.curr.class_ != Class.RPAREN:
            if len(elems) > 0:
                self.eat(Class.COMMA)
            elems.append(self.expr())
        return Elems(elems)

    def exit_(self):
        self.eat(Class.EXIT)
        expr = self.expr()
        self.eat(Class.SEMICOLON)
        return Exit(expr)

    def break_(self):
        self.eat(Class.BREAK)
        self.eat(Class.SEMICOLON)
        return Break()

    def continue_(self):
        self.eat(Class.CONTINUE)
        self.eat(Class.SEMICOLON)
        return Continue()

    def type_(self):
        type_ = Type(self.curr.lexeme)
        self.eat(Class.TYPE)
        return type_

    def factor(self):
        if self.curr.class_ == Class.INT:
            value = Int(self.curr.lexeme)
            self.eat(Class.INT)
            return value
        elif self.curr.class_ == Class.REAL:
            value = Real(self.curr.lexeme)
            self.eat(Class.REAL)
            return value
        elif self.curr.class_ == Class.CHAR:
            value = Char(self.curr.lexeme)
            self.eat(Class.CHAR)
            return value
        elif self.curr.class_ == Class.STRING:
            value = String(self.curr.lexeme)
            self.eat(Class.STRING)
            return value
        elif self.curr.class_ == Class.BOOL:
            value = Bool(self.curr.lexeme)
            self.eat(Class.BOOL)
            return value
        elif self.curr.class_ == Class.ID:
            return self.id_()
        elif self.curr.class_ in [Class.MINUS, Class.NOT, Class.ADDRESS]:
            op = self.curr
            self.eat(self.curr.class_)
            first = None
            if self.curr.class_ == Class.LPAREN:
                self.eat(Class.LPAREN)
                first = self.logic()
                self.eat(Class.RPAREN)
            else:
                first = self.factor()
            return UnOp(op.lexeme, first)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.logic()
            self.eat(Class.RPAREN)
            return first
        elif self.curr.class_ == Class.SEMICOLON:
            return None
        else:
            self.die_deriv(self.factor.__name__)

    def term(self):
        first = self.factor()
        while self.curr.class_ in [Class.STAR, Class.DIV, Class.MOD, Class.FWDSLASH]:
            if self.curr.class_ == Class.STAR:
                op = self.curr.lexeme
                self.eat(Class.STAR)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.DIV:
                op = self.curr.lexeme
                self.eat(Class.DIV)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MOD:
                op = self.curr.lexeme
                self.eat(Class.MOD)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.FWDSLASH:
                op = self.curr.lexeme
                self.eat(Class.FWDSLASH)
                second = self.factor()
                first = BinOp(op, first, second)
        return first

    def expr(self):
        first = self.term()
        while self.curr.class_ in [Class.PLUS, Class.MINUS]:
            if self.curr.class_ == Class.PLUS:
                op = self.curr.lexeme
                self.eat(Class.PLUS)
                second = self.term()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MINUS:
                op = self.curr.lexeme
                self.eat(Class.MINUS)
                second = self.term()
                first = BinOp(op, first, second)
        return first

    def compare(self):
        first = self.expr()
        if self.curr.class_ == Class.EQ:
            op = self.curr.lexeme
            self.eat(Class.EQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.NEQ:
            op = self.curr.lexeme
            self.eat(Class.NEQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LT:
            op = self.curr.lexeme
            self.eat(Class.LT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GT:
            op = self.curr.lexeme
            self.eat(Class.GT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LTE:
            op = self.curr.lexeme
            self.eat(Class.LTE)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GTE:
            op = self.curr.lexeme
            self.eat(Class.GTE)
            second = self.expr()
            return BinOp(op, first, second)
        else:
            return first

    def logic_term(self):
        first = self.compare()
        while self.curr.class_ == Class.AND:
            op = self.curr.lexeme
            self.eat(Class.AND)
            second = self.compare()
            first = BinOp(op, first, second)
        return first

    def logic(self):
        first = self.logic_term()
        while self.curr.class_ == Class.OR:
            op = self.curr.lexeme
            self.eat(Class.OR)
            second = self.logic_term()
            first = BinOp(op, first, second)
        return first

    @restorable
    def is_func_call(self):
        try:
            if self.prev.lexeme == 'write' or self.prev.lexeme == 'writeln':
                self.is_write = True
            self.eat(Class.LPAREN)
            self.args()
            self.eat(Class.RPAREN)
            self.is_write = False
            return self.curr.class_ != Class.BEGIN
        except Exception as e:
            print(e)
            return False

    def parse(self):
        return self.program()

    def die(self, text):
        print(len(self.tokens))
        raise SystemExit(text)

    def die_deriv(self, fun):
        self.die("Derivation error: {}".format(fun))

    def die_type(self, expected, found):
        self.die("Expected: {}, Found: {}".format(expected, found))
