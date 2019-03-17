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
from stl import Mesh
from src.util import Util
from src.model_conversion.face import *
from src.model_conversion.edge import Edge
from src.model_conversion.mesh_triangulation import get_unit_normal


class TestFace(unittest.TestCase):

    def setUp(self):
        mesh = Mesh.from_file(Util.path_conversion("tests/test_models/2_holes.stl"))
        mesh_triangles = []  # array of Triangles
        self.triangles_count = 0
        for data in mesh.data:
            normal = get_unit_normal(data[0])
            vertex_1 = data[1][0]
            vertex_2 = data[1][1]
            vertex_3 = data[1][2]
            edge_1 = Edge(vertex_1[0], vertex_1[1], vertex_1[2], vertex_2[0], vertex_2[1], vertex_2[2])
            edge_2 = Edge(vertex_2[0], vertex_2[1], vertex_2[2], vertex_3[0], vertex_3[1], vertex_3[2])
            edge_3 = Edge(vertex_3[0], vertex_3[1], vertex_3[2], vertex_1[0], vertex_1[1], vertex_1[2])
            self.triangles_count += 1
            mesh_triangles.append(Triangle(edge_1, edge_2, edge_3, normal=normal))
        self.face = Face(mesh_triangles)
        self.normal = [0, 0, 1]

    def testMatchNormal(self):
        self.assertTrue(self.face.match_normal(self.normal))
        self.assertFalse(self.face.match_normal([0, 1, 0]))

    def testCount(self):
        self.assertEqual(self.face.count(), self.triangles_count)

    def testAddTriangle(self):
        test_edge1 = Edge(-1, 1, 1, 1, 1, 1)
        test_edge2 = Edge(1, 1, 1, 1, 1, -1)
        test_edge3 = Edge(1, 1, -1, -1, 1, 1)
        triangle = Triangle(test_edge1, test_edge2, test_edge3, self.normal)
        triangles_count_before = self.face.count()
        self.face.add_triangle(triangle)
        triangles_count_after = self.face.count()
        change = triangles_count_after - triangles_count_before
        self.assertEqual(change, 1)

    def testGetNormal(self):
        self.assertCountEqual(self.face.get_normal(), self.normal)

    def testHasNeighbor(self):
        test_triangle = self.face.triangles[0]
        self.assertTrue(self.face.has_neighbor(test_triangle))

    def testSetDifference(self):
        face_triangles = self.face.triangles
        set_1 = [face_triangles[0], face_triangles[1]]
        set_2 = [face_triangles[0], face_triangles[2]]
        self.assertEqual(len(Face.set_difference(set_1, set_2)), 1)
