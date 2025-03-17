from lark import Transformer

class ASTBuilder(Transformer):
    def start(self, items):
        # items is a list of function nodes
        return {
            "type": "program",
            "functions": items
        }

    def function(self, items):
        # items = [CNAME, type, block]
        name = items[0]
        ret_type = items[1]
        block = items[2]
        # Convert name to string if it's a token
        name_value = name.value if hasattr(name, "value") else name
        return {
            "type": "function",
            "name": name_value,
            "ret_type": ret_type,
            "body": block
        }

    def block(self, items):
        return items

    def statement(self, items):
        # Flatten statement so you don't get Tree('statement', ...)
        return items[0]

    # --- Statements ---
    def let_stmt(self, items):
        # items = [type, CNAME, expr]
        var_type, var_name, value = items
        var_name_value = var_name.value if hasattr(var_name, "value") else var_name
        return {
            "type": "let",
            "var_type": var_type,
            "name": var_name_value,
            "value": value
        }

    def mut_stmt(self, items):
        # items = [CNAME, expr]
        var_name, value = items
        var_name_value = var_name.value if hasattr(var_name, "value") else var_name
        return {
            "type": "mut",
            "name": var_name_value,
            "value": value
        }

    def print_stmt(self, items):
        return {
            "type": "print",
            "value": items[0]
        }

    def if_stmt(self, items):
        # items = [condition, then_block, (optional) else_block]
        node = {
            "type": "if",
            "condition": items[0],
            "then": items[1]
        }
        if len(items) == 3:
            node["else"] = items[2]
        return node

    def while_stmt(self, items):
        # items = [condition, block]
        return {
            "type": "while",
            "condition": items[0],
            "body": items[1]
        }

    def return_stmt(self, items):
        return {
            "type": "return",
            "value": items[0]
        }

    # --- Type ---
    def type(self, items):
        return "int"

    # --- Expressions ---
    def add(self, items):
        return {"type": "add", "left": items[0], "right": items[1]}

    def sub(self, items):
        return {"type": "sub", "left": items[0], "right": items[1]}

    def mul(self, items):
        return {"type": "mul", "left": items[0], "right": items[1]}

    def div(self, items):
        return {"type": "div", "left": items[0], "right": items[1]}

    def number(self, items):
        return int(items[0])

    def variable(self, items):
        token = items[0]
        return {"type": "variable", "name": token.value if hasattr(token, "value") else token}
