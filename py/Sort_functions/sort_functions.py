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
    begin = time.time()
    result = func()
    elapsed_time = time.time() - begin
    print(f'function {func.__qualname__} elapsed {elapsed_time} sec.')
    return result


def print_center(string: str, fill_char: str = '-') -> NoReturn:
    print(f'{string:{fill_char}^{CONSOLE_COLUMNS}}')


def EOF(string) -> str:
    return textwrap.dedent(string).strip()


def sort_functions(
    file_path: str,
    debug_mode: bool = False
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
            name: str,
            begin_at: int
        ):
            self.begin_at: int = begin_at
            self.end_at: int
            self.name: str = name

        def get_string(self):
            ''.join(lines[self.begin_at:self.end_at])

    REGEX_FUNC_START = re.compile(r'^[\w_0-9]+\(\) ?{')
    REGEX_FUNC_NAME = re.compile(r'^([\w_0-9]+)\(\) ?{')
    REGEX_FUNC_END = re.compile(r'^}')
    functions: List[Function_string] = []
    current_func: Function_string
    section_of_function_begins_at: int = 0
    section_of_function_ends_at: int = 0
    in_func: bool = False

    for line in enumerate(lines):
        if re.match(REGEX_FUNC_START, line[1]):
            if in_func:
                print(f'Function start is duplicated at {line[0]} .')
                return False
            if section_of_function_begins_at == 0:
                section_of_function_begins_at = line[0]

            in_func = True
            current_func = Function_string(
                re.sub(REGEX_FUNC_NAME, r'\1', line[1]),
                line[0]
            )
            continue

        if not in_func:
            continue

        if re.match(REGEX_FUNC_END, line[1]):
            in_func = False
            section_of_function_ends_at = line[0]
            current_func.end_at = line[0]
            functions.append(current_func)

    if len(functions) == 0:
        print(f'{file_path} has NO function .')
        return False

    sorted_functions: List[Function_string] = sorted(
        functions, key=lambda f: f.name)

    new_lines: List[str] = []
    new_lines.extend(lines[0:section_of_function_begins_at])
    for f in sorted_functions:
        new_lines.extend(lines[f.begin_at:f.end_at + 1])
        new_lines.append('\n')
    new_lines.extend(lines[section_of_function_ends_at + 1:])

    new_str: str = ''.join(new_lines)
    if debug_mode:
        print(new_str)
    else:
        with open(file_path, mode='w') as f:
            f.write(new_str)

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
                        help='(required)[str] File path.'),
    PARSER.add_argument('--debug',  '-d',
                        action='store_true', required=False,
                        help='(optional)[flag] Print only. Don\'t write. ')

    RESULT = sort_functions(*vars(PARSER.parse_args()).values())
    print(f'End the main process {"successfully" if RESULT else "failed"}.')
    print_center(f' {sys._getframe().f_code.co_name}() ')


if __name__ == '__main__':
    measure_execution_time(main)
