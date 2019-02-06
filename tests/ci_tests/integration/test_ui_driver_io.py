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
from src.ui.ui_driver import UIDriver


class TextUIDriverIO(unittest.TestCase):

    def testReadAssetsFileAboutText(self):
        about_text = UIDriver.get_assets_file_text("ABOUT.txt")
        self.assertIsNotNone(about_text)
        # The about text file should always contain the MIT License.
        # This way we can make sure the about text file contains the information we expect.
        self.assertTrue(about_text.find("MIT License") != -1)

    def testReadAssetsFileHelpText(self):
        help_text = UIDriver.get_assets_file_text("HELP.txt")
        self.assertIsNotNone(help_text)
        # The help text file probably will always contain the LDraw word.
        # This way we can make sure the help text contains the information we expect.
        self.assertTrue(help_text.find("LDraw") != -1)

    def testReadAssetsFileNotExist(self):
        no_text = UIDriver.get_assets_file_text("THIS_FILE_SERIOUSLY_SHOULD_NOT_EXISTS.txt")
        self.assertIsNone(no_text)
