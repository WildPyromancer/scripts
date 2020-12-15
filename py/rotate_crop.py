#!/usr/bin/env python
import argparse
import math
import re
import shutil
import sys
import textwrap
import time
from pathlib import Path
from PIL import Image, ImageOps
from typing import NoReturn

CONSOLE_COLUMNS = shutil.get_terminal_size().columns
CONSOLE_COLUMNS_HALF = int(CONSOLE_COLUMNS / 2)
__DEFAULT_DEGREE_STEP = 2
__DEFAULT_SAVE_QUALITY = 100
__DEFAULT_TIMES = 5


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


def rotateAndCrop(
    input_file_path,
    output_directory_path,
    radius=0,
    center_x=0,
    center_y=0,
    DEGREE_STEP=__DEFAULT_DEGREE_STEP,
    TIMES=__DEFAULT_TIMES,
    SAVE_QUALITY=__DEFAULT_SAVE_QUALITY,
    FILE_NAME_IS_FORMATTED=False
) -> bool:

    def printError(string):
        print('[Error] ', string)

    print_center(f' {sys._getframe().f_code.co_name}() ', '+')
    print_center(' Checking arguments ', '+')

    input_file_path = Path(input_file_path)
    output_directory_path = Path(output_directory_path)

    if input_file_path.is_file():
        pass
    else:
        printError(f'[file path] {input_file_path} does not found.')
        return False

    IMAGE = Image.open(input_file_path)
    W, H = IMAGE.width, IMAGE.height
    FILE_NAME = input_file_path.stem
    SUFFIX = input_file_path.suffix

    if radius == 0:
        if W == H and W % 3 == 0:
            radius = int(W / 3)
        else:
            printError(
                EOF('''
                    You can omit the radius argument if the image meets the following conditions.
                    - square
                    - side length is a multiple of 3
                    In this case, crop the image to 2/3 of the side length of the image.'''
                    )
            )
            return False
    else:
        pass

    if FILE_NAME_IS_FORMATTED:
        if re.fullmatch(r'.+(_\d+?){3}', FILE_NAME) is None:
            print('Flagged but file name is invalid.')
        else:
            print('Input file name fullmatched the format.')
            NEW_ARGS = FILE_NAME.split('_')
            radius = int(NEW_ARGS[len(NEW_ARGS)-3])
            center_x = int(NEW_ARGS[len(NEW_ARGS)-2])
            center_y = int(NEW_ARGS[len(NEW_ARGS)-1])

    if center_x < 1:
        center_x = int(W/2)
    if center_y < 1:
        center_y = int(H/2)

    if \
            math.isnan(radius) or\
            math.isnan(center_x) or\
            math.isnan(center_y) or\
            math.isnan(DEGREE_STEP) or \
            math.isnan(TIMES) or\
            math.isnan(SAVE_QUALITY):
        printError('Some args are not number.')
        return False

    if \
            0 > radius or\
            0 > DEGREE_STEP or\
            0 > TIMES or\
            0 > SAVE_QUALITY:
        printError(
            'radius, degree and step, save quality should be greater than 0.')
        return False

    if \
            W < center_x + radius or\
            H < center_y + radius or\
            0 > center_x - radius or\
            0 > center_y - radius:
        printError('The cropped area protrudes from the image.')
        return False

    if output_directory_path.is_dir():
        pass
    else:
        output_directory_path.mkdir()
        print(f'Make directory => {output_directory_path}')

    print_center(' Checking arguments ')
    print_center(' Rotating and cropping ', '+')

    for i in range(TIMES + 1):
        current_degree = i * DEGREE_STEP
        print(f'{str(current_degree)}˚')
        new_image = IMAGE.rotate(current_degree, center=(center_x, center_y))
        new_image = new_image.crop((
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        ))
        new_image_path = output_directory_path.joinpath(
            f'{FILE_NAME}+{current_degree:02}{SUFFIX}'
        )
        print(new_image_path)
        new_image.save(
            new_image_path,
            quality=SAVE_QUALITY
        )
        if i == 0:
            continue

        new_image_path = output_directory_path.joinpath(
            f'{FILE_NAME}-{current_degree:02}{SUFFIX}'
        )
        print(new_image_path)
        ImageOps.mirror(new_image).save(
            new_image_path,
            quality=SAVE_QUALITY
        )
    print_center(' Rotating and cropping ')
    print_center(f' {sys._getframe().f_code.co_name}() ')
    return True


def main() -> NoReturn:
    print_center(f' {sys._getframe().f_code.co_name}() ', '+')
    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=EOF('''
            This script crops the image into a square with the specified radius,
            rotating the image around the specified coordinates.
            Requires 3 or more arguments.
        ''')
    )
    PARSER.add_argument('--input', '--image',  '-i',
                        type=str, required=True,
                        help='(required)[str] Input image\'s path.')
    PARSER.add_argument('--output', '--directory',  '-o',
                        type=str, required=True,
                        help='(required)[str] Output directory path.')
    PARSER.add_argument('--radius', '-r',
                        type=int,
                        help='[int] Cropping radius.')
    PARSER.add_argument('--center_x', '-x',
                        type=int, default=0,
                        help=EOF('''
                            [int] X-coordinate of the rotation axis.
                            (default: (image\'s width)/2)
                        ''')
                        )
    PARSER.add_argument('--center_y', '-y',
                        type=int, default=0,
                        help=EOF('''
                            [int] X-coordinate of the rotation axis.
                            (default: (image\'s width)/2)
                        ''')
                        )
    PARSER.add_argument('--degree_step', '-ds',
                        type=int, default=__DEFAULT_DEGREE_STEP,
                        help=EOF(f'''
                            [int] Degree(˚) step for rotation.
                            (default: {__DEFAULT_DEGREE_STEP}˚)
                        ''')
                        )
    PARSER.add_argument('--times', '-t',
                        type=int, default=__DEFAULT_TIMES,
                        help=EOF(f'''
                            [int] Number of times to rotate.
                            (default: {__DEFAULT_TIMES})
                        '''))
    PARSER.add_argument('--save_quality', '-q',
                        type=int, default=__DEFAULT_SAVE_QUALITY,
                        help=EOF(f'''
                            [int] 1 to 100.
                            (default: {__DEFAULT_SAVE_QUALITY})
                        ''')
                        )
    PARSER.add_argument('--formatted_name_mode', '-f',
                        action='store_true',
                        help=EOF('''
                            This is a mode flag if the file name is in the specified format.
                            By enabling this, the following arguments are received from the file name.
                            - Radius
                            - X-coordinate of the rotation axis
                            - Y-coordinate of the rotation axis

                            file name format:
                            ... _(radius)_(X)_(Y).(suffix)
                            example: hoge_512_650_702.jpg
                        ''')
                        )
    RESULT = rotateAndCrop(*vars(PARSER.parse_args()).values())
    print(f'End the main process {"successfully" if RESULT else "failed"}.')
    print_center(f' {sys._getframe().f_code.co_name}() ')


if __name__ == '__main__':
    measure_execution_time(main)
