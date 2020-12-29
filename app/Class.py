
from enum import Enum, auto


class Class(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    FWDSLASH = auto()
    DIV = auto()
    MOD = auto()

    OR = auto()
    AND = auto()
    NOT = auto()
    XOR = auto()

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
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    DDOT = auto()

    VAR = auto()
    TYPE = auto()
    INT = auto()
    CHAR = auto()
    STRING = auto()
    BOOL = auto()
    REAL = auto()
    ARRAY = auto()

    PROCEDURE = auto()
    FUNCTION = auto()

    IF = auto()
    ELSEIF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    DO = auto()
    TO = auto()
    DOWNTO = auto()
    REPEAT = auto()
    UNTIL = auto()
    OF = auto()
    THEN = auto()

    BEGIN = auto()
    END = auto()

    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()

    ADDRESS = auto()

    EXIT = auto()

    ID = auto()
    EOF = auto()
