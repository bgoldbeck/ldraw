# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent


class IUIBehavior:
    """The psuedo interface for some wx controls to also inherit method properties from.
    """

    def on_state_changed(self, new_state: ApplicationState):
        """
        :param new_state:
        :return:
        """
        raise NotImplementedError("This method is not implemented")

    def on_event(self, event: UserEvent):
        """
        :param event:
        :return:
        """
        raise NotImplementedError("This method is not implemented")

    def update(self, dt: float):
        """
        :param event:
        :return:
        """
        raise NotImplementedError("This method is not implemented")






