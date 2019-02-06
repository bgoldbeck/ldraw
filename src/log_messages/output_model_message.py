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
from src.model_conversion.ldraw_model import LDrawModel


class OutputModelMessage(LogMessage):
    """Log message for storing LDraw model data.
    """
    def __init__(self, message_type: LogType, message: str, model: LDrawModel):
        """Constructor for the OutputModelMessage class.
        """
        LogMessage.__init__(self, message_type, message)
        self.model = model

    def get_model(self):
        """Get the model data.

        :return: The model data as a Mesh object
        """
        return self.model


