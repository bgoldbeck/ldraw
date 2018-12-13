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


class MainPanel(wx.Panel):

    """The child of the MainFrame. This panel will hold the main applications
    remaining controls.
    """
    def __init__(self, parent):
        """Default constructor for MainPanel class.
        """
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.SetBackgroundColour("#777777")

        # Create the OpenGL canvas to render our 3D objects within.
        self.canvas = OpenGLCanvas(self)

        self.parent.Layout()
