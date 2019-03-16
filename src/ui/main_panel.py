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
from src.ui.log_panel import LogPanel
from src.ui.conversion_panel import ConversionPanel
from src.ui.opengl_panel import OpenGLPanel
from src.ui.metadata_panel import MetadataPanel
from src.ui.iui_behavior import IUIBehavior
from src.ui.application_state import ApplicationState
from src.ui.ui_style import UIStyle
from src.threading.thread_manager import UserEvent


class MainPanel(wx.Panel, IUIBehavior):
    """The child of the MainFrame. This panel will hold the main applications sub-panels.
    """

    def __init__(self, parent):
        """Default constructor for MainPanel class.

        :param parent: The parent wx object that will be the parent of this main panel.
        """
        wx.Panel.__init__(self, parent, size=parent.GetSize())
        self.parent = parent
        self.opengl_panel = None
        self.log_panel = None
        self.metadata_panel = None
        self.conversion_panel = None
        self._build_gui()

    def _build_gui(self):
        """Create all the sub-panels and their layout on this main panel.
        :return: None
        """
        self.SetBackgroundColour(UIStyle.main_panel_background_color)

        # Create the sub-panels
        self.metadata_panel = MetadataPanel(self)
        self.conversion_panel = ConversionPanel(self)
        self.log_panel = LogPanel(self)
        self.opengl_panel = OpenGLPanel(self)

        log_panel_height = UIStyle.log_panel_size[1]

        # Add more height to the log panel if OpenGL cannot be used.
        if not self.opengl_panel.can_use_opengl():
            log_panel_height += (UIStyle.opengl_panel_size[1] - 10)

        self.log_panel.resize_log_ctrl_height(log_panel_height)

        # Create the layout of the sub-panels.
        vertical_layout = wx.BoxSizer(wx.VERTICAL)
        vertical_layout.Add(self.metadata_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Don't add the OpenGL Panel if OpenGL is not supported.
        if self.opengl_panel.can_use_opengl():
            vertical_layout.Add(self.opengl_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        else:
            self.opengl_panel.Show(False)
            self.opengl_panel = None

        vertical_layout.Add(self.conversion_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vertical_layout.Add(self.log_panel, 0, wx.EXPAND)

        self.SetSizer(vertical_layout)

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the MainPanel.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        pass

    def on_event(self, event: UserEvent):
        """A user event was passed to the MainPanel.

        :param event: The recorded UserEvent.
        :return: None
        """
        pass

    def update(self, dt: float):
        """Called every loop by the GUIEventLoop

        :param dt: The delta time between the last call.
        :return: None
        """
        pass
