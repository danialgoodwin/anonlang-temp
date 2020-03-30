


HTML_ELEMENTS_WITH_NO_CLOSE_TAG = ['input', 'br', 'hr']


def parse_tokens(tokens: [(str, str)]):
    output = ''
    previous_token = None
    nest_stack = []
    for i, token in enumerate(tokens):
        text, tag = token
        if text == '<' or text == '(':
            nest_stack.append(text)
        elif text == '>' or text == ')':
            if nest_stack[-1] == text:
                nest_stack.pop()
            else:
                raise AssertionError(f'Error: Unmatched closure, nest_stack={nest_stack}, text={text}')

        if previous_token is not None and previous_token[0] == '=':
            logging.debug(f'    = token={token}')
        elif previous_token is not None and previous_token[0] == '<':
            logging.debug(f'    < token={token}')
        elif tag == TEXT_DOUBLE:
            output += text.strip('"')
        elif tag == TEXT_SINGLE:
            output += text.strip("'")
        previous_token = token
    if nest_stack:
        raise AssertionError(f'Error: nest_stack should be empty by the time the program finishes, nest_stack={nest_stack}')
    return output


def transpile(anonlang: str) -> str:
    print('transpile()')
    tokens = tokenize(anonlang)
    output = parse_tokens(tokens)
    return output


