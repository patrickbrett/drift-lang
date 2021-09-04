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


class IfStatement:
    def __init__(self, expr, statement):
        self.expr = parse.parse_expression(expr)
        self.statement = parse.parse_statement(statement)
    
    def __repr__(self):
        return f"IfStatement(? {self.expr} -> {self.statement})"


class ElseStatement:
    def __init__(self, statement):
        self.statement = parse.parse_statement(statement)
    
    def __repr__(self):
        return f"ElseStatement(! -> {self.statement})"
