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
import time
from src.ui.ui_driver import UIDriver


class UIEventLoop(wx.GUIEventLoop):
    """This code is refernced from the demo on github.
    https://github.com/wxWidgets/Phoenix/blob/master/samples/mainloop/mainloop.py
    """
    def __init__(self):
        wx.GUIEventLoop.__init__(self)
        self.exitCode = 0
        self.shouldExit = False
        self.last = time.time()

    def update(self):
        # Do whatever you want to have done for each iteration of the event
        # loop. In this example we'll just sleep a bit to simulate something
        # real happening.
        current = time.time()
        if current - self.last >= 0.00833333334:
            UIDriver.update(current - self.last)
            self.last = current

    def Run(self):
        # Set this loop as the active one. It will automatically reset to the
        # original evtloop when the context manager exits.
        with wx.EventLoopActivator(self):
            while True:

                self.update()

                # Generate and process idles events for as long as there
                # isn't anything else to do
                while not self.shouldExit and not self.Pending() and self.ProcessIdle():
                    pass

                if self.shouldExit:
                    break

                # dispatch all the pending events and call Dispatch() to wait
                # for the next message
                if not self.ProcessEvents():
                    break

                # Currently on wxOSX Pending always returns true, so the
                # ProcessIdle above is not ever called. Call it here instead.
                if 'wxOSX' in wx.PlatformInfo:
                    self.ProcessIdle()

            # Process remaining queued messages, if any
            while True:
                checkAgain = False
                if wx.GetApp() and wx.GetApp().HasPendingEvents():
                    wx.GetApp().ProcessPendingEvents()
                    checkAgain = True
                if 'wxOSX' not in wx.PlatformInfo and self.Pending():
                    self.Dispatch()
                    checkAgain = True
                if not checkAgain:
                    break

        return self.exitCode

    def Exit(self, rc=0):
        self.exitCode = rc
        self.shouldExit = True
        self.OnExit()
        self.WakeUp()

    def ProcessEvents(self):
        if wx.GetApp():
            wx.GetApp().ProcessPendingEvents()

        if self.shouldExit:
            return False

        return self.Dispatch()
