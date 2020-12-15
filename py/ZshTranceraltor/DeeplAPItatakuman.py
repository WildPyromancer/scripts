#!/usr/bin/env python
import argparse
import re
import sys
import textwrap
import urllib
from collections import deque
from enum import Enum, unique
from pathlib import Path
from typing import List


__FLEN = 60
__HLEN = int(__FLEN / 2)


@unique
class Languages(Enum):
    Chinese = 'ZH'
    Dutch = 'NL'
    English = 'EN'
    French = 'FR'
    German = 'DE'
    Italian = 'IT'
    Japanese = 'JA'
    Polish = 'PL'
    Portuguese = 'PT'
    Russian = 'RU'
    Spanish = 'ES'


def __EOF(string: str):
    return textwrap.dedent(string).strip()


# {行番号:文字列}
# キューに入れる
# キューからpop
# 文字列 -> translate
# 行番号 -> 元の配列[行番号] = 文字列

# def translate(string: str) -> List[int, str]:
#     return ''


def HOGE(
        input_file_path: str,
        output_file_path: str,
        target_lang: str = Languages.Japanese,
        source_lang: str = Languages.English
):
    input_file_path: Path = Path(input_file_path)
    output_file_path: Path = Path(output_file_path)
    if not input_file_path.is_file():
        print(f'{input_file_path} does NOT exist.')
        return False

    lines: List[str] = []
    with input_file_path.open(mode='r') as f:
        lines = f.readlines()

    # [
    #   index:int,
    #   number_of_head_blanks:int,
    #   text(removed head blanks):str
    # ]
    line_que: deque[int][int][str] = deque()
    REGEXP_BLANKS = re.compile(r'^ {7,}\S')
    REGEXP_START_WITH_HYPHEN = re.compile(r'^ {7,}-')
    REGEXP_START_WITH_BIGCHAR = re.compile(r'^ {7,}[A-Z_]{2,}')
    REGEXP_CONTAINS_WORD = re.compile("\\w{2,}")
    REGEXP_NOT_BLANK = re.compile(r'[^ ]')

    for i in enumerate(lines):
        # ^{7個以上のスペース}{{1文字目は'-'以外}[大文字と'_']の２連続以外で始まる}
        if not re.match(REGEXP_BLANKS, i[1]):
            break
        if not re.match(REGEXP_CONTAINS_WORD, i[1]):
            break
        if re.match(REGEXP_START_WITH_HYPHEN, i[1]):
            break
        if re.match(REGEXP_START_WITH_BIGCHAR, i[1]):
            break

            i_removed_return: str = i[1][0:-1]
            blanks: int = \
                re.search(REGEXP_NOT_BLANK, i_removed_return).start()

            line_que.append([
                i[0],
                # 改行文字を削除。
                blanks,
                i_removed_return[blanks:]
            ])


# https: // api.deepl.com/v2/translate?auth_key={認証キー}
# &text={翻訳したい文字列}&text={翻訳したい文字列}
# &target_lang = {翻訳したい言語の指定}
    query_base: str = 'https://api.deepl.com/v2/translate?'
    auth_key: str = 'auth_key'
    split_sentences: int = 0

    index_que: deque[int] = deque()
    max_txt: int = 1
    while len(line_que) > 0:
        text_list: List[str] = []
        for i in enumerate(range(max_txt)):
            index, text = line_que.popleft()
            index_que.append(index)
            text = urllib.parse.quote(text)
            text_list.append(f'&text={text}')
            if len(line_que) == 0:
                break

        texts: str = "".join(text_list)
        # print(urllib.parse.unquote(texts))
        http_request_str: str = \
            f'{query_base}auth_key={auth_key}{texts}&target_lang={target_lang}&source_lang={source_lang}$split_sentences={split_sentences}'
        # print(http_request_str)
    return True


def main():
    print(f'{" Start " + sys._getframe().f_code.co_name + "() ":=^{__FLEN}}')
    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=__EOF('''
            This script
        ''')
    )
    PARSER.add_argument('--input-file', '-i',
                        type=str, required=True,
                        help='(required)[str]')
    PARSER.add_argument('--output-file',  '-o',
                        type=str, required=True,
                        help='(required)[str]')
    PARSER.add_argument('--target_lang', '-tl',
                        type=str, required=False,
                        choices=Languages._member_names_,
                        default=Languages.Japanese),
    PARSER.add_argument('--source_lang', '-sl',
                        type=str, required=False,
                        choices=Languages._member_names_,
                        default=Languages.English)

    RESULT = HOGE(*vars(PARSER.parse_args()).values())
    print(f'End the main process {"successfully" if RESULT else "failed"}.')
    print(f'{"  End " + sys._getframe().f_code.co_name + "()  ":=^{__FLEN}}')


if __name__ == "__main__":
    main()
