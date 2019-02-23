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

    @staticmethod
    def create_settings(filename: str):
        """Generate initial settings file based on current working directory.

                :param name:
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
                json.dump(default_settings, file)
        except FileNotFoundError as ferr:
            print(ferr)

