#!/usr/bin/env python
import sys
import re


if __name__ == "__main__":
    path: str = 'newzsh'
    f: str = open(sys.argv[1], 'r')
    body: str = f.read()
    f.close()
    REGEXP_s14 = r"(\s{14}[\w'#].+)\n\s{14}([\w'#].+)"
    REGEXP_s7 = r"(\s{7}[\w'#].+)\n\s{7}([\w'#].+)"
    REGEXP_hifn = r'(\w+)‐\s{1,}'
    REGEXP_hoge = r'(\w)-(\w)'
    REGEXP_dup_space = r'(\S) {2,3}'
    REGEXP_110 = r'( {14})(.{96})(.+)'

    new_str: str = re.sub(REGEXP_s14, r'\1 \2', body)
    new_str = re.sub('`', "'", new_str)
    for i in range(5):
        new_str = re.sub(REGEXP_s14, r'\1 \2', new_str)
        pass
    for i in range(5):
        new_str = re.sub(REGEXP_s7, r'\1 \2', new_str)

    new_str = re.sub(REGEXP_dup_space, r'\1 ', new_str)
    new_str = re.sub(REGEXP_hifn, r'\1', new_str)
    new_str = re.sub(REGEXP_hoge, r'\1 \2', new_str)
    # for i in range(5):
    #     new_str = re.sub(REGEXP_110, r'\1\2\n\1\3', new_str)

    with open(path, mode='w') as f:
        f.write(new_str)
    pass
