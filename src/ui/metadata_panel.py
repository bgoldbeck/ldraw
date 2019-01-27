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
from src.ui.iui_behavior import IUIBehavior
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.user_event_type import UserEventType
from src.ui.ui_driver import UIDriver


class MetadataPanel(wx.Panel, IUIBehavior):
    """This class contains the wx widgets for control over metadata information in the
    program. These widgets may include, but not limited to author, license, stl file input,
    and ldraw file output.
    """
    text_ctrl_size = (400, 20)
    max_path_length = 256
    big_button = (120, 25)
    small_button_size = (30, 25)
    panel_size = (1024, 100)
    label_size = (150, 25)

    def __init__(self, parent):
        """Default constructor for MainPanel class.
        """
        wx.Panel.__init__(self, parent, size=self.panel_size, style=wx.BORDER_SUNKEN)
        self.parent = parent
        self.browse_stl_button = None
        self.help_button = None
        self.about_button = None
        self.browse_stl_button = None
        self.author_input = None
        self.license_input = None
        self.stl_path_input = None
        self.stl_path_text = None
        self.stl_path_isvalid = False
        self.ldraw_name_input = None
        self.ldraw_name_text = None
        self.ldraw_name_isvalid = False
        self._build_gui()
        self.parent.Layout()

    def _build_gui(self):
        """Initializing input, output, process control, and log panel elements
        :return:
        """
        self.SetBackgroundColour("#777fea")

        # Input
        path_name_static_text = wx.StaticText(
            self,
            label="Path to Input STL File",
            size=self.label_size,
            style=wx.ALIGN_RIGHT)

        # Stl input.
        self.stl_path_input = wx.TextCtrl(self, size=self.text_ctrl_size)
        self.stl_path_input.SetMaxLength(self.max_path_length)

        self.browse_stl_button = wx.Button(self, label="Browse STL", size=self.big_button)

        # Help / About.
        self.help_button = wx.Button(self, label="?", size=self.small_button_size)
        self.about_button = wx.Button(self, label="i", size=self.small_button_size)

        # Output path selection.
        path_part_static_text = wx.StaticText(self, label="Part Name", size=self.label_size, style=wx.ALIGN_RIGHT)
        self.ldraw_name_input = wx.TextCtrl(self, size=self.text_ctrl_size)
        self.ldraw_name_input.SetMaxLength(self.max_path_length)

        self.browse_output_button = wx.Button(self, label="Browse Output", size=self.big_button)

        # Author
        author_static_text = wx.StaticText(self, label="Author", size=self.label_size, style=wx.ALIGN_RIGHT)
        self.author_input = wx.TextCtrl(self, size=self.text_ctrl_size)
        self.author_input.SetMaxLength(self.max_path_length)

        # License information.
        license_static_text = wx.StaticText(self, label="License", size=self.label_size, style=wx.ALIGN_RIGHT)
        self.license_input = wx.TextCtrl(self, size=self.text_ctrl_size)
        self.license_input.SetMaxLength(self.max_path_length)

        # Create the layout.
        horizontal_input = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_output = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_author = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_license = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_input.Add(path_name_static_text, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(self.stl_path_input, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(self.browse_stl_button, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(self.help_button, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(self.about_button, 0, wx.ALIGN_CENTER)

        horizontal_output.Add(path_part_static_text, 0, wx.ALIGN_LEFT)
        horizontal_output.AddSpacer(5)
        horizontal_output.Add(self.ldraw_name_input, 0, wx.ALIGN_LEFT)
        horizontal_output.AddSpacer(5)
        horizontal_output.Add(self.browse_output_button, 0, wx.ALIGN_LEFT)

        horizontal_author.Add(author_static_text, 0, wx.ALIGN_LEFT)
        horizontal_author.AddSpacer(5)
        horizontal_author.Add(self.author_input, 0, wx.ALIGN_LEFT)

        horizontal_license.Add(license_static_text, 0, wx.ALIGN_LEFT)
        horizontal_license.AddSpacer(5)
        horizontal_license.Add(self.license_input, 0, wx.ALIGN_LEFT)

        vertical_layout = wx.BoxSizer(wx.VERTICAL)
        vertical_layout.Add(horizontal_input, 0, wx.ALIGN_LEFT)
        vertical_layout.Add(horizontal_output, 0, wx.ALIGN_LEFT)
        vertical_layout.Add(horizontal_author, 0, wx.ALIGN_LEFT)
        vertical_layout.Add(horizontal_license, 0, wx.ALIGN_LEFT)

        horizontal_split = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_split.AddSpacer(150)
        horizontal_split.Add(vertical_layout, 0, wx.ALIGN_LEFT)

        self.SetSizer(horizontal_split)

        # Register events.
        self.Bind(wx.EVT_BUTTON, self.about, self.about_button)
        self.Bind(wx.EVT_BUTTON, self.browse_output, self.browse_output_button)
        self.Bind(wx.EVT_BUTTON, self.help, self.help_button)
        self.Bind(wx.EVT_BUTTON, self.browse_file, self.browse_stl_button)

        # Bind input field change events
        self.stl_path_input.Bind(wx.EVT_KILL_FOCUS, self.check_input)
        self.ldraw_name_input.Bind(wx.EVT_KILL_FOCUS, self.check_input)


    def check_input(self, event):
        """Checks if stl input field has changed since last check. If it has
        changed, input is checked for validity and program state may be changed.
        :param event:
        :return:
        """
        current_stl = self.stl_path_input.GetValue()
        if (current_stl != self.stl_path_text):
            self.stl_path_text = current_stl
            self.stl_path_isvalid = self.stl_input_isvalid(current_stl)

        current_ldraw = self.ldraw_name_input.GetValue()
        if (current_ldraw != self.ldraw_name_text):
            self.ldraw_name_text = current_ldraw
            self.ldraw_name_isvalid = self.ldraw_input_isvalid(current_ldraw)

        if (self.ldraw_name_isvalid and self.stl_path_isvalid):
            if(UIDriver.application_state != ApplicationState.WAITING_GO):
                UIDriver.change_application_state(ApplicationState.WAITING_GO)
                #save settings here
                #clear log
        else:
            if(UIDriver.application_state != ApplicationState.WAITING_INPUT):
                UIDriver.change_application_state(
                    ApplicationState.WAITING_INPUT)
                #log errors
        event.Skip()

    def stl_input_isvalid(self, input):
        """Checks if input stl is a valid path.
        :param input: The input path
        :return: Boolean if valid or not
        """

        # ONLY CHECKS FOR LENGTH, put in actual validation check here
        return len(input) > 0

    def ldraw_input_isvalid(self, input):
        """Checks if ldraw name is a valid path.
        :param input: The input path
        :return: Boolean if valid or not
        """

        # ONLY CHECKS FOR LENGTH, put in actual validation check here
        return len(input) > 0

    def help(self, event):
        """Presents program limitations, common troubleshooting steps, and steps to update LDraw parts library.
        :param event:
        :return:
        """
        help_text = UIDriver.get_assets_file_text("HELP.txt")
        if help_text is not None:
            wx.MessageBox(help_text, "Help", wx.OK | wx.ICON_QUESTION)
        else:
            wx.MessageBox("Could not read help text file, sorry.", "Error", wx.OK | wx.ICON_INFORMATION)

    def about(self, event):
        """Presents program name, program version, copyright information, licensing information, and authors to user.
        :param event:
        :return:
        """
        about_text = UIDriver.get_assets_file_text("ABOUT.txt")
        if about_text is not None:
            wx.MessageBox(about_text, "About LScan", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Could not read about text file, sorry.", "Error", wx.OK | wx.ICON_INFORMATION)

    def browse_file(self, event):
        """Browse for a valid STL input file.
        :param event:
        :return:
        """
        pass

    def browse_output(self, event):
        """Browse for a valid DAT output file location.

        :param event:
        :return:
        """
        pass

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the MetadataPanel.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        if new_state == ApplicationState.STARTUP:
            self.stl_path_input.Enable()
            self.ldraw_name_input.Enable()
        elif new_state == ApplicationState.WAITING_GO:
            self.stl_path_input.Enable()
            self.ldraw_name_input.Enable()
        elif new_state == ApplicationState.WORKING:
            self.stl_path_input.Disable()
            self.ldraw_name_input.Disable()

    def on_event(self, event: UserEvent):
        """A user event was passed to the MetadataPanel.

        :param event: The recorded UserEvent.
        :return: None
        """
        pass
