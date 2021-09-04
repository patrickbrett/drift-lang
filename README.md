# drift-lang

Very basic scripting language, built to experiment with custom interpreters

## To run

```
python3 lib/drift-interpeter.py -f examples/demo1.drift
```

## Example program

See `demo5.drift`

```
y := 10 $ set y to 10
repeat *y -> show 3 * y - 4 / 2 | y-- $ decrement y and print some things
show y - 400 $ print some more
```

## Syntax and functionality

- `$` indicates that rest of line is a comment
- `:=` assigns variables
- `show` prints to the console
- `|` allows multiple expressions on one line
- `repeat *n ->` repeats the following expression n times
