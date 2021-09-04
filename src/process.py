from src.actions import IncrAction, RepeatAction, SetAction, ShowAction, CompoundStatement


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
