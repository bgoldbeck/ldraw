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
from src.ui.opengl_canvas import OpenGLCanvas
import os
import sys
from numpy import *
from src.ui.log_panel import LogPanel
from src.ui.conversion_panel import ConversionPanel
from src.ui.metadata_panel import MetadataPanel


class MainPanel(wx.Panel):
    max_path_length = 256
    small_button_size = (30, 30)
    big_button = (100, 30)
    text_size = (100, 30)
    text_ctrl_size = (400, 20)
    #output_log_size = (800, 120)

    """The child of the MainFrame. This panel will hold the main applications remaining controls.
    """

    def __init__(self, parent):
        """Default constructor for MainPanel class."""
        wx.Panel.__init__(self, parent, size=(1024, 640))
        self.parent = parent
        self.opengl_canvas = None
        self.log_panel = None
        self.metadata_panel = None
        self.conversion_panel = None

        self.SetBackgroundColour("#666666")

        self._build_gui()
        self.parent.Layout()

    def _build_gui(self):
        """Initializing input, output, process control, and log panel elements
        :return: None
        """

        # Create the OpenGL canvas to render our 3D objects within.
        vertical_layout = wx.BoxSizer(wx.VERTICAL)

        self.metadata_panel = MetadataPanel(self)
        self.opengl_canvas = OpenGLCanvas(self)
        self.conversion_panel = ConversionPanel(self)
        self.log_panel = LogPanel(self)

        vertical_layout.Add(self.metadata_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vertical_layout.Add(self.opengl_canvas, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vertical_layout.Add(self.conversion_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vertical_layout.Add(self.log_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(vertical_layout)

