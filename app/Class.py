
from enum import Enum, auto

class Class(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    FWDSLASH = auto()
    PERCENT = auto()

    OR = auto()
    AND = auto()
    NOT = auto()

    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()

    ASSIGN = auto()
    SEMICOLON = auto()
    COMMA = auto()

    TYPE = auto()
    INT = auto()
    CHAR = auto()
    STRING = auto()

    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()

    BEGIN = auto()
    END = auto()

    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()

    ADDRESS = auto()

    ID = auto()
    EOF = auto()