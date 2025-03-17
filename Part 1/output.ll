; ModuleID = "xdlang_module"
target triple = "arm64-apple-macosx15.0.0"
target datalayout = ""

define i32 @"main"()
{
entry:
  %"x" = alloca i32
  store i32 5, i32* %"x"
  %".3" = bitcast [16 x i8]* @"str_0" to i8*
  %".4" = call i32 (i8*, ...) @"printf"(i8* %".3")
  %".5" = add i32 1, 1
  %".6" = icmp ne i32 %".5", 0
  br i1 %".6", label %"then", label %"else"
then:
  %".8" = bitcast [11 x i8]* @"str_1" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8")
  br label %"ifcont"
else:
  %".11" = bitcast [13 x i8]* @"str_2" to i8*
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".11")
  br label %"ifcont"
ifcont:
  br label %"while.cond"
while.cond:
  %".15" = load i32, i32* %"x"
  %".16" = icmp ne i32 %".15", 0
  br i1 %".16", label %"while.body", label %"while.end"
while.body:
  %".18" = bitcast [12 x i8]* @"str_3" to i8*
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".18")
  %".20" = load i32, i32* %"x"
  %".21" = sub i32 %".20", 1
  store i32 %".21", i32* %"x"
  br label %"while.cond"
while.end:
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...)

@"str_0" = internal constant [16 x i8] c"Hello, XDLANG!\0a\00"
@"str_1" = internal constant [11 x i8] c"Inside if\0a\00"
@"str_2" = internal constant [13 x i8] c"Inside else\0a\00"
@"str_3" = internal constant [12 x i8] c"Looping...\0a\00"