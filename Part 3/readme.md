# XDLANG Compiler — Part 3

**Creating a Parser for a Programming Language (xdlang part 3)**

This repository demonstrates **Part 3** of building the XDLANG compiler, focusing on **refining and expanding the parser**. We use **Lark** (for parsing) and **llvmlite** (for LLVM IR generation) to handle more complex language constructs, correct operator precedence, and additional statements.

## Overview

In **Part 2**, we had a basic compiler that recognized a small subset of statements (`let`, `mut`, `print`, `return`, `if`, `while`) and arithmetic operators (`+`, `-`, `*`, `/`). **Part 3** aims to:

1. **Expand the Grammar**:  
   - Add multi-level expression rules to handle operator precedence for logical operators (`and`, `or`), comparisons (`==`, `!=`, `<`, `>`, etc.), unary negation (`-x`), and logical not (`!x`).
   - Potentially add statements like `break` and `continue` for loop control.

2. **Enhance the Parser**:  
   - A more robust grammar that systematically orders expression rules from highest to lowest precedence (factor, term, sum, comparisons, etc.).  
   - Improved parse error handling with Lark’s `UnexpectedInput`.

3. **Integrate With the Existing Pipeline**:  
   - The new grammar is integrated into the existing AST builder, semantic analyzer, and code generator.  
   - Ensures we can parse `.xd` files, produce an AST with advanced expressions, validate them, and generate LLVM IR to run complex code.

## Key Changes in Part 3

1. **Rewritten/Expanded Grammar** (`xdlang_grammar_part3.lark`):
   - Uses layered expression rules: `or_expr`, `and_expr`, `comp_expr`, `sum_expr`, `term`, `factor`, `unary`, `atom`.
   - Adds new operators: `%`, `==`, `!=`, `<=`, `>=`, `and`, `or`, unary `!` and `-`.
   - (Optional) Adds `break` and `continue` statements.

2. **Parser & AST Builder**:
   - The parser (`parser.py`) loads the updated grammar.  
   - `ast_builder.py` transforms parse-tree nodes for each operator/statement into a dictionary-based AST.  
   - For instance, `x < 5` becomes `{"type": "lt", "left": {"type": "variable", "name": "x"}, "right": 5}` in the AST.

3. **Semantic Analysis**:
   - Checks for declared variables, existence of `main()`, and whether `break/continue` appear only inside loops.  
   - Additional checks remain minimal but can be extended.

4. **Code Generation**:
   - The code generator now handles new operators: `%` (via `srem`), comparisons (via `icmp_signed`), logical ops (`and`, `or`), and unary negation/logical not.  
   - Minimal approach for `break/continue`—you can extend it further if needed.

5. **CLI & Running**:
   - You can run the compiler with either a **single-command** approach (`python compiler.py main.xd`) or a **subcommand** approach (`python compiler.py compile-file main.xd`), depending on how you set up `Typer`.  
   - The essential point is to parse the `.xd` file, build the AST, do semantic checks, generate IR, compile with `clang`, and run the final executable.

## Usage

1. **Install Dependencies**:
   ```bash
   pip install lark-parser llvmlite typer
   ```
   Make sure you have **clang** installed.

2. **Compile & Run**:
   - If using a single-command approach:
     ```bash
     python compiler.py main.xd
     ```
   - If using a subcommand approach (`compile-file`):
     ```bash
     python compiler.py compile-file main.xd
     ```
   Either way, the compiler will parse `main.xd`, build an AST, perform semantic analysis, generate LLVM IR (`output.ll`), compile it to an executable (`output`), and finally run that executable.

3. **Check the Output**:
   - For example, if `main.xd` contains:
     ```plaintext
     fn main(): int {
         let int x = 10;
         if (x > 5 and x < 20) {
             print(111);
         }
         while (x != 0) {
             print(x);
             mut x = x - 1;
         }
         return x;
     }
     ```
     The compiler might print:
     ```
     111
     10
     9
     8
     ...
     1
     ```
     and then exit.

4. **Debugging**:
   - Use `python build_ast.py main.xd` to see the final AST structure if you need to troubleshoot your grammar or parse rules.
   - If parse errors occur, the script will catch `UnexpectedInput` and display a snippet of the offending code.

## Example Grammar Snippet

```lark
?expr: or_expr

?or_expr: and_expr
        | or_expr "or" and_expr   -> logical_or

?and_expr: comp_expr
         | and_expr "and" comp_expr -> logical_and

?comp_expr: sum_expr
          | comp_expr "==" sum_expr -> eq
          | comp_expr "!=" sum_expr -> ne
          ...
```
This layered approach ensures correct precedence: **logical** ops → **comparison** → **arithmetic** → **unary** → **atom**.


