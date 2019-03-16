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
import re
from pyrr import *
from src.rendering.camera import Camera
from OpenGL import GL


class RenderingEngine:
    """Contains static rendering context information for OpenGL
    """
    projection = matrix44.create_perspective_projection_matrix(75.0, 4/3, 0.1, 100.0)
    camera = Camera("default")

    @staticmethod
    def gl_version():
        """Returns the current OpenGL version string as specified by the
        OpenGL drivers.
        """
        return GL.glGetString(GL.GL_VERSION)

    @staticmethod
    def glsl_version():
        """Returns the GLSL version string.
        """
        return GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)

    @staticmethod
    def glsl_version_major_minor():
        """Returns the GLSL version as a tuple.

        :return: The major and minor version strings as an array [major, minor].
        """
        return RenderingEngine._gl_retrieve_versions(RenderingEngine.glsl_version())

    @staticmethod
    def gl_version_major_minor():
        """Retrieve the OpenGL Major and Minor version.

        :return: An array of the OpenGL Major and Minor version. [Major, Minor]
        """
        return RenderingEngine._gl_retrieve_versions(RenderingEngine.gl_version())

    @staticmethod
    def _gl_retrieve_versions(version):
        """Extracts the major and minor versions from an OpenGL version string.
        Can handle driver's appending their specific driver version to the string.
        """
        # version is guaranteed to be 'MAJOR.MINOR<XXX>'
        # there can be a 3rd version
        version = version.decode("utf-8")
        versions = re.split(r'[\.\s\-]', version)
        return [int(versions[0]), int(versions[1])]
