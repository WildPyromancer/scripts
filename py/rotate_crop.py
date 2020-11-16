#!/usr/bin/env python3
import math
import argparse
import re
import textwrap
from pathlib import Path
from PIL import Image, ImageOps


__DEFAULT_DEGREE_STEP = 2
__DEFAULT_TIMES = 5
__DEFAULT_SAVE_QUALITY = 100
__FLEN = 60
__HLEN = int(__FLEN / 2)


def EOF(string):
    return textwrap.dedent(string).strip()


def rotateAndCrop(
        input_file_path,
        output_directory_path,
        radius=0,
        center_x=0,
        center_y=0,
        DEGREE_STEP=__DEFAULT_DEGREE_STEP,
        TIMES=__DEFAULT_TIMES,
        SAVE_QUALITY=__DEFAULT_SAVE_QUALITY,
        FILE_NAME_IS_FORMATTED=False):

    def printError(string):
        print('[Error] ', string)

    print(f'{" Start rotateAndCrop() ":=^{__FLEN}}')
    print(f'{"-"*5}{" Start checking arguments ":^{__FLEN-10}s}{"-"*5}')

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

    def fprint(str, var):
        print(f'{str:<{__HLEN - 2}} : {var:>{__HLEN - 1}}')

    print(f'{"-"*10}{" Variables ":^{__FLEN - 20}s}{"-"*10}')
    fprint("Input image path", str(input_file_path))
    fprint("Output directory path", str(output_directory_path))
    fprint("Cropping radius", radius)
    fprint("Coordinate of center",
           f'({center_x:{DIGIT}d},{center_y:{DIGIT}d})')
    fprint("Degree step of rotation", DEGREE_STEP)
    fprint("Number of times to rotate", TIMES)
    fprint("Save quality", SAVE_QUALITY)
    fprint("Image height", H)
    fprint("Is the file name formatted ?", FILE_NAME_IS_FORMATTED)
    fprint("Image width", W)
    fprint("Image height", H)

    print(f'{"-"*10}{"":{__FLEN - 20}s}{"-"*10}')
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

    print(f'{"-"*5}{"  End  checking arguments ":^{__FLEN-10}s}{"-"*5}')

    print(f'{"-"*5}{" Start rotating and cropping ":^{__FLEN-10}s}{"-"*5}')
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
    print(f'{"-"*5}{"  End  rotating and cropping ":^{__FLEN-10}s}{"-"*5}')
    print(f'{"  End  rotateAndCrop() ":=^{__FLEN}}')
    return True


def main():
    print(f'{" Start main() ":=^{__FLEN}}')
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
    print(f'{"  End  main() ":=^{__FLEN}}')


if __name__ == "__main__":
    main()
