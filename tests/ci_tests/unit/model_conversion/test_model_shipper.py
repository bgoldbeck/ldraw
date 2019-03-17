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

import numpy
import unittest
import json
from src.settings_manager import SettingsManager
from src.util import Util
from src.model_conversion.model_shipper import ModelShipper

path = Util.path_conversion("tests/test_models/cube.stl")


class ModelShipperTest(unittest.TestCase):
    """Class to verify the proper implementation of the model_shipper

    return: none
    """
    def setUp(self):
        ModelShipper.input_model = ModelShipper.load_stl_model(path)
        ModelShipper.output_model = None
        ModelShipper.output_data_text = None
        ModelShipper.output_metadata_text = None

    def test_get_input_model(self):
        self.assertEqual(len(ModelShipper.input_model), len(ModelShipper.get_input_model()))
        self.assertTrue(numpy.array_equal(ModelShipper.input_model.data, ModelShipper.get_input_model().data))

    def test_update_metadata(self):
        with open(SettingsManager.file_path, "r") as file:
            file_settings = json.load(file)
            file_name = file_settings["part_name"]
            part_name = file_name
            if part_name.endswith(".dat"):
                part_name = part_name[:-4]
            author = file_settings["author"]
            license = file_settings["license"]
        test_file_info = f"0 LScan auto generated part {file_name}\n0 Name: {file_name}\n0 Author: {author}\n" \
            f"0 !LICENSE {license}\n"
        self.assertEqual(test_file_info, ModelShipper.get_metadata())
