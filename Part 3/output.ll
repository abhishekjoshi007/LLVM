; ModuleID = "xdlang_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
entry:
  %"x" = alloca i32
  store i32 10, i32* %"x"
  %".3" = load i32, i32* %"x"
  %".4" = icmp sgt i32 %".3", 5
  %".5" = zext i1 %".4" to i32
  %".6" = load i32, i32* %"x"
  %".7" = icmp slt i32 %".6", 20
  %".8" = zext i1 %".7" to i32
  %".9" = icmp ne i32 %".5", 0
  %".10" = icmp ne i32 %".8", 0
  %".11" = and i1 %".9", %".10"
  %".12" = zext i1 %".11" to i32
  %".13" = icmp ne i32 %".12", 0
  br i1 %".13", label %"then", label %"merge"
then:
  %".15" = bitcast [4 x i8]* @"str_0" to i8*
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15", i32 111)
  br label %"merge"
merge:
  br label %"while.cond"
while.cond:
  %".19" = load i32, i32* %"x"
  %".20" = icmp ne i32 %".19", 0
  %".21" = zext i1 %".20" to i32
  %".22" = icmp ne i32 %".21", 0
  br i1 %".22", label %"while.body", label %"while.end"
while.body:
  %".24" = load i32, i32* %"x"
  %".25" = call i32 (i8*, ...) @"printf"(i8* %".15", i32 %".24")
  %".26" = load i32, i32* %"x"
  %".27" = sub i32 %".26", 1
  store i32 %".27", i32* %"x"
  %".29" = load i32, i32* %"x"
  %".30" = icmp eq i32 %".29", 5
  %".31" = zext i1 %".30" to i32
  %".32" = icmp ne i32 %".31", 0
  br i1 %".32", label %"then.1", label %"merge.1"
while.end:
  %".36" = load i32, i32* %"x"
  ret i32 %".36"
then.1:
  br label %"merge.1"
merge.1:
  br label %"while.cond"
}

declare i32 @"printf"(i8* %".1", ...)

@"str_0" = internal constant [4 x i8] c"%d\0a\00"