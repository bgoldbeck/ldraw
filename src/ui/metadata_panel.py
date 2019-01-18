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


class MetadataPanel(wx.Panel):
    """This class contains the wx widgets for control over metadata information in the
    program. These widgets may include, but not limited to author, license, stl file input,
    and ldraw file output.
    """

    text_ctrl_size = (400, 20)
    max_path_length = 256
    big_button = (120, 25)
    small_button_size = (30, 25)

    def __init__(self, parent):
        """Default constructor for MainPanel class.
        """
        wx.Panel.__init__(self, parent, size=(1024, 100))
        self.parent = parent
        self.SetBackgroundColour("#777777")
        self._build_gui()
        self.parent.Layout()

    def _build_gui(self):
        """Initializing input, output, process control, and log panel elements
        :return:
        """
        label_size = (150, 25)

        # Input
        path_name_static_text = wx.StaticText(self, label="Path to Input STL File", size=label_size, style=wx.ALIGN_RIGHT)

        stl_path_name_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        stl_path_name_text.SetMaxLength(self.max_path_length)

        browse_stl_button = wx.Button(self, label="Browse STL", size=self.big_button)
        self.Bind(wx.EVT_BUTTON, self.browse_file, browse_stl_button)

        help_button = wx.Button(self, label="?", size=self.small_button_size)
        self.Bind(wx.EVT_BUTTON, self.help, help_button)

        about_button = wx.Button(self, label="i", size=self.small_button_size)
        self.Bind(wx.EVT_BUTTON, self.about, about_button)

        # Output path/selection
        path_part_static_text = wx.StaticText(self, label="Part Name", size=label_size, style=wx.ALIGN_RIGHT)
        ldraw_name_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        ldraw_name_text.SetMaxLength(self.max_path_length)

        browse_output_button = wx.Button(self, label="Browse Output", size=self.big_button)
        self.Bind(wx.EVT_BUTTON, self.browse_output, browse_output_button)

        # Author
        author_static_text = wx.StaticText(self, label="Author", size=label_size, style=wx.ALIGN_RIGHT)
        author_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        author_text.SetMaxLength(self.max_path_length)

        # License information.
        license_static_text = wx.StaticText(self, label="License", size=label_size, style=wx.ALIGN_RIGHT)
        license_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        license_text.SetMaxLength(self.max_path_length)

        vertical_layout = wx.BoxSizer(wx.VERTICAL)

        horizontal_split = wx.BoxSizer(wx.HORIZONTAL)

        # Input stl file and help and about
        horizontal_input = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_output = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_author = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_license = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_input.Add(path_name_static_text, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(stl_path_name_text, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(browse_stl_button, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(help_button, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(about_button, 0, wx.ALIGN_CENTER)

        horizontal_output.Add(path_part_static_text, 0, wx.ALIGN_LEFT)
        horizontal_output.AddSpacer(5)
        horizontal_output.Add(ldraw_name_text, 0, wx.ALIGN_LEFT)
        horizontal_output.AddSpacer(5)
        horizontal_output.Add(browse_output_button, 0, wx.ALIGN_LEFT)

        horizontal_author.Add(author_static_text, 0, wx.ALIGN_LEFT)
        horizontal_author.AddSpacer(5)
        horizontal_author.Add(author_text, 0, wx.ALIGN_LEFT)

        horizontal_license.Add(license_static_text, 0, wx.ALIGN_LEFT)
        horizontal_license.AddSpacer(5)
        horizontal_license.Add(license_text, 0, wx.ALIGN_LEFT)

        vertical_layout.Add(horizontal_input, 0, wx.ALIGN_LEFT)
        vertical_layout.Add(horizontal_output, 0, wx.ALIGN_LEFT)
        vertical_layout.Add(horizontal_author, 0, wx.ALIGN_LEFT)
        vertical_layout.Add(horizontal_license, 0, wx.ALIGN_LEFT)

        #horizontal_split.Add(dummy_panel, 0, wx.ALIGN_LEFT)
        horizontal_split.AddSpacer(150)
        horizontal_split.Add(vertical_layout, 0, wx.ALIGN_LEFT)

        self.SetSizer(horizontal_split)

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

    def browse_output(self, event):
        """

        :param event:
        :return:
        """
        pass