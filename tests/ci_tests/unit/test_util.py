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
import os
from src.util import Util


class UtilTest(unittest.TestCase):

    def setUp(self):
        self.project_path = Util.ROOT_DIR
        self.relative_path = "assets/info/HELP.txt"
        if os.name == 'nt':
            self.valid_file = self.project_path + "\\assets\\info\\HELP.txt"
            self.invalid_file = self.project_path + "\\invalid\\INVALID.txt"
        else:
            self.valid_file = self.project_path + "/assets/info/HELP.txt"
            self.invalid_file = self.project_path + "/invalid/INVALID.txt"

    def test_path_conversion(self):
        self.assertEqual(Util.path_conversion(self.relative_path), self.valid_file)

    def test_is_file(self):
        self.assertTrue(Util.is_file(self.valid_file))
        self.assertFalse(Util.is_file(self.invalid_file))

    def test_get_filename(self):
        self.assertEqual(Util.get_filename(self.valid_file), 'HELP.txt')

    def test_is_dir(self):
        self.assertTrue(Util.is_dir(self.valid_file.rstrip("HELP.txt")))
        self.assertFalse(Util.is_dir(self.invalid_file.rstrip("INVALID.txt")))

    def test_get_parent(self):
        self.assertEqual(Util.get_parent(self.valid_file), self.valid_file.rstrip("/HELP.txt"))

    def test_mkdir(self):
        temp_test_dir = Util.path_conversion("tests/temp/temp_test")
        Util.mkdir(temp_test_dir)
        self.assertTrue(Util.is_dir(temp_test_dir))
        Util.rmdir(temp_test_dir)
        Util.rmdir(Util.path_conversion("tests/temp"))

    def test_rmdir(self):
        temp_test_dir = Util.path_conversion("tests/temp/temp_test")
        Util.mkdir(temp_test_dir)
        self.assertTrue(Util.is_dir(temp_test_dir))
        Util.rmdir(temp_test_dir)
        self.assertFalse(Util.is_dir(temp_test_dir))
        Util.rmdir(Util.path_conversion("tests/temp"))




