#!/usr/bin/env python3
import argparse
import textwrap
import shutil
import sys

from pathlib import Path
__FLEN = 60
__HLEN = int(__FLEN / 2)


def __EOF(string: str):
    return textwrap.dedent(string).strip()


def RCWSN(
        INPUT_DIRECTORY_STR: str = './',
        OUTPUT_DIRECTORY_STR: str = './renamed',
        SUFFIX: str = None,
        DIGIT: int = 3,
        NAME: str = None,
        MOVE_MODE: bool = False,
        DEBUG_MODE: bool = False):

    def printError(string):
        print('[Error] ', string)

    print(f'{" Start " + sys._getframe().f_code.co_name + "() ":=^{__FLEN}}')
    INPUT_DIRECTORY_PATH = Path(INPUT_DIRECTORY_STR)
    OUTPUT_DIRECTORY_PATH = Path(OUTPUT_DIRECTORY_STR)

    if INPUT_DIRECTORY_PATH.is_dir():
        pass
    else:
        printError(f'{INPUT_DIRECTORY_PATH=} is NOT directory.')
        return False

    if OUTPUT_DIRECTORY_PATH.is_dir():
        pass
    else:
        printError(f'{OUTPUT_DIRECTORY_PATH=} is NOT directory.')
        return False

    if 0 < len(list(OUTPUT_DIRECTORY_PATH.iterdir())):
        printError(f'{OUTPUT_DIRECTORY_PATH=} contains child.')
        return False

    CHILDLEN = sorted(list(filter(lambda f: f.is_file(),
                                  INPUT_DIRECTORY_PATH.glob('*'))))

    if SUFFIX is None:
        print('The files with any suffix are eligible.')
    else:
        print(f'Filtering with {SUFFIX} suffix.')
        # lll = copy.deepcopy(CHILDLEN)
        # CHILDLEN = filter(lambda f: f.suffix == f'.{SUFFIX}', CHILDLEN)
        CHILDLEN = list(filter(lambda p: p.suffix == f'.{SUFFIX}', CHILDLEN))
    print(f'{len(list(CHILDLEN))} target files.')

    if DEBUG_MODE:
        print(f'{MOVE_MODE=}')
        print(f'{SUFFIX=}')
        print(*CHILDLEN)

    counter = 0
    for FILE_PATH in CHILDLEN:
        NEW_FILE_PATH = OUTPUT_DIRECTORY_PATH.joinpath(
            f'{NAME or ""}{counter:0{DIGIT}d}{FILE_PATH.suffix}'
        )
        print(f'{FILE_PATH} -> {NEW_FILE_PATH}')
        if not DEBUG_MODE:
            if MOVE_MODE:
                shutil.move(FILE_PATH, NEW_FILE_PATH)
            else:
                shutil.copy(FILE_PATH, NEW_FILE_PATH)
            print('Successeed')
        counter += 1

    print(f'{"  End " + sys._getframe().f_code.co_name + "()  ":=^{__FLEN}}')
    return True


def main():
    print(f'{" Start " + sys._getframe().f_code.co_name + "() ":=^{__FLEN}}')
    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=__EOF('''
            This script copies or moves (optional) all the files in the folder,
            renaming them sequentially, to the folder.
            example:
                abc.txt -> 01.txt,
                def.txt -> 02.txt
        ''')
    )
    PARSER.add_argument('--input_directory', '--input', '-i',
                        type=str, default='.',
                        help=__EOF('''
                            [str] The path of the input directory.
                        ''')
                        )
    PARSER.add_argument('--output_directory', '--output', '-o',
                        type=str, default='./renamed',
                        help=__EOF('''
                            [str] The path of the output directory.
                        ''')
                        )
    PARSER.add_argument('--suffix', '-s',
                        type=str,
                        help=__EOF('''
                            [str] The suffix of the file you will copy or move.
                            (default: all)
                        ''')
                        )
    PARSER.add_argument('--digit', '-d',
                        type=int, default=3,
                        help=__EOF('''
                            [int] Digit for 0 fill.
                            001, 002, 003, ...
                            (default: 3)
                        ''')
                        )
    PARSER.add_argument('--name', '-n',
                        type=str,
                        help=__EOF('''
                            [str] Initial name.
                            {name}001.{suffix},
                            {name}002.{suffix},
                            ...
                            (default: None)
                        ''')
                        )
    PARSER.add_argument('--move',  '-m',
                        action='store_true',
                        help=__EOF('''
                            [flag] Instead of copy, move(rename) only.
                        ''')
                        )
    PARSER.add_argument('--whatIdo', '--debug', '-w',
                        action='store_true',
                        help=__EOF('''
                            [flag] The copy or move is not actually performed.
                            This is used when you want to check the result of a renaming operation.
                        ''')
                        )
    RESULT = RCWSN(*vars(PARSER.parse_args()).values())
    print(f'End the main process {"successfully" if RESULT else "failed"}.')
    print(f'{"  End " + sys._getframe().f_code.co_name + "()  ":=^{__FLEN}}')


if __name__ == "__main__":
    main()
