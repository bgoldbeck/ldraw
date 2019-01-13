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
from stl import Mesh
from src.model_conversion.ldraw_model import LDrawModel
import os

class ModelShipper:
    @staticmethod
    def load_stl_model(file_path):
        """

        :param file_path:
        :return:
        """
        #TODO: confirm valid filepath
        return Mesh.from_file(file_path)

    @staticmethod
    def save_ldraw_file_model(file_path, model: LDrawModel):
        """
        :param file_path:
        :param model:
        :return:
        """
        # Open file
        file = open(file_path, "w")

        if model.get_name() != "":
            ModelShipper._line_type0_to_file(file, model.get_name())

        if model.get_author() != "":
            ModelShipper._line_type0_to_file(file, "Author: " + model.get_author())

        # Loop through main model mesh facets
        ModelShipper._line_type3_to_file(file, model.get_mesh())

        # Loop through child models mesh
        for i in range(len(model.get_children())):
            ModelShipper._line_type3_to_file(file, model.get_children()[i])

    @staticmethod
    def _line_type0_to_file(file, comment):
        """

        :param file:
        :param comment:
        :return:
        """
        file.write("0 // " + comment + "\n")


    @staticmethod
    def _line_type3_to_file(file, mesh):
        """

        :param file:
        :param mesh:
        :return:
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
