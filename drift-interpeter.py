from src.tokenise import tokenise
from src.parse import parse_statement, combine_statements
from src.process import process_statement, ProgramState
from src.utils import parse_args

debug = True


def interpret(filename):
    with open(filename) as f:
        lines = f.read().split('\n')
        lines = list(map(lambda x: x.replace('\\n', '\n'), lines))

    tokens = list(map(tokenise, lines[:-1]))
    parsed = list(map(parse_statement, tokens))

    # Combine multi-line statements such as if/else
    parsed = combine_statements(parsed)

    program_state = ProgramState()

    global debug
    if debug:
        print("Tokens:")
        print(tokens)
        print()
        print("AST:")
        print(parsed)
        print()

    for statement in parsed:
        process_statement(statement, program_state)


if __name__ == '__main__':
    args = parse_args()
    filename = args.filename

    interpret(filename)
