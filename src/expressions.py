import src.parse as parse
from src.actions import CompoundStatement


class MultExpr:
    chars = set(['*'])

    def __init__(self, a, b):
        self.a = parse.parse_expression(a)
        self.b = parse.parse_expression(b)

    def __repr__(self):
        return f"MultExpr({self.a} * {self.b})"

    def evaluate(self, program_state, scoped_variables={}):
        return self.a.evaluate(program_state, scoped_variables) * self.b.evaluate(program_state, scoped_variables)


class AddExpr:
    chars = set(['+'])
    
    def __init__(self, a, b):
        self.a = parse.parse_expression(a)
        self.b = parse.parse_expression(b)

    def __repr__(self):
        return f"AddExpr({self.a} + {self.b})"

    def evaluate(self, program_state, scoped_variables={}):
        return self.a.evaluate(program_state, scoped_variables) + self.b.evaluate(program_state, scoped_variables)


class SubExpr():
    chars = set(['-'])
    
    def __init__(self, a, b):
        self.a = parse.parse_expression(a)
        self.b = parse.parse_expression(b)
    
    def __repr__(self):
        return f"SubExpr({self.a} - {self.b})"

    def evaluate(self, program_state, scoped_variables={}):
        return self.a.evaluate(program_state, scoped_variables) - self.b.evaluate(program_state, scoped_variables)


class DivExpr():
    chars = set(['/'])

    def __init__(self, a, b):
        self.a = parse.parse_expression(a)
        self.b = parse.parse_expression(b)
    
    def __repr__(self):
        return f"DivExpr({self.a} / {self.b})"

    def evaluate(self, program_state, scoped_variables={}):
        return self.a.evaluate(program_state, scoped_variables) // self.b.evaluate(program_state, scoped_variables)


class VariableRefExpr:
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"VariableRefExpr({self.var})"

    def evaluate(self, program_state, scoped_variables={}):
        if self.var in scoped_variables:
            return scoped_variables[self.var]
        else:
            return program_state.global_variables[self.var]


class IntLiteralExpr:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"IntLiteralExpr({self.val})"

    def evaluate(self, program_state, scoped_variables={}):
        return self.val


class StringLiteralExpr:
    def __init__(self, val):
        self.val = val[1:-1] # strip quotes

    def __repr__(self):
        return f"StringLiteralExpr({self.val})"

    def evaluate(self, program_state, scoped_variables={}):
        return self.val


class CompExpr:
    chars = set(['>', '<', '>=', '<='])

    def __init__(self, first, comp, second):
        self.first = parse.parse_expression(first)
        self.comp = comp
        self.second = parse.parse_expression(second)


    def __repr__(self):
        return f"CompExpr({self.first} {self.comp} {self.second})"


    def evaluate(self, program_state, scoped_variables={}):
        f, s  = self.first.evaluate(program_state, scoped_variables), self.second.evaluate(program_state, scoped_variables)
        if self.comp == '>':
            return f > s
        elif self.comp == '<':
            return f < s
        elif self.comp == '>=':
            return f >= s
        elif self.comp == '<=':
            return f <= s


class BracketExpr:
    def __init__(self, inner):
        self.inner = parse.parse_expression(inner)
    
    def __repr__(self):
        return f"BracketExpr({self.inner})"
    
    def evaluate(self, program_state, scoped_variables={}):
        return self.inner.evaluate(program_state, scoped_variables)


class InvokeFunctionExpr:
    def __init__(self, function_name, function_args):
        self.function_name = function_name
        self.function_args = list(map(parse.parse_expression, function_args))
    
    def __repr__(self):
        return f"InvokeFunctionExpr(name={self.function_name}, args={self.function_args})"

    def evaluate(self, program_state, scoped_variables={}):
        # TODO handle multiple levels of scoped variables
        # perhaps just an array of dicts
        # also, this *could* be stored in the program state, with a stack.

        func = program_state.functions[self.function_name]
        scoped_variables = { param: value.evaluate(program_state) for (param, value) in zip(func.params, self.function_args) }
        return func.expr.evaluate(program_state, scoped_variables)
