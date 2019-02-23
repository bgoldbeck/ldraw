# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
from src.util import Util
import json
from pathlib import Path


class SettingsManager:
    settings_path = Util.path_conversion("assets/settings")
    filename = "user_settings.json"
    file_path = settings_path + "/" + filename

    @staticmethod
    def create_settings(filename: str):
        """Generate initial settings file based on current working directory.

        :param filename:
        :return:
        """
        # default stl directory
        default_stl_dir = Util.path_conversion("assets/models/")
        # default part name
        default_part_name = "untitled.dat"
        # default part name directory
        default_part_dir = Util.path_conversion("assets/parts/")
        # default author
        default_author = "First Last"
        # default license
        default_license = "Redistributable under CCAL version 2.0 : see CAreadme.txt"
        # default Log directory
        default_log_dir = Util.path_conversion(str(Path.home()) + "/Documents")

        default_settings = {"stl_dir": default_stl_dir,
                            "part_name": default_part_name,
                            "part_dir": default_part_dir,
                            "author": default_author,
                            "license": default_license,
                            "log_dir": default_log_dir}
        file_path = Util.path_conversion(f"assets/settings/{filename}")

        try:
            with open(file_path, "w") as file:
                json.dump(default_settings, file, indent=4)
        except FileNotFoundError as ferr:
            print(ferr)

    @staticmethod
    def save_settings(setting: str, val: str):
        """Save changes to user settings file.
        :param setting:
        :param val:
        :return:
        """
        # Write out settings changes
        # default_part_name is always "untitled.dat"

        try:
            with open(SettingsManager.file_path, "r") as file:
                file_settings = json.load(file)
                file_settings[setting] = val

            with open(SettingsManager.file_path, "w") as file:
                json.dump(file_settings, file, indent=4)

        except FileNotFoundError as ferr:
            print(ferr)

    @staticmethod
    def display_settings():
        """Display all settings and stl file path to standard out."""
        print("\n\nDisplay settings\n")
        try:
            with open(SettingsManager.file_path, "r") as file:
                all_settings = json.load(file)
                print(all_settings)
        except FileNotFoundError as ferr:
            print(ferr)

    @staticmethod
    def get_settings(settings: [str]):
        """
        Return a dictionary of settings and their values
        :param settings:
        :return requested settings:
        """

        if settings:
            try:
                with open(SettingsManager.file_path, "r") as file:
                    all_settings = json.load(file)
                    requested = []
                    for setting in settings:
                        if all_settings[setting]:
                            requested[setting] = all_settings[setting]
                    return requested
            except FileNotFoundError as ferr:
                print(ferr)



