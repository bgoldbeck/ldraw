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


class ConversionPanel(wx.Panel):
    big_button = (100, 30)

    def __init__(self, parent):
        """Default constructor for MainPanel class."""
        wx.Panel.__init__(self, parent, size=(1024, 30), style=wx.SIMPLE_BORDER)
        self.parent = parent
        self.SetBackgroundColour("#444444")
        self._build_gui()
        self.parent.Layout()

    def _build_gui(self):
        """Initializing input, output, process control, and log panel elements
        :return:
        """
        vertical_layout = wx.BoxSizer(wx.VERTICAL)
        horizontal_layout = wx.BoxSizer(wx.HORIZONTAL)

        # process control
        convert_button = wx.Button(self, label="Convert to LDraw", size=self.big_button)
        self.Bind(wx.EVT_BUTTON, self.convert, convert_button)

        pause_button = wx.Button(self, label="Pause/Continue", size=self.big_button)
        self.Bind(wx.EVT_BUTTON, self.pause, pause_button)
        pause_button.Disable()

        cancel_button = wx.Button(self, label="Cancel", size=self.big_button)
        self.Bind(wx.EVT_BUTTON, self.cancel, cancel_button)
        cancel_button.Disable()

        save_button = wx.Button(self, label="Save Conversion", size=self.big_button)
        self.Bind(wx.EVT_BUTTON, self.save, save_button)
        save_button.Disable()

        horizontal_layout.Add(save_button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        horizontal_layout.Add(cancel_button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        horizontal_layout.Add(pause_button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        horizontal_layout.Add(convert_button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vertical_layout.Add(horizontal_layout, 0, wx.ALIGN_CENTER)

        self.SetSizer(vertical_layout)

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
