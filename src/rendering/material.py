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
from OpenGL.GL import *
from pyrr import Vector3


class Material:
    """Base material class for handling a shader object.
    """
    def __init__(self):
        self.shader = None

    def set_uniform_matrix4fv(self, key, value):
        """Set a shader matrix 4x4 float at key with value.

        :param key: The key to search for.
        :param value: The matrix value to set.
        :return: None
        """
        # TODO: ensure key is a valid string. ensure value is a valid matrix 4x4
        assert self.shader is not None, "Shader program not set."
        glUniformMatrix4fv(glGetUniformLocation(self.shader, key), 1, GL_FALSE, value)

    def set_uniform1i(self, key, value):
        """Set a shader integer at key with value.

        :param key: The key to search for.
        :param value: The integer value.
        :return: None
        """
        assert self.shader is not None, "Shader program not set."
        glUniform1i(glGetUniformLocation(self.shader, key), value)

    def set_uniform1f(self, key, value):
        """Set a shader float at key with value.

        :param key: The key to search for.
        :param value: The float value.
        :return: None
        """
        assert self.shader is not None, "Shader program not set."
        glUniform1f(glGetUniformLocation(self.shader, key), value)

    def set_uniform2f(self, key, x, y):
        """Set a shader vec2 with x, and y values.

        :param key: The key to search for.
        :param x: The x float value.
        :param y: The y float value.
        :return: None
        """
        assert self.shader is not None, "Shader program not set."
        glUniform2f(glGetUniformLocation(self.shader, key), x, y)

    def set_uniform3f(self, key, value: Vector3):
        """Set a shader vec3 value.

        :param key: The key to search for.
        :param value: A Vector containing the x, y, z float values.
        :return: None
        """
        assert self.shader is not None, "Shader program not set."
        glUniform3f(glGetUniformLocation(self.shader, key),
                    value[0],
                    value[1],
                    value[2])
