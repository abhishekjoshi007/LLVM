from llvmlite import ir

class CodeGen:
    def __init__(self):
        self.module = ir.Module(name="xdlang_module")

       
        self.module.triple = "arm64-apple-darwin24.0.0"  
        
        self.builder = None
        self.function = None
        self.printf = self.create_print_function()  
        self.fmt_str = self.create_format_string()  

    def generate_ir(self):
        return str(self.module)

    def create_main_function(self):
        """Creates the 'main' function in LLVM IR."""
        func_type = ir.FunctionType(ir.VoidType(), [])
        self.function = ir.Function(self.module, func_type, name="main")
        block = self.function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        # ✅ Fix: Ensure `main()` returns properly
        self.generate_print(42)  # Call printf
        self.builder.ret_void()   # Properly return from main()

    def create_print_function(self):
        """Creates an LLVM declaration for printf."""
        voidptr_ty = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        return ir.Function(self.module, printf_ty, name="printf")

    def create_format_string(self):
        """Creates a global format string for printf ("%d\n")."""
        format_str = ir.GlobalVariable(self.module, ir.ArrayType(ir.IntType(8), 4), name="fmt")
        format_str.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), 4), bytearray("%d\n\0", "utf8"))
        format_str.global_constant = True
        format_str.linkage = "internal"
        return format_str

    def generate_print(self, value):
        """Generates LLVM IR for printing an integer."""
        fmt_ptr = self.builder.bitcast(self.fmt_str, ir.IntType(8).as_pointer())  
        int_value = ir.Constant(ir.IntType(32), value)
        self.builder.call(self.printf, [fmt_ptr, int_value])  


codegen = CodeGen()
codegen.create_main_function()
print(codegen.generate_ir())
