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


class LogPanel(wx.Panel):
    big_button = (100, 30)
    output_log_size = (800, 120)

    def __init__(self, parent):
        """Default constructor for MainPanel class."""
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.SetBackgroundColour("#777777")
        self.gui()
        self.parent.Layout()

    def gui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        save_log_button = wx.Button(self, label="Save Log", pos=(750, 150), size=self.big_button)
        self.Bind(wx.EVT_BUTTON, self.save_log, save_log_button)
        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.TE_RICH
        self.log = wx.TextCtrl(self, wx.ID_ANY, size=self.output_log_size, style=style)
        vbox.Add(save_log_button, 0, wx.ALIGN_RIGHT)
        vbox.Add(self.log, 0, wx.ALIGN_CENTER)
        self.SetSizer(vbox)

    def save_log(self, event):
        """Save the feedback log to a file.

        :param event:
        :return:
        """
        pass
