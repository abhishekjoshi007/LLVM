from lark import Transformer, v_args

class ASTBuilder(Transformer):
    """
    Transforms the parse tree from parser.py into a Python dictionary AST.
    Each rule in the grammar has a corresponding method.
    """

    def start(self, items):
        # items is a list of function nodes
        return {
            "type": "program",
            "functions": items
        }

    def function(self, items):
        # items = [CNAME, type, block]
        fn_name = items[0].value if hasattr(items[0], "value") else items[0]
        fn_ret_type = items[1]
        fn_body = items[2]
        return {
            "type": "function",
            "name": fn_name,
            "ret_type": fn_ret_type,
            "body": fn_body
        }

    def block(self, items):
        # items is a list of statements
        return items

    def statement(self, items):
        # Flatten the statement rule
        return items[0]

    def return_stmt(self, items):
        return {"type": "return", "value": items[0]}

    def let_stmt(self, items):
        # items = [type, CNAME, expr]
        var_type, var_name, value = items
        var_name_str = var_name.value if hasattr(var_name, "value") else var_name
        return {
            "type": "let",
            "var_type": var_type,
            "name": var_name_str,
            "value": value
        }

    def mut_stmt(self, items):
        # items = [CNAME, expr]
        var_name, value = items
        var_name_str = var_name.value if hasattr(var_name, "value") else var_name
        return {
            "type": "mut",
            "name": var_name_str,
            "value": value
        }

    def print_stmt(self, items):
        return {"type": "print", "value": items[0]}

    def if_stmt(self, items):
        # items = [expr, then_block, (optional) else_block]
        node = {
            "type": "if",
            "condition": items[0],
            "then": items[1]
        }
        if len(items) == 3:
            node["else"] = items[2]
        return node

    def while_stmt(self, items):
        # items = [expr, block]
        return {
            "type": "while",
            "condition": items[0],
            "body": items[1]
        }

    def break_stmt(self, items):
        return {"type": "break"}

    def continue_stmt(self, items):
        return {"type": "continue"}

    def type(self, items):
        # We only have "int" for now
        return "int"

    # ------------------ Expressions ------------------
    def logical_or(self, items):
        return {"type": "or", "left": items[0], "right": items[1]}

    def logical_and(self, items):
        return {"type": "and", "left": items[0], "right": items[1]}

    def eq(self, items):
        return {"type": "eq", "left": items[0], "right": items[1]}

    def ne(self, items):
        return {"type": "ne", "left": items[0], "right": items[1]}

    def lt(self, items):
        return {"type": "lt", "left": items[0], "right": items[1]}

    def le(self, items):
        return {"type": "le", "left": items[0], "right": items[1]}

    def gt(self, items):
        return {"type": "gt", "left": items[0], "right": items[1]}

    def ge(self, items):
        return {"type": "ge", "left": items[0], "right": items[1]}

    def add(self, items):
        return {"type": "add", "left": items[0], "right": items[1]}

    def sub(self, items):
        return {"type": "sub", "left": items[0], "right": items[1]}

    def mul(self, items):
        return {"type": "mul", "left": items[0], "right": items[1]}

    def div(self, items):
        return {"type": "div", "left": items[0], "right": items[1]}

    def mod(self, items):
        return {"type": "mod", "left": items[0], "right": items[1]}

    def logical_not(self, items):
        return {"type": "not", "value": items[0]}

    def neg(self, items):
        return {"type": "neg", "value": items[0]}

    def number(self, items):
        # Convert the token to an integer
        return int(items[0])

    def variable(self, items):
        # Return a dict so we know it's a variable reference
        token = items[0]
        return {"type": "variable", "name": token.value if hasattr(token, "value") else token}
