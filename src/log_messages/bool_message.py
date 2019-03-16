# Copyright (C) 2018
# This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License.
# See LICENSE file for the full text.
from src.log_messages.log_message import LogMessage
from src.log_messages.log_type import LogType


class BoolMessage(LogMessage):
    """Log message for storing bool data.
    """
    def __init__(self, message_type: LogType, message: str, value: bool):
        """Constructor for the FloatMessage class.

        :param message_type: The LogType for the message.
        :param message: The str message contained in the LogMessage.
        :param value: The bool value that is contained.
        """
        LogMessage.__init__(self, message_type, message)
        self.value = value

    def get_bool(self):
        """Get the bool value.

        :return: The bool data stored in the LogMessage
        """
        return self.value


