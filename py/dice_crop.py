#!/usr/bin/env python
import math
import argparse
import textwrap
from pathlib import Path
from PIL import Image

__DEFAULT_SAVE_QUALITY = 100
__DAFAULT_OUTPUT_DIRECTORY_PATH = Path('diced')
__DAFAULT_RADIUS = 256
__DAFAULT_CROPPING_STEP = 128
__FLEN = 60
__HLEN = int(__FLEN / 2)


def EOF(string):
    return textwrap.dedent(string).strip()


def diceCrop(
        input_file_path,
        output_directory_path,
        RADIUS=__DAFAULT_RADIUS,
        CROPPING_STEP=__DAFAULT_CROPPING_STEP,
        SAVE_QUALITY=__DEFAULT_SAVE_QUALITY):

    print(f'{" Start diceCrop() ":=^{__FLEN}}')
    print(f'{"-"*5}{" Start checking arguments ":^{__FLEN-10}s}{"-"*5}')

    def printError(string):
        print('[Error] ', string)

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
    DIGIT = len(str(max(W, H)))

    def fprint(str, var):
        print(f'{str:<{__HLEN - 2}} : {var:>{__HLEN - 1}}')

    print(f'{"-"*10}{" Variables ":^{__FLEN - 20}s}{"-"*10}')
    fprint("Input image path", str(input_file_path))
    fprint("Output directory path", str(output_directory_path))
    fprint("Cropping radius", RADIUS)
    fprint("Cropping step", CROPPING_STEP)
    fprint("Save quality", SAVE_QUALITY)
    fprint("Image width", W)
    fprint("Image height", H)
    print(f'{"-"*10}{"":{__FLEN - 20}s}{"-"*10}')

    if \
            math.isnan(RADIUS) or\
            math.isnan(CROPPING_STEP) or\
            math.isnan(SAVE_QUALITY):
        printError('Some args are not number.')
        return False

    if output_directory_path.is_dir():
        pass
    else:
        output_directory_path.mkdir()
        print(f'Make directory => {output_directory_path}')

    print(f'{"-"*5}{"  End  checking arguments ":^{__FLEN-10}s}{"-"*5}')
    print(f'{"-"*5}{" Start dice cropping ":^{__FLEN-10}s}{"-"*5}')
    for x in range(RADIUS, W, CROPPING_STEP):
        start_x = x - RADIUS
        for y in range(RADIUS, H, CROPPING_STEP):
            start_y = y - RADIUS
            NEW_FILE_NAME = output_directory_path.joinpath(
                f'{FILE_NAME}_{start_x:0{DIGIT}}_{start_y:0{DIGIT}}{SUFFIX}'
            )
            print(EOF(f'''
                ({start_x:{DIGIT}d},{start_y:{DIGIT}d}) to \
                {x:{DIGIT}d},{y:{DIGIT}d})
                {NEW_FILE_NAME}
            '''))
            IMAGE.crop((start_x, start_y, x, y)).save(
                NEW_FILE_NAME,
                quality=SAVE_QUALITY
            )
    print(f'{"-"*5}{"  End  dice cropping ":^{__FLEN-10}s}{"-"*5}')
    print(f'{"  End  diceCrop() ":=^{__FLEN}}')
    return True


def main():
    print(f'{" Start main() ":=^{__FLEN}}')
    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=EOF('''
            This script crops the image while changing its position.
            Repeat the following process within the size of the image.
            1.Trim an image to a specified length of a square and save it.
            2.Move the trimming position to the right by the specified amount.
              If the cropping area isn\'t outside the range of the image, -> 1.
            3.Move the trimming position downward by the specified amount.
              If the cropping area isn\'t outside the range of the image, -> 2.
        ''')
    )
    PARSER.add_argument('--input', '--image',  '-i',
                        type=str, required=True,
                        help='(required)[str] Input image\'s path.')
    PARSER.add_argument('--output', '--directory',  '-o',
                        type=str,
                        help=f'[str] Output directory path.\n'
                        f'(default: {__DAFAULT_OUTPUT_DIRECTORY_PATH})')
    PARSER.add_argument('--radius', '-r',
                        type=int, default=__DAFAULT_RADIUS,
                        help=f'[int] Cropping radius.\n'
                        f'(default: {__DAFAULT_RADIUS})')
    PARSER.add_argument('--cropping_step', '-ds',
                        type=int, default=__DAFAULT_CROPPING_STEP,
                        help=f'[int] Cropping step.\n'
                        f'(default: {__DAFAULT_CROPPING_STEP})')
    PARSER.add_argument('--save_quality', '-q',
                        type=int, default=__DEFAULT_SAVE_QUALITY,
                        help=f'[int] 1 to 100.\n'
                        f'(default: {__DEFAULT_SAVE_QUALITY})')

    RESULT = diceCrop(*vars(PARSER.parse_args()).values())
    print(f'End the main process {"successfully" if RESULT else "failed"}.')
    print(f'{"  End  main() ":=^{__FLEN}}')


if __name__ == "__main__":
    main()
