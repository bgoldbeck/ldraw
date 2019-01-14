import unittest
import os
from src.model_conversion.model_shipper import *
from pyrr import *


class ModelShipperTest(unittest.TestCase):

    def testImportPlane(self):
        # Load the model from the assets folder.
        mesh_data = ModelShipper.load_stl_model("assets/models/plane.stl")

        # First triangle facet.
        self.assertEqual(mesh_data.v0[0], Vector3([0.5, 0., -0.5]))
        self.assertEqual(mesh_data.v1[0], Vector3([-0.5, 0., -0.5]))
        self.assertEqual(mesh_data.v2[0], Vector3([-0.5, 0., 0.5]))

        # Second triangle facet.
        self.assertEqual(mesh_data.v0[1], Vector3([-0.5, 0., 0.5]))
        self.assertEqual(mesh_data.v1[1], Vector3([0.5, 0., 0.5]))
        self.assertEqual(mesh_data.v2[1], Vector3([0.5, 0., -0.5]))

    def testExportPlane(self):
        # Create an empty temp folder to use for temporary model files.
        try:
            os.mkdir("tests/temp")
        except OSError:
            print("Directory already exists.")

        # The file path we will use.
        file_path = "tests/temp/plane.dat"

        # Import the model.
        mesh_data = ModelShipper.load_stl_model("assets/models/plane.stl")
        model = LDrawModel(
            "plane",  # Model name
            "Rando",  # Author
            "!LICENSE Redistributable under CCAL version 2.0 : see CAreadme.txt",  #  License info
            mesh_data  # Mesh
        )

        # Export the model.
        ModelShipper.save_ldraw_file_model(file_path, model)

        # Read the file.
        with open(file_path, 'r') as file:
            file_data = file.read()

        # Cleanup.
        if os.path.exists(file_path):
            os.remove(file_path)

        # The final file data should look like this.
        self.assertEqual(
            file_data,
            "0 // !LICENSE Redistributable under CCAL version 2.0 : see CAreadme.txt\n0 // plane\n0 // Author: Rando\n3 4 -0.5 0.0 0.5 -0.5 0.0 -0.5 0.5 0.0 -0.5\n3 4 0.5 0.0 -0.5 0.5 0.0 0.5 -0.5 0.0 0.5\n")
