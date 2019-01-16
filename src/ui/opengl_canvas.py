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
from wx import glcanvas
from OpenGL.GL import *


class OpenGLCanvas(glcanvas.GLCanvas):
    """This is the canvas for OpenGL to render objects to.
    """
    size = (600, 300)

    def __init__(self, parent):
        """Default constructor for MainPanel class.
        """
        self.parent = parent
        self.context = None
        self.init = False
        self.aspect_ratio = self.size[0] / self.size[1]

        # Call the base constructor for the OpenGL canvas.
        glcanvas.GLCanvas.__init__(self, parent, -1, size=self.size)#,
                                   #pos=wx.Point(125, 100))

        # Bind events to functions.
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_resize(self, event):
        """Event that occurs when resize is detected.
        :param event: the event that occurred.
        :return: None
        """
        size = self.GetClientSize()
        glViewport(0, 0, size.width, size.height)

    def on_paint(self, event):
        """Event that occurs when the canvas paint event is called.
        :param event: the event that occurred.
        :return: None
        """
        wx.PaintDC(self)
        if not self.init:
            self.init_gl()
            self.init = True
        self.draw()

    def init_gl(self):
        """Initialize OpenGL functionality.
        :return: None
        """
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        glClearColor(0.1, 0.15, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)

    def draw(self):
        """Draw the previous OpenGL buffer with all the 3D data.
        :return: None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.SwapBuffers()
