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
from src.lscan import LScan
from src.ui.application_state import ApplicationState
from src.ui.main_frame import MainFrame


class UIDriverTest(unittest.TestCase):
    def setUp(self):
        self.ui_driver = UIDriver(None)

    def tearDown(self):
        pass

    def testInitialized(self):
        self.assertIsNone(self.ui_driver.root_frame)
        self.assertEqual(self.ui_driver.application_state, ApplicationState.WAITING_INPUT)
        self.assertEqual(self.ui_driver.instance, self.ui_driver)
