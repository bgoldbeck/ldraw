# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import wx, os
from sys import platform
from pathlib import Path
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.iui_behavior import IUIBehavior


class UIDriver:
    """This class is responsible for driving the UI. It holds the root frame wx widget as well as
    keeping track of the application state. It will send user events and application state changes
    to the child IUIBehavior objects.
    """

    instance = None
    application_state = None
    root_frame = None

    def __init__(self, root):
        """Default constructor for the UIDriver object.

        """
        if not UIDriver.instance:
            UIDriver.instance = self

            UIDriver.root_frame = root

            # Set application to STARTUP state.
            UIDriver.change_application_state(ApplicationState.STARTUP)

            # Automatically go right into WAITING_INPUT state.
            UIDriver.change_application_state(ApplicationState.WAITING_INPUT)

    @staticmethod
    def get_all_ui_behaviors(root, behaviors):
        """Traverse the child-parent relationship between wx widgets. Return all the children objects that
        are instances of the IUIBehavior.

        :param root: The root wx widget.
        :param behaviors: The IUIBehavior objects to return by reference.
        :return: None
        """
        if root is None:
            return

        children = root.GetChildren()

        for child in children:
            if isinstance(child, IUIBehavior):
                behaviors.append(child)
            UIDriver.get_all_ui_behaviors(child, behaviors)

    @staticmethod
    def fire_event(event: UserEvent):
        """Send an event down the wx widget tree to all IUIBehavior objects.

        :param event:
        :return:
        """
        # We need to notify all the ui behaviors of the event.
        ui_behaviors = []
        UIDriver.get_all_ui_behaviors(UIDriver.root_frame, ui_behaviors)

        for ui_behavior in ui_behaviors:
            ui_behavior.on_event(event)

    @staticmethod
    def change_application_state(new_state: ApplicationState):
        """Send a state change down the wx widget tree to all IUIBehavior objects.

        :param new_state: The state the application was changed to.
        :return: None
        """
        # Set the new state.
        UIDriver.application_state = new_state

        # Notify all the ui behavior objects of the state change.
        ui_behaviors = []
        UIDriver.get_all_ui_behaviors(UIDriver.root_frame, ui_behaviors)

        for ui_behavior in ui_behaviors:
            ui_behavior.on_state_changed(new_state)

    @staticmethod
    def get_assets_file_text(file_name: str):
        """Return the contents of the file in the folder CWD/assets/info/

        :param file_name: The name of the file contained in the assets/info folder.
        :return: The text that was read from the file or None
        """
        enc = "utf-8"
        if platform == "win32" or os.name == "nt":
            file_path = str(Path.cwd()) + "\\assets\\info\\" + file_name
        else:
            file_path = str(Path.cwd()) + "/assets/info/" + file_name

        text = None
        # Try to open the complete file path and record the text.
        try:
            with open(str(file_path), "r", encoding=enc) as file:
                text = file.read()
        except PermissionError as perr:
            pass
        except FileNotFoundError as ferr:
            pass

        return text