#!/usr/bin/env python
import time
import textwrap
import re
import argparse
from pathlib import Path
from typing import List

__FLEN = 60
__HLEN = int(__FLEN / 2)


def measure_execution_time(func):
    start = time.time()
    func()
    elapsed_time = time.time() - start
    print(f'{elapsed_time}')
    pass


def EOF(string):
    return textwrap.dedent(string).strip()


def sort_functions(
    file_path: str
):
    file_path: Path = Path(file_path)
    if not file_path.is_file():
        print(f'{file_path} does NOT exist.')
        return False

    lines: List[str] = []
    with file_path.open(mode='r') as f:
        lines = f.readlines()

    # [
    #   func_name:str,
    #   start_line_index:int,
    #   lines:int
    # ]

    REGEX_FUNC_START = re.compile(r'[ \t]*[\w_]+\(\)\s?{')
    REGEX_FUNC_END = re.compile(r'[ \t]*}')
    func_section_start_at: int = 0
    func_section_finish_at: int = 0
    flag_in_func: bool = False
    for line in enumerate(lines):

        if re.match(REGEX_FUNC_START, line[1]) and not flag_in_func:
            flag_in_func = True
            print(f'Start func at line {line[0]}')
            print(line[1])
            if func_section_start_at == 0:
                func_section_start_at = line[0]

        if re.match(REGEX_FUNC_END, line[1]) and flag_in_func:
            print(f'End func at line {line[0]}')
            print(line[1])
            flag_in_func = False
            func_section_finish_at = line[0]

    print(EOF(f'''
        {lines[0]}
        {func_section_start_at=}
        {func_section_finish_at=}
    '''))

    return True


def main():
    print(f'{" Start main() ":=^{__FLEN}}')
    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=EOF('''
            aaaa
        ''')
    )
    PARSER.add_argument('--file',  '-f',
                        type=str, required=True,
                        help='(required)[str] Input file path.')

    RESULT = sort_functions(*vars(PARSER.parse_args()).values())
    print(f'End the main process {"successfully" if RESULT else "failed"}.')
    print(f'{"  End  main() ":=^{__FLEN}}')


if __name__ == "__main__":
    measure_execution_time(main)
    pass
