from src.actions import IncrAction, RepeatAction, SetAction, ShowAction, CompoundStatement, IfElseStatement, DefineFunctionAction
from src.expressions import UserInputExpr


class FunctionObject:
    def __init__(self, params, expr):
        self.params = params
        self.expr = expr
    
    def __repr__(self):
        return f"FunctionObject(params={self.params}, expr={self.expr})"


class ProgramState():
    def __init__(self):
        self.global_variables = {}
        self.functions = {
            '#': FunctionObject(['prompt'], UserInputExpr(to_int=True)),
            '@': FunctionObject(['prompt'], UserInputExpr()),
        }
    
    def __repr__(self):
        return f"ProgramState(global_variables={self.global_variables}, functions={self.functions}, scoped_variables={self.scoped_variables})"


def process_statement(statement, program_state):
    if statement is None:
        return
    
    if isinstance(statement, SetAction):
        # TODO handle setting scoped variables from within functions
        program_state.global_variables[statement.var] = statement.expr.evaluate(program_state)

    elif isinstance(statement, RepeatAction):
        count = statement.count.evaluate(program_state)
        for i in range(count):
            process_statement(statement.statement, program_state)

    elif isinstance(statement, IncrAction):
        program_state.global_variables[statement.var] += statement.expr.evaluate(program_state)

    elif isinstance(statement, ShowAction):
        print(statement.expr.evaluate(program_state), end='')

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
