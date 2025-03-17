import typer
import subprocess
import os

from build_ast import build_ast
from semantic_analyzer import SemanticAnalyzer
from codegen import CodeGen

app = typer.Typer()

@app.command()
def compile_file(filename: str):
    """
    This is a subcommand named 'compile-file'.
    Usage: python compiler.py compile-file main.xd
    """
    # 1. Build AST
    ast = build_ast(filename)
    if not ast:
        print("AST build failed. Exiting.")
        return

    # 2. Semantic Analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    # 3. Code Generation
    codegen = CodeGen()
    codegen.generate_ir(ast)
    ll_str = str(codegen.module)

    # 4. Write IR to file
    with open("output.ll", "w") as f:
        f.write(ll_str)

    # 5. Compile with clang
    subprocess.run([
        "clang",
        "-isysroot", subprocess.check_output(["xcrun", "--sdk", "macosx", "--show-sdk-path"]).decode().strip(),
        "-o", "output",
        "output.ll"
    ])

    # 6. Run the executable
    subprocess.run(["./output"])

if __name__ == "__main__":
    app()
