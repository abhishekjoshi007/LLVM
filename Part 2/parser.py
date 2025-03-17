from lark import Lark
import os

def parse_code(code: str):
    grammar_path = os.path.abspath("xdlang_grammar_part2.lark")
    print("DEBUG: Reading grammar from:", grammar_path)

    with open(grammar_path) as f:
        grammar = f.read()
    print("DEBUG grammar:\n", grammar)

    parser = Lark(grammar, start="start", parser="lalr")
    tree = parser.parse(code)
    print("DEBUG parse tree:\n", tree.pretty())
    return tree
