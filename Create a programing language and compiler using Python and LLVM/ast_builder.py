from lark import Transformer, Token

class ASTBuilder(Transformer):
    def start(self, items):
        return items

    def assign_stmt(self, items):
        # items: variable, expression
        return {"type": "assign", "name": items[0], "value": items[1]}
    
    def print_stmt(self, items):
        # items: expression to print
        return {"type": "print", "value": items[0]}
    
    def if_stmt(self, items):
        # items: condition, then-statements, (optional) else-statements
        node = {"type": "if", "condition": items[0], "then": items[1]}
        if len(items) > 2:
            node["else"] = items[2]
        return node

    def while_stmt(self, items):
        # items: condition, body-statements
        return {"type": "while", "condition": items[0], "body": items[1]}
    
    def func_def(self, items):
        # items: function name, optional parameter list, and body-statements
        name = items[0]
        if len(items) == 3:
            params = items[1]
            body = items[2]
        else:
            params = []
            body = items[1]
        return {"type": "function_def", "name": name, "params": params, "body": body}

    def param_list(self, items):
        return items

    def func_call(self, items):
        # items: function name, optional argument list
        name = items[0]
        args = items[1] if len(items) == 2 else []
        return {"type": "func_call", "name": name, "args": args}

    def arg_list(self, items):
        return items

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
    
    def string(self, items):
        token = items[0]
        return token.value.strip('"') if isinstance(token, Token) else token
    
    def variable(self, items):
        token = items[0]
        return {"type": "variable", "name": token.value if isinstance(token, Token) else token}
