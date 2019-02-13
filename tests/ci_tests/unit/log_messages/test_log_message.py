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
from src.log_messages.log_type import LogType
from src.log_messages.log_message import LogMessage


class TestLogMessage(unittest.TestCase):
    def setUp(self):
        self.log_type = LogType.ERROR
        self.log_color = [255, 0, 0]
        self.message = 'This is a test error'
        self.log = LogMessage(self.log_type, self.message)

    def test_get_message(self):
        self.assertEqual(self.log.get_message(), self.message)

    def test_get_message_type(self):
        self.assertEqual(self.log.get_message_type(), self.log_type)

    def test_get_timestamp(self):
        self.assertIsInstance(self.log.get_timestamp(), str)

    def test_get_log_message_color(self):
        self.assertEqual(self.log.get_log_message_color(), self.log_color)
