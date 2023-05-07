from lexer import Lexer

text_input = """
baptize int as a = 3; proclaim a;
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

for token in tokens:
    print(token)
