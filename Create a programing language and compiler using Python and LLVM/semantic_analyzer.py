class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, ast):
        for node in ast:
            self.visit(node)

    def visit(self, node):
        t = node["type"]
        if t == "assign":
            var_name = node["name"]
            # In a real analyzer, you would check types and previous definitions.
            self.symbol_table[var_name] = "variable"
        elif t == "function_def":
            self.symbol_table[node["name"]] = "function"
        elif t in ("if", "while"):
            # Recursively check inside blocks
            self.visit(node["condition"])
            for stmt in node.get("then", []):
                self.visit(stmt)
            for stmt in node.get("else", []):
                self.visit(stmt)
            for stmt in node.get("body", []):
                self.visit(stmt)
        elif t in ("print", "add", "sub", "mul", "div", "func_call"):
            # For these, further analysis could be added
            pass
        # Extend as needed for more node types.
