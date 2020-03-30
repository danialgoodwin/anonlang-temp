import unittest

from experimental.transpile_to_html import transpile, tokenize


class TestTokenize(unittest.TestCase):

    def test_no_input(self):
        anonlang = ''
        expected = []
        self.assertListEqual(tokenize(anonlang), expected)

    def test_empty_string(self):
        anonlang = '''
            ''
        '''
        expected = [("''", 'TEXT_SINGLE')]
        self.assertListEqual(tokenize(anonlang), expected)

    def test_hello_world(self):
        anonlang = '''
            'Hello, World!'
        '''
        expected = [("'Hello, World!'", 'TEXT_SINGLE')]
        self.assertListEqual(tokenize(anonlang), expected)

    def test_double_quote(self):
        anonlang = '''
            "Hello, World!"
        '''
        expected = [('"Hello, World!"', 'TEXT_DOUBLE')]
        self.assertListEqual(tokenize(anonlang), expected)

    def test_comment(self):
        anonlang = '''
            // hi
            'Hello, World!'
            // hi
            's2'
        '''
        expected = [("'Hello, World!'", 'TEXT_SINGLE'), ("'s2'", 'TEXT_SINGLE')]
        self.assertListEqual(tokenize(anonlang), expected)

    def test_long_sentence_with_symbols(self):
        anonlang = '''
            '1234567890!@#$%^&*() []{}=+'          's2'
        '''
        expected = [("'1234567890!@#$%^&*() []{}=+'", 'TEXT_SINGLE'), ("'s2'", 'TEXT_SINGLE')]
        self.assertListEqual(tokenize(anonlang), expected)

    def test_variable(self):
        anonlang = '''
            my_variable
            my_var = 'hi'
            'Hello, World!'
        '''
        expected = [('my_variable', 'ID'), ('my_var', 'ID'), ('=', 'RESERVED'), ("'hi'", 'TEXT_SINGLE'),
                    ("'Hello, World!'", 'TEXT_SINGLE')]
        self.assertEqual(tokenize(anonlang), expected)

    def test_math(self):
        anonlang = 'fahrenheit = celsius * 1.8 + 32'
        expected = [('fahrenheit', 'ID'), ('=', 'RESERVED'), ('celsius', 'ID'), ('*', 'RESERVED'), ('1.8', 'NUMBER'),
                    ('+', 'RESERVED'), ('32', 'NUMBER')]
        self.assertListEqual(tokenize(anonlang), expected)

    def test_text_with_view(self):
        anonlang = "'Fahrenheit: ' <input id=fah bind=solve(fahrenheit, celsius=cel)>"
        expected = [("'Fahrenheit: '", 'TEXT_SINGLE'), ('<', 'RESERVED'), ('input', 'ID'), ('id', 'ID'), ('=', 'RESERVED'),
                    ('fah', 'ID'), ('bind', 'ID'), ('=', 'RESERVED'), ('solve', 'ID'), ('(', 'RESERVED'),
                    ('fahrenheit', 'ID'), (',', 'RESERVED'), ('celsius', 'ID'), ('=', 'RESERVED'), ('cel', 'ID'),
                    (')', 'RESERVED'), ('>', 'RESERVED')]
        self.assertListEqual(tokenize(anonlang), expected)


class TestTranspile(unittest.TestCase):

    def test_hello_world(self):
        anonlang = '''
            'Hello, World!'
        '''
        expected = 'Hello, World!'
        self.assertEqual(transpile(anonlang), expected)

    def test_variable(self):
        anonlang = '''
            my_variable
            my_var = 'hi'
            'Hello, World!'
        '''
        expected = 'Hello, World!'
        self.assertEqual(transpile(anonlang), expected)

    def test_math(self):
        anonlang = 'fahrenheit = celsius * 1.8 + 32'
        expected = ''
        self.assertEqual(transpile(anonlang), expected)

    # def test_text_with_view(self):
    #     anonlang = "'Fahrenheit: ' <input id=fah bind=solve(fahrenheit, celsius=cel)>"
    #     expected = "Fahrenheit: <input id='fah'>"
    #     self.assertEqual(transpile(anonlang), expected)


# class TestTranspileView(unittest.TestCase):
#
#     def test_view_minimal(self):
#         anonlang = '<input>'
#         expected = '<input>'
#         self.assertEqual(transpile(anonlang), expected)


if __name__ == '__main__':
    unittest.main()
