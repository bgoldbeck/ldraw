# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import wx
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.user_event_type import UserEventType
from src.ui.iui_behavior import IUIBehavior


class LogPanel(wx.Panel, IUIBehavior):
    """This panel controls the behavior for the output log panel that will display
    running information to the user about the programs progress while running
    various algorithms.
    """
    big_button = (70, 25)
    output_log_size = (920, 165)
    panel_size = (1022, 500)
    _log_file_path = "log.txt"

    def __init__(self, parent):
        """Default constructor for MainPanel class.

        :param parent: The parent wx object for this panel.
        """
        wx.Panel.__init__(self, parent, size=self.panel_size, style=wx.BORDER_SUNKEN)
        self.parent = parent
        self.save_log_button = None
        self.log = None
        self._build_gui()

    def _build_gui(self):
        """Create the necessary wx objects for the functional purposes of this output
        log panel.

        :return: None
        """
        # Build the wx control objects.
        self.SetBackgroundColour("#eee111")
        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.TE_RICH

        self.save_log_button = wx.Button(self, label="Save Log", size=self.big_button)
        self.log = wx.TextCtrl(self, wx.ID_ANY, size=self.output_log_size, style=style)
        self.Bind(wx.EVT_BUTTON, self.save_log, self.save_log_button)

        # Build the layout.
        horizontal_layout = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_layout.Add(self.log, 0, flag=wx.ALIGN_LEFT)
        horizontal_layout.AddSpacer(5)
        horizontal_layout.Add(self.save_log_button, 0, wx.ALIGN_RIGHT)

        self.SetSizer(horizontal_layout)
        self.Show()

    def save_log(self, event):
        """Save the feedback log to a file.

        :param event: The event that was called.
        :return: None
        """
        pass

    def display_log(self, event, message):
        """Print a message to the log.

        :param event:
        :param message:
        :return:
        """
        # Check message!
        # Color message appropriately!
        self.log.AppendText(message)

    def clear_log(self, event):
        """Clears the log.

        :param event:
        :return:
        """

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the LogPanel.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        if new_state == ApplicationState.STARTUP:
            self.save_log_button.Disable()

    def on_event(self, event: UserEvent):
        """A user event was passed to the LogPanel.

        :param event: The recorded UserEvent.
        :return: None
        """
        pass
