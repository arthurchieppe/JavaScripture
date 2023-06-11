from AST import *

from tokenizer import Tokenizer


class Parser:

    def parseBlock(isSubBlock=False, block=None):
        if block is None:
            block = Block(None, [])
        while True:
            if isSubBlock:
                if Parser.tokenizer.next.token_type == "ELSE":
                    return block

            if Parser.tokenizer.next.token_type == "EOF":
                return block
            if Parser.tokenizer.next.token_type == "CL_BRACK" and isSubBlock:
                return block
            res_statement = Parser.parseStatement()
            Parser.checkTokenType("SEMICOLON")
            Parser.tokenizer.selectNext()
            block.children.append(res_statement)

    @staticmethod
    def checkTokenType(expected_type, error_message=None):
        if error_message is None:
            error_message = f"Syntax error: expected {expected_type} and got {Parser.tokenizer.next.token_type} {Parser.tokenizer.next.value}"
        if Parser.tokenizer.next.token_type != expected_type:
            raise Exception(error_message)

    @ staticmethod
    def parseStatement():
        if Parser.tokenizer.next.token_type == "DECLARATION":
            return Parser.parseDeclaration()
        elif Parser.tokenizer.next.token_type == "IDEN":
            return Parser.parseIdentifier()
        elif Parser.tokenizer.next.token_type == "PRINT":
            return Parser.parsePrintln()
        elif Parser.tokenizer.next.token_type == "WHILE":
            return Parser.parseWhile()
        elif Parser.tokenizer.next.token_type == "IF":
            return Parser.parseIf()
        elif Parser.tokenizer.next.token_type == "FUNCTION":
            return Parser.parseFuncDec()
        elif Parser.tokenizer.next.token_type == "RETURN":
            return Parser.parseReturn()

        else:
            raise Exception(
                "Sintaxe nào aderente à gramática (parseStatement)" + Parser.tokenizer.next.token_type + Parser.tokenizer.next.value)

    @ staticmethod
    def parseReturn():
        Parser.tokenizer.selectNext()
        expression = Parser.parseRelExpression()
        return Return(None, [expression])

    @ staticmethod
    def parseFuncDec():
        Parser.tokenizer.selectNext()
        if Parser.tokenizer.next.token_type != "IDEN":
            raise Exception("Sintaxe nào aderente à gramática (parseFuncDec)")
        name = Parser.tokenizer.next.value
        Parser.tokenizer.selectNext()
        if Parser.tokenizer.next.token_type != "OP_PAR":
            raise Exception("Sintaxe nào aderente à gramática (parseFuncDec)")
        varDecs = []
        # Parse parameters
        Parser.tokenizer.selectNext()
        while Parser.tokenizer.next.token_type != "CL_PAR":
            if Parser.tokenizer.next.token_type != "IDEN":
                raise Exception(
                    "Sintaxe nào aderente à gramática (parseFuncDec)")
            identifier = Identifier(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.token_type != "DEC":
                raise Exception(
                    "Sintaxe nào aderente à gramática (parseFuncDec)")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.token_type != "TYPE":
                raise Exception(
                    "Sintaxe nào aderente à gramática (parseFuncDec)")
            varDecs.append(VarDec(Parser.tokenizer.next.value, [identifier]))
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.token_type == "CL_PAR":
                break
            if Parser.tokenizer.next.token_type != "COMMA":
                raise Exception(
                    "Sintaxe nào aderente à gramática (parseFuncDec)")
            Parser.tokenizer.selectNext()

        # Parse function return type
        Parser.tokenizer.selectNext()
        if Parser.tokenizer.next.token_type != "DEC":
            raise Exception("Sintaxe nào aderente à gramática (parseFuncDec)")
        Parser.tokenizer.selectNext()
        if Parser.tokenizer.next.token_type != "TYPE":
            raise Exception("Sintaxe nào aderente à gramática (parseFuncDec)")
        funcReturnType = Parser.tokenizer.next.value
        Parser.tokenizer.selectNext()
        if Parser.tokenizer.next.token_type != "EOL":
            raise Exception("Sintaxe nào aderente à gramática (parseFuncDec)")

        block = Parser.parseBlock(isSubBlock=True)
        if Parser.tokenizer.next.token_type != "END":
            raise Exception("Sintaxe nào aderente à gramática (parseFuncDec)")
        Parser.tokenizer.selectNext()

        return FuncDec(funcReturnType, [Identifier(name)] + varDecs + [block])

    @ staticmethod
    def parseIf():
        Parser.tokenizer.selectNext()
        expression = Parser.parseRelExpression()
        if Parser.tokenizer.next.token_type != "EOL":
            raise Exception("Sintaxe nào aderente à gramática (parseIf)")
        Parser.tokenizer.selectNext()
        if_block = Parser.parseBlock(isSubBlock=True)
        if Parser.tokenizer.next.token_type == "END":
            Parser.tokenizer.selectNext()
            return If(None, [expression, if_block])
        elif Parser.tokenizer.next.token_type == "ELSE":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.token_type != "EOL":
                raise Exception("Sintaxe nào aderente à gramática (parseIf)")
            Parser.tokenizer.selectNext()
            else_block = Parser.parseBlock(isSubBlock=True)
            if Parser.tokenizer.next.token_type != "END":
                raise Exception("Sintaxe nào aderente à gramática (parseIf)")

            Parser.tokenizer.selectNext()
            return If(None, [expression, if_block, else_block])

    @ staticmethod
    def parseWhile():
        Parser.tokenizer.selectNext()
        # print("Cheguei")
        expression = Parser.parseRelExpression()
        # print("Cheguei 2")

        if Parser.tokenizer.next.token_type != "EOL":
            raise Exception("Sintaxe nào aderente à gramática (parseWhile)")
        Parser.tokenizer.selectNext()
        block = Parser.parseBlock(isSubBlock=True)
        if Parser.tokenizer.next.token_type != "END":
            raise Exception("Sintaxe nào aderente à gramática (parseWhile)")
        Parser.tokenizer.selectNext()
        # print("Block do parseWhile:" + str(block.children))
        return While(None, [expression, block])

    @staticmethod
    def parseIdentifier():
        identifier = Identifier(Parser.tokenizer.next.value)
        Parser.tokenizer.selectNext()
        if Parser.tokenizer.next.token_type == "ASSIGNMENT":
            Parser.tokenizer.selectNext()
            expression = Parser.parseRelExpression()
            return Assignment(None, [identifier, expression])
        Parser.checkTokenType("OP_PAR")
        Parser.tokenizer.selectNext()
        funcArguments = []
        while Parser.tokenizer.next.token_type != "CL_PAR":
            Parser.tokenizer.selectNext()
            funcArguments.append(
                Parser.parseRelExpression(isSubExpression=True))
            if Parser.tokenizer.next.token_type not in ["CL_PAR", "COMMA"]:
                raise Exception(
                    "Error parsing function call, expected ',' or ')'")
        return FuncCall(identifier, funcArguments)

    @ staticmethod
    def parseDeclaration():
        Parser.tokenizer.selectNext()
        Parser.checkTokenType("TYPE")
        dec_type = Parser.tokenizer.next.value
        Parser.tokenizer.selectNext()
        Parser.checkTokenType("AS")
        Parser.tokenizer.selectNext()
        Parser.checkTokenType("IDEN")
        identifier = Identifier(Parser.tokenizer.next.value)
        Parser.tokenizer.selectNext()
        if Parser.tokenizer.next.token_type == "SEMICOLON":
            return VarDec(dec_type, [identifier])
        Parser.checkTokenType("ASSIGNMENT")
        Parser.tokenizer.selectNext()
        expression = Parser.parseRelExpression()
        return VarDec(dec_type, [identifier, expression])

    @ staticmethod
    def parsePrintln():
        Parser.tokenizer.selectNext()
        Parser.checkTokenType("OP_PAR")
        Parser.tokenizer.selectNext()
        expression = Parser.parseRelExpression(isSubExpression=True)
        Parser.checkTokenType("CL_PAR")
        Parser.tokenizer.selectNext()
        return Println(None, [expression])

    @ staticmethod
    def parseRelExpression(isSubExpression: bool = False):
        expression = Parser.parseExpression()
        while True:
            if Parser.tokenizer.next.token_type == "CL_PAR" or Parser.tokenizer.next.token_type == "COMMA":
                if isSubExpression:
                    return expression
                else:
                    raise Exception(
                        f"Sintaxe nào aderente à gramática (parseRelExpression) {Parser.tokenizer.next.token_type} {Parser.tokenizer.next.value}")

            if Parser.tokenizer.next.token_type == "SEMICOLON" or Parser.tokenizer.next.token_type == "EOF":
                return expression

            elif Parser.tokenizer.next.token_type == "GRT":
                Parser.tokenizer.selectNext()
                expression = BinOp(">", [expression, Parser.parseExpression()])

            elif Parser.tokenizer.next.token_type == "LST":
                Parser.tokenizer.selectNext()
                expression = BinOp("<", [expression, Parser.parseExpression()])

            elif Parser.tokenizer.next.token_type == "EQ":
                Parser.tokenizer.selectNext()
                expression = BinOp(
                    "==", [expression, Parser.parseExpression()])
            elif Parser.tokenizer.next.token_type == "CONCAT":
                Parser.tokenizer.selectNext()
                expression = BinOp(".", [expression, Parser.parseExpression()])

            else:
                raise Exception(
                    "Sintaxe nào aderente à gramática (parseRelExpression)" + Parser.tokenizer.next.token_type + Parser.tokenizer.next.value)

    @ staticmethod
    def parseExpression():
        expression = Parser.parseTerm()
        while True:

            if Parser.tokenizer.next.token_type == "ADD":
                Parser.tokenizer.selectNext()
                expression = BinOp("+", [expression, Parser.parseTerm()])

            elif Parser.tokenizer.next.token_type == "SUB":
                Parser.tokenizer.selectNext()
                expression = BinOp("-", [expression, Parser.parseTerm()])

            elif Parser.tokenizer.next.token_type == "OR":
                Parser.tokenizer.selectNext()
                expression = BinOp("||", [expression, Parser.parseTerm()])

            else:
                return expression

    @ staticmethod
    def parseTerm():
        expression = Parser.parseFactor()
        while True:
            if Parser.tokenizer.next.token_type == "MULT":
                Parser.tokenizer.selectNext()
                expression = BinOp("*", [expression, Parser.parseFactor()])

            elif Parser.tokenizer.next.token_type == "DIV":
                Parser.tokenizer.selectNext()
                expression = BinOp("/", [expression, Parser.parseFactor()])

            elif Parser.tokenizer.next.token_type == "AND":
                Parser.tokenizer.selectNext()
                expression = BinOp("&&", [expression, Parser.parseTerm()])

            else:
                return expression

    @ staticmethod
    def parseFactor():
        if Parser.tokenizer.next.token_type == "INT":
            # result = Parser.tokenizer.next.value
            result = IntVal(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            return result
        if Parser.tokenizer.next.token_type == "STRING":
            result = StringVal(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            return result

        if Parser.tokenizer.next.token_type == "IDEN":
            identifier = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.token_type == "OP_PAR":
                funcArguments = []
                Parser.tokenizer.selectNext()
                while Parser.tokenizer.next.token_type != "CL_PAR":
                    funcArguments.append(
                        Parser.parseRelExpression(isSubExpression=True))
                    if Parser.tokenizer.next.token_type == "CL_PAR":
                        break

                    if Parser.tokenizer.next.token_type != "COMMA":
                        raise Exception(
                            "Error parsing function call, expected ',' or ')'")
                    Parser.tokenizer.selectNext()
                Parser.tokenizer.selectNext()
                return FuncCall(identifier, funcArguments)

            result = Identifier(identifier)
            # Parser.tokenizer.selectNext()
            return result

        elif Parser.tokenizer.next.token_type == "ADD":
            Parser.tokenizer.selectNext()
            return UnOp("+", [Parser.parseFactor()])

        elif Parser.tokenizer.next.token_type == "SUB":
            Parser.tokenizer.selectNext()
            return UnOp("-", [Parser.parseFactor()])

        elif Parser.tokenizer.next.token_type == "NOT":
            Parser.tokenizer.selectNext()
            return UnOp("!", [Parser.parseFactor()])

        elif Parser.tokenizer.next.token_type == "OP_PAR":
            Parser.tokenizer.selectNext()
            result = Parser.parseRelExpression(isSubExpression=True)
            if Parser.tokenizer.next.token_type == "CL_PAR":
                Parser.tokenizer.selectNext()
                return result
            else:
                raise Exception(
                    "Sintaxe nào aderente à gramática (parseFactor parenteses)")
        else:
            raise Exception(
                "Sintaxe nào aderente à gramática (parseFactor))\n Token: " + Parser.tokenizer.next.token_type + "\n  \
                        Position: " + str(Parser.tokenizer.position) + "\n Lenght: " + str(len(Parser.tokenizer.source)))

    @ staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        # Print all tokens
        # while Parser.tokenizer.next.token_type != "EOF":
        #     print(Parser.tokenizer.next.token_type,
        #           Parser.tokenizer.next.value)
        #     Parser.tokenizer.selectNext()
        return Parser.parseBlock()


class PrePro:
    @ staticmethod
    def filter(expression):
        ls_statement = expression.splitlines()
        for i, line in enumerate(ls_statement):
            if (index := line.find("#")) != -1:
                ls_statement[i] = line[:index]
        return "\n".join(ls_statement)
