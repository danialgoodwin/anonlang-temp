import logging

from src.equality import Equality

logging.basicConfig(level=logging.INFO)


class Result(Equality):
    def __init__(self, value, position: int):
        self.value = value
        self.position = position

    def __repr__(self):
        return f'Result({self.value}, {self.position})'


class Parser:
    """Simplify combinator usage in the real parser by adding operator overrides."""

    def __call__(self, tokens: [], position: int):
        return None  # Override in subclasses

    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Otherwise(self, other)

    def __xor__(self, function):
        return Process(self, function)


class Reserved(Parser):
    """Match reserved tokens."""

    def __init__(self, value: str, tag: str):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, position):
        if position < len(tokens) and tokens[position][0] == self.value and tokens[position][1] is self.tag:
            return Result(tokens[position][0], position + 1)
        return None


class Tag(Parser):
    """Match any token."""

    def __init__(self, tag: str):
        self.tag = tag

    def __call__(self, tokens, position):
        if position < len(tokens) and tokens[position][1] is self.tag:
            return Result(tokens[position][0], position + 1)
        return None


# Example, to parse `1 + 2`:
#     parser = Concat(Concat(Tag(INT), Reserved('+', RESERVED)), Tag(INT))
#     parser = Tag(INT) + Reserved('+', RESERVED) + Tag(INT)
class Concat(Parser):
    """Match combination of two parsers, otherwise None."""

    def __init__(self, left: Parser, right: Parser):
        self.left = left
        self.right = right

    def __call__(self, tokens, position):
        left_result = self.left(tokens, position)
        if left_result:
            right_result = self.right(tokens, left_result.position)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.position)
        return None


class Otherwise(Parser):
    """Apply the left parser. If successful, return that result. Otherwise, return the result of the right parser.
    Example usage: parser = Reserved('*', RESERVED) | Reserved('+', RESERVED) | Reserved('-', RESERVED)
    """

    def __init__(self, left: Parser, right: Parser):
        self.left = left
        self.right = right

    def __call__(self, tokens, position):
        left_result = self.left(tokens, position)
        if left_result:
            return left_result
        else:
            right_result = self.right(tokens, position)
            return right_result


class Optional(Parser):
    """Match an optional token. Always returns valid."""

    def __init__(self, parser: Parser):
        self.parser = parser

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)
        if result:
            return result
        return Result(None, position)


class Repeat(Parser):
    """Match an list of token. Always returns valid, including empty lists."""

    def __init__(self, parser: Parser):
        self.parser = parser

    def __call__(self, tokens, position):
        results = []
        result = self.parser(tokens, position)
        while result:
            results.append(result.value)
            position = result.position
            result = self.parser(tokens, position)
        return Result(results, position)


class Process(Parser):
    """Modify the value from a parser with the given function."""

    def __init__(self, parser: Parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)
        if result:
            result.value = self.function(result.value)
            return result


class Lazy(Parser):
    """Lazy-load a parser. Useful for preventing circular recursion."""

    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, position):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, position)


class Phrase(Parser):
    """Top-level parser to prevent us from partially matching a program with garbage at the end."""

    def __init__(self, parser):
        logging.debug(f'Phrase(), init')
        self.parser = parser

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)
        logging.debug(f'Phrase(), result={result}')
        if result and result.position == len(tokens):
            return result
        else:
            return None


class Exp(Parser):
    """Match multiple Parsers, separated by the provided separator."""

    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)

        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.value, right)
        next_parser = self.separator + self.parser ^ process_next

        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.position)
            if next_result:
                result = next_result
        return result
