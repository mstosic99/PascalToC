from app.Token import Token
from app.Class import Class


class Lexer:
    def __init__(self, text):
        self.text = text
        self.len = len(text)
        self.pos = -1

    def read_space(self):
        while self.pos + 1 < self.len and self.text[self.pos + 1].isspace():
            self.advance_pos()

    def read_int(self):
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and self.text[self.pos + 1].isdigit():
            lexeme += self.advance_pos()
        return int(lexeme)

    def read_num(self):
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and self.text[self.pos + 1].isdigit():
            lexeme += self.advance_pos()
        if self.pos + 1 < self.len and self.text[self.pos + 1] == '.' and self.text[self.pos + 2] != '.':
            lexeme += self.text[self.pos + 1]
            self.advance_pos()
            while self.pos + 1 < self.len and self.text[self.pos + 1].isdigit():
                lexeme += self.advance_pos()
            return Token(Class.REAL, float(lexeme))
        else:
            return Token(Class.INT, int(lexeme))

    def read_char(self):
        self.pos += 1
        lexeme = self.text[self.pos]
        self.pos += 1
        return lexeme

    def read_string(self):
        lexeme = ''
        while self.pos + 1 < self.len and self.text[self.pos + 1] != '\'':
            lexeme += self.advance_pos()
        self.pos += 1
        return lexeme

    def read_keyword(self):
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and self.text[self.pos + 1].isalnum() or self.text[self.pos + 1] == '_':
            lexeme += self.advance_pos()
        if lexeme == 'if':
            return Token(Class.IF, lexeme)
        elif lexeme == 'else':
            if self.text[self.pos + 2] == 'i' and self.text[self.pos + 3] == 'f':
                lexeme += self.advance_pos() + self.advance_pos() + self.advance_pos()
                return Token(Class.ELSEIF, lexeme)
            else:
                return Token(Class.ELSE, lexeme)
        elif lexeme == 'while':
            return Token(Class.WHILE, lexeme)
        elif lexeme == 'for':
            return Token(Class.FOR, lexeme)
        elif lexeme == 'do':
            return Token(Class.DO, lexeme)
        elif lexeme == 'to':
            return Token(Class.TO, lexeme)
        elif lexeme == 'downto':
            return Token(Class.DOWNTO, lexeme)
        elif lexeme == 'break':
            return Token(Class.BREAK, lexeme)
        elif lexeme == 'continue':
            return Token(Class.CONTINUE, lexeme)
        elif lexeme == 'return':
            return Token(Class.RETURN, lexeme)
        elif lexeme == 'integer' or lexeme == 'char' or lexeme == 'boolean' or lexeme == 'string' or lexeme == 'real':
            return Token(Class.TYPE, lexeme)
        elif lexeme == 'begin':
            return Token(Class.BEGIN, lexeme)
        elif lexeme == 'end':
            return Token(Class.END, lexeme)
        elif lexeme == 'var':
            return Token(Class.VAR, lexeme)
        elif lexeme == 'div':
            return Token(Class.DIV, lexeme)
        elif lexeme == 'mod':
            return Token(Class.MOD, lexeme)
        elif lexeme == 'true' or lexeme == 'false':
            return Token(Class.BOOL, lexeme)
        elif lexeme == 'exit':
            return Token(Class.EXIT, lexeme)
        elif lexeme == 'repeat':
            return Token(Class.REPEAT, lexeme)
        elif lexeme == 'until':
            return Token(Class.UNTIL, lexeme)
        elif lexeme == 'procedure':
            return Token(Class.PROCEDURE, lexeme)
        elif lexeme == 'function':
            return Token(Class.FUNCTION, lexeme)
        elif lexeme == 'of':
            return Token(Class.OF, lexeme)
        elif lexeme == 'array':
            return Token(Class.ARRAY, lexeme)
        elif lexeme == 'then':
            return Token(Class.THEN, lexeme)
        elif lexeme == 'and':
            return Token(Class.AND, lexeme)
        elif lexeme == 'or':
            return Token(Class.OR, lexeme)
        elif lexeme == 'xor':
            return Token(Class.XOR, lexeme)
        elif lexeme == 'not':
            return Token(Class.NOT, lexeme)
        return Token(Class.ID, lexeme)

    def advance_pos(self):
        self.pos += 1
        if self.pos >= self.len:
            return None
        return self.text[self.pos]

    def next_token(self):
        self.read_space()
        curr = self.advance_pos()
        if curr is None:
            return Token(Class.EOF, curr)
        token = None
        if curr.isalpha() or curr == '_':
            token = self.read_keyword()
        elif curr.isdigit():
            token = self.read_num()
        elif curr == '\'':
            self.advance_pos()
            curr = self.advance_pos()
            if curr == '\'':
                self.pos -= 2
                token = Token(Class.CHAR, self.read_char())
            else:
                self.pos -= 2
                token = Token(Class.STRING, self.read_string())
        elif curr == '+':
            token = Token(Class.PLUS, curr)
        elif curr == '-':
            token = Token(Class.MINUS, curr)
        elif curr == '*':
            token = Token(Class.STAR, curr)
        elif curr == '/':
            token = Token(Class.FWDSLASH, curr)
        elif curr == '.':
            curr = self.advance_pos()
            if curr == '.':
                token = Token(Class.DDOT, '..')
            else:
                self.pos -= 1
                token = Token(Class.DOT, '.')
        elif curr == '=':
            curr = self.advance_pos()
            if curr == ' ':
                token = Token(Class.EQ, '=')
            else:
                self.die(curr)
        elif curr == ':':
            curr = self.advance_pos()
            if curr == '=':
                token = Token(Class.ASSIGN, ':=')
            else:
                token = Token(Class.COLON, ':')
                self.pos -= 1
        elif curr == '<':
            curr = self.advance_pos()
            if curr == '=':
                token = Token(Class.LTE, '<=')
            elif curr == '>':
                token = Token(Class.NEQ, '<>')
            else:
                token = Token(Class.LT, '<')
                self.pos -= 1
        elif curr == '>':
            curr = self.advance_pos()
            if curr == '=':
                token = Token(Class.GTE, '>=')
            else:
                token = Token(Class.GT, '>')
                self.pos -= 1
        elif curr == '(':
            token = Token(Class.LPAREN, curr)
        elif curr == ')':
            token = Token(Class.RPAREN, curr)
        elif curr == '[':
            token = Token(Class.LBRACKET, curr)
        elif curr == ']':
            token = Token(Class.RBRACKET, curr)
        elif curr == '{':
            token = Token(Class.LBRACE, curr)
        elif curr == '}':
            token = Token(Class.RBRACE, curr)
        elif curr == ';':
            token = Token(Class.SEMICOLON, curr)
        elif curr == ',':
            token = Token(Class.COMMA, curr)
        else:
            self.die(curr)
        return token

    def lex(self):
        tokens = []
        while True:
            curr = self.next_token()
            tokens.append(curr)
            if curr.class_ == Class.EOF:
                break
        return tokens

    def die(self, char):
        raise SystemExit("Unexpected character: {}".format(char))
