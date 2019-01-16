# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.


class LogMessage:
    """

    """

    def __init__(self, msg_type, timestamp, message):
        """

        :param msg_type:
        :param timestamp:
        :param message:
        """
        self.msg_type = msg_type
        self.timestamp = timestamp
        self.message = message

    def get_message_type(self):
        """

        :return:
        """
        return self.msg_type

    def get_message(self):
        """

        :return:
        """
        return self.message

    def get_timestamp(self):
        """

        :return:
        """
        return self.timestamp

