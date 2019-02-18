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
from src.ui.user_event import UserEvent
from src.ui.user_event_type import UserEventType
from src.log_messages.log_message import LogMessage
from src.log_messages.log_type import LogType


class TestLogPanel(unittest.TestCase):
    """Test cases for the user event.
    """

    def test_handle_log_message(self):
        """

        :return: 
        """

