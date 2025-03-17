class SemanticAnalyzer:
    def __init__(self):
        self.has_main = False
        self.symbols = {}  # var_name -> type

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
            if func["ret_type"] != "int":
                raise Exception("main() must return int")

        # Reset symbol table per function (simple approach)
        self.symbols = {}

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
                raise Exception(f"Variable '{var_name}' not declared before mut.")
        elif stype == "print":
            pass
        elif stype == "if":
            # Optionally analyze condition, then, else
            pass
        elif stype == "while":
            pass
        elif stype == "return":
            pass
        else:
            raise Exception(f"Unknown statement type: {stype}")

    
