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
from src.ui.ui_style import UIStyle


class Popup(wx.Frame):
    """Popup window that displays text. Can only be closed and moved.
    """
    def __init__(self, parent, title, msg):
        super(Popup, self).__init__(parent, title=title, style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE & ~(wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.SetBackgroundColour(UIStyle.metadata_background_color)
        panel = wx.Panel(self)
        st = wx.StaticText(panel, -1, msg, pos=(10, 10))
        st.SetForegroundColour(UIStyle.metadata_input_text_color)
        sz = st.GetBestSize()
        self.SetSize((sz.width + 60, sz.height + 60))
        panel.SetSize((sz.width + 60, sz.height + 60))

        win_rect = parent.GetTopLevelParent().GetRect()
        popup_size = self.GetSize()
        center = (int(win_rect[2] / 2 + win_rect[0] - popup_size[0] / 2),
                  int(win_rect[3] / 2 + win_rect[1] - popup_size[1] / 2))

        self.SetPosition(center)
        wx.CallAfter(self.Refresh)
