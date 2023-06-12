reserved_keywords = [
    "baptize",
    "giveth",
    "proclaim",
    "prayAsLongAs",
    "testify",
    "otherwise",
    "preach",
    "amen",
    "as",
]

translated_reserved_keywords = [
    "DECLARATION",
    "ASSIGNMENT",
    "PRINT",
    "WHILE_LOOP",
    "IF",
    "ELSE",
    "FUNCTION_DECLARATION",
    "RETURN",
    "AS"
]


variable_types = [
    "int",
    "string",
]


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value


class Tokenizer():
    def __init__(self, source: str):
        self.source = source.strip()
        self.position = 0
        self.next = None

    def selectNext(self):
        if self.position == len(self.source):
            self.next = Token("EOF", None)
            return

        # # Remove os zeros que precedem o tokem:
        while self.source[self.position] == " " or self.source[self.position] == "\n":
            self.position += 1

        # Checa por INT
        if self.source[self.position].isdigit():
            int_string = ""
            for char in self.source[self.position:]:
                if char.isdigit():
                    int_string += char
                else:
                    break
            self.next = Token("INT", int(int_string))
            self.position += len(int_string)

        # Checa por IDENTIFIER
        elif self.source[self.position].isalpha():
            assign_string = ""
            for char in self.source[self.position:]:
                if char.isdigit() or char.isalpha() or char == "_":
                    assign_string += char
                else:
                    break
            if assign_string in reserved_keywords:
                index = reserved_keywords.index(assign_string)
                self.next = Token(
                    translated_reserved_keywords[index], assign_string)
            elif assign_string in variable_types:
                self.next = Token("TYPE", assign_string)
            else:
                self.next = Token("IDEN", str(assign_string))
            self.position += len(assign_string)

        # Check for String:
        elif self.source[self.position] == '"':
            string = ""
            for char in self.source[self.position + 1:]:
                if char != '"':
                    string += char
                else:
                    break
            self.next = Token("STRING", string)
            self.position += len(string) + 2

        # Check for ==:
        elif self.source[self.position] == "=" and self.source[self.position + 1] == "=":
            self.next = Token("EQ", "==")
            self.position += 2
        # Check for ||:
        elif self.source[self.position] == "|" and self.source[self.position + 1] == "|":
            self.next = Token("OR", "||")
            self.position += 2

        # Check for &&:
        elif self.source[self.position] == "&" and self.source[self.position + 1] == "&":
            self.next = Token("AND", "&&")
            self.position += 2

        else:
            for index, char in enumerate(self.source[self.position:]):
                if char == "+":
                    self.next = Token("ADD", char)
                    break
                elif char == "-":
                    self.next = Token("SUB", char)
                    break
                elif char == "*":
                    self.next = Token("MULT", char)
                    break
                elif char == "/":
                    self.next = Token("DIV", char)
                    break
                elif char == "(":
                    self.next = Token("OP_PAR", char)
                    break
                elif char == ")":
                    self.next = Token("CL_PAR", char)
                    break
                elif char == "{":
                    self.next = Token("OP_BRACK", char)
                    break
                elif char == "}":
                    self.next = Token("CL_BRACK", char)
                    break
                # elif char == "=":
                #     self.next = Token("ASSIGN", char)
                #     break
                elif char == ">":
                    self.next = Token("GRT", char)
                    break
                elif char == "<":
                    self.next = Token("LST", char)
                    break
                elif char == "!":
                    self.next = Token("NOT", char)
                    break
                elif char == ".":
                    self.next = Token("CONCAT", char)
                    break
                elif char == ",":
                    self.next = Token("COMMA", char)
                    break
                elif char == ";":
                    self.next = Token("SEMICOLON", char)
                    break
                else:
                    raise Exception(f"Invalid character {char}")
            self.position += index + 1
        # print(f"Chamada do selectNext(): {self.next.token_type} e {self.next.value}")
        return
