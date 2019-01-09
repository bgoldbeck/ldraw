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
    def save_ldraw_file_model(file_path, model : LDrawModel):
        """
        :param file_path:
        :param model:
        :return:
        """
        # Open file
        file = open(file_path, "w")
        # Loop through main model
        ModelShipper._line_type3_to_file(file, model)
        # Loop through child models
        for i in range(len(model.get_children().count())):
            ModelShipper._line_type3_to_file(file, model.get_children()[i])

    @staticmethod
    def _line_type3_to_file(file, model):
        """

        :param file:
        :param model:
        :return:
        """
        for i in range(len(model.mesh.normals)):
            # Export vertices information in ldraw format
            file.write("3 4 " + model.mesh_data.v2[i][0]
                       + " " + model.mesh_data.v2[i][1]
                       + " " + model.mesh_data.v2[i][2]
                       + " " + model.mesh_data.v1[i][0]
                       + " " + model.mesh_data.v1[i][1]
                       + " " + model.mesh_data.v1[i][2]
                       + " " + model.mesh_data.v0[i][0]
                       + " " + model.mesh_data.v0[i][1]
                       + " " + model.mesh_data.v0[i][2]
                       + "\n")
