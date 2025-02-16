; ModuleID = "xdlang_module"
target triple = "arm64-apple-darwin24.0.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

@"fmt" = internal constant [4 x i8] c"%d\0a\00"
define void @"main"()
{
entry:
  %".2" = bitcast [4 x i8]* @"fmt" to i8*
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2", i32 42)
  ret void
}

