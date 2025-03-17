; ModuleID = "xdlang_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
entry:
  %"x" = alloca i32
  store i32 5, i32* %"x"
  %".3" = load i32, i32* %"x"
  %".4" = add i32 %".3", 2
  store i32 %".4", i32* %"x"
  %".6" = load i32, i32* %"x"
  %".7" = bitcast [4 x i8]* @"str_0" to i8*
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 %".6")
  %".9" = load i32, i32* %"x"
  %".10" = icmp ne i32 %".9", 0
  br i1 %".10", label %"then", label %"merge"
then:
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 123)
  br label %"merge"
merge:
  %"counter" = alloca i32
  store i32 3, i32* %"counter"
  br label %"while.cond"
while.cond:
  %".16" = load i32, i32* %"counter"
  %".17" = icmp ne i32 %".16", 0
  br i1 %".17", label %"while.body", label %"while.end"
while.body:
  %".19" = load i32, i32* %"counter"
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 %".19")
  %".21" = load i32, i32* %"counter"
  %".22" = sub i32 %".21", 1
  store i32 %".22", i32* %"counter"
  br label %"while.cond"
while.end:
  %".25" = load i32, i32* %"x"
  ret i32 %".25"
}

declare i32 @"printf"(i8* %".1", ...)

@"str_0" = internal constant [4 x i8] c"%d\0a\00"