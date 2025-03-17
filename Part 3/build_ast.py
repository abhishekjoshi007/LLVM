from parser import parse_code
from ast_builder import ASTBuilder
import sys

def build_ast(filename):
    """
    Reads .xd file, parses it into a parse tree,
    then transforms into an AST using ASTBuilder.
    """
    with open(filename) as f:
        code = f.read()
    tree = parse_code(code)
    if tree is None:
        return None
    ast = ASTBuilder().transform(tree)
    return ast

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_ast.py <file.xd>")
        sys.exit(1)

    filename = sys.argv[1]
    ast = build_ast(filename)
    if ast:
        print(ast)
    else:
        print("Failed to build AST.")
