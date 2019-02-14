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
from src.ui.user_event import *
from src.log_messages.log_type import LogType


class UserEventTest(unittest.TestCase):
    def setUp(self):
        self.event_type = UserEventType.INPUT_MODEL_READY
        self.log_message = LogMessage(LogType.WARNING, "This is the test ")
        self.event = UserEvent(self.event_type, self.log_message)

    def tearDown(self):
        pass

    def test_get_event_type(self):
        self.assertEqual(self.event.get_event_type(), self.event_type)

    def test_get_log_messages(self):
        self.assertEqual(self.event.get_log_message(), self.log_message)
