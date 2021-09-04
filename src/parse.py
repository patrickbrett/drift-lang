
from src.expressions import VariableRefExpr, IntLiteralExpr, StringLiteralExpr, AddExpr, SubExpr, MultExpr, DivExpr, CompExpr, BracketExpr
from src.actions import IncrAction, RepeatAction, SetAction, ShowAction, CompoundStatement, IfIntermediate, ElseIntermediate, IfElseStatement, DefineFunctionAction, InvokeFunctionAction
from src.utils import is_variable, split_list


def parse_expression(expr):
    # if there are brackets, process them first
    if '(' in expr:
        bracket_start = expr.index('(')
        bracket_end = expr.index(')')
        new_expr = expr[:bracket_start] + [BracketExpr(expr[bracket_start+1 : bracket_end])] + expr[bracket_end+1:]
        return parse_expression(new_expr)

    if not isinstance(expr, list):
        expr = [expr]

    if len(expr) == 1:
        if isinstance(expr[0], BracketExpr):
            return expr[0]

        if is_variable(expr[0]):
            return VariableRefExpr(expr[0])
        try:
            int_val = int(expr[0])
            return IntLiteralExpr(int_val)
        except:
            return StringLiteralExpr(expr[0])
    
    if len(expr) >= 3:
        search_order = [CompExpr, AddExpr, SubExpr, MultExpr, DivExpr]

        for i in range(len(search_order)):
            parse_container = search_order[i]
            chars = parse_container.chars
            for char in chars:
                if char in expr:
                    j = expr.index(char)
                    if search_order[i] == CompExpr:
                        return search_order[i](expr[:j], char, expr[j+1:])
                    else:
                        return search_order[i](expr[:j], expr[j+1:])

    print("couldnt parse expr", expr)


def parse_statement(statement):
    # Remove comments
    if '$' in statement:
        statement = statement[:statement.index('$')]

    if len(statement) == 0:
        return

    if statement[0] == 'f':
        print(statement)
        arg_index_low, arg_index_high = statement.index('{'), statement.index('}')
        expr_index_low = statement.index('->')
        name = statement[1]
        params = statement[arg_index_low+1:arg_index_high]
        expr = statement[expr_index_low+1:]
        return DefineFunctionAction(name, params, expr)

    if statement[0] == 'repeat':
        return RepeatAction(statement[2], statement[4:])

    if statement[0] == '?':
        split = split_list(statement, '->')
        return IfIntermediate(split[0][1:], split[1])

    if statement[0] == '!':
        split = split_list(statement, '->')
        return ElseIntermediate(split[1])

    if '|' in statement:
        return CompoundStatement(split_list(statement, '|'))

    if statement[0] == 'show':
        return ShowAction(statement[1:])

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


"""
Combine if/else and other compound statements
"""
def combine_statements(parsed):
    new_statements = []
    for i in range(len(parsed)):
        curr = parsed[i]
        if isinstance(curr, IfIntermediate):
            continue
        elif isinstance(curr, ElseIntermediate):
            if i > 0 and isinstance(parsed[i-1], IfIntermediate):
                new_statements.append(IfElseStatement(parsed[i-1], parsed[i]))
        else:
            new_statements.append(curr)

    return new_statements
