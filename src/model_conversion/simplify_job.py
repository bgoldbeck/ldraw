# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.

from src.threading.base_job import BaseJob
from src.model_conversion.model_shipper import ModelShipper
import src.model_conversion.mesh_triangulation as MeshTriangulation
from src.model_conversion.ldraw_model import LDrawModel


class SimplifyJob(BaseJob):
    """This job simplifies the mesh
    """
    def __init__(self, feedback_log):
        super().__init__(feedback_log)
        self.name = "mesh simplification"

    def do_job(self):
        self.update_status("Starting " + self.name + ".")
        self.is_running.wait()
        # Setting output model as input LDraw object
        mesh = None # The mesh to be converted
        if not self.is_killed:
            model = ModelShipper.input_model
            mesh = model.get_mesh()

        self.is_running.wait()
        if not self.is_killed:
            # Step 1: Create list of triangle objects from mesh
            self.update_status("Separating faces...")
            triangles = MeshTriangulation.get_mesh_triangles(mesh)

        self.is_running.wait()
        if not self.is_killed:
            # Step 2: Group triangles by their normals
            normal_groups = MeshTriangulation.make_normal_groups(triangles)

        self.is_running.wait()
        if not self.is_killed:
            # Group normal groups into faces (by connected parts)
            faces = MeshTriangulation.make_face_groups_loop(normal_groups)

        self.is_running.wait()
        if not self.is_killed:
            # Step 3: Get only outline edges for each face
            self.update_status("Simplifying faces...")
            face_boundaries, face_normals = MeshTriangulation.make_face_boundaries(
                faces)

        self.is_running.wait()
        if not self.is_killed:
            # Simplify outline edges for each face (remove redundant vertices)
            simple_boundaries = MeshTriangulation.make_simple_boundaries(
            face_boundaries)

        self.is_running.wait()
        if not self.is_killed:
            # Split each outline by connected parts
            separate_boundaries = MeshTriangulation.split_boundaries(
                simple_boundaries)

        self.is_running.wait()
        if not self.is_killed:
            # Rearranges edges in each face so that outer edge at index 0
            ordered_separate_boundaries = MeshTriangulation.find_outside_boundary(
                separate_boundaries)

        self.is_running.wait()
        if not self.is_killed:
            self.update_status("Triangulating...")
            # Convert output data to different format
            triangulated_faces = MeshTriangulation.buckets_to_dicts(
                ordered_separate_boundaries)

        # Triangulate each face
        triangulations = []
        for face in triangulated_faces:
            self.is_running.wait()
            if not self.is_killed:
                triangulations.append(MeshTriangulation.triangulate(face))
            else:
                break

        self.is_running.wait()
        if not self.is_killed:
            self.update_status("Recombining into mesh...")
            # Convert to a mesh
            simple_model = MeshTriangulation.triangulation_to_mesh(triangulations,
                                                                   face_normals)
            ModelShipper.output_model = LDrawModel(mesh=simple_model)

        self.is_running.wait()
        if not self.is_killed: # Job completed (not killed)
            self.update_status("Finished " + self.name + ".")

        else:  # Job was killed
            # do any cleanup before exiting
            self.update_status("Cancelled during " + self.name + ".")

        self.is_done.set()  # Set this so thread manager knows job is done
