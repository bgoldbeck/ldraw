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

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def path_conversion(file_path: str):
        """
        Used to convert file paths depending on operating system.

        :param file_path: file path to convert
        :return: converted file path
        """

        return os.path.join(Util.ROOT_DIR, Path(file_path))

    @staticmethod
    def is_file(file_path: str):
        """
        Checks whether a file exists or not.

        :param file_path: absolute file path
        :return: True or False
        """
        return Path(file_path).is_file()

    @staticmethod
    def get_filename(file_path: str):
        """
        Gets the filename from file path.

        :param file_path: absolute file path
        :return: the filename in string
        """
        return str(Path(file_path).parts[-1])

    @staticmethod
    def is_dir(dir_path: str):
        """
        Checks if the path is a valid directory or not

        :param dir_path: absolute directory path
        :return: True or False
        """
        return Path(dir_path).is_dir()

    @staticmethod
    def get_parent(file_path: str):
        """
        Gets the parent path of a file path

        :param file_path: absolute file path
        :return: parent path in string
        """
        return str(Path(file_path).parent)

    @staticmethod
    def mkdir(dir_path: str):
        """
        Creates a directory with given path

        :param dir_path: absolute directory path
        :return:
        """
        Path(dir_path).mkdir(parents=True)

    @staticmethod
    def rmdir(dir_path: str):
        """
        Removes a directory with given path

        :param dir_path: absolute directory path
        :return:
        """
        Path(dir_path).rmdir()
