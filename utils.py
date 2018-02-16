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
# Venkatesh Duppada

import logging
import os
import sys

from pydub import AudioSegment


# List all files in base_path
def list_files(base_path, predicate):
    for folder, subs, files in os.walk(base_path):
        for filename in files:
            if predicate(filename):
                yield os.path.join(folder, filename)


def get_wav_files(base_path):
    for file in list_files(base_path, lambda x: x.endswith('.mp3')):
        logging.info(file)
        audio = AudioSegment.from_file(file)
        audio = audio.set_channels(1)
        audio.export(os.path.join(os.path.dirname(file), os.path.basename(
            file).split(".")[0] + ".wav"), format="wav")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    base_path = sys.argv[1]
    get_wav_files(base_path)
