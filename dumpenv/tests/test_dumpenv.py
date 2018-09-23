# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import codecs
import io
import tempfile
import unittest

import os

import shutil

import dumpenv


class MyTestCase(unittest.TestCase):


    def test_dumpenv(self):
        os.environ['umlaut_latin1']='umlaut ü'.encode('latin1')
        os.environ['umlaut_utf8']='umlaut ü'.encode('utf8')
        out_dir = dumpenv.create_data_and_dump_it()

        # EXTEND README IF A NEW FILE GETS CREATED
        self.assertEqual(['PATH', 'os', 'os_environ', 'pip_freeze',
                          'platform', 'site','sys_path'],
                         sorted(os.listdir(out_dir)))

