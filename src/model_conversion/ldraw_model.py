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
    def __init__(self, name, mesh: Mesh):
        self.name = ""
        self.mesh = mesh
        self.children = []

    def get_mesh(self):
        return self.mesh

    def get_name(self):
        return self.name

    def add_child(self, ldraw_model):
        self.children.append(ldraw_model)

    def get_children(self):
        return self.children
