"""
Convert from Anonsage lexemes (tokens) to AST.
"""
import logging
from functools import reduce

from src.anon_ast import *
from src.anon_lexer import *
from src.generic_combinators import *

logging.basicConfig(level=logging.DEBUG, filename='debug.log')


id = Tag(ID)
number = Tag(NUMBER) ^ (lambda i: float(i))


def keyword(kw):
    return Reserved(kw, RESERVED)


###################################################################################################


def arithmetic_exp_value():
    return (number ^ (lambda i: NumberArithmeticExpression(i))) | (id ^ (lambda v: VarArithmeticExpression(v)))


def process_group(parsed):
    ((_, p), _) = parsed
    return p


def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group


def aexp_term():
    return arithmetic_exp_value() | aexp_group()


def process_binary_op(op):
    return lambda l, r: BinaryOpArithmeticExpression(op, l, r)


def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser


aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]


def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser


def aexp():
    return precedence(aexp_term(), aexp_precedence_levels, process_binary_op)


###################################################################################################


def process_relop(parsed):
    ((left, op), right) = parsed
    return RelationalOpBooleanExpression(op, left, right)


def bexp_relop():
    relops = ['<', '<=', '>', '>=', '==', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop


def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBooleanExpression(parsed[1]))


def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group


def bexp_term():
    return bexp_not() | bexp_relop() | bexp_group()


bexp_precedence_levels = [
    ['and'],
    ['or'],
]


def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBooleanExpression(l, r)
    elif op == 'or':
        return lambda l, r: OrBooleanExpression(l, r)
    else:
        raise RuntimeError(f'Unknown logic operator: {op}')


def bexp():
    return precedence(bexp_term(), bexp_precedence_levels, process_logic)


###################################################################################################


def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword('=') + aexp() ^ process


def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)


def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)
    return keyword('if') + bexp() + \
           keyword('then') + Lazy(stmt_list) + \
           Optional(keyword('else') + Lazy(stmt_list)) + \
           keyword('end') ^ process


def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return LoopStatement(condition, body)
    return keyword('loop') + bexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process


def stmt():
    return assign_stmt() | if_stmt() | while_stmt()


###################################################################################################

def parser():
    logging.debug(f'parser()')
    return Phrase(stmt_list())


def parse(tokens):
    ast = parser()(tokens, 0)
    return ast
