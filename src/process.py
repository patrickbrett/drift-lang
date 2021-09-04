from src.actions import IncrAction, RepeatAction, SetAction, ShowAction, CompoundStatement, IfElseStatement, DefineFunctionAction, InvokeFunctionAction


class FunctionObject:
    def __init__(self, params, expr):
        self.params = params
        self.expr = expr
    
    def __repr__(self):
        return f"FunctionObject(params={self.params}, expr={self.expr})"


class ProgramState():
    def __init__(self):
        self.global_variables = {}
        self.functions = {}
        self.scoped_variables = {}
    
    def __repr__(self):
        return f"ProgramState(variables={self.variables}, functions={self.functions})"


def process_statement(statement, program_state):
    if statement is None:
        return
    
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
        if statement.expr.evaluate(program_state):
            process_statement(statement.if_statement, program_state)
        else:
            process_statement(statement.else_statement, program_state)

    elif isinstance(statement, DefineFunctionAction):
        program_state.functions[statement.function_name] = FunctionObject(statement.function_params, statement.function_expr)

    elif isinstance(statement, InvokeFunctionAction):
        func = program_state.functions[statement.function_name]
