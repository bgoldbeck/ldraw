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


class MainPanel(wx.Panel):
    max_path_length = 256
    small_button_size = (30, 30)
    big_button = (100, 30)
    text_size = (100, 30)
    text_ctrl_size = (400, 20)
    output_log_size = (800, 120)

    """The child of the MainFrame. This panel will hold the main applications remaining controls.
    """

    def __init__(self, parent):
        """Default constructor for MainPanel class."""
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.SetBackgroundColour("#777777")

        # Create the OpenGL canvas to render our 3D objects within.
        self.canvas = OpenGLCanvas(self)
        self.gui()
        self.parent.Layout()

    def gui(self):
        """Initializing input, output, process control, and log panel elements
        :return:
        """

        vbox = wx.BoxSizer(wx.VERTICAL)
        # input stl file
        hbox_input = wx.BoxSizer(wx.HORIZONTAL)

        # metadata
        hbox_output = wx.BoxSizer(wx.HORIZONTAL)
        hbox_author = wx.BoxSizer(wx.HORIZONTAL)
        hbox_license = wx.BoxSizer(wx.HORIZONTAL)
        # process control
        hbox_procctrl = wx.BoxSizer(wx.HORIZONTAL)

        # opengl viewport
        hbox_opengl = wx.BoxSizer(wx.HORIZONTAL)
        hbox_opengl.Add(self.canvas, 0, wx.ALIGN_CENTER)

        # input
        path_name_static_text = wx.StaticText(self, label="Path to Input STL File")
        hbox_input.Add(path_name_static_text, 0, wx.ALIGN_CENTER)

        path_name_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        hbox_input.Add(path_name_text, 0, wx.ALIGN_CENTER)
        path_name_text.SetMaxLength(self.max_path_length)

        browse_stl_button = wx.Button(self, label="Browse STL", size=self.big_button)
        hbox_input.Add(browse_stl_button, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.browse_file, browse_stl_button)

        help_button = wx.Button(self, label="?", size=self.small_button_size)
        hbox_input.Add(help_button, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.help, help_button)

        about_button = wx.Button(self, label="i", size=self.small_button_size)
        hbox_input.Add(about_button, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.about, about_button)

        # output path/selection
        path_part_static_text = wx.StaticText(self, label="Part Name")
        hbox_output.Add(path_part_static_text, 0, wx.ALIGN_CENTER)
        part_name_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        hbox_output.Add(part_name_text, 0, wx.ALIGN_CENTER)
        part_name_text.SetMaxLength(self.max_path_length)

        browse_output_button = wx.Button(self, label="Browse Output", size=self.big_button)
        hbox_output.Add(browse_output_button, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.browse_output, browse_output_button)

        # author
        author_static_text = wx.StaticText(self, label="Author")
        hbox_author.Add(author_static_text, 0, wx.ALIGN_CENTER)
        author_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        hbox_author.Add(author_text, 0, wx.ALIGN_CENTER)
        author_text.SetMaxLength(self.max_path_length)

        # license
        license_static_text = wx.StaticText(self, label="License")
        hbox_license.Add(license_static_text, 0, wx.ALIGN_CENTER)
        license_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        hbox_license.Add(license_text, 0, wx.ALIGN_CENTER)
        license_text.SetMaxLength(self.max_path_length)

        # process control
        convert_button = wx.Button(self, label="Convert to LDraw", size=self.big_button)
        hbox_procctrl.Add(convert_button, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.convert, convert_button)

        pause_button = wx.Button(self, label="Pause/Continue", size=self.big_button)
        hbox_procctrl.Add(pause_button, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.pause, pause_button)
        pause_button.Disable()

        cancel_button = wx.Button(self, label="Cancel", size=self.big_button)
        hbox_procctrl.Add(cancel_button, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.cancel, cancel_button)
        cancel_button.Disable()

        save_button = wx.Button(self, label="Save Conversion", size=self.big_button)
        hbox_procctrl.Add(save_button, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.save, save_button)
        save_button.Disable()

        save_log_button = wx.Button(self, label="Save Log", pos=(750, 150), size=self.big_button)
        self.Bind(wx.EVT_BUTTON, self.save_log, save_log_button)
        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.TE_RICH
        self.log = wx.TextCtrl(self, wx.ID_ANY, size=self.output_log_size, style=style)

        vbox.Add(hbox_input, 0, wx.ALIGN_CENTER)
        vbox.Add(hbox_output, 0, wx.ALIGN_CENTER)
        vbox.Add(hbox_author, 0, wx.ALIGN_CENTER)
        vbox.Add(hbox_license, 0, wx.ALIGN_CENTER)
        vbox.Add(hbox_procctrl, 0, wx.ALIGN_CENTER)
        vbox.Add(hbox_opengl, 0, wx.ALIGN_CENTER)
        vbox.Add(save_log_button, 0, wx.ALIGN_RIGHT)
        vbox.Add(self.log, 0, wx.ALIGN_CENTER)
        self.SetSizer(vbox)

    def help(self, event):
        """Presents program limitations, common troubleshooting steps, and steps to update LDraw parts library.
        :param event:
        :return:
        """
        wx.MessageBox("""
            Program Limitations
            TEXT
            Troubleshooting
            TEXT
            How to update LDraw Parts Library
            TEXT""", "Help info", wx.OK | wx.ICON_QUESTION)

    def about(self, event):
        """Presents program name, program version, copyright information, licensing information, and authors to user.
        :param event:
        :return:
        """
        wx.MessageBox("""
            LScan
            Version 1.0
            Copyright (C) 2018 - This notice is to be included in all relevant source files.
            
            This software is licensed under the MIT License. See LICENSE file for the full text.

            Authors
            "Brandon Goldbeck" <bpg@pdx.edu>
            “Anthony Namba” <anamba@pdx.edu>
            “Brandon Le” <lebran@pdx.edu>
            “Ann Peake” <peakean@pdx.edu>
            “Sohan Tamang” <sohan@pdx.edu>
            “An Huynh” <an35@pdx.edu>
            “Theron Anderson” <atheron@pdx.edu>""", "About LScan", wx.OK | wx.ICON_INFORMATION)

    def browse_file(self, event):
        """Browse for a valid STL input file.
        :param event:
        :return:
        """
        pass

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


    def save_log(self, event):
        """Save the feedback log to a file.

        :param event:
        :return:
        """
        pass

    def browse_output(self, event):
        """

        :param event:
        :return:
        """
        pass
