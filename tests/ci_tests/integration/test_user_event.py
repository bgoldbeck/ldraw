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


class UserEventTest(unittest.TestCase):
    """Test cases for the user event.
    """

    def test_constructor_user_event(self):
        """Test the constructor builds the correct user event.

        :return: None
        """
        event_type = UserEventType.INPUT_MODEL_READY
        log_type = LogType.ERROR
        log_message = "test user event"

        user_event = UserEvent(event_type, LogMessage(log_type, log_message))

        self.assertTrue(user_event.get_event_type(), event_type)
        self.assertTrue(user_event.log_message.get_message_type(), log_type)
        self.assertTrue(user_event.log_message.get_message(), log_message)

        # The log message color for ERROR should return full Red intensity. [255, 0, 0]
        self.assertTrue(user_event.get_log_message().get_log_message_color(), [255, 0, 0])
