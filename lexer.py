
from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Print
        # Parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        # Semi Colon
        self.lexer.add('SEMI_COLON', r'\;')

        # Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')

        # Relative operators
        self.lexer.add('EQQ', r'\=\=')
        self.lexer.add('LES', r'\<')
        self.lexer.add('LEQ', r'\<\=')
        self.lexer.add('GRT', r'\>')
        self.lexer.add('GEQ', r'\>\=')
        self.lexer.add('AND', r'\&\&')
        self.lexer.add('OR', r'\|\|')

        # Unary operators
        self.lexer.add('NOT', r'\!')

        self.lexer.add('BLOCK_START', r'\{')
        self.lexer.add('BLOCK_END', r'\}')
        self.lexer.add('DECLARATION', r'baptize')
        self.lexer.add('ASSIGNMENT', r'giveth')
        self.lexer.add('PRINT', r'proclaim')
        self.lexer.add('WHILE_LOOP', r'prayAsLongAs')
        self.lexer.add('FOR_LOOP', r'blessFor')
        self.lexer.add('IF', r'testify')
        self.lexer.add('ELSE', r'otherwise')
        self.lexer.add('FUNCTION_DECLARATION', r'preach')
        self.lexer.add('COMMA', r',')
        self.lexer.add('STATEMENT_END', r';')
        self.lexer.add('RETURN', r'amen')
        self.lexer.add('AS', r'as')

        # Variable types
        self.lexer.add('TYPE', r'int|string')

        # Variables
        self.lexer.add('INT', r'\d+')
        self.lexer.add('STRING', r'\".*?\"')

        # Identifier
        self.lexer.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
