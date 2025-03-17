# XDLANG Compiler

A simple compiler for XDLANG, a minimal imperative programming language, implemented in Python using Lark and LLVM (llvmlite). This project demonstrates the entire compilation pipeline—from lexical analysis and parsing to LLVM IR generation and code execution.

## Overview

XDLANG is designed as a simple, statically-typed language with basic features including:
- Variable assignment
- Print statements
- Arithmetic expressions
- Conditional statements (if/else)
- Loops (while)

The compiler is split into several stages:
1. **Lexical Analysis & Parsing:** Uses [Lark](https://github.com/lark-parser/lark) to define the language grammar and generate a parse tree.
2. **AST Transformation:** A custom transformer converts the parse tree into a clean Abstract Syntax Tree (AST).
3. **Semantic Analysis:** (Basic) Checks variable assignments and records definitions.
4. **IR Generation & Code Generation:** Uses [llvmlite](https://llvmlite.readthedocs.io/) to produce LLVM Intermediate Representation (IR) for the language constructs.
5. **Compilation & Execution:** The LLVM IR is compiled into an executable using clang and then executed.

## Prerequisites

- **Python 3.6+**
- **llvmlite**  
  pip install llvmlite
  
- **Lark Parser**  
  pip install lark-parser
 
- **Clang and Xcode Command Line Tools** (macOS)  
  xcode-select --install
  
- **LLVM**  
  brew install llvm

## Project Structure

```
/Root
├── ast_builder.py         # Transforms the parse tree into an AST.
├── codegen.py             # Generates LLVM IR from the AST and writes output.ll.
├── xdlang_grammar.lark    # Lark grammar definition for XDLANG.
└── README.md              # This file.
```

## How to Use

### 1. Generate LLVM IR

Run the code generator which uses the AST and produces LLVM IR:
python codegen.py

This will create an `output.ll` file and print a confirmation message:

LLVM IR written to output.ll

### 2. Compile the LLVM IR

Use clang to compile the generated LLVM IR into an executable. On macOS, run:

bash
clang -isysroot $(xcrun --sdk macosx --show-sdk-path) -o output output.ll

### 3. Run the Executable

Finally, run your compiled program:

bash
./output

You should see output similar to:

Hello, XDLANG!
Inside if
Looping...
Looping...
Looping...
Looping...
Looping...
