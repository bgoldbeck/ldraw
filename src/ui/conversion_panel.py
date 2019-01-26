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
from src.ui.iui_behavior import IUIBehavior
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.user_event_type import UserEventType


class ConversionPanel(wx.Panel, IUIBehavior):
    """Holds wx controls relevant to controlling the program behavior for starting, stopping,
    pausing, and canceling the conversion process.
    """
    big_button_size = (120, 30)

    def __init__(self, parent):
        """Default constructor for ConversionPanel class.

        :param parent: The parent wx object for this panel.
        """
        wx.Panel.__init__(self, parent, size=(1024, 30), style=wx.SIMPLE_BORDER)
        self.parent = parent
        self.convert_button = None
        self.pause_button = None
        self.cancel_button = None
        self.save_button = None
        self._build_gui()

    def _build_gui(self):
        """Initializing wx objects that make up this conversion panel and their layout within.

        :return: None
        """
        self.SetBackgroundColour("#456eab")

        # Create the wx controls for this conversion panel.
        self.convert_button = wx.Button(self, label="Convert to LDraw", size=self.big_button_size)
        self.pause_button = wx.Button(self, label="Pause/Continue", size=self.big_button_size)
        self.cancel_button = wx.Button(self, label="Cancel", size=self.big_button_size)
        self.save_button = wx.Button(self, label="Save Conversion", size=self.big_button_size)

        # Create the layout.
        horizontal_layout = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_layout.Add(self.save_button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        horizontal_layout.AddSpacer(5)
        horizontal_layout.Add(self.cancel_button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        horizontal_layout.AddSpacer(5)
        horizontal_layout.Add(self.pause_button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        horizontal_layout.AddSpacer(5)
        horizontal_layout.Add(self.convert_button, 0, wx.ALIGN_CENTER_HORIZONTAL)

        vertical_layout = wx.BoxSizer(wx.VERTICAL)
        vertical_layout.Add(horizontal_layout, 0, wx.ALIGN_CENTER)

        self.SetSizer(vertical_layout)

        # Bind the events for each wx control.
        self.Bind(wx.EVT_BUTTON, self.convert, self.convert_button)
        self.Bind(wx.EVT_BUTTON, self.pause, self.pause_button)
        self.Bind(wx.EVT_BUTTON, self.cancel, self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.save, self.save_button)

    def convert(self, event):
        """Convert the selected STL file into an LDraw file.
        :param event:
        :return:
        """
        pass

    def pause(self, e):
        """Pause the conversion process.
        :param e:
        :return:
        """
        pass

    def resume(self, event):
        """Continue/resume the conversion process again.
        :param event:
        :return:
        """
        pass

    def cancel(self, event):
        """Cancel the conversion operation.
        :param event:
        :return:
        """
        pass

    def save(self, event):
        """Save the finalized conversion of the input file. Hide main window options and replace them with metadata
        options. Once the user finalizes their metadata options (back or save), they return to the original options.
        :param event:
        :return:
        """
        pass

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the ConversionPanel.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        if new_state == ApplicationState.STARTUP:
            self.save_button.Disable()
            self.cancel_button.Disable()
            self.pause_button.Disable()
            self.convert_button.Disable()
        elif new_state == ApplicationState.WAITING_GO:
            self.convert_button.Enable()

    def on_event(self, event: UserEvent):
        """A user event was passed to the ConversionPanel.

        :param event: The recorded UserEvent.
        :return: None
        """
        pass
