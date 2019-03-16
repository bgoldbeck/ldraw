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
from OpenGL.GL import *
from src.rendering.basic_material import BasicMaterial
from src.rendering.scene_object import SceneObject
from src.rendering.rendering_engine import RenderingEngine


class BasicMeshObject(SceneObject):
    """This class serves as a derived class for a SceneObject that contains mesh data
    for OpenGL rendering context.
    """

    def __init__(self, tag, mesh):
        """Constructor for a BasicMeshObject.

        :param tag: The tag str to recognize this object.
        :param mesh: The Mesh object to use for OpenGL rendering.
        """
        SceneObject.__init__(self, tag)
        self.mesh_data = mesh

        triangle_data = []
        for i in range(len(self.mesh_data.normals)):
                triangle_data.append(self.mesh_data.v2[i][0])
                triangle_data.append(self.mesh_data.v2[i][1])
                triangle_data.append(self.mesh_data.v2[i][2])
                triangle_data.append(0.000059)
                triangle_data.append(1.0 - 0.000059)
                triangle_data.append(self.mesh_data.normals[i][0])
                triangle_data.append(self.mesh_data.normals[i][1])
                triangle_data.append(self.mesh_data.normals[i][2])
                triangle_data.append(self.mesh_data.v1[i][0])
                triangle_data.append(self.mesh_data.v1[i][1])
                triangle_data.append(self.mesh_data.v1[i][2])
                triangle_data.append(0.000103)
                triangle_data.append(1.0 - 0.336048)
                triangle_data.append(self.mesh_data.normals[i][0])
                triangle_data.append(self.mesh_data.normals[i][1])
                triangle_data.append(self.mesh_data.normals[i][2])
                triangle_data.append(self.mesh_data.v0[i][0])
                triangle_data.append(self.mesh_data.v0[i][1])
                triangle_data.append(self.mesh_data.v0[i][2])
                triangle_data.append(0.335973)
                triangle_data.append(1.0 - 0.335903)
                triangle_data.append(self.mesh_data.normals[i][0])
                triangle_data.append(self.mesh_data.normals[i][1])
                triangle_data.append(self.mesh_data.normals[i][2])
        if glInitGl42VERSION():
            RenderingEngine.opengl_success = True
            self.vao = glGenVertexArrays(1)

            self.bind()
            self.material = BasicMaterial(numpy.array(triangle_data, dtype=numpy.float32))
            self.unbind()
        else:
            RenderingEngine.opengl_success = False

    def bind(self):
        """Bind the vertex array object.

        :return: None
        """
        if RenderingEngine.opengl_success:
            glBindVertexArray(self.vao)

    def unbind(self):
        """Unbind the vertex array object.

        :return:
        """
        if RenderingEngine.opengl_success:
            glBindVertexArray(0)

    def draw(self):
        """Draw the vertex buffer.

        :return: None
        """
        if RenderingEngine.opengl_success:
            self.bind()
            glDrawArrays(GL_TRIANGLES, 0, len(self.mesh_data.normals) * 3)
            self.unbind()

    def update(self):
        """Update the material values for the vertex buffers.

        :return: None
        """
        if RenderingEngine.opengl_success:
            self.material.set_view_matrix(RenderingEngine.camera.get_view_matrix())
            self.material.set_model_matrix(self.transform.get_trs_matrix())

    def get_mesh_data(self):
        """Retrieve the stored mesh data.

        :return: The Mesh data stored in this object.
        """
        return self.mesh_data
