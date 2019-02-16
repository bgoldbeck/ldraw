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
from src.rendering.tranform import Transform
from pyrr import *


class TransformTest(unittest.TestCase):

    def setUp(self):
        self.transform = Transform()

    def tearDown(self):
        self.transform = None

    def testDefaultPosition(self):
        self.assertEqual(self.transform.position, Vector3([0.0, 0.0, 0.0]))

    def testDefaultRotation(self):
        self.assertEqual(self.transform.euler_angles, Vector3([0.0, 0.0, 0.0]))

    def testDefaultForward(self):
        self.assertEqual(self.transform.forward, Vector3([0.0, 0.0, 1.0]))

    def testDefaultUp(self):
        self.assertEqual(self.transform.up, Vector3([0.0, 1.0, 0.0]))

    def testDefaultRight(self):
        self.assertEqual(self.transform.right, Vector3([1.0, 0.0, 0.0]))

    def testDefaultScale(self):
        self.assertEqual(self.transform.scale, Vector3([1.0, 1.0, 1.0]))

    def testTranslateAlongXAxisByOne(self):
        self.transform.position = Vector3([0.0, 0.0, 0.0])
        self.transform.translate(Vector3([1.0, 0.0, 0.0]), 1.0)
        self.assertEqual(self.transform.position, Vector3([1.0, 0.0, 0.0]))

    def testTranslateAlongYAxisByOne(self):
        self.transform.position = Vector3([0.0, 0.0, 0.0])
        self.transform.translate(Vector3([0.0, 1.0, 0.0]), 1.0)
        self.assertEqual(self.transform.position, Vector3([0.0, 1.0, 0.0]))

    def testTranslateAlongZAxisByOne(self):
        self.transform.position = Vector3([0.0, 0.0, 0.0])
        self.transform.translate(Vector3([0.0, 0.0, 1.0]), 1.0)
        self.assertEqual(self.transform.position, Vector3([0.0, 0.0, 1.0]))





