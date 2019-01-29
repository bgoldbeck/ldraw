# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import os
from pathlib import Path


class Util:
    """This class is responsible for being a helper function library.

    """

    @staticmethod
    def path_conversion(file_path: str):
        """
        Used to convert file paths depending on operating system.

        :param file_path: file path to convert
        :return: converted file path
        """
        root_dir = os.path.dirname(os.path.abspath(__file__))

        return str(root_dir) + str(Path(file_path))


