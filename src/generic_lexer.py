"""
Convert text into tokens.
This generic lexer can be re-used for many different languages.
Reference: http://www.jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python--part-1-
"""
import re


def lex(characters: str, token_expressions: []):
    position = 0
    tokens = []
    size = len(characters)
    while position < size:
        match = None
        for token_expression in token_expressions:
            pattern, tag = token_expression
            regex = re.compile(pattern)
            match = regex.match(characters, position)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if match:
            position = match.end(0)
        else:
            raise SyntaxError(f'Unexpected character at position({position}): {characters[position]}')
    return tokens
