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
            raise Exception("Expected 'program' node.")
        for func in ast["functions"]:
            self.compile_function(func)

    def compile_function(self, func):
        fn_return_type = ir.IntType(32)
        fn_type = ir.FunctionType(fn_return_type, [])
        llvm_func = ir.Function(self.module, fn_type, name=func["name"])

        block = llvm_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        # Declare printf if not done
        if not self.printf:
            self.declare_printf()

        # Clear local vars
        self.local_vars = {}

        for stmt in func["body"]:
            self.compile_stmt(stmt)

        # If no return encountered, return 0 by default
        if not block.is_terminated:
            self.builder.ret(ir.Constant(ir.IntType(32), 0))

    def declare_printf(self):
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
        elif stype == "break":
            # Minimal approach: we won't implement break in codegen yet
            pass
        elif stype == "continue":
            # Minimal approach: not implementing yet
            pass
        elif stype == "return":
            ret_val = self.compile_expr(stmt["value"])
            self.builder.ret(ret_val)
        else:
            raise Exception(f"Unhandled stmt type: {stype}")

    def compile_expr(self, expr):
        # If it's an integer literal
        if isinstance(expr, int):
            return ir.Constant(ir.IntType(32), expr)
        if not isinstance(expr, dict):
            raise Exception(f"Unknown expr: {expr}")

        etype = expr["type"]
        if etype == "variable":
            var_ptr = self.local_vars[expr["name"]]
            return self.builder.load(var_ptr)
        elif etype in ("add","sub","mul","div","mod"):
            left = self.compile_expr(expr["left"])
            right = self.compile_expr(expr["right"])
            if etype == "add":
                return self.builder.add(left, right)
            elif etype == "sub":
                return self.builder.sub(left, right)
            elif etype == "mul":
                return self.builder.mul(left, right)
            elif etype == "div":
                return self.builder.sdiv(left, right)
            elif etype == "mod":
                return self.builder.srem(left, right)
        elif etype in ("eq","ne","lt","le","gt","ge"):
            left = self.compile_expr(expr["left"])
            right = self.compile_expr(expr["right"])
            if etype == "eq":
                cmp_val = self.builder.icmp_signed("==", left, right)
            elif etype == "ne":
                cmp_val = self.builder.icmp_signed("!=", left, right)
            elif etype == "lt":
                cmp_val = self.builder.icmp_signed("<", left, right)
            elif etype == "le":
                cmp_val = self.builder.icmp_signed("<=", left, right)
            elif etype == "gt":
                cmp_val = self.builder.icmp_signed(">", left, right)
            elif etype == "ge":
                cmp_val = self.builder.icmp_signed(">=", left, right)
            # Convert i1 -> i32 (0 or 1)
            return self.builder.zext(cmp_val, ir.IntType(32))
        elif etype == "and":
            left = self.compile_expr(expr["left"])
            right = self.compile_expr(expr["right"])
            # minimal approach: nonzero => true
            left_bool = self.builder.icmp_signed("!=", left, ir.Constant(left.type, 0))
            right_bool = self.builder.icmp_signed("!=", right, ir.Constant(right.type, 0))
            and_val = self.builder.and_(left_bool, right_bool)
            return self.builder.zext(and_val, ir.IntType(32))
        elif etype == "or":
            left = self.compile_expr(expr["left"])
            right = self.compile_expr(expr["right"])
            left_bool = self.builder.icmp_signed("!=", left, ir.Constant(left.type, 0))
            right_bool = self.builder.icmp_signed("!=", right, ir.Constant(right.type, 0))
            or_val = self.builder.or_(left_bool, right_bool)
            return self.builder.zext(or_val, ir.IntType(32))
        elif etype == "neg":
            val = self.compile_expr(expr["value"])
            return self.builder.neg(val)
        elif etype == "not":
            val = self.compile_expr(expr["value"])
            val_bool = self.builder.icmp_signed("!=", val, ir.Constant(val.type, 0))
            # flip bit
            not_val = self.builder.xor(val_bool, ir.Constant(val_bool.type, True))
            return self.builder.zext(not_val, ir.IntType(32))
        else:
            raise Exception(f"Unhandled expr type: {etype}")

    def compile_if(self, stmt):
        cond_val = self.compile_expr(stmt["condition"])
        # convert i32 -> i1
        cond_bool = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))

        then_bb = self.builder.append_basic_block("then")
        else_bb = self.builder.append_basic_block("else") if "else" in stmt else None
        merge_bb = self.builder.append_basic_block("merge")

        if else_bb:
            self.builder.cbranch(cond_bool, then_bb, else_bb)
        else:
            self.builder.cbranch(cond_bool, then_bb, merge_bb)

        # then block
        self.builder.position_at_start(then_bb)
        for s in stmt["then"]:
            self.compile_stmt(s)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_bb)

        # else block
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
        end_bb  = self.builder.append_basic_block("while.end")

        # jump to cond
        self.builder.branch(cond_bb)
        self.builder.position_at_start(cond_bb)

        cond_val = self.compile_expr(stmt["condition"])
        cond_bool = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))
        self.builder.cbranch(cond_bool, body_bb, end_bb)

        # body
        self.builder.position_at_start(body_bb)
        for s in stmt["body"]:
            self.compile_stmt(s)
        if not self.builder.block.is_terminated:
            self.builder.branch(cond_bb)

        self.builder.position_at_start(end_bb)

    def print_int(self, val):
        # create or reuse "%d\n"
        fmt_str = "%d\n"
        c_str = self.get_string_constant(fmt_str)
        self.builder.call(self.printf, [c_str, val])

    def get_string_constant(self, text):
        if text in self.string_constants:
            return self.string_constants[text]
        byte_arr = bytearray(text.encode("utf8")) + b"\0"
        const_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(byte_arr)), byte_arr)
        global_var = ir.GlobalVariable(self.module, const_str.type, name=f"str_{len(self.string_constants)}")
        global_var.linkage = "internal"
        global_var.global_constant = True
        global_var.initializer = const_str
        ptr = self.builder.bitcast(global_var, ir.PointerType(ir.IntType(8)))
        self.string_constants[text] = ptr
        return ptr
