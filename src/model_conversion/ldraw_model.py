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


class LDrawModel:
    """Data class representation of an LDraw parts file

    """
    def __init__(self, mesh: Mesh):
        """Constructor for the LDrawModel class.
        :param mesh: Vertex data structure of the model from the numpy library.
        """
        self.mesh = mesh
        self.children = []

    def get_mesh(self):
        """Get the vertex data model.

        :return: The vertex data as a BaseStl object.
        """
        return self.mesh

    def add_child(self, ldraw_model):
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
