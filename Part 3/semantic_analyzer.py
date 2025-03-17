class SemanticAnalyzer:
    """
    Performs basic checks on the AST:
    - Ensures a 'main' function exists
    - Variables declared before use (simple approach)
    - (Optional) Ensures break/continue appear inside loops
    """

    def __init__(self):
        self.has_main = False
        self.symbols = {}  # var_name -> type
        self.in_loop = 0   # track if we're inside a loop

    def analyze(self, ast):
        if ast["type"] != "program":
            raise Exception("Top-level AST must be 'program'")

        for func in ast["functions"]:
            self.visit_function(func)

        if not self.has_main:
            raise Exception("No 'main' function found!")

    def visit_function(self, func):
        if func["name"] == "main":
            self.has_main = True
            # Check return type
            if func["ret_type"] != "int":
                raise Exception("main() must return int")

        # Reset symbols for each function
        self.symbols = {}
        self.in_loop = 0

        for stmt in func["body"]:
            self.visit_stmt(stmt)

    def visit_stmt(self, stmt):
        stype = stmt["type"]
        if stype == "let":
            var_name = stmt["name"]
            if var_name in self.symbols:
                raise Exception(f"Variable '{var_name}' already declared.")
            self.symbols[var_name] = stmt["var_type"]
        elif stype == "mut":
            var_name = stmt["name"]
            if var_name not in self.symbols:
                raise Exception(f"Variable '{var_name}' not declared.")
        elif stype == "print":
            pass
        elif stype == "if":
            self.visit_expr(stmt["condition"])
            for s in stmt["then"]:
                self.visit_stmt(s)
            if "else" in stmt:
                for s in stmt["else"]:
                    self.visit_stmt(s)
        elif stype == "while":
            self.visit_expr(stmt["condition"])
            self.in_loop += 1
            for s in stmt["body"]:
                self.visit_stmt(s)
            self.in_loop -= 1
        elif stype == "break":
            if self.in_loop == 0:
                raise Exception("break statement not inside a loop")
        elif stype == "continue":
            if self.in_loop == 0:
                raise Exception("continue statement not inside a loop")
        elif stype == "return":
            self.visit_expr(stmt["value"])
        else:
            raise Exception(f"Unknown statement type: {stype}")

    def visit_expr(self, expr):
        # If it's an int, or basic dict with 'type'
        if isinstance(expr, int):
            return
        if not isinstance(expr, dict):
            return
        etype = expr["type"]
        if etype == "variable":
            var_name = expr["name"]
            if var_name not in self.symbols:
                raise Exception(f"Variable '{var_name}' not declared.")
        elif etype in ("add","sub","mul","div","mod","eq","ne","lt","le","gt","ge","or","and"):
            self.visit_expr(expr["left"])
            self.visit_expr(expr["right"])
        elif etype in ("neg","not"):
            self.visit_expr(expr["value"])
        else:
            # Possibly other checks
            pass
