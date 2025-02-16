from lark import Lark

# Load the grammar
with open("xdlang_grammar.lark") as grammar_file:
    parser = Lark(grammar_file.read(), start="start")

# Example XDLANG code
xdlang_code = """
    x = 10;
    print(x);
    func add(a, b) {
        return a + b;
    }
"""

# Parse the code
tree = parser.parse(xdlang_code)

# Print the Abstract Syntax Tree (AST)
print(tree.pretty())
