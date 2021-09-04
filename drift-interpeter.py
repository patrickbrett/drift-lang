from argparse import ArgumentParser
import string


def flatten(t):
    return [item for sublist in t for item in sublist]


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="Filename to load", metavar="FILE")
    args = parser.parse_args()
    return args


class ProgramState():
    def __init__(self):
        self.variables = {}
    
    def __repr__(self):
        return f"ProgramState(vars={self.variables})"


def tokenise(chars):
    i = 0
    lw = set(string.ascii_lowercase)
    nums = set(map(str, range(0, 10)))
    symbol_chars = set([':', '=', ';', '-', '>', '-', '+', '*'])
    # symbols = set([':=', ';', '->', '--', '++', '*'])

    tokens = []
    current_token = []
    while i < len(chars):
        char = chars[i]
        if char == ' ':
            tokens.append("".join(current_token))
            current_token = []

        if char in lw:
            if not len(current_token) or current_token[-1] in lw:
                current_token.append(char)
            else:
                tokens.append("".join(current_token))
                current_token = [char]
        
        if char in nums:
            if not len(current_token) or current_token[-1] in nums:
                current_token.append(char)
            else:
                tokens.append("".join(current_token))
                current_token = [char]

        if char in symbol_chars:
            if not len(current_token) or current_token[-1] in symbol_chars:
                current_token.append(char)
            else:
                tokens.append("".join(current_token))
                current_token = [char]

        i += 1

    tokens.append("".join(current_token))

    return tokens


class Variable:
    def __init__(self, name):
        self.name = name


class SetAction:
    def __init__(self, var, expr):
        self.var = var
        self.expr = parse_expression(expr)
    
    def __repr__(self):
        return f"SetAction({self.var} := {self.expr})"


class RepeatAction:
    def __init__(self, count, statement):
        self.count = parse_expression(count)
        self.statement = statement
    
    def __repr__(self):
        return f"RepeatAction(*{self.count}, {self.statement})"


class ShowAction:
    def __init__(self, expr):
        self.expr = parse_expression(expr)
    
    def __repr__(self):
        return f"ShowAction({self.expr})"


class IncrAction:
    def __init__(self, var, expr):
        self.var = var
        self.expr = parse_expression(expr)
    
    def __repr__(self):
        return f"IncrAction({self.var} += {self.expr})"


class Expression:
    def __init__(self, expr):
        self.expr = parse_expression(expr)

    def __repr__(self):
        return f"Expression({self.expr})"

    def evaluate(self, program_state):
        if isinstance(self.expr, MultExpr):
            return self.expr.evaluate(program_state)
        elif isinstance(self.expr, AddExpr):
            return self.expr.evaluate(program_state)
        elif isinstance(self.expr, VariableRefExpr):
            return self.expr.evaluate(program_state)
        else:
            try:
                return int(self.expr)
            except:
                return self.expr


class MultExpr:
    char = '*'

    def __init__(self, a, b):
        self.a = parse_expression(a)
        self.b = parse_expression(b)

    def __repr__(self):
        return f"MultExpr({self.a} * {self.b})"

    def evaluate(self, program_state):
        return self.a.evaluate(program_state) * self.b.evaluate(program_state)


class AddExpr:
    char = '+'
    
    def __init__(self, a, b):
        self.a = parse_expression(a)
        self.b = parse_expression(b)

    def __repr__(self):
        return f"AddExpr({self.a} + {self.b})"

    def evaluate(self, program_state):
        return self.a.evaluate(program_state) + self.b.evaluate(program_state)


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


def parse_expression(expr):
    if not isinstance(expr, list):
        expr = [expr]

    if len(expr) == 1:
        if is_variable(expr[0]):
            return VariableRefExpr(expr[0])
        try:
            int_val = int(expr[0])
            return IntLiteralExpr(int_val)
        except:
            print("Couldn't match")
            return expr[0]
    
    if len(expr) >= 3:
        search_order = [AddExpr, MultExpr]

        for i in range(len(search_order)):
            parse_container = search_order[i]
            char = parse_container.char
            if char in expr:
                j = expr.index(char)
                return search_order[i](expr[:j], expr[j+1:])

    print("couldnt parse expr", expr)

def is_variable(token):
    lw = set(string.ascii_lowercase)
    return all(char in lw for char in token)


def parse_statement(statement):
    if statement[0] == 'show':
        return ShowAction(statement[1:])

    if statement[0] == 'repeat':
        return RepeatAction(statement[2], parse_statement(statement[4:]))

    if len(statement) >= 2:
        if is_variable(statement[0]):
            if statement[1] == '--':
                return IncrAction(statement[0], '-1')
            if statement[1] == '++':
                return IncrAction(statement[0], '1')

    if len(statement) >= 3:
        if is_variable(statement[0]) and statement[1] == ':=':
            return SetAction(statement[0], statement[2:])

    return statement


def process(statement, program_state):
    if isinstance(statement, SetAction):
        program_state.variables[statement.var] = statement.expr.evaluate(program_state)
    elif isinstance(statement, RepeatAction):
        count = statement.count.evaluate(program_state)
        for i in range(count):
            process(statement.statement, program_state)
    elif isinstance(statement, IncrAction):
        program_state.variables[statement.var] += statement.expr.evaluate(program_state)
    elif isinstance(statement, ShowAction):
        print("Program output:", statement.expr.evaluate(program_state))


def interpret(filename):
    with open(filename) as f:
        lines = f.read().split('\n')

    tokens = list(map(tokenise, lines[:-1]))

    program_state = ProgramState()
    
    parsed = list(map(parse_statement, tokens))

    print(tokens)
    print(parsed)
    print()

    for statement in parsed:
        process(statement, program_state)



if __name__ == '__main__':
    args = parse_args()
    filename = args.filename

    interpret(filename)
