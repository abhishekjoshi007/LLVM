from lark import Lark, UnexpectedInput

def parse_code(code: str):
    """
    Parses the XDLANG source code using xdlang_grammar_part3.lark.
    Returns a Lark parse tree if successful, or None if there's a parse error.
    """
    try:
        with open("xdlang_grammar_part3.lark") as f:
            grammar = f.read()
        parser = Lark(grammar, start="start", parser="lalr")
        tree = parser.parse(code)
        return tree
    except UnexpectedInput as e:
        print("Parse Error:")
        # Show a snippet of the error location
        line = e.get_context(code)
        print(line)
        return None
