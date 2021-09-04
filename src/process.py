from src.actions import IncrAction, RepeatAction, SetAction, ShowAction, CompoundStatement, IfElseStatement


class ProgramState():
    def __init__(self):
        self.variables = {}
    
    def __repr__(self):
        return f"ProgramState(vars={self.variables})"


def process_statement(statement, program_state):
    if isinstance(statement, SetAction):
        program_state.variables[statement.var] = statement.expr.evaluate(program_state)

    elif isinstance(statement, RepeatAction):
        count = statement.count.evaluate(program_state)
        for i in range(count):
            process_statement(statement.statement, program_state)

    elif isinstance(statement, IncrAction):
        program_state.variables[statement.var] += statement.expr.evaluate(program_state)

    elif isinstance(statement, ShowAction):
        print("Program output:", statement.expr.evaluate(program_state))

    elif isinstance(statement, CompoundStatement):
        for s in statement.statements:
            process_statement(s, program_state)

    elif isinstance(statement, IfElseStatement):
        program_state.if_context = statement.expr
        if statement.expr.evaluate(program_state):
            process_statement(statement.if_statement, program_state)
        else:
            process_statement(statement.else_statement, program_state)
