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
import copy
from stl import Mesh
from src.util import Util
import src.model_conversion.mesh_triangulation as MeshTriangulation


class TestMeshTriangulation(unittest.TestCase):
    model_folder = "tests/test_models/"

    @staticmethod
    def build_mesh_triangulation_data(file_path):
        mesh = Mesh.from_file(Util.path_conversion(file_path))
        triangles = MeshTriangulation.get_mesh_triangles(mesh)
        normal_groups = MeshTriangulation.make_normal_groups(triangles)
        normal_groups_copy = copy.deepcopy(normal_groups)
        faces = MeshTriangulation.make_face_groups_loop(normal_groups_copy)
        face_boundaries, normals = MeshTriangulation.make_face_boundaries(faces)
        simple_boundaries = MeshTriangulation.make_simple_boundaries(face_boundaries)
        separate_boundaries = MeshTriangulation.split_boundaries(simple_boundaries)
        ordered_separate_boundaries = MeshTriangulation.find_outside_boundary(separate_boundaries)
        triangulated_faces = MeshTriangulation.buckets_to_dicts(ordered_separate_boundaries)
        mesh_dict = {
            "input_mesh": mesh,
            "triangles": triangles,
            "normal_groups": normal_groups,
            "faces": faces,
            "separate_boundaries": separate_boundaries,
            "ordered_separate_boundaries": ordered_separate_boundaries,
            "triangulated_faces": triangulated_faces}

        return mesh_dict

    def test_mesh_triangulation(self):
        file_path = self.model_folder + "3001_dense.stl"
        mesh = Mesh.from_file(Util.path_conversion(file_path))

        # Step 1: Create list of triangle objects from mesh
        triangles = MeshTriangulation.get_mesh_triangles(mesh)

        # Step 2: Group triangles by their normals
        normal_groups = MeshTriangulation.make_normal_groups(triangles)

        # Group normal groups into faces (by connected parts)
        faces = MeshTriangulation.make_face_groups_loop(normal_groups)

        # Step 3: Get only outline edges for each face
        face_boundaries, face_normals = MeshTriangulation.make_face_boundaries(faces)

        # Simplify outline edges for each face (remove redundant vertices)
        simple_boundaries = MeshTriangulation.make_simple_boundaries(face_boundaries)

        # Split each outline by connected parts
        separate_boundaries = MeshTriangulation.split_boundaries(simple_boundaries)

        # Rearranges edges in each face so that outer
        ordered_separate_boundaries = MeshTriangulation.find_outside_boundary(separate_boundaries)

        triangulated_faces = MeshTriangulation.buckets_to_dicts(ordered_separate_boundaries)

        triangulations = []
        for face in triangulated_faces:
            triangulations.append(MeshTriangulation.triangulate(face))

        MeshTriangulation.triangulation_to_mesh(triangulations, face_normals)

    def test_simple_plane_triangles(self):
        file_path = self.model_folder + "simple_plane_on_xy_180_tris.stl"
        mesh = Mesh.from_file(Util.path_conversion(file_path))
        triangles = MeshTriangulation.get_mesh_triangles(mesh)
        self.assertTrue(len(triangles) == 180)

    def test_simple_plane_normal_groups(self):
        file_path = self.model_folder + "simple_plane_on_xy_180_tris.stl"
        mesh_dict = TestMeshTriangulation.build_mesh_triangulation_data(file_path)
        self.assertTrue(len(mesh_dict["normal_groups"]) == 1)

    def test_simple_plane_faces(self):
        file_path = self.model_folder + "simple_plane_on_xy_180_tris.stl"
        mesh_dict = TestMeshTriangulation.build_mesh_triangulation_data(file_path)
        self.assertTrue(len(mesh_dict["faces"]) == 1)

    def test_simple_plane_boundaries(self):
        file_path = self.model_folder + "simple_plane_on_xy_180_tris.stl"
        mesh_dict = TestMeshTriangulation.build_mesh_triangulation_data(file_path)
        ordered_separate_boundaries = mesh_dict["ordered_separate_boundaries"]
        self.assertTrue(len(ordered_separate_boundaries) == 1)
        self.assertTrue(len(ordered_separate_boundaries[0][0].edge_list) == 4)
