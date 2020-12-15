#!/usr/bin/env python

import argparse
import re
import shutil
import sys
import textwrap
import time
from pathlib import Path
from typing import List, NoReturn

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


def sort_functions(
    file_path: str
) -> bool:
    print_center(f' {sys._getframe().f_code.co_name}() ', '+')

    file_path: Path = Path(file_path)
    if not file_path.is_file():
        print(f'{file_path} does NOT exist.')
        return False

    lines: List[str] = []
    with file_path.open(mode='r') as f:
        lines = f.readlines()

    class Function_string:
        def __init__(
            self,
            func_name: str,
            start_at: int
        ):
            self.func_name: str = func_name
            self.lines: int = 1
            self.start_at: int = start_at

    REGEX_FUNC_START = re.compile(r'[ \t]*[\w_0-9]+\(\) ?{')
    REGEX_FUNC_NAME = re.compile(r'[ \t]*([\w_0-9]+)\(\) ?{')
    REGEX_FUNC_END = re.compile(r'[ \t]*}')
    functions: List[Function_string] = []
    current_func: Function_string
    function_section_start_at: int = 0
    function_section_finish_at: int = 0
    in_func: bool = False

    for line in enumerate(lines):
        if re.match(REGEX_FUNC_START, line[1]) and not in_func:
            if function_section_start_at == 0:
                function_section_start_at = line[0]

            in_func = True
            current_func = Function_string(
                re.sub(REGEX_FUNC_NAME, r'\1', line[1]),
                line[0]
            )
            continue

        if not in_func:
            continue

        current_func.lines += 1

        if re.match(REGEX_FUNC_END, line[1]):
            in_func = False
            function_section_finish_at = line[0]
            functions.append(current_func)

    print(EOF(f'''
        {function_section_start_at=}
        {function_section_finish_at=}
    '''))

    # def sort(func: Function_string):
    #     pass

    sorted_functions = sorted(functions, key=lambda f: f.func_name)

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

    RESULT = sort_functions(*vars(PARSER.parse_args()).values())
    print(f'End the main process {"successfully" if RESULT else "failed"}.')
    print_center(f' {sys._getframe().f_code.co_name}() ')


if __name__ == '__main__':
    measure_execution_time(main)
