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
import pickle as pkl
import random
import sys

from utils import list_files

random.seed(1729)


def represent_int(s):
    try:
        int(s)
        return True
    except ValueError as e:
        return False


def get_secs(x):
    return x * 4 * 2.0 / 8000


def get_start_duration(t1, t2):
    t1 = get_secs(t1)
    t2 = get_secs(t2)
    return t1, t2 - t1


def parse_transcripts(f_path):
    lines = open(f_path, 'r').read().splitlines()
    segments = []
    for i, line in enumerate(lines):
        if line.startswith('*'):
            id = line.split(':')[0][1:]
        splits = line.split(" ")
        if splits[-1].find('_') != -1:
            indexes = splits[-1].strip()
            start = indexes.split("_")[0].strip()[1:]
            end = indexes.split("_")[1].strip()[:-1]
            if represent_int(start) and represent_int(end):
                segments.append([id, int(start), int(end)])

    merged_segments = []
    completed = []
    for i in range(len(segments)):
        if i in completed:
            continue
        curr_id = segments[i][0]
        start = segments[i][1]
        end = segments[i][2]
        completed.append(i)
        for j in range(i + 1, len(segments)):
            if segments[j][0] != curr_id:
                break
            else:
                completed.append(j)
                end = segments[j][2]
        merged_segments.append([curr_id, start, end])
    pkl.dump(merged_segments, open('{}_pickle'.format(f_path), 'wb'))
    return segments


def mdtm_helper(split, files):
    mdtm_fobj = open('./CallHome/data/callhome.{}.mdtm'.format(split), 'w')
    uem_fobj = open('./CallHome/data/callhome.{}.uem'.format(split), 'w')
    mdtm_temp_data = "{} 1 {} {} speaker NA unknown {}\n"
    uem_temp_data = "{} 1 {} {}\n"
    logging.info("{} size: {}".format(split, len(files)))
    for f in files:
        audio_f = os.path.split(f)[1].split('.')[0]
        segs = pkl.load(open(f, 'rb'))
        for i, seg in enumerate(segs):
            start, duration = get_start_duration(seg[1], seg[2])
            mdtm_fobj.write(mdtm_temp_data.format(audio_f, start, duration, audio_f + '_{}'.format(seg[0])))
        uem_fobj.write(uem_temp_data.format(audio_f, get_secs(segs[0][1]), get_secs(segs[-1][2])))
    uem_fobj.close()
    mdtm_fobj.close()


def create_mdtm_files(base_path, train_frac, val_frac):
    files = list(list_files(base_path, lambda x: x.endswith("cha_pickle")))
    random.shuffle(files)
    n = len(files)
    mdtm_helper("train", files[:int(train_frac * n)])
    mdtm_helper("validation", files[int(train_frac * n):int((train_frac + val_frac) * n)])
    mdtm_helper("test", files[int((train_frac + val_frac) * n):])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    base_path = sys.argv[1]
    try:
        train_frac = float(sys.argv[2])
    except:
        train_frac = 0.8

    try:
        val_frac = float(sys.argv[3])
    except:
        val_frac = 0.1

    for f_path in list_files(base_path, lambda x: x.endswith(".cha")):
        if os.path.exists(f_path.split('.')[0] + '.wav'):
            segments = parse_transcripts(f_path)
    create_mdtm_files(base_path, train_frac, val_frac)
