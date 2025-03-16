from lark import Lark
from ast_builder import ASTBuilder

# Load grammar from file
with open("xdlang_grammar.lark") as f:
    xdlang_grammar = f.read()

# Initialize parser with LALR algorithm
parser = Lark(xdlang_grammar, start="start", parser="lalr")
transformer = ASTBuilder()

def parse_xdlang(code):
    tree = parser.parse(code)
    return transformer.transform(tree)

# Sample XDLANG code
code = """
    let x = 10;
    print("Hello, XDLANG!");
"""

ast = parse_xdlang(code)
print(ast)
