# XDLANG Compiler — Parts 1, 2, and 3

## Part 1: Initial Concepts & Minimal Compiler

- **Overview**  
  In Part 1, we laid the **foundation** of the compiler. We introduced XDLANG, discussed why we want to build a compiler, and set up a minimal pipeline to parse the simplest possible program (e.g., `fn main(): int { return 0; }`).
- **Key Achievements**  
  1. Created a **basic grammar** (or placeholders) for a tiny subset of XDLANG.  
  2. Used **Lark** to parse a single function returning an integer.  
  3. Demonstrated **end-to-end compilation**: parse → minimal AST → IR generation → produce a working executable returning `0`.
- **Outcome**  
  This part showed how to set up a **basic multi-pass** structure (parsing, semantic checks, codegen) and compile a trivial program.


## Part 2: Expanding Language Features & Full Pipeline

- **Overview**  
  Building on Part 1, Part 2 added more **statements** and integrated them into the **complete pipeline**. We introduced additional grammar rules, a more thorough AST, semantic checks, and code generation for a bigger subset of XDLANG.
- **Key Achievements**  
  1. Introduced statements like **`let`**, **`mut`**, **`print`**, **`if`**, **`while`**, and a more flexible `return`.  
  2. Enhanced the **parser** and **AST builder** to handle multiple statements in a block.  
  3. Improved **semantic analysis** (symbol table for variables, ensuring `main` function exists).  
  4. Extended **LLVM IR generation** to handle new constructs and produce fully executable code.
- **Outcome**  
  By the end of Part 2, we could parse and compile a variety of programs using loops, conditionals, variable declarations, and print statements.


## Part 3: Parser Refinement & Advanced Expressions

- **Overview**  
  In Part 3, the focus turned to **refining and expanding the parser**. We reorganized the grammar to properly handle **operator precedence**, logical operators, comparisons, unary operators, and potentially added statements like `break` and `continue`.
- **Key Achievements**  
  1. **Layered grammar** for expressions (logical, comparison, arithmetic, unary, etc.) to ensure correct precedence.  
  2. More robust **parse-time error handling** (e.g., catching and displaying `UnexpectedInput` in Lark).  
  3. Updated **AST builder** to reflect new operators (`==`, `!=`, `<`, `>`, `<=`, `>=`, `%`, `and`, `or`, `!`, etc.).  
  4. Integrated new statements (if desired) into the **semantic analyzer** and **codegen**.  
- **Outcome**  
  We ended up with a **powerful parser** that can handle complex expressions and a variety of statements, giving XDLANG a more complete feel.


## Next Steps

- **Data Types**: Extend to floats, bools, chars, or user-defined types.  
- **Function Calls**: Implement multi-argument functions, returns, etc.  
- **Optimizations**: Use LLVM passes for IR optimization.  
- **Error Handling**: Provide friendlier compile-time messages for semantic or parse errors.


## How to Use

1. **Install Dependencies**  
   - `pip install lark-parser llvmlite typer`  
   - Ensure `clang` is installed.

2. **Compile & Run**  
   - Depending on your CLI setup, either:  
     ```bash
     python compiler.py main.xd (Inside the subfolder of Part1, Part2 and Part3)
     ```  
     **or**  
     ```bash
     python compiler.py compile-file main.xd (Inside the subfolder of Part1, Part2 and Part3)
     ```
   - This parses the `.xd` file, builds the AST, runs semantic checks, generates IR, compiles with clang, and executes the result.


This completes a high-level overview of **Parts 1, 2, and 3** of the XDLANG compiler project. You now have a working language with increasingly sophisticated grammar, a solid multi-pass compiler architecture, and a foundation for future expansions.