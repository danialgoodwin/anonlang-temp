"""
Convert from Anonsage language (text) to lexemes (tokens).
"""
import logging

from src import generic_lexer

logging.basicConfig(level=logging.INFO)


ID = 'ID'
NUMBER = 'NUMBER'
RESERVED = 'RESERVED'
TEXT = 'TEXT'

TOKEN_EXPRESSIONS = [
    # Gets rid of whitespace and comments
    (r'[ \n\t]+', None),
    (r';;[^\n]*', None),

    # Extracts the core language
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r'\[', RESERVED),
    (r']', RESERVED),
    (r'{', RESERVED),
    (r'}', RESERVED),

    (r'<=', RESERVED),  # Must go before `<` in order to be detected
    (r'>=', RESERVED),  # Must go before `>` in order to be detected
    (r'<', RESERVED),
    (r'>', RESERVED),
    (r'==', RESERVED),  # Must go before `=` in order to be detected
    (r'=', RESERVED),
    (r'\*', RESERVED),
    (r'\+', RESERVED),
    (r'/', RESERVED),
    (r'-', RESERVED),

    (r'!!', RESERVED),
    (r'@', RESERVED),
    (r'#', RESERVED),
    (r'%%', RESERVED),  # Must go before `%` in order to be detected
    (r'%', RESERVED),
    (r'\^', RESERVED),
    (r',', RESERVED),
    (r'\?', RESERVED),
    (r';', RESERVED),
    (r':', RESERVED),

    (f'and', RESERVED),
    (f'as', RESERVED),
    (f'do', RESERVED),
    (r'else', RESERVED),
    (r'end', RESERVED),
    (r'if', RESERVED),
    (r'in', RESERVED),
    (r'loop', RESERVED),
    (r'not', RESERVED),
    (r'or', RESERVED),
    (r'otherwise', RESERVED),
    (r'then', RESERVED),

    (r"[rf]?'[^']*'", TEXT),
    (r'[rf]?"[^"]*"', TEXT),

    (r'[0-9]+[\.]?[0-9]*', NUMBER),
    (r'[a-zA-Z0-9_]+', ID)  # Must go after everything else in order for other tokens to be recognized
]


def lex(characters):
    logging.debug('lex()')
    return generic_lexer.lex(characters, TOKEN_EXPRESSIONS)
