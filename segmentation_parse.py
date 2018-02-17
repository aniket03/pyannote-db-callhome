#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2018 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# ROYAL JAIN

import logging
import os
import pickle as pkl
import random
import sys
import audioread
from utils import list_files

random.seed(1729)


def str_next(prev_str):
    last_chr = prev_str[-1]

    if last_chr == 'Z':
        return prev_str + 'A'

    last_chr = chr(ord(last_chr) + 1)
    # prev_str[-1] = last_chr
    new_str = prev_str[:len(prev_str) - 1] + last_chr
    return new_str


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    read_mdtm = sys.argv[1]
    write_mdtm = sys.argv[2]

    f_read = open(read_mdtm, 'r')
    f_write = open(write_mdtm, 'w')

    init_str = 'A'

    prev_uri = ''

    for line in f_read:
        uri = line.split(' ')[0]

        if prev_uri != uri:
            prev_uri = uri
            init_str = 'A'

        print(uri)

        cols = line.split(' ')
        cols[7] = init_str

        init_str = str_next(init_str)
        write_line = ' '.join(cols) + '\n'
        f_write.write(write_line)

    f_write.close()
    f_read.close()
