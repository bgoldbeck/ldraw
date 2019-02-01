# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import unittest
import re
import os
from util import Util


class UtilTest(unittest.TestCase):

    def setUp(self):
        self.relative_path = "/assets/info/help.txt"

    def test_path_conversion(self):
        full_path = Util.path_conversion(self.relative_path)
        if os.name == 'nt':
            self.assertTrue(re.search("\\assets\\info\\help.txt", full_path))
        else:
            self.assertTrue(re.search("/assets/info/help.txt", full_path))
