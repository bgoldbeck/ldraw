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
from pathlib import Path
from sys import platform
import re

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

        self.stl_file = None
        self.out_file = None
        # Settings
        self.stl_dir = None
        self.part_name = None
        self.part_dir = None
        self.author = None
        self.license = None
        self.load_settings()

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
        self.Bind(wx.EVT_BUTTON, self.browse_input, self.browse_stl_button)

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
        if current_stl != self.stl_path_text:
            self.stl_path_text = current_stl
            self.stl_path_isvalid = self.stl_input_is_valid(current_stl)

        current_ldraw = self.ldraw_name_input.GetValue()
        if current_ldraw != self.ldraw_name_text:
            self.ldraw_name_text = current_ldraw
            self.ldraw_name_isvalid = self.ldraw_input_is_valid(current_ldraw)

        if self.ldraw_name_isvalid and self.stl_path_isvalid:
            if UIDriver.application_state != ApplicationState.WAITING_GO:
                UIDriver.change_application_state(ApplicationState.WAITING_GO)
                # Save settings here
                # Clear log
        else:
            if UIDriver.application_state != ApplicationState.WAITING_INPUT:
                UIDriver.change_application_state(
                    ApplicationState.WAITING_INPUT)
                # Log errors
        event.Skip()

    def stl_input_is_valid(self, input):
        """Checks if input stl is a valid path.
        :param input: The input path
        :return: Boolean if valid or not
        """

        # ONLY CHECKS FOR LENGTH, put in actual validation check here
        return len(input) > 0

    def ldraw_input_is_valid(self, input):
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

    def browse_input(self, event):
        """Browse for a valid STL input file.
        :param event:
        :return:
        """
        stl_wildcard = "*.stl"
        dialog = wx.FileDialog(self, "Choose a STL file", defaultDir="", wildcard=stl_wildcard, style=wx.FD_OPEN
                               | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            # Check for file existing
            # If valid, pass to worker thread who will check data
            self.stl_file = filename
        dialog.Destroy()

    def text_ctrl_input(self, event):
        """Get the path for STL input file from user typing into TextCtrl element.
        :param event:
        :return:
        """
        filepath = Path(self.stl_path_input.GetValue())
        # Check file path validity

        if filepath.is_file():
            if filepath != self.stl_file and filepath is not None:
                self.stl_file = str(filepath)
                self.save_settings()
        
        self.display_settings()
        event.Skip()

    def browse_output(self, event):
        """Browse for a valid output file path
        :param event:
        :return:
        """
        dialog = wx.FileDialog(self, "Choose a location for the LDraw file", defaultDir="",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            pathname = dialog.GetPath()
            self.part_name = pathname
            self.save_settings()
        dialog.Destroy()

    def text_ctrl_output(self, event):
        """Get file output path from user in TextCtrl element.
        :param event:
        :return:
        """
        # Detect if you need to use:
        # default directory and default part name
        # current default directory and new part name
        # new part directory and new part name

        output_path = self.ldraw_name_input.GetValue()

        if output_path is not None:
            full_output_path = Path(self.part_dir + output_path)

            # Only needs to be a filename like part.dat. Cannot be an entire filepath.

            # If there isn't an existing file with this name
            if not full_output_path.is_file():
                # Append the default parts directory to the path
                self.part_name = output_path
                self.out_file = full_output_path
                self.save_settings()

            # There exists a file in that path
            elif full_output_path.is_file():
                confirm = wx.MessageDialog(None, "A file already exists with that name. Overwrite?", wx.YES_NO)
                confirm_choice = confirm.ShowModal()

                # The user wants to overwrite the existing file
                if confirm_choice == wx.ID_YES:
                    self.part_name = output_path
                    self.out_file = full_output_path
                    self.save_settings()
                #elif confirm_choice == wx.ID_NO:
        
        self.display_settings()
        event.Skip()

    def text_ctrl_author(self, event):
        """Get the author value from the user and update the settings file as needed."""
        author = self.author_input.GetValue()

        # Update settings file author info
        if author != self.author and author != "":
            self.author = author
            self.save_settings()

        self.display_settings()
        event.Skip()

    def text_ctrl_license(self, event):
        """Get the license value from the user and update the settings file as needed."""
        license = self.license_input.GetValue()

        # Update settings file license info
        if license != self.license and license != "":
            self.license = license
            self.save_settings()

        self.display_settings()
        event.Skip()

    # States and events

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the MetadataPanel.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        if new_state == ApplicationState.WAITING_GO:
            self.stl_path_input.Enable()
            self.ldraw_name_input.Enable()
            self.author_input.Enable()
            self.license_input.Enable()
            self.about_button.Enable()
            self.browse_output_button.Enable()
            self.help_button.Enable()
            self.browse_stl_button.Enable()
        elif new_state == ApplicationState.WORKING:
            self.stl_path_input.Disable()
            self.ldraw_name_input.Disable()
            self.author_input.Disable()
            self.license_input.Disable()
            self.about_button.Disable()
            self.browse_output_button.Disable()
            self.help_button.Disable()
            self.browse_stl_button.Disable()

    def on_event(self, event: UserEvent):
        """A user event was passed to the MetadataPanel.

        :param event: The recorded UserEvent.
        :return: None
        """
        pass

    # Checks

    def check_good_path(self, str):
        """Returns True if the string doesn't contain invalid values."""
        # Windows
        #if platform == "win32":

        # Mac
        #if platform == "darwin":

        # Linux
        #if platform == "linux":
        pass

    # Settings

    def create_settings(self, name):
        """Generate initial settings file based on current working directory.
        """
        # default stl directory
        default_stl_dir = Path.cwd() / "assets/models/"
        # default part name
        default_part_name = "untitled.dat"
        # default part name directory
        default_part_dir = Path.cwd() / "assets/parts/"
        # default author
        default_author = "First Last "
        # default license
        default_license = "Redistributable under CCAL version 2.0 : see CAreadme.txt"

        default_settings = [default_stl_dir, default_part_name, default_part_dir, default_author, default_license]
        name = "assets/settings/" + name + ".txt"
        filepath = Path.cwd() / name

        try:
            with open(str(filepath), "w") as file:
                for setting in default_settings:
                    print(setting, file=file)
        except FileNotFoundError as ferr:
            print(ferr)

    def save_settings(self):
        """Save changes to user settings file.
        """
        # Determine changes to settings file
        # Write out changes to stl_dir, part_dir, author, license
        # default_part_name is always "untitled.dat"

        print("\n\nSave settings function\n\n")

        settings = [self.stl_dir, "untitled.dat", self.part_dir, self.author, self.license]
        filepath = Path.cwd() / "assets/settings/user_settings.txt"
        try:
            with open(str(filepath), "w") as file:
                print(settings)
                for setting in settings:
                    print(setting)
                    if setting is not None:
                        print(setting, file=file)

        except FileNotFoundError as ferr:
            print(ferr)

        self.display_settings()

    def load_settings(self):
        """Load settings values into memory on startup."""
        default_filepath = Path.cwd() / "assets/settings/default_user_settings.txt"
        filepath = Path.cwd() / "assets/settings/user_settings.txt"

        # If there isn't a default user settings file, create one and create a user settings file. The default is
        # is to remain the same. The user settings file will change.
        if not default_filepath.is_file():
            self.create_settings("default_user_settings")
            self.create_settings("user_settings")

        settings = [self.stl_dir, self.part_name, self.part_dir, self.author, self.license]
        with open(str(filepath), "r") as file:
            file_settings = file.readlines()
            """"
            for s, f in zip(settings, file_settings):
                s = f.rstrip()
                print("file " + f)
                print("settings " + s)
            """
            self.stl_dir = file_settings[0].rstrip()
            self.part_name = file_settings[1].rstrip()
            self.part_dir = file_settings[2].rstrip()
            self.author = file_settings[3].rstrip()
            self.license = file_settings[4].rstrip()

        self.display_settings()

    def display_settings(self):
        """Display all settings and stl file path to standard out."""
        print("\n\nDisplay settings\n")
        all_settings = [self.stl_file, self.stl_dir, self.part_name, self.part_dir, self.author, self.license]
        print(all_settings)
        for setting in all_settings:
            print(setting)

    # Getters

    def get_stl_file(self):
        """Return the string of the path to the input stl file."""
        return self.stl_file

    def get_stl_dir(self):
        """Return the string of the stl directory."""
        return self.stl_dir

    def get_dat_file(self):
        """Return the string of the path to the output dat file."""
        return self.part_name

    def get_part_dir(self):
        """Return the string of to the parts directory."""
        return self.part_dir

    def get_author(self):
        """Return the string of the author."""
        return self.author

    def get_license(self):
        """Return the string of the license."""
        return self.license
