import logging
import sys

from src import anon_lexer, anon_parser

logging.basicConfig(level=logging.DEBUG, filename='debug.log')


def run(code: str):
    print(f'run(), code={code}')
    tokens = anon_lexer.lex(code)
    logging.debug(f'    tokens={tokens}')
    parse_result = anon_parser.parse(tokens)
    logging.debug(f'    parse_result={parse_result}')
    if not parse_result:
        sys.stderr.write('Error parsing!')
        sys.exit(1)
    ast = parse_result.value
    env = {}

    ast_result = ast.eval(env)
    print(f'\n=========\nast_result={ast_result}')
    sys.stdout.write('\nFinal variable values:\n')
    for name in env:
        sys.stdout.write(f'{name}: {env[name]}\n')

    ast_result = ast.as_html(env)
    print(f'\n=========\nast_result={ast_result}')
    sys.stdout.write('\nFinal variable values:\n')
    for name in env:
        sys.stdout.write(f'{name}: {env[name]}\n')


def main():
    print('main()')
    run("""
    x = 42; y = hi; n = 5; p = 1;
    loop n > 0 do
      p = p * n;
      n = n - 1
    end
    """)


if __name__ == '__main__':
    main()
