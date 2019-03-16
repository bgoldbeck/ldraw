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
import json
from src.ui.iui_behavior import IUIBehavior
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.user_event_type import UserEventType
from src.ui.ui_driver import UIDriver
from src.model_conversion.model_shipper import ModelShipper
from src.model_conversion.ldraw_model import LDrawModel
from src.log_messages.log_message import LogMessage
from src.log_messages.log_type import LogType
from src.ui.ui_style import UIStyle
from src.util import Util
from src.ui.popup import Popup
from src.ui.button import Button
from src.settings_manager import SettingsManager


class MetadataPanel(wx.Panel, IUIBehavior):
    """This class contains the wx widgets for control over
    metadata information in the program. These widgets may include,
    but not limited to author, license, stl file input,
    and ldraw file output.
    """
    max_path_length = 256

    def __init__(self, parent):
        """Default constructor for MainPanel class.
        """
        wx.Panel.__init__(self, parent, size=UIStyle.metadata_panel_size,
                          style=UIStyle.metadata_border)
        self.parent = parent
        self.browse_stl_button = None
        self.help_button = None
        self.about_button = None
        self.popup = None
        self.browse_stl_button = None
        self.author_input = None
        self.license_input = None
        self.stl_path_input = None  # The input element
        self.stl_path_text = None  # The text entered
        self.stl_path_isvalid = False
        self.ldraw_name_input = None
        self.ldraw_name_isvalid = False
        self.out_file = None  # entire output file path

        # Settings
        self.stl_dir = None  # Essentially stl_path_text minus file part
        self.part_dir = None  # ldraw_name_text minus file part
        self.part_name = None  # "untitled.dat" or whatever user entered
        self.author_default = None  # The one loaded from file at start
        self.license_default = None
        self.load_settings()
        self.license_text = self.license_default
        self.author_text = self.author_default  # The text entered by user
        self._build_gui()
        self.parent.Layout()

    def _build_gui(self):
        """Initializing input, output, process control, and log panel elements
        :return:
        """
        self.SetBackgroundColour(UIStyle.metadata_background_color)

        # Input
        path_name_static_text = wx.StaticText(
            self,
            label="Step 1: Choose Input STL File",
            size=UIStyle.metadata_label_size,
            style=wx.ALIGN_RIGHT)
        path_name_static_text.SetForegroundColour(UIStyle.metadata_label_color)
        # Stl input.
        self.stl_path_input = wx.TextCtrl(self, size=UIStyle.metadata_text_ctrl_size)
        self.stl_path_input.SetMaxLength(self.max_path_length)
        self.stl_path_input.SetBackgroundColour(UIStyle.metadata_input_valid_background)
        self.stl_path_input.SetForegroundColour(UIStyle.metadata_input_text_color)

        self.browse_stl_button = Button(self, label="Browse Input",
                                           size=UIStyle.metadata_big_button)
        self.browse_stl_button.SetForegroundColour(UIStyle.button_text)
        self.browse_stl_button.SetBackgroundColour(UIStyle.button_background)

        # Help / About.
        self.help_button = Button(self, label="?",
                                     size=UIStyle.metadata_small_button_size)
        self.help_button.SetForegroundColour(UIStyle.button_text)
        self.help_button.SetBackgroundColour(UIStyle.button_background)
        self.about_button = Button(self, label="i",
                                      size=UIStyle.metadata_small_button_size)
        self.about_button.SetForegroundColour(UIStyle.button_text)
        self.about_button.SetBackgroundColour(UIStyle.button_background)

        # Output path selection.
        path_part_static_text = wx.StaticText(self, label="Step 2: Choose Output Name",
                                              size=UIStyle.metadata_label_size,
                                              style=wx.ALIGN_RIGHT)
        path_part_static_text.SetForegroundColour(UIStyle.metadata_label_color)
        self.ldraw_name_input = wx.TextCtrl(self, size=UIStyle.metadata_text_ctrl_size,
                                            style= wx.TE_READONLY)
        self.ldraw_name_input.SetMaxLength(self.max_path_length)
        self.ldraw_name_input.SetValue("Browse output -->")
        self.ldraw_name_input.SetForegroundColour(UIStyle.metadata_input_text_color)
        self.ldraw_name_input.SetBackgroundColour(UIStyle.metadata_input_valid_background)

        self.browse_output_button = Button(self, label="Browse Output",
                                              size=UIStyle.metadata_big_button)
        self.browse_output_button.SetForegroundColour(UIStyle.button_text)
        self.browse_output_button.SetBackgroundColour(UIStyle.button_background)

        # Author
        author_static_text = wx.StaticText(self, label="Optional: Set Author",
                                           size=UIStyle.metadata_label_size, style=wx.ALIGN_RIGHT)
        author_static_text.SetForegroundColour(UIStyle.metadata_label_color)
        self.author_input = wx.TextCtrl(self, size=UIStyle.metadata_text_ctrl_size)
        self.author_input.SetForegroundColour(UIStyle.metadata_input_text_color)
        self.author_input.SetBackgroundColour(UIStyle.metadata_input_valid_background)
        self.author_input.SetMaxLength(self.max_path_length)

        # License information.
        license_static_text = wx.StaticText(self, label="Optional: Set License",
                                            size=UIStyle.metadata_label_size, style=wx.ALIGN_RIGHT)
        license_static_text.SetForegroundColour(UIStyle.metadata_label_color)
        self.license_input = wx.TextCtrl(self, size=UIStyle.metadata_text_ctrl_size)
        self.license_input.SetForegroundColour(UIStyle.metadata_input_text_color)
        self.license_input.SetBackgroundColour(UIStyle.metadata_input_valid_background)
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
        horizontal_split.AddSpacer(100)
        horizontal_split.Add(vertical_layout, 0, wx.ALIGN_LEFT)

        self.SetSizer(horizontal_split)

        # Fill in default fields
        self.reset_author()
        self.reset_license()

        # Register events.
        self.Bind(wx.EVT_BUTTON, self.about, self.about_button)
        self.Bind(wx.EVT_BUTTON, self.browse_output, self.browse_output_button)
        self.Bind(wx.EVT_BUTTON, self.help, self.help_button)
        self.Bind(wx.EVT_BUTTON, self.browse_input, self.browse_stl_button)

        # Bind input field change events
        self.stl_path_input.Bind(wx.EVT_KILL_FOCUS, self.text_ctrl_input_on_kill_focus)
        self.stl_path_input.Bind(wx.EVT_SET_FOCUS, self.text_ctrl_input_on_gain_focus)
        self.ldraw_name_input.Bind(wx.EVT_KILL_FOCUS, self.text_ctrl_output_on_kill_focus)
        self.ldraw_name_input.Bind(wx.EVT_SET_FOCUS, self.text_ctrl_placeholder_on_gain_focus)
        self.author_input.Bind(wx.EVT_KILL_FOCUS, self.text_ctrl_author_on_kill_focus)
        self.license_input.Bind(wx.EVT_KILL_FOCUS, self.text_ctrl_license_on_kill_focus)

    def check_input(self):
        """Checks if all input fields have valid flag, and changes program
        state if needed. Should be called after an input field updates.

        :return: None
        """
        if self.ldraw_name_isvalid and self.stl_path_isvalid:
            if UIDriver.application_state != ApplicationState.WAITING_GO:
                UIDriver.fire_event(UserEvent(
                    UserEventType.INPUT_VALID,
                    LogMessage(LogType.IGNORE, "")))
        else:
            if UIDriver.application_state != ApplicationState.WAITING_INPUT:
                UIDriver.fire_event(UserEvent(
                    UserEventType.INPUT_INVALID,
                    LogMessage(LogType.IGNORE, "")))

        # Set colors
        if self.ldraw_name_isvalid:
            self.ldraw_name_input.SetBackgroundColour(UIStyle.metadata_input_valid_background)
        else:
            self.ldraw_name_input.SetBackgroundColour(UIStyle.metadata_input_invalid_background)
        if self.stl_path_isvalid:
            self.stl_path_input.SetBackgroundColour(UIStyle.metadata_input_valid_background)
        else:
            self.stl_path_input.SetBackgroundColour(wx.Colour(UIStyle.metadata_input_invalid_background))

    def help(self, event):
        """Presents program limitations, common troubleshooting steps,
        and steps to update LDraw parts library.
        :param event:
        :return:
        """
        help_text = UIDriver.get_assets_file_text("HELP.txt")
        if help_text is not None:
            self.popup = Popup(self.GetTopLevelParent(), "Help", help_text)
        else:
            self.popup = Popup(self.GetTopLevelParent(), "Error",
                          "Could not read help text file, sorry.")
        self.help_button.Disable()
        self.about_button.Disable()
        self.popup.Show(True)
        self.popup.Bind(wx.EVT_CLOSE, self.popup_on_close)

    def about(self, event):
        """Presents program name, program version, copyright information, licensing information, and authors to user.
        :param event:
        :return:
        """
        about_text = UIDriver.get_assets_file_text("ABOUT.txt")
        if about_text is not None:
            self.popup = Popup(self.GetTopLevelParent(), "About", about_text)
        else:
            self.popup = Popup(self.GetTopLevelParent(), "Error",
                          "Could not read about text file, sorry.")
        self.help_button.Disable()
        self.about_button.Disable()
        self.popup.Show(True)
        self.popup.Bind(wx.EVT_CLOSE, self.popup_on_close)

    def popup_on_close(self, event):
        print("window closed")
        self.popup.Destroy()
        self.popup = None
        self.help_button.Enable()
        self.about_button.Enable()

    def browse_input(self, event):
        """Browse for a valid STL input file.
        :param event:
        :return:
        """
        UIDriver.fire_event(UserEvent(
            UserEventType.RENDERING_CANVAS_DISABLE,
            LogMessage(LogType.IGNORE, "")))
        stl_wildcard = "*.stl"
        dialog = wx.FileDialog(self, "Choose a STL file",
                               defaultDir=self.stl_dir, wildcard=stl_wildcard,
                               style=wx.FD_OPEN
                               | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            # Check for file existing
            # If valid, pass to worker thread who will check data
            if self.stl_path_text != filename:
                self.stl_path_input.SetValue(filename)
                self.stl_path_input.SetValue(MetadataPanel.reduce_text_path(self.stl_path_input.GetValue()))

                # Only update stuff if selection changed
                # Check if this .stl is valid
                mesh = ModelShipper.load_stl_model(filename)
                if mesh:
                    # Load in LDraw object to input model
                    ModelShipper.input_model = LDrawModel(mesh)
                    self.stl_dir = Util.get_parent(filename)  # Only the dir
                    self.stl_path_text = filename  # The whole path to file
                    self.stl_path_isvalid = True
                    SettingsManager.save_settings("stl_dir", self.stl_dir)

                    UIDriver.fire_event(
                        UserEvent(UserEventType.INPUT_MODEL_READY,
                                  LogMessage(LogType.INFORMATION,
                                             "Input file loaded from: '" +
                                             self.stl_path_text + "'.")))
                else:
                    self.stl_path_isvalid = False
                    UIDriver.fire_event(
                        UserEvent(UserEventType.LOG_INFO,
                                  LogMessage(LogType.ERROR,
                                             "The input file '" +
                                             filename +
                                             "' is not a valid STL file.")))
                self.check_input()

            UIDriver.fire_event(UserEvent(
                UserEventType.RENDERING_CANVAS_ENABLE,
                LogMessage(LogType.IGNORE, "")))

        dialog.Destroy()

    def text_ctrl_input_on_gain_focus(self, event):
        """ Return the path to the original.
        :param event:
        :return:
        """
        if self.stl_path_text:
            self.stl_path_input.SetValue(self.stl_path_text)

        event.Skip()

    def text_ctrl_input_on_kill_focus(self, event):
        """Get the path for STL input file from user typing into TextCtrl element.
        :param event:
        :return:
        """
        prev_text = self.stl_path_text
        self.stl_path_text = self.stl_path_input.GetValue()
        self.stl_path_input.SetValue(MetadataPanel.reduce_text_path(self.stl_path_input.GetValue()))

        if prev_text != self.stl_path_text:

            # Check file path validity
            if Util.is_file(self.stl_path_text):
                if self.stl_path_text.endswith('.stl'):

                    # Check if this .stl is valid

                    mesh = ModelShipper.load_stl_model(self.stl_path_text)

                    if mesh:
                        # Load in LDraw object to input model
                        ModelShipper.input_model = LDrawModel(mesh)
                        self.stl_dir = Util.get_parent(self.stl_path_text)  # Only the dir
                        SettingsManager.save_settings("stl_dir", self.stl_dir)
                        self.stl_path_isvalid = True
                        UIDriver.fire_event(
                            UserEvent(UserEventType.INPUT_MODEL_READY,
                                      LogMessage(LogType.INFORMATION,
                                                 "Input file loaded from: '" +
                                                 self.stl_path_text + "'.")))
                    else:
                        self.stl_path_isvalid = False
                        UIDriver.fire_event(
                            UserEvent(UserEventType.LOG_INFO,
                                      LogMessage(LogType.ERROR,
                                                 "The input file '" +
                                                 self.stl_path_text +
                                                 "' is not a valid STL file.")))
                else:
                    self.stl_path_isvalid = False
                    UIDriver.fire_event(
                        UserEvent(UserEventType.LOG_INFO,
                                  LogMessage(LogType.ERROR,
                                             "Input file must have .stl extension.")))
            else:
                self.stl_path_isvalid = False
                if len(self.stl_path_text) <=0:
                    log_msg = "Input filepath cannot be blank."
                else:
                    log_msg = "The path '" + self.stl_path_text + "' could not be found."
                UIDriver.fire_event(
                    UserEvent(UserEventType.LOG_INFO,
                              LogMessage(LogType.ERROR, log_msg)))
            self.check_input()
        event.Skip()

    def browse_output(self, event):
        """Browse for a valid output file path
        :param event:
        :return:
        """
        UIDriver.fire_event(UserEvent(
            UserEventType.RENDERING_CANVAS_DISABLE,
            LogMessage(LogType.IGNORE, "")))

        dat_wildcard = "*.dat"
        dialog = wx.FileDialog(self, "Choose a location for the LDraw file",
                               defaultDir=self.part_dir,
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                               wildcard=dat_wildcard)

        dialog.SetFilename(self.part_name)

        if dialog.ShowModal() == wx.ID_OK:
            pathname = dialog.GetPath()

            if self.out_file != pathname:
                # Check if part name ends with .dat, if not append that
                if not pathname.endswith('.dat'):
                    pathname = pathname + '.dat'

                self.out_file = pathname  # Full path
                self.part_dir = Util.get_parent(pathname)  # Only the dir
                self.part_name = Util.get_filename(pathname)  # Only filename
                self.ldraw_name_isvalid = True
                SettingsManager.save_settings("part_dir", self.part_dir)
                SettingsManager.save_settings("part_name", self.part_name)
                self.ldraw_name_input.SetValue(self.out_file)
                self.ldraw_name_input.SetValue(MetadataPanel.reduce_text_path(self.ldraw_name_input.GetValue()))
                self.check_input()
                UIDriver.fire_event(
                    UserEvent(UserEventType.LOG_INFO,
                              LogMessage(LogType.INFORMATION,
                                         "Output file will be saved as: '" +
                                         self.out_file + "'.")))

        UIDriver.fire_event(UserEvent(
            UserEventType.RENDERING_CANVAS_ENABLE,
            LogMessage(LogType.IGNORE, "")))
        dialog.Destroy()

    def text_ctrl_placeholder_on_gain_focus(self, event):
        """Remove placeholder text and reset style if output has not been set
        :param event:
        :return:
        """
        if not self.ldraw_name_isvalid:
            self.ldraw_name_input.SetValue("")

        event.Skip()

    def text_ctrl_output_on_kill_focus(self, event):
        """Called when the output text control loses focus.

        :param event: The event that occurred.
        :return: None.
        """
        output_text = self.ldraw_name_input.GetValue()
        if len(output_text) <= 0:
            self.ldraw_name_input.SetValue("Browse output -->")
            if len(self.ldraw_name_input.GetValue()) > 0:
                self.ldraw_name_input.SetBackgroundColour(UIStyle.metadata_input_valid_background)
            UIDriver.fire_event(
                UserEvent(UserEventType.LOG_INFO,
                          LogMessage(LogType.ERROR,
                                     "Output file path cannot be blank.")))
        event.Skip()

    def text_ctrl_author_on_kill_focus(self, event):
        """Get the author value from the user and update the settings file
        as needed.

        :param event: The event that occurred.
        :return: None
        """
        author = self.author_input.GetValue()

        # Update settings file author info
        if author != self.author_text and author != "":
            self.author_text = author
            UIDriver.fire_event(
                UserEvent(UserEventType.LOG_INFO,
                          LogMessage(LogType.INFORMATION,
                                     "Author changed to: " +
                                     self.author_text)))
            SettingsManager.save_settings("author", self.author_text)

        elif len(author) == 0:
            self.reset_author()
        event.Skip()

    def text_ctrl_license_on_kill_focus(self, event):
        """Get the license value from the user and update the settings file
        as needed."""
        license_input_text = self.license_input.GetValue()

        # Update settings file license info
        if license_input_text != self.license_text and license_input_text != "":
            self.license_text = license_input_text
            UIDriver.fire_event(
                UserEvent(UserEventType.LOG_INFO,
                          LogMessage(LogType.INFORMATION,
                                     "License changed to: " +
                                     self.license_text)))
            SettingsManager.save_settings("license", self.license_text)

        elif len(license_input_text) == 0:
            self.reset_license()
        event.Skip()

    def reset_author(self):
        """Fill in author field with default"""
        self.author_input.SetValue(self.author_default)

    def reset_license(self):
        """Fill in license field with default"""
        self.license_input.SetValue(self.license_default)

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
            self.browse_output_button.Enable()
            self.browse_stl_button.Enable()
        elif new_state == ApplicationState.WORKING:
            self.stl_path_input.Disable()
            self.ldraw_name_input.Disable()
            self.author_input.Disable()
            self.license_input.Disable()
            self.browse_output_button.Disable()
            self.browse_stl_button.Disable()

    def on_event(self, event: UserEvent):
        """A user event was passed to the MetadataPanel.

        :param event: The recorded UserEvent.
        :return: None
        """
        pass

    def load_settings(self):
        """Load settings values into memory on startup.
        """
        # If settings file doesnt exist
        if not Util.is_file(SettingsManager.file_path):
            # If directory doesnt exist
            if not Util.is_dir(SettingsManager.settings_path):
                Util.mkdir(SettingsManager.settings_path)
            # Create user settings with default
            SettingsManager.create_settings(SettingsManager.filename)

        with open(SettingsManager.file_path, "r") as file:
            file_settings = json.load(file)
            self.stl_dir = file_settings["stl_dir"]
            self.part_name = file_settings["part_name"]
            self.part_dir = file_settings["part_dir"]
            self.author_default = file_settings["author"]
            self.license_default = file_settings["license"]

    def get_stl_path_text(self):
        """Return the string of the path to the input stl file.
        """
        return self.stl_path_text

    def get_stl_dir(self):
        """Return the string of the stl directory.
        """
        return self.stl_dir

    def get_out_file(self):
        """Return the string of the path to the output dat file.
        """
        return self.out_file

    def get_part_dir(self):
        """Return the string of the parts directory.
        """
        return self.part_dir

    def get_part_name(self):
        """Return string of the part name."""
        return self.part_name

    def get_author(self):
        """Return the string of the author.
        """
        return self.author_text

    def get_license(self):
        """Return the string of the license.
        """
        return self.license_text

    def update(self, dt: float):
        """Called every loop by the GUIEventLoop

        :param dt: The delta time between the last call.
        :return: None
        """
        pass

    @staticmethod
    def reduce_text_path(path_text):
        """
        Reduce text length to fit the wx.textctrl box
        :param path_text:
        :return: the reduce text that is long equal or less than 64 characters.(Unless the file's name is super long)
        """
        windows = False
        # Both Linux and Mac start with "/", so we could decide what kind of path is it.
        if path_text:
            if path_text[0] != "/":
                windows = True
            if windows:
                # Windows format.
                # The file path format is Root:\something\something\file.stl
                list_str = path_text.split("\\")
                length_text = MetadataPanel.list_string_length(list_str)
                pop = False
                while length_text > 60 and len(list_str) > 1:
                    list_str.pop(0)
                    pop = True
                    length_text = MetadataPanel.list_string_length(list_str)
                text = "\\"
                text = text.join(list_str)
                if pop:
                    text = "...\\" + text
                return text
            else:
                # Mac or Linux format.
                # The file format is /something/something/.../file.stl
                list_str = path_text.split("/")
                list_str.pop(0)
                length_text = MetadataPanel.list_string_length(list_str)
                pop = False
                while length_text > 59 and len(list_str) != 1:
                    list_str.pop(0)
                    pop = True
                    length_text = MetadataPanel.list_string_length(list_str)
                text = "/"
                text = text.join(list_str)
                if pop:
                    text = "/.../" + text
                else:
                    text = "/" + text
                return text
        return path_text

    @staticmethod
    def list_string_length(list_str):
        """
        Return the length of the path
        :param list_str: list of string after the list.
        :return:
        """
        sum_str = 0
        for a_str in list_str:
            sum_str += len(a_str)
        return len(list_str) + sum_str - 1
