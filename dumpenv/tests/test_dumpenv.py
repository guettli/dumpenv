# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import codecs
import io
import tempfile
import unittest

import os

import shutil

import dumpenv


class MyTestCase(unittest.TestCase):


    def test_dumpenv(self):
        out_dir = dumpenv.create_data_and_dump_it()

        # EXTEND README IF A NEW FILE GETS CREATED
        self.assertEqual(['PATH', 'os', 'os_environ', 'pip_freeze',
                          'platform', 'site','sys_path'],
                         sorted(os.listdir(out_dir)))

