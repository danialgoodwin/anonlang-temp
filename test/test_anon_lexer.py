import unittest

from src import anon_lexer


class TestAnonLexer(unittest.TestCase):

    def assert_single_token_recognition(self, characters: str, tag: str = anon_lexer.RESERVED):
        self.assertListEqual(anon_lexer.lex(characters), [(characters.strip(), tag)])

    def assert_double_token_recognition(self, characters: str, value1, value2, tag1=anon_lexer.RESERVED, tag2=anon_lexer.RESERVED):
        self.assertListEqual(anon_lexer.lex(characters), [(value1, tag1), (value2, tag2)])

    def test_single_token_recognition(self):
        self.assert_single_token_recognition('(')
        self.assert_single_token_recognition(')')
        self.assert_single_token_recognition('[')
        self.assert_single_token_recognition(']')
        self.assert_single_token_recognition('{')
        self.assert_single_token_recognition('}')

        self.assert_single_token_recognition('<')
        self.assert_single_token_recognition('>')
        self.assert_single_token_recognition('<=')
        self.assert_single_token_recognition('>=')
        self.assert_single_token_recognition('==')
        self.assert_single_token_recognition('=')
        self.assert_single_token_recognition('*')
        self.assert_single_token_recognition('+')
        self.assert_single_token_recognition('/')
        self.assert_single_token_recognition('-')

        self.assert_single_token_recognition('!!')
        self.assert_single_token_recognition('@')
        self.assert_single_token_recognition('#')
        self.assert_single_token_recognition('%%')
        self.assert_single_token_recognition('%')
        self.assert_single_token_recognition('^')
        self.assert_single_token_recognition(',')
        self.assert_single_token_recognition('?')
        self.assert_single_token_recognition(':')

        self.assert_single_token_recognition('as')
        self.assert_single_token_recognition('else')
        self.assert_single_token_recognition('if')
        self.assert_single_token_recognition('in')
        self.assert_single_token_recognition('loop')
        self.assert_single_token_recognition('otherwise')
        self.assert_single_token_recognition('then')

        self.assert_single_token_recognition('"test"', anon_lexer.TEXT)
        self.assert_single_token_recognition('"1234"', anon_lexer.TEXT)
        self.assert_single_token_recognition("  ' test '  ", anon_lexer.TEXT)

        self.assert_single_token_recognition('0', anon_lexer.NUMBER)
        self.assert_single_token_recognition('3.14', anon_lexer.NUMBER)
        self.assert_single_token_recognition('0123456789', anon_lexer.NUMBER)

        self.assert_single_token_recognition('test', anon_lexer.ID)
        self.assert_single_token_recognition('test1234', anon_lexer.ID)
        self.assert_single_token_recognition('  test  ', anon_lexer.ID)

    def test_multiple_token_recognition(self):
        self.assert_double_token_recognition('  test  1234  ', 'test', '1234', anon_lexer.ID, anon_lexer.NUMBER)
        self.assert_double_token_recognition('  1234test  ', '1234', 'test', anon_lexer.NUMBER, anon_lexer.ID)
        self.assert_double_token_recognition('test(', 'test', '(', anon_lexer.ID)
        self.assert_double_token_recognition('()', '(', ')')
        self.assert_double_token_recognition('if test', 'if', 'test', anon_lexer.RESERVED, anon_lexer.ID)


if __name__ == '__main__':
    unittest.main()
