from llvmlite import ir

class CodeGen:
    def __init__(self):
        self.module = ir.Module(name="xdlang_module")
        self.module.triple = "arm64-apple-macosx15.0.0"
        self.builder = None
        self.printf = None
        self.symbol_table = {}  
        self.string_constants = {}

    def declare_printf(self):
        # Declaring the printf function: int printf(const char *, ...)
        printf_ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        self.printf = ir.Function(self.module, printf_ty, name="printf")
    
    def get_string_constant(self, text):
        if text in self.string_constants:
            return self.string_constants[text]
        text_bytes = bytearray(text.encode("utf8")) + b"\0"
        const = ir.Constant(ir.ArrayType(ir.IntType(8), len(text_bytes)), text_bytes)
        global_str = ir.GlobalVariable(self.module, const.type, name=f"str_{len(self.string_constants)}")
        global_str.linkage = "internal"
        global_str.global_constant = True
        global_str.initializer = const
        ptr = self.builder.bitcast(global_str, ir.PointerType(ir.IntType(8)))
        self.string_constants[text] = ptr
        return ptr
    
    def create_main_function(self):
        func_type = ir.FunctionType(ir.IntType(32), [])
        main_func = ir.Function(self.module, func_type, name="main")
        entry = main_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(entry)
        self.declare_printf()
        return main_func

    def compile_ast(self, ast):
        for stmt in ast:
            self.compile_stmt(stmt)

    def compile_stmt(self, stmt):
        stype = stmt["type"]
        if stype == "assign":
            var_name = stmt["name"]
            val = self.compile_expr(stmt["value"])
            # If the variable already exists, just store the new value.
            if var_name in self.symbol_table:
                var_ptr = self.symbol_table[var_name]
                self.builder.store(val, var_ptr)
            else:
                # Allocate space for the variable in the entry block and store the value.
                var_ptr = self.builder.alloca(ir.IntType(32), name=var_name)
                self.builder.store(val, var_ptr)
                self.symbol_table[var_name] = var_ptr
        elif stype == "print":
            # For simplicity, assume print is used for string literals.
            if isinstance(stmt["value"], str):
                string_ptr = self.get_string_constant(stmt["value"])
                self.builder.call(self.printf, [string_ptr])
            else:
                # For non-string types, you would add a conversion routine.
                pass
        elif stype == "if":
            cond_val = self.compile_expr(stmt["condition"])
            # Convert condition to a boolean (i1) if needed:
            if cond_val.type != ir.IntType(1):
                cond_val = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))
            then_bb = self.builder.append_basic_block("then")
            else_bb = self.builder.append_basic_block("else") if "else" in stmt else None
            merge_bb = self.builder.append_basic_block("ifcont")
            if else_bb:
                self.builder.cbranch(cond_val, then_bb, else_bb)
            else:
                self.builder.cbranch(cond_val, then_bb, merge_bb)
            # Then block
            self.builder.position_at_start(then_bb)
            for s in stmt["then"]:
                self.compile_stmt(s)
            self.builder.branch(merge_bb)
            # Else block if exists
            if else_bb:
                self.builder.position_at_start(else_bb)
                for s in stmt["else"]:
                    self.compile_stmt(s)
                self.builder.branch(merge_bb)
            self.builder.position_at_start(merge_bb)
        elif stype == "while":
            cond_bb = self.builder.append_basic_block("while.cond")
            body_bb = self.builder.append_basic_block("while.body")
            end_bb = self.builder.append_basic_block("while.end")
            self.builder.branch(cond_bb)
            # Condition block
            self.builder.position_at_start(cond_bb)
            cond_val = self.compile_expr(stmt["condition"])
            if cond_val.type != ir.IntType(1):
                cond_val = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))
            self.builder.cbranch(cond_val, body_bb, end_bb)
            # Loop body
            self.builder.position_at_start(body_bb)
            for s in stmt["body"]:
                self.compile_stmt(s)
            self.builder.branch(cond_bb)
            # Continue after loop
            self.builder.position_at_start(end_bb)
        elif stype == "function_def":
            # Placeholder for function definitions
            pass
        elif stype == "func_call":
            # Placeholder for function calls
            pass
        else:
            raise Exception("Unknown statement type: " + stype)

    def compile_expr(self, expr):
        if isinstance(expr, int):
            return ir.Constant(ir.IntType(32), expr)
        if isinstance(expr, str):
            return self.get_string_constant(expr)
        # Otherwise, expr should be a dictionary with a "type" key.
        etype = expr.get("type")
        if etype == "variable":
            var_name = expr["name"]
            var_ptr = self.symbol_table.get(var_name)
            if var_ptr is None:
                raise Exception("Undefined variable: " + var_name)
            return self.builder.load(var_ptr)
        elif etype == "add":
            left = self.compile_expr(expr["left"])
            right = self.compile_expr(expr["right"])
            return self.builder.add(left, right)
        elif etype == "sub":
            left = self.compile_expr(expr["left"])
            right = self.compile_expr(expr["right"])
            return self.builder.sub(left, right)
        elif etype == "mul":
            left = self.compile_expr(expr["left"])
            right = self.compile_expr(expr["right"])
            return self.builder.mul(left, right)
        elif etype == "div":
            left = self.compile_expr(expr["left"])
            right = self.compile_expr(expr["right"])
            return self.builder.sdiv(left, right)
        else:
            raise Exception("Unhandled expression type: " + str(etype))
    
    def finalize(self):
        self.builder.ret(ir.Constant(ir.IntType(32), 0))
        return self.module

if __name__ == "__main__":
    # Updated sample AST with a terminating loop.
    ast = [
        {"type": "assign", "name": "x", "value": 5},  # Initialize x = 5
        {"type": "print", "value": "Hello, XDLANG!\n"},
        {"type": "if", "condition": {"type": "add", "left": 1, "right": 1},
         "then": [
             {"type": "print", "value": "Inside if\n"}
         ],
         "else": [
             {"type": "print", "value": "Inside else\n"}
         ]
        },
        {"type": "while", "condition": {"type": "variable", "name": "x"},
         "body": [
             {"type": "print", "value": "Looping...\n"},
             {"type": "assign", "name": "x", "value": {"type": "sub", "left": {"type": "variable", "name": "x"}, "right": 1}}
         ]
        }
    ]
    
    codegen = CodeGen()
    codegen.create_main_function()
    codegen.compile_ast(ast)
    module = codegen.finalize()
    
    with open("output.ll", "w") as f:
        f.write(str(module))
    
    print("LLVM IR written to output.ll")
