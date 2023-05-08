from rply import ParserGenerator
from ast import Number, Sum, Sub, Print


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['OPEN_PAREN',
             'CLOSE_PAREN',
             'SEMI_COLON',
             'SUM',
             'SUB',
             'MUL',
             'DIV',
             'EQQ',
             'LES',
             'LEQ',
             'GRT',
             'GEQ',
             'AND',
             'OR',
             'NOT',
             'BLOCK_START',
             'BLOCK_END',
             'DECLARATION',
             'ASSIGNMENT',
             'PRINT',
             'WHILE_LOOP',
             'FOR_LOOP',
             'IF',
             'ELSE',
             'FUNCTION_DECLARATION',
             'COMMA',
             'STATEMENT_END',
             'RETURN',
             'AS',
             'TYPE',
             'INT',
             'STRING',
             'IDENTIFIER']
        )

    def parse(self):
        @self.pg.production("program : statements")
        def program(p):
            return p

        @self.pg.production('statements : statements statement')
        @self.pg.production('statements : statement')
        def statements(p):
            return p

        @self.pg.production("statement : declaration")
        @self.pg.production("statement : assignment")
        @self.pg.production("statement : print")
        @self.pg.production("statement : if_statement")
        @self.pg.production("statement : while_loop")
        @self.pg.production("statement : for_loop")
        @self.pg.production("statement : function_declaration")
        @self.pg.production("statement : function_call")
        @self.pg.production("statement : return")
        def statement(p):
            return p

        @self.pg.production("block: BLOCK_START statements BLOCK_END")
        def block(p):
            return p

        @self.pg.production("assignment : IDENTIFIER ASSIGNMENT relExpression SEMI_COLON")
        def assignment(p):
            pass

        @self.pg.production("declaration : DECLARATION TYPE AS IDENTIFIER SEMI_COLON")
        @self.pg.production("declaration : DECLARATION TYPE AS IDENTIFIER ASSIGNMENT relExpression SEMI_COLON")
        def declaration(p):
            pass

        @self.pg.production("print : PRINT OPEN_PAREN relExpression CLOSE_PAREN SEMI_COLON")
        def print(p):
            pass

        @self.pg.production("while_loop : WHILE_LOOP OPEN_PAREN relExpression CLOSE_PAREN block SEMI_COLON")
        def while_loop(p):
            pass

        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN (assignment)? SEMICOLON (relExpression)? SEMICOLON (relExpression)? CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN (declaration)? SEMICOLON (relExpression)? SEMICOLON (relExpression)? CLOSE_PAREN block SEMI_COLON")
        def for_loop(p):
            pass

        @self.pg.production("if_statement : 'testify' LPAREN relExpression RPAREN block")
        @self.pg.production("if_statement : 'testify' LPAREN relExpression RPAREN block 'otherwise' block")
        def if_statement(p):
            pass

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'SUM':
                return Sum(left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(left, right)

        @self.pg.production('expression : NUMBER')
        def number(p):
            return Number(p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
