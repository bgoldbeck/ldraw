import unittest
import os
from src.model_conversion.model_shipper import *
from pyrr import *


class ModelShipperTest(unittest.TestCase):

    def testImportPlane(self):
        mesh_data = ModelShipper.load_stl_model("assets/models/plane.stl")
        # First triangle facet
        self.assertEqual(mesh_data.v0[0], Vector3([0.5, 0., -0.5]))
        self.assertEqual(mesh_data.v1[0], Vector3([-0.5, 0., -0.5]))
        self.assertEqual(mesh_data.v2[0], Vector3([-0.5, 0., 0.5]))

        # Second triangle facet
        self.assertEqual(mesh_data.v0[1], Vector3([-0.5, 0., 0.5]))
        self.assertEqual(mesh_data.v1[1], Vector3([0.5, 0., 0.5]))
        self.assertEqual(mesh_data.v2[1], Vector3([0.5, 0., -0.5]))

    def testExportPlane(self):
        try:
            os.mkdir("tests/temp")
        except OSError:
            print("Failed to create temp directory")

        file_path = "tests/temp/plane.dat"

        # Import the model
        mesh_data = ModelShipper.load_stl_model("assets/models/plane.stl")
        model = LDrawModel("plane", mesh_data)

        # Export the model
        ModelShipper.save_ldraw_file_model(file_path, model)

        # Read the file
        with open(file_path, 'r') as file:
            file_data = file.read()

        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

        self.assertEqual(
            file_data,
            "3 4 -0.5 0.0 0.5 -0.5 0.0 -0.5 0.5 0.0 -0.5\n3 4 0.5 0.0 -0.5 0.5 0.0 0.5 -0.5 0.0 0.5\n")
