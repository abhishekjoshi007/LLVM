from llvmlite import ir

class CodeGen:
    def __init__(self):
        self.module = ir.Module(name="xdlang_module")
        self.builder = None
        self.printf = None
        self.string_constants = {}
        self.local_vars = {}

    def generate_ir(self, ast):
        if ast["type"] != "program":
            raise Exception("Expected top-level 'program' node")

        for func in ast["functions"]:
            self.compile_function(func)

    def compile_function(self, func):
        fn_return_type = ir.IntType(32)
        fn_type = ir.FunctionType(fn_return_type, [])
        llvm_func = ir.Function(self.module, fn_type, name=func["name"])

        block = llvm_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        if not self.printf:
            self.declare_printf()

        self.local_vars = {}

        for stmt in func["body"]:
            self.compile_stmt(stmt)

        # If no return statement was hit, return 0 by default
        if not block.is_terminated:
            self.builder.ret(ir.Constant(ir.IntType(32), 0))

    def declare_printf(self):
        # int printf(const char*, ...)
        printf_ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        self.printf = ir.Function(self.module, printf_ty, name="printf")

    def compile_stmt(self, stmt):
        stype = stmt["type"]
        if stype == "let":
            var_name = stmt["name"]
            var_ptr = self.builder.alloca(ir.IntType(32), name=var_name)
            val = self.compile_expr(stmt["value"])
            self.builder.store(val, var_ptr)
            self.local_vars[var_name] = var_ptr
        elif stype == "mut":
            var_name = stmt["name"]
            var_ptr = self.local_vars[var_name]
            val = self.compile_expr(stmt["value"])
            self.builder.store(val, var_ptr)
        elif stype == "print":
            val = self.compile_expr(stmt["value"])
            self.print_int(val)
        elif stype == "if":
            self.compile_if(stmt)
        elif stype == "while":
            self.compile_while(stmt)
        elif stype == "return":
            ret_val = self.compile_expr(stmt["value"])
            self.builder.ret(ret_val)
        else:
            raise Exception(f"Unhandled statement type: {stype}")

    def compile_expr(self, expr):
        if isinstance(expr, int):
            return ir.Constant(ir.IntType(32), expr)

        if isinstance(expr, dict) and expr["type"] == "variable":
            var_ptr = self.local_vars[expr["name"]]
            return self.builder.load(var_ptr)

        etype = expr.get("type")
        if etype == "add":
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
            raise Exception(f"Unknown expression type: {etype}")

    def print_int(self, val):
        fmt_str = "%d\n"
        c_str = self.get_string_constant(fmt_str)
        self.builder.call(self.printf, [c_str, val])

    def get_string_constant(self, text):
        if text in self.string_constants:
            return self.string_constants[text]
        text_bytes = bytearray(text.encode("utf8")) + b"\0"
        const_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(text_bytes)), text_bytes)
        global_var = ir.GlobalVariable(self.module, const_str.type, name=f"str_{len(self.string_constants)}")
        global_var.linkage = "internal"
        global_var.global_constant = True
        global_var.initializer = const_str
        ptr = self.builder.bitcast(global_var, ir.PointerType(ir.IntType(8)))
        self.string_constants[text] = ptr
        return ptr

    def compile_if(self, stmt):
        cond_val = self.compile_expr(stmt["condition"])
        if cond_val.type != ir.IntType(1):
            cond_val = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))

        then_bb = self.builder.append_basic_block("then")
        else_bb = self.builder.append_basic_block("else") if "else" in stmt else None
        merge_bb = self.builder.append_basic_block("merge")

        if else_bb:
            self.builder.cbranch(cond_val, then_bb, else_bb)
        else:
            self.builder.cbranch(cond_val, then_bb, merge_bb)

        # Then block
        self.builder.position_at_start(then_bb)
        for s in stmt["then"]:
            self.compile_stmt(s)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_bb)

        # Else block
        if else_bb:
            self.builder.position_at_start(else_bb)
            for s in stmt["else"]:
                self.compile_stmt(s)
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_bb)

        self.builder.position_at_start(merge_bb)

    def compile_while(self, stmt):
        cond_bb = self.builder.append_basic_block("while.cond")
        body_bb = self.builder.append_basic_block("while.body")
        end_bb = self.builder.append_basic_block("while.end")

        self.builder.branch(cond_bb)
        self.builder.position_at_start(cond_bb)
        cond_val = self.compile_expr(stmt["condition"])
        if cond_val.type != ir.IntType(1):
            cond_val = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))
        self.builder.cbranch(cond_val, body_bb, end_bb)

        self.builder.position_at_start(body_bb)
        for s in stmt["body"]:
            self.compile_stmt(s)
        if not self.builder.block.is_terminated:
            self.builder.branch(cond_bb)

        self.builder.position_at_start(end_bb)
