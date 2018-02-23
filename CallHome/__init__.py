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


import os.path as op

from pyannote.database import Database
from pyannote.database.protocol import SpeakerDiarizationProtocol
from pyannote.parser.annotation.mdtm import MDTMParser
from pyannote.parser.timeline.uem import UEMParser


class CallHomeProtocol(SpeakerDiarizationProtocol):
    """CallHome speaker diarization protocol """

    def trn_iter(self):
        data_dir = op.join(op.dirname(op.realpath(__file__)), 'data')
        annotations = MDTMParser().read(op.join(data_dir, 'callhome.train.mdtm'))
        uems = UEMParser().read(op.join(data_dir, 'callhome.train.uem'))

        for uri in sorted(annotations.uris):
            annotation = annotations(uri)
            annotated = uems(uri)
            yield {
                'database': 'CallHome',
                'uri': uri,
                'annotation': annotation,
                'annotated': annotated
            }

    def dev_iter(self):
        data_dir = op.join(op.dirname(op.realpath(__file__)), 'data')
        annotations = MDTMParser().read(op.join(data_dir, 'callhome.validation.mdtm'))
        uems = UEMParser().read(op.join(data_dir, 'callhome.validation.uem'))

        for uri in sorted(annotations.uris):
            annotation = annotations(uri)
            annotated = uems(uri)
            yield {
                'database': 'CallHome',
                'uri': uri,
                'annotation': annotation,
                'annotated': annotated
            }

    def tst_iter(self):
        data_dir = op.join(op.dirname(op.realpath(__file__)), 'data')
        annotations = MDTMParser().read(op.join(data_dir, 'callhome.test.mdtm'))
        uems = UEMParser().read(op.join(data_dir, 'callhome.test.uem'))

        for uri in sorted(annotations.uris):
            annotation = annotations(uri)
            annotated = uems(uri)
            yield {
                'database': 'CallHome',
                'uri': uri,
                'annotation': annotation,
                'annotated': annotated
            }


class CallHome(Database):
    """CallHome database"""

    def __init__(self, preprocessors=None, **kwargs):
        super(CallHome, self).__init__(preprocessors=preprocessors)

        if preprocessors is None:
            preprocessors = {}
        self.register_protocol('SpeakerDiarization', 'CallHomeProtocol', CallHomeProtocol)
        self.register_protocol('SpeechDetection', 'CallHomeProtocol', CallHomeProtocol)
