import src.parse as parse


class MultExpr:
    chars = set(['*'])

    def __init__(self, a, b):
        self.a = parse.parse_expression(a)
        self.b = parse.parse_expression(b)

    def __repr__(self):
        return f"MultExpr({self.a} * {self.b})"

    def evaluate(self, program_state):
        return self.a.evaluate(program_state) * self.b.evaluate(program_state)


class AddExpr:
    chars = set(['+'])
    
    def __init__(self, a, b):
        self.a = parse.parse_expression(a)
        self.b = parse.parse_expression(b)

    def __repr__(self):
        return f"AddExpr({self.a} + {self.b})"

    def evaluate(self, program_state):
        return self.a.evaluate(program_state) + self.b.evaluate(program_state)


class SubExpr():
    chars = set(['-'])
    
    def __init__(self, a, b):
        self.a = parse.parse_expression(a)
        self.b = parse.parse_expression(b)
    
    def __repr__(self):
        return f"SubExpr({self.a} - {self.b})"

    def evaluate(self, program_state):
        return self.a.evaluate(program_state) - self.b.evaluate(program_state)


class DivExpr():
    chars = set(['/'])

    def __init__(self, a, b):
        self.a = parse.parse_expression(a)
        self.b = parse.parse_expression(b)
    
    def __repr__(self):
        return f"DivExpr({self.a} / {self.b})"

    def evaluate(self, program_state):
        return self.a.evaluate(program_state) // self.b.evaluate(program_state)


class VariableRefExpr:
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"VariableRefExpr({self.var})"

    def evaluate(self, program_state):
        return program_state.variables[self.var]


class IntLiteralExpr:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"IntLiteralExpr({self.val})"

    def evaluate(self, program_state):
        return self.val


class StringLiteralExpr:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"StringLiteralExpr({self.val})"

    def evaluate(self, program_state):
        return self.val


class CompExpr:
    chars = set(['>', '<', '>=', '<='])

    def __init__(self, first, comp, second):
        self.first = parse.parse_expression(first)
        self.comp = comp
        self.second = parse.parse_expression(second)


    def __repr__(self):
        return f"CompExpr({self.first} {self.comp} {self.second})"


    def evaluate(self, program_state):
        f, s  = self.first.evaluate(program_state), self.second.evaluate(program_state)
        if self.comp == '>':
            return f > s
        elif self.comp == '<':
            return f < s
        elif self.comp == '>=':
            return f >= s
        elif self.comp == '<=':
            return f <= s
