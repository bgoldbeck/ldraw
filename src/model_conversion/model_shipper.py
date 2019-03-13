# Copyright (C) 2018
# This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License.
# See LICENSE file for the full text.
import logging
from stl import Mesh
from src.settings_manager import SettingsManager
import json


class ModelShipper:
    """The static class responsible for import/export of models.

    Will be mainly responsible for importing STL models and exporting
    LDraw (.dat) files.
    """
    input_model = None # Mesh loaded in from input file
    output_model = None # LDraw file
    output_data_text = None # The text to write out to output path when save pressed

    @staticmethod
    def load_stl_model(file_path: str):
        """Load an STL model into ModelShipper.input_model.

        :param file_path: The path to the stl file.
        :return: The BaseStl model (numpy-stl) loaded from the file_path or None.
        """
        try:
            return Mesh.from_file(file_path)
        except Exception as err:
            logging.error(f"Failed to open the STL file : {err}")
            return False

    @staticmethod
    def get_input_model():
        """Gets input_model
        :return: input_model contents (should be a Mesh, or None)
        """

        return ModelShipper.input_model

    @staticmethod
    def get_metadata():
        """Build and return a string of metadata lines
        :return: String containing all metadata lines
        """

        with open(SettingsManager.file_path, "r") as file:
            file_settings = json.load(file)
            file_name = file_settings["part_name"]
            part_name = file_name
            if part_name.endswith(".dat"):
                part_name = part_name[:-4]
            author = file_settings["author"]
            license = file_settings["license"]

        metadata_text = "0 " + "LScan auto generated part " + part_name + "\n"
        metadata_text += "0 " + "Name: " + file_name + "\n"
        metadata_text += "0 " + "Author: " + author + "\n"
        metadata_text += "0 " + "!LICENSE " + license + "\n"
        return metadata_text