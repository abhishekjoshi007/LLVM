from parser import parse_code
from ast_builder import ASTBuilder

def build_ast(filename):
    with open(filename) as f:
        code = f.read()
    parse_tree = parse_code(code)
    ast = ASTBuilder().transform(parse_tree)
    return ast

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python build_ast.py <filename.xd>")
        exit(1)

    filename = sys.argv[1]
    ast = build_ast(filename)
    print(ast)
