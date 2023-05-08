from holy_lexer import Lexer
from holy_parser import Parser

# Open test.amen file and read it
with open("test.amen", "r") as file:
    text_input = file.read()

# Remove endfile
text_input = text_input.replace("$end", "")


lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)


def token_iter(tokens):
    for token in tokens:
        print(token)
        yield token


pg = Parser()
pg.parse()
parser = pg.get_parser()
try:
    parser.parse(token_iter(tokens))
    print("Parsing complete!")
except Exception as e:
    print(e)
    print("Parsing failed!")
