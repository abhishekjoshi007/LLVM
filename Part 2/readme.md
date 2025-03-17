# XDLANG Compiler (Part 2)

This repository contains **Part 2** of the XDLANG compiler, demonstrating a multi-pass compiler in Python using **Lark** (for parsing) and **llvmlite** (for LLVM IR generation). It builds upon the minimal setup from Part 1, adding new statements and control flow.

## Features Implemented

1. **Single-File Programs**  
   - A `.xd` file contains all the code, including a special `main()` function that acts as the program’s entry point.

2. **Functions**  
   - The compiler recognizes `fn main(): int { ... }` as the entry point.
   - Each function has a return type (currently only `int`).

3. **Statements**  
   - **`return`**: Return from a function, optionally returning an integer value.  
   - **`let`**: Declare a variable (e.g., `let int x = 5;`).  
   - **`mut`**: Mutate a previously declared variable (e.g., `mut x = x + 1;`).  
   - **`print`**: Print an integer expression to the console (via `printf`).  
   - **`if`**: Basic conditional statement with an optional `else` block.  
   - **`while`**: Loop that continues while an expression is nonzero.

4. **Expressions & Operators**  
   - Integer literals (e.g., `0`, `5`, `123`)  
   - Variables (e.g., `x`)  
   - Basic arithmetic: `+`, `-`, `*`, `/`  
   - Parentheses for grouping `(x + 1)`

5. **Semantic Analysis**  
   - A simple symbol table checks that variables are declared before use.  
   - Ensures a `main` function exists and returns `int`.

6. **LLVM IR Generation**  
   - Uses **llvmlite** to create IR instructions for assignments, arithmetic, conditionals, loops, printing, and returns.  
   - Compiles IR into a native executable using `clang`.

## Repository Structure

```
.
├── xdlang_grammar_part2.lark   # Grammar for Part 2
├── parser.py                   # Parses .xd code into a Lark parse tree
├── ast_builder.py              # Transforms parse tree into an AST
├── build_ast.py                # CLI script to parse and build AST (for debugging)
├── semantic_analyzer.py        # Checks variable declarations and main() existence
├── codegen.py                  # Generates LLVM IR with llvmlite
├── compiler.py                 # Typer-based CLI to compile & run .xd files
└── main.xd                     # Example XDLANG source
```

## How to Use

1. **Install Dependencies**

   ```bash
   pip install lark-parser llvmlite typer
   ```
   
   Make sure you have **clang** installed (on macOS, install Xcode Command Line Tools).

2. **Compile & Run**

   ```bash
   python compiler.py main.xd
   ```
   or, if your function is a Typer subcommand, you might do:
   ```bash
   python compiler.py compile-and-run main.xd
   ```
   Depending on how you structured your Typer CLI.

3. **What Happens?**
   - **Parsing & AST**: Lark reads `xdlang_grammar_part2.lark`, then `ast_builder.py` builds a structured AST.  
   - **Semantic Analysis**: Checks the program for declared variables and ensures `main()` is present.  
   - **IR Generation**: `codegen.py` produces `output.ll` (LLVM IR).  
   - **Native Compilation**: Calls `clang` to compile `output.ll` into an executable `output`.  
   - **Execution**: Runs the resulting `./output`, printing or returning results based on your XDLANG code.

4. **Example Program**

   ```plaintext
   fn main(): int {
       let int x = 5;
       mut x = x + 2;
       print(x);  // prints 7

       if (x) {
           print(123);  // prints 123
       }

       let int counter = 3;
       while (counter) {
           print(counter); // prints 3, 2, 1
           mut counter = counter - 1;
       }

       return x; // returns 7
   }
   ```

   **Expected Output**:
   ```
   7
   123
   3
   2
   1
   ```

## Next Steps

- **Additional Data Types**: 64-bit integers (if not already), floats, bool, char, etc.  
- **More Operators**: `%`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `and`, `or`, unary minus, logical negation `!`.  
- **break/continue** in loops.  
- **Function Calls**: multiple arguments, user-defined functions beyond `main`.  
- **Casting**: e.g., `cast<int>(78.5)`.  
- **User-Defined Types**, arrays, and strings.

Each new feature requires updating the grammar, AST builder, semantic analyzer, and code generator. As you continue to Part 3 and beyond, you’ll build a richer, more powerful XDLANG.

## Contributing

Feel free to open issues or PRs if you’d like to suggest improvements, additional language features, or optimizations.

## License

This project is provided as-is for educational purposes. See [LICENSE](LICENSE) for details (if you have one).

---

**Enjoy hacking on your XDLANG compiler for Part 2!**