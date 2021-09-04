import src.parse as parse


class RepeatAction:
    def __init__(self, count, statement):
        self.count = parse.parse_expression(count)
        self.statement = parse.parse_statement(statement)
    
    def __repr__(self):
        return f"RepeatAction(*{self.count}, {self.statement})"


class ShowAction:
    def __init__(self, expr):
        self.expr = parse.parse_expression(expr)
    
    def __repr__(self):
        return f"ShowAction({self.expr})"


class SetAction:
    def __init__(self, var, expr):
        self.var = var
        self.expr = parse.parse_expression(expr)
    
    def __repr__(self):
        return f"SetAction({self.var} := {self.expr})"


class IncrAction:
    def __init__(self, var, expr):
        self.var = var
        self.expr = parse.parse_expression(expr)
    
    def __repr__(self):
        return f"IncrAction({self.var} += {self.expr})"


class CompoundStatement:
    def __init__(self, statements):
        self.statements = list(map(parse.parse_statement, statements))
    
    def __repr__(self):
        return f"CompoundStatement({self.statements})"


class IfIntermediate:
    def __init__(self, expr, statement):
        self.expr = parse.parse_expression(expr)
        self.statement = parse.parse_statement(statement)
    
    def __repr__(self):
        return f"IfIntermediate(? {self.expr} -> {self.statement})"


class ElseIntermediate:
    def __init__(self, statement):
        self.statement = parse.parse_statement(statement)
    
    def __repr__(self):
        return f"ElseIntermediate(! -> {self.statement})"


class IfElseStatement:
    def __init__(self, _if, _else):
        self.expr = _if.expr
        self.if_statement = _if.statement
        self.else_statement = _else.statement
    
    def __repr__(self):
        return f"IfElseStatement(? {self.expr} -> {self.if_statement} ! -> {self.else_statement})"


class DefineFunctionAction:
    def __init__(self, function_name, function_params, function_expr):
        self.function_name = function_name
        self.function_params = function_params
        self.function_expr = parse.parse_expression(function_expr)
    
    def __repr__(self):
        return f"DefineFunctionAction(name={self.function_name}, params={self.function_params}, expr={self.function_expr})"
