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
from src.model_conversion.ldraw_model import *


class LDrawModel:
    """Data class representation of an LDraw parts file

    """
    def __init__(self, name: str, author: str, license_info: str, mesh: Mesh):
        """

        :param name: Name of the model.
        :param author: Author of the model.
        :param license_info: License information for the model
        :param mesh: Vertex data structure of the model from the numpy library.
        """
        self.name = name
        self.author = author
        self.mesh = mesh
        self.license_info = license_info
        self.children = []

    def get_mesh(self):
        """Get the vertex data model.

        :return: The vertex data as a BaseStl object.
        """
        return self.mesh

    def get_name(self):
        """Get the model name.

        :return: The name of the model as a str.
        """
        return self.name

    def get_author(self):
        """Get the author name.

        :return: The author name as a str.
        """
        return self.author

    def get_license_info(self):
        """Get the license info

        :return: The license info as a str.
        """
        return self.license_info

    def add_child(self, ldraw_model: LDrawModel):
        """Add a child LDrawModel object to this one.

        :param ldraw_model: The child LDrawModel to add.
        :return: None
        """

        self.children.append(ldraw_model)

    def get_children(self):
        """Get the children LDrawModel's from this one.

        :return: The children LDrawModel's
        """
        return self.children
