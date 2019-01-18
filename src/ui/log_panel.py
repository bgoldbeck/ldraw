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
    big_button = (100, 25)
    output_log_size = (870, 165)

    def __init__(self, parent):
        """Default constructor for MainPanel class."""
        wx.Panel.__init__(self, parent, size=parent.GetSize(), style=wx.SIMPLE_BORDER)
        self.parent = parent
        self.SetBackgroundColour("#777777")
        self._build_gui()
        self.parent.Layout()

    def _build_gui(self):
        """

        :return: None
        """
        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.TE_RICH
        self.log = wx.TextCtrl(self, wx.ID_ANY, size=self.output_log_size, style=style)

        save_log_button = wx.Button(self, label="Save Log", size=self.big_button)

        horizontal_layout = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_layout.Add(self.log, 0, wx.ALIGN_LEFT)
        horizontal_layout.AddSpacer(5)
        horizontal_layout.Add(save_log_button, 0, wx.ALIGN_LEFT)


        self.SetSizer(horizontal_layout)

        self.Bind(wx.EVT_BUTTON, self.save_log, save_log_button)

    def save_log(self, event):
        """Save the feedback log to a file.

        :param event:
        :return:
        """
        pass
