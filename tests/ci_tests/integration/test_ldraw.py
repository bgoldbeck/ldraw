# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.

import numpy
import unittest
from stl import Mesh
from src.util import Util
from src.model_conversion.ldraw_model import LDrawModel


path = Util.path_conversion("tests/test_models/cube.stl")


class LDrawModelTest(unittest.TestCase):
    """Class to verify the proper implementation of the ldraw_model

    :return: None
    """
    def setUp(self):
        self.mesh = Mesh.from_file(path)
        self.children = []
        self.ldraw_model = LDrawModel(self.mesh)

    def test_initialized(self):
        self.assertEqual(self.mesh.__dict__, self.ldraw_model.mesh.__dict__)
        self.assertEqual([], self.ldraw_model.children)

    def test_mesh(self):
        self.assertEqual(len(self.mesh), len(self.ldraw_model.get_mesh()))
        self.assertTrue(numpy.array_equal(self.mesh.data, self.ldraw_model.get_mesh().data))

    def test_children(self):
        self.ldraw_model.add_child(self.ldraw_model)
        self.assertEqual(len(self.mesh), len(self.ldraw_model.children[0].get_mesh()))
        self.assertTrue(numpy.array_equal(self.mesh.data, self.ldraw_model.children[0].get_mesh().data))
        self.assertTrue(len(self.ldraw_model.children), len(self.ldraw_model.get_children()))

