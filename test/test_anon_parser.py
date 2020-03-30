import unittest

from src import anon_lexer, anon_parser
from src.anon_parser import *


class TestAnonParse(unittest.TestCase):
    def assert_parser(self, characters, _parser, expected):
        tokens = anon_lexer.lex(characters)
        result = _parser(tokens, 0)
        self.assertNotEqual(None, result)
        self.assertEqual(expected, result.value)

    def test_precedence(self):
        def combine(op):
            if op == '*':
                return lambda l, r: int(l) * int(r)
            else:
                return lambda l, r: int(l) + int(r)
        levels = [['*'], ['+']]
        parser = precedence(number, levels, combine)
        self.assert_parser('2 * 3 + 4', parser, 10)
        self.assert_parser('2 + 3 * 4', parser, 14)

    def test_aexp_num(self):
        self.assert_parser('42', aexp(), NumberArithmeticExpression(42))
        self.assert_parser('3.14', aexp(), NumberArithmeticExpression(3.14))

    def test_aexp_var(self):
        self.assert_parser('x', aexp(), VarArithmeticExpression('x'))

    def test_aexp_group(self):
        self.assert_parser('(42)', aexp(), NumberArithmeticExpression(42))

    def test_aexp_binop(self):
        code = '2 * 3 + 4'
        expected = BinaryOpArithmeticExpression('+', BinaryOpArithmeticExpression('*',
                NumberArithmeticExpression(2), NumberArithmeticExpression(3)), NumberArithmeticExpression(4))
        self.assert_parser('2 * 3 + 4', aexp(), expected)

    def test_aexp_binop_group(self):
        code = '2 * (3 + 4)'
        expected = BinaryOpArithmeticExpression('*', NumberArithmeticExpression(2),
                BinaryOpArithmeticExpression('+', NumberArithmeticExpression(3), NumberArithmeticExpression(4)))
        self.assert_parser(code, aexp(), expected)

    def test_bexp_relop(self):
        self.assert_parser('2 < 3', bexp(), RelationalOpBooleanExpression('<', NumberArithmeticExpression(2), NumberArithmeticExpression(3)))

    def test_bexp_not(self):
        self.assert_parser('not 2 < 3', bexp(), NotBooleanExpression(RelationalOpBooleanExpression('<', NumberArithmeticExpression(2), NumberArithmeticExpression(3))))

    def test_bexp_and(self):
        expected = AndBooleanExpression(RelationalOpBooleanExpression('<', NumberArithmeticExpression(2), NumberArithmeticExpression(3)), RelationalOpBooleanExpression('<', NumberArithmeticExpression(3), NumberArithmeticExpression(4)))
        self.assert_parser('2 < 3 and 3 < 4', bexp(), expected)

    def test_bexp_logic(self):
        code = '1 < 2 and 3 < 4 or 5 < 6'
        expected = OrBooleanExpression(AndBooleanExpression(RelationalOpBooleanExpression('<', NumberArithmeticExpression(1), NumberArithmeticExpression(2)),
                                  RelationalOpBooleanExpression('<', NumberArithmeticExpression(3), NumberArithmeticExpression(4))),
                          RelationalOpBooleanExpression('<', NumberArithmeticExpression(5), NumberArithmeticExpression(6)))
        self.assert_parser(code, bexp(), expected)

    def test_bexp_logic_group(self):
        code = '1 < 2 and (3 < 4 or 5 < 6)'
        expected = AndBooleanExpression(RelationalOpBooleanExpression('<', NumberArithmeticExpression(1), NumberArithmeticExpression(2)),
                           OrBooleanExpression(RelationalOpBooleanExpression('<', NumberArithmeticExpression(3), NumberArithmeticExpression(4)),
                                  RelationalOpBooleanExpression('<', NumberArithmeticExpression(5), NumberArithmeticExpression(6))))
        self.assert_parser(code, bexp(), expected)

    def test_bexp_not_precedence(self):
        code = 'not 1 < 2 and 3 < 4'
        expected = AndBooleanExpression(NotBooleanExpression(RelationalOpBooleanExpression('<', NumberArithmeticExpression(1), NumberArithmeticExpression(2))),
                           RelationalOpBooleanExpression('<', NumberArithmeticExpression(3), NumberArithmeticExpression(4)))
        self.assert_parser(code, bexp(), expected)

    def test_assign_stmt(self):
        self.assert_parser('x = 1', stmt_list(), AssignStatement('x', NumberArithmeticExpression(1)))

    def test_if_stmt(self):
        code = 'if 1 < 2 then x = 3 else x = 4 end'
        expected = IfStatement(RelationalOpBooleanExpression('<', NumberArithmeticExpression(1), NumberArithmeticExpression(2)),
                               AssignStatement('x', NumberArithmeticExpression(3)),
                               AssignStatement('x', NumberArithmeticExpression(4)))
        self.assert_parser(code, stmt_list(), expected)

    def test_while_stmt(self):
        code = 'loop 1 < 2 do x = 3 end'
        expected = LoopStatement(RelationalOpBooleanExpression('<', NumberArithmeticExpression(1), NumberArithmeticExpression(2)),
                                  AssignStatement('x', NumberArithmeticExpression(3)))
        self.assert_parser(code, stmt_list(), expected)

    def test_compound_stmt(self):
        code = 'x = 1; y = 2'
        expected = CompoundStatement(AssignStatement('x', NumberArithmeticExpression(1)),
                                     AssignStatement('y', NumberArithmeticExpression(2)))
        self.assert_parser(code, stmt_list(), expected)


if __name__ == '__main__':
    unittest.main()
