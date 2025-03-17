import typer
import subprocess
import os

from build_ast import build_ast
from semantic_analyzer import SemanticAnalyzer
from codegen import CodeGen

app = typer.Typer()

@app.command()
def compile_and_run(filename: str):
    # 1. Build AST
    ast = build_ast(filename)

    # 2. Semantic Analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    # 3. Code Generation
    codegen = CodeGen()
    codegen.generate_ir(ast)
    ll_code = str(codegen.module)

    # 4. Write LLVM IR to file
    with open("output.ll", "w") as f:
        f.write(ll_code)

    # 5. Compile with clang -> output
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
