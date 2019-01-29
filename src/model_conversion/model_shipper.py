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
from src.model_conversion.ldraw_model import LDrawModel
from src.log_messages.log_type import LogType
from src.log_messages.log_message import LogMessage


class ModelShipper:
    """The static class responsible for import/export of models.

    Will be mainly responsible for importing STL models and exporting
    LDraw (.dat) files.
    """

    @staticmethod
    def load_stl_model(file_path: str):
        """Load an STL model and return its mesh data.

        :param file_path: The path to the stl file.
        :return: The BaseStl model (numpy-stl) loaded from the file_path or None.
        """
        try:
            return Mesh.from_file(file_path)
        except (RuntimeError, AssertionError, AttributeError, ValueError, FileNotFoundError) as err:
            logging.error(f"Failed to open the STL file : {err}")
            return None

    @staticmethod
    def save_ldraw_file_model(file_path, model: LDrawModel):
        """Export an LDrawModel information to a file.

        :param file_path: The full filepath to save to.
        :param model: The LDrawModel representation.
        :return: None
        """
        # Open file
        file = open(file_path, "w")

        # Write out the model name.
        if model.get_name() != "":
            ModelShipper._line_type0_to_file(file, "Name: " + model.get_name())

        # Write out the author name.
        if model.get_author() != "":
            ModelShipper._line_type0_to_file(file, "Author: " + model.get_author())

        # Write out the license
        if model.get_name() != "":
            ModelShipper._line_type0_to_file(file, "!LICENSE " + model.get_license_info())

        # Loop through main model mesh facets
        ModelShipper._line_type3_to_file(file, model.get_mesh())

        # Loop through child models mesh
        for i in range(len(model.get_children())):
            ModelShipper._line_type3_to_file(file, model.get_children()[i])

        file.close()

    @staticmethod
    def _line_type0_to_file(file, command):
        """Write a meta-command line to the file using LDraw File Format line type 0
        A meta-command line is formatted:
        0 <meta-command> <additional parameters>

        :param file: The file reference.
        :param command: The command
        :return: None
        """
        file.write("0 " + command + "\n")

    @staticmethod
    def _line_type3_to_file(file, mesh):
        """Write a line using LDraw File Format line type 3
        Line type 3 is a filled triangle drawn between three points. The generic format is:
        3 <colour> x1 y1 z1 x2 y2 z2 x3 y3 z3

        :param file: The file reference
        :param mesh: The mesh (vertex data) structure.
        :return: None
        """

        for i in range(len(mesh.normals)):
            # Export vertices information in ldraw format
            file.write("3 4 " + str(mesh.v2[i][0])
                       + " " + str(mesh.v2[i][1])
                       + " " + str(mesh.v2[i][2])
                       + " " + str(mesh.v1[i][0])
                       + " " + str(mesh.v1[i][1])
                       + " " + str(mesh.v1[i][2])
                       + " " + str(mesh.v0[i][0])
                       + " " + str(mesh.v0[i][1])
                       + " " + str(mesh.v0[i][2])
                       + "\n")

