# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
from src.ui.user_event_type import UserEventType
from src.log_messages.log_message import LogMessage


class UserEvent:
    """The class that contains a UI event with event type and log message.
    """

    def __init__(self, event_type: UserEventType, log_message: LogMessage):
        """Constructor for UserEvent.

        :param event_type: The UserEventType to store.
        :param log_message: The LogMessage to store.
        """
        self.event_type = event_type
        self.log_message = log_message

    def get_event_type(self):
        """Get the user event type stored with this user event.

        :return: The UserEventType stored in this user event.
        """
        return self.event_type

    def get_log_message(self):
        """Get the log message stored with this user event.

        :return: The LogMessage stored in this user event.
        """
        return self.log_message
