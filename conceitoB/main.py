import sys
from classes import Parser

def print_ast(node, level=0, max_depth=8):
    if level >= max_depth:
        return
    print('    ' * level + str(node.__class__.__name__) + ' ' + str(node.value))
    for child in node.children:
        print_ast(child, level+1, max_depth)


def main(expression: str, debug=False):
    parser = Parser()
    ast = parser.run(expression)
    if debug:
        print_ast(ast)
    else:
        ast.evaluate()
    return


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.exit()
    try:
        with open(sys.argv[1], "r") as f:
            file = f.read()
    except:
        raise Exception("Erro ao ler o arquivo de input")

    main(file, len(sys.argv) == 3)
    # main(sys.argv[1])
