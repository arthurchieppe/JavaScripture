from rply import ParserGenerator
from AST import *


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
            print("Edir")
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

        @self.pg.production("block : BLOCK_START statements BLOCK_END")
        def block(p):
            return p

        @self.pg.production("assignment : IDENTIFIER ASSIGNMENT relExpression SEMI_COLON")
        def assignment(p):
            return p

        @self.pg.production("declaration : DECLARATION TYPE AS IDENTIFIER SEMI_COLON")
        @self.pg.production("declaration : DECLARATION TYPE AS IDENTIFIER ASSIGNMENT relExpression SEMI_COLON")
        def declaration(p):
            return p

        @self.pg.production("print : PRINT OPEN_PAREN relExpression CLOSE_PAREN SEMI_COLON")
        def print(p):
            return p

        @self.pg.production("while_loop : WHILE_LOOP OPEN_PAREN relExpression CLOSE_PAREN block SEMI_COLON")
        def while_loop(p):
            return p

        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN assignment SEMI_COLON relExpression SEMI_COLON relExpression CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN declaration SEMI_COLON relExpression SEMI_COLON relExpression CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN declaration SEMI_COLON relExpression SEMI_COLON relExpression CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN SEMI_COLON relExpression SEMI_COLON relExpression CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN assignment SEMI_COLON SEMI_COLON relExpression CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN declaration SEMI_COLON SEMI_COLON relExpression CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN assignment SEMI_COLON relExpression SEMI_COLON CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN declaration SEMI_COLON relExpression SEMI_COLON CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("for_loop : FOR_LOOP OPEN_PAREN SEMI_COLON SEMI_COLON CLOSE_PAREN block SEMI_COLON")
        def for_loop(p):
            return p

        @self.pg.production("if_statement : IF OPEN_PAREN relExpression CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("if_statement : IF OPEN_PAREN relExpression CLOSE_PAREN block ELSE block SEMI_COLON")
        def if_statement(p):
            return p

        # Function declaration
        @self.pg.production("function_declaration : FUNCTION_DECLARATION TYPE AS IDENTIFIER OPEN_PAREN CLOSE_PAREN block SEMI_COLON")
        @self.pg.production("function_declaration : FUNCTION_DECLARATION TYPE AS IDENTIFIER OPEN_PAREN parameters CLOSE_PAREN block SEMI_COLON")
        def function_declaration(p):
            return p

        # Parameters
        @self.pg.production("parameters : parameter")
        @self.pg.production("parameters : parameter COMMA parameters")
        def parameters(p):
            return p

        # Parameter
        @self.pg.production("parameter : TYPE AS IDENTIFIER")
        def parameter(p):
            return p

        # Function call
        @self.pg.production("function_call : IDENTIFIER OPEN_PAREN CLOSE_PAREN SEMI_COLON")
        @self.pg.production("function_call : IDENTIFIER OPEN_PAREN arguments CLOSE_PAREN SEMI_COLON")
        def function_call(p):
            return p

        # Arguments
        @self.pg.production("arguments : relExpression")
        @self.pg.production("arguments : relExpression COMMA arguments")
        def arguments(p):
            return p

        @self.pg.production("return : RETURN relExpression SEMI_COLON")
        def return_statement(p):
            return p

        @self.pg.production("relExpression : expression")
        @self.pg.production("relExpression : expression EQQ expression")
        @self.pg.production("relExpression : expression LES expression")
        @self.pg.production("relExpression : expression LEQ expression")
        @self.pg.production("relExpression : expression GRT expression")
        @self.pg.production("relExpression : expression GEQ expression")
        def relExpression(p):
            return p

        @self.pg.production("expression : term")
        @self.pg.production("expression : term SUM term")
        @self.pg.production("expression : term SUB term")
        @self.pg.production("expression : term OR term")
        def expression(p):
            return p

        @self.pg.production("term : factor")
        @self.pg.production("term : factor MUL factor")
        @self.pg.production("term : factor DIV factor")
        @self.pg.production("term : factor AND factor")
        def term(p):
            return p

        @self.pg.production("factor : OPEN_PAREN relExpression CLOSE_PAREN")
        @self.pg.production("factor : SUM factor")
        @self.pg.production("factor : SUB factor")
        @self.pg.production("factor : NOT factor")
        @self.pg.production("factor : INT")
        @self.pg.production("factor : STRING")
        @self.pg.production("factor : IDENTIFIER")
        def factor(p):
            return p

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
