from src.tokenise import tokenise
from src.parse import parse_statement
from src.process import process_statement
from src.utils import parse_args

debug = True


class ProgramState():
    def __init__(self):
        self.variables = {}
    
    def __repr__(self):
        return f"ProgramState(vars={self.variables})"


def interpret(filename):
    with open(filename) as f:
        lines = f.read().split('\n')

    tokens = list(map(tokenise, lines[:-1]))
    parsed = list(map(parse_statement, tokens))

    program_state = ProgramState()

    global debug
    if debug:
        print(tokens)
        print(parsed)
        print()

    for statement in parsed:
        process_statement(statement, program_state)


if __name__ == '__main__':
    args = parse_args()
    filename = args.filename

    interpret(filename)
