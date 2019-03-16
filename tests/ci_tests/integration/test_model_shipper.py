# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import unittest
import os
import numpy
import unittest
from src.model_conversion.model_shipper import *
from pyrr import *
from src.util import Util
from stl import Mesh
path = Util.path_conversion("tests/test_models/cube.stl")
from src.model_conversion.ldraw_model import LDrawModel


class ModelShipperTest(unittest.TestCase):

    def setUp(self):
        ModelShipper.input_model = ModelShipper.load_stl_model(path)
        ModelShipper.output_model = None
        ModelShipper.output_data_text = None
        ModelShipper.output_path = None
        ModelShipper.output_metadata_text = None

    def testImportPlane(self):
        # Load the model from the assets folder.
        mesh = ModelShipper.load_stl_model(Util.path_conversion("tests/test_models/plane.stl"))
        self.assertNotEqual(mesh, False)
        # First triangle facet.
        self.assertEqual(mesh.v0[0], Vector3([0.5, 0., -0.5]))
        self.assertEqual(mesh.v1[0], Vector3([-0.5, 0., -0.5]))
        self.assertEqual(mesh.v2[0], Vector3([-0.5, 0., 0.5]))

        # Second triangle facet.
        self.assertEqual(mesh.v0[1], Vector3([-0.5, 0., 0.5]))
        self.assertEqual(mesh.v1[1], Vector3([0.5, 0., 0.5]))
        self.assertEqual(mesh.v2[1], Vector3([0.5, 0., -0.5]))

    def testExportPlane(self):
        # Create an empty temp folder to use for temporary model files.
        try:
            os.mkdir(Util.path_conversion("tests/temp"))
        except OSError:
            pass

        pass
        # The file path we will use.
        file_path = Util.path_conversion("tests/temp/plane.dat")

        # Import the model.
        mesh = ModelShipper.load_stl_model(Util.path_conversion("tests/test_models/plane.stl"))
        self.assertNotEqual(mesh, False)

        model = LDrawModel(mesh)

        """# Export the model.
        ModelShipper.save_ldraw_file_model(file_path, model)

        # Read the file.
        with open(file_path, 'r') as file:
            file_data = file.read()

        # The final file data should look like this.
        self.assertEqual(
            file_data,
            "0 LScan auto generated part plane\n0 Name: plane.dat\n0 Author: Rando\n0 !LICENSE Redistributable under CCAL version 2.0 : see CAreadme.txt\n3 4 -0.5 0.0 0.5 -0.5 0.0 -0.5 0.5 0.0 -0.5\n3 4 0.5 0.0 -0.5 0.5 0.0 0.5 -0.5 0.0 0.5\n")
        """
        # Cleanup.
        if os.path.exists(file_path):
            os.remove(file_path)
        os.rmdir(Util.path_conversion("tests/temp/"))

    def test_get_input_model(self):
        self.assertEqual(len(ModelShipper.input_model), len(ModelShipper.get_input_model()))
        self.assertTrue(numpy.array_equal(ModelShipper.input_model.data, ModelShipper.get_input_model().data))
