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
from src.model_conversion.triangle import *


class TestTriangle(unittest.TestCase):

    def setUp(self):
        self.test_edge1 = Edge(-1, 1, 1, 1, 1, 1)
        self.test_edge2 = Edge(1, 1, 1, 1, 1, -1)
        self.test_edge3 = Edge(1, 1, -1, -1, 1, 1)
        self.normal = [0, 1, 0]
        self.triangle = Triangle(self.test_edge1, self.test_edge2, self.test_edge3, self.normal)

    def testIsClosedLoop(self):
        self.assertTrue(self.triangle.is_closed_loop())

    def testGetNormal(self):
        self.assertEqual(self.normal, self.triangle.get_normal())

    def testHasEdge(self):
        invalid_edge = Edge(5, 4, 3, 2, 0, 0)
        self.assertFalse(self.triangle.has_edge(invalid_edge))
        self.assertTrue(self.triangle.has_edge(self.test_edge3))

    def testGetFirstEdge(self):
        self.assertEqual(self.test_edge1, self.triangle.get_first_edge())

    def testGetSecondEdge(self):
        self.assertEqual(self.test_edge2, self.triangle.get_second_edge())

    def testGetThirdEdge(self):
        self.assertEqual(self.test_edge3, self.triangle.get_third_edge())

    def testAreNeighbors(self):
        triangle_2 = Triangle(self.test_edge1, Edge(1, 1, 1, 4, 4, 4), Edge(4, 4, 4, 0, 0, 0))
        triangle_3 = Triangle(Edge(2, 2, 2, 1, 1, 1), Edge(1, 1, 1, 4, 4, 4), Edge(4, 4, 4, 2, 2, 2))
        self.assertTrue(Triangle.are_neighbors(self.triangle, self.triangle))
        self.assertTrue(Triangle.are_neighbors(self.triangle, triangle_2))
        self.assertFalse(Triangle.are_neighbors(self.triangle, triangle_3))

    def testMacthTriangleIndices(self):
        triangles = [self.triangle]
        invalid_edge = Edge(5, 4, 3, 2, 0, 0)
        self.assertCountEqual(Triangle.match_triangle_indices(self.test_edge1, triangles), [0])
        self.assertCountEqual(Triangle.match_triangle_indices(invalid_edge, triangles), [])
