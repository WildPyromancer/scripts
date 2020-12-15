#!/usr/bin/env python
import argparse
import shutil
import sys
import textwrap
import time
from typing import NoReturn

CONSOLE_COLUMNS = shutil.get_terminal_size().columns
CONSOLE_COLUMNS_HALF = int(CONSOLE_COLUMNS / 2)


def measure_execution_time(func):
    start = time.time()
    result = func()
    elapsed_time = time.time() - start
    print(f'function {func.__qualname__} elapsed {elapsed_time} sec.')
    return result


def print_center(string: str, fill_char: str = '-') -> NoReturn:
    print(f'{string:{fill_char}^{CONSOLE_COLUMNS}}')


def EOF(string) -> str:
    return textwrap.dedent(string).strip()


def hoge(
    file_path: str
) -> bool:
    print_center(f' {sys._getframe().f_code.co_name}() ', '+')
    print_center(f' {sys._getframe().f_code.co_name}() ')
    return True


def main() -> NoReturn:
    print_center(f' {sys._getframe().f_code.co_name}() ', '+')
    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=EOF('''
            usage
        ''')
    )
    PARSER.add_argument('--file',  '-f',
                        type=str, required=True,
                        help='(required)[str] Input file path.')

    RESULT = hoge(*vars(PARSER.parse_args()).values())
    print(f'End the main process {"successfully" if RESULT else "failed"}.')
    print_center(f' {sys._getframe().f_code.co_name}() ')


if __name__ == '__main__':
    measure_execution_time(main)
