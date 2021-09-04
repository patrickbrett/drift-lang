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


class Expression:
    def __init__(self, expr):
        self.expr = expr


class SetAction:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr
    
    def __repr__(self):
        return f"SetAction({self.var} := {self.expr})"


class RepeatAction:
    def __init__(self, count, statement):
        self.statement = statement
        self.count = count
    
    def __repr__(self):
        return f"RepeatAction(*{self.count}, {self.statement})"


class ShowAction:
    def __init__(self, expr):
        self.expr = expr
    
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


class MultExpr:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"MultExpr({self.a} * {self.b})"


class AddExpr:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"AddExpr({self.a} + {self.b})"


def parse_expression(expr):
    if not isinstance(expr, list):
        return expr

    if len(expr) == 1:
        return expr[0]
    
    if len(expr) >= 3:
        if expr[1] == '*':
            return MultExpr(Expression(expr[0]), Expression(expr[2:]))
        elif expr[1] == '+':
            return AddExpr(Expression(expr[0]), Expression(expr[2:]))

    return expr


def is_variable(token):
    lw = set(string.ascii_lowercase)
    return all(char in lw for char in token)


def parse_statement(statement):
    if statement[0] == 'show':
        return ShowAction(Expression(statement[1:]))

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
            return SetAction(statement[0], Expression(statement[2:]))

    return statement


def process(statement, program_state):
    pass


def interpret(filename):
    with open(filename) as f:
        lines = f.read().split('\n')

    tokens = list(map(tokenise, lines[:-1]))

    program_state = ProgramState()
    
    parsed = map(parse_statement, tokens)

    # for statement in parsed:
    #     process(statement, program_state)

    print(list(tokens))
    print(list(parsed))


if __name__ == '__main__':
    args = parse_args()
    filename = args.filename

    interpret(filename)
