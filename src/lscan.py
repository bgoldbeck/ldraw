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
from src.ui.ui_driver import UIDriver
from src.ui.main_frame import MainFrame
from src.ui.ui_event_loop import UIEventLoop


class LScan(wx.App):
    """The main application driver class module.
    """
    ui_driver = None

    def __init__(self):
        """Default constructor for LScan class.
        """
        wx.App.__init__(self)
        self.main_loop = None
        root_frame = MainFrame()
        root_frame.Show()

        self.ui_driver = UIDriver(root_frame)

    def MainLoop(self):
        self.SetExitOnFrameDelete(True)
        self.main_loop = UIEventLoop()
        self.main_loop.Run()

    def ExitMainLoop(self):
        self.main_loop.Exit()

    def OnInit(self):
        """Called by WxPython on startup.

        :return: bool -- true, if the initializing was successful.
        """
        return True


# Call the main application loop.
if __name__ == "__main__":
    app = LScan()
    app.MainLoop()
