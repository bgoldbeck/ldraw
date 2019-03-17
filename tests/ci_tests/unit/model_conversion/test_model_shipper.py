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
from stl import Mesh
from src.util import Util
from src.model_conversion.model_shipper import ModelShipper

path = Util.path_conversion("assets/models/cube.stl")


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
        pass
        #self.assertEqual(len(ModelShipper.input_model), len(ModelShipper.get_input_model()))
        #self.assertTrue(numpy.array_equal(ModelShipper.input_model.data, ModelShipper.get_input_model().data))

    def test_update_metadata(self):
        pass
        #test_file_info =  "0 LScan auto generated part file_name\n0 Name: file_name\n0 Author: author\n0 !LICENSE license_info\n"
        #ModelShipper.update_metadata("author", "file_name", "license_info")
        #self.assertEqual(test_file_info, ModelShipper.output_metadata_text)
