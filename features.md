# Features

## Implemented

- variable assignment
- variable increment
- variable decrement
- repeat (count = result of an expression)
- compound expressions
- addition, subtraction, multiplication, division
- comments

## To do

- strings
- brackets
- functions
- lists
- stacks (with stack property enforced)
- queues (with queue property enforced)
- custom classes
- inheritance
- first class functions
- logical expressions
- if
- else
- for loops
- while

## Bugs and implementation difficulties so far

if/else statements should be evaluated simultaneously, with the path determined from the outcome of the expression in the first case.

This may be done by combining if/else statements at the parsing stage into IfElse statements.

Otherwise, the outcome of the expression may change and if/else may be run zero or two times.
