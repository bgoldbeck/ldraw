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
