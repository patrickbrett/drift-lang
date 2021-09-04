# drift-lang

Very basic scripting language, built to experiment with custom interpreters

## To run

```
python3 drift-interpeter.py -f examples/beer.drift
```

## Example program

See `beer.drift`

```
x := 9
y := "of beer on the wall!"
z := x - 1
repeat *z -> show x | show " bottles " + y + "\n" | x--
show x | show " bottle " + y + "\n"
```

This will output:

```
9 bottles of beer on the wall!
8 bottles of beer on the wall!
7 bottles of beer on the wall!
6 bottles of beer on the wall!
5 bottles of beer on the wall!
4 bottles of beer on the wall!
3 bottles of beer on the wall!
2 bottles of beer on the wall!
1 bottle of beer on the wall!
```

Unless `debug` is disabled, it will also output the calculated tokens and AST:

```
Tokens:
[['x', ':=', '9'], ['y', ':=', '"of beer on the wall!"'], ['z', ':=', 'x', '-', '1'], ['repeat', '*', 'z', '->', 'show', 'x', '|', 'show', '" bottles "', '+', 'y', '+', '"\n"', '|', 'x', '--'], ['show', 'x', '|', 'show', '" bottle "', '+', 'y', '+', '"\n"']]

AST:
[SetAction(x := IntLiteralExpr(9)), SetAction(y := StringLiteralExpr(of beer on the wall!)), SetAction(z := SubExpr(VariableRefExpr(x) - IntLiteralExpr(1))), RepeatAction(*VariableRefExpr(z), CompoundStatement([ShowAction(VariableRefExpr(x)), ShowAction(AddExpr(StringLiteralExpr( bottles ) + AddExpr(VariableRefExpr(y) + StringLiteralExpr(
)))), IncrAction(x += IntLiteralExpr(-1))])), CompoundStatement([ShowAction(VariableRefExpr(x)), ShowAction(AddExpr(StringLiteralExpr( bottle ) + AddExpr(VariableRefExpr(y) + StringLiteralExpr(
))))])]
```

These are an important part of the intepretation process, and help to understand and debug the interpreter (or the programs themselves!) when they are not working.

## Syntax and functionality

- `$` indicates that rest of line is a comment
- `:=` assigns variables
- `show` prints to the console
- `|` allows multiple expressions on one line
- `repeat *n ->` repeats the following statement n times (can be a literal integer or a variable)
- `? expr ->` runs the following statement if `expr` evaluates to true
- `! ->` runs the following statement if the directly preceding `?` evaluated to false
- `f add { x; y } -> x + y` defines a function that adds two values
- `add { 3; 4 }` calls this function with the arguments 3 and 4
- whitespace is largely ignored (though it naturally separates variables, etc)
- all variables must be lowercase without underscores
- `"hello"` is a string literal

## Takeaways from this project

- There is a LOT of thought that goes into modern language design - many of the syntactical strangeness in Drift simply arose out of my desire to do things slightly differently than the use C/Python/Lisp style syntax. Of course, things are usually done for good reason and so inventing novel syntax for mundane tasks is interesting but ultimately, probably not that useful!
- Working within a powerful and concise framework like Python made this task a whole lot easier than it would have been in C/Java/what have you.
- I feel like it would be interesting to build a Python or JavaScript interpreter in Python or JavaScript, just for the fun of it. If Python is considered slow, what about Python interpreting Python interpreting JavaScript interpreting Python? 😈
- Building an interpreter or compiler is an interesting pursuit in that *your test cases are programs!*
- I like how the structure of dividing the program into expressions and statements naturally arose after encountering the same problem several times over.
- Doing this in a language without support for classes seems like it would be much harder. Doing it in a language with proper type checking seems like it would be much easier.
