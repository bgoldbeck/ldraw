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
from src.ui.user_event_type import UserEventType
from src.log_messages.log_message import *
from src.ui.iui_behavior import *


class TestIuiBehavior(unittest.TestCase):

    def setUp(self):
        self.new_state = ApplicationState.STARTUP
        self.event = UserEvent(UserEventType.LOG_INFO, LogMessage(LogType.ERROR, "this is test"))
        self.iui = IUIBehavior()

    def test_on_state_changed(self):
        with self.assertRaises(NotImplementedError) as context:
            self.iui.on_state_changed(self.new_state)
        self.assertEqual("This method is not implemented", str(context.exception))

    def test_on_event(self):
        with self.assertRaises(NotImplementedError) as context:
            self.iui.on_event(self.event)
        self.assertEqual("This method is not implemented", str(context.exception))
