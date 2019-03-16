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
from pyrr import *
import math


class Transform:
    """The class that controls information about a transform.
    """
    euler_angles = Vector3([0.0, 0.0, 0.0])
    position = Vector3([0.0, 0.0, 0.0])
    scale = Vector3([1.0, 1.0, 1.0])

    forward = Vector3([0.0, 0.0, 1.0])
    up = Vector3([0.0, 1.0, 0.0])
    right = Vector3([1.0, 0.0, 0.0])

    def __init__(self):
        pass

    def translate(self, direction, distance):
        """Translate this transform a direction by a distance.

        :param direction: The direction to translate.
        :param distance: The distance to translate.

        :return: None
        """
        self.position += direction * distance

    def _get_rotation_matrix(self):
        """Retrieve the rotation matrix

        :return: Matrix44: The rotation matrix stored in this transform.
        """
        for i in range(0, 2):
            if self.euler_angles[i] >= 360.0:
                self.euler_angles[i] = 0.0
            if self.euler_angles[i] < 0.0:
                self.euler_angles[i] += 360.0

        angles = Vector3()
        angles[0] = self.euler_angles[0] * (math.pi / 180.0)
        angles[1] = self.euler_angles[1] * (math.pi / 180.0)
        angles[2] = self.euler_angles[2] * (math.pi / 180.0)

        return Matrix44.from_eulers(angles)

    def get_trs_matrix(self):
        """Retrieve the translation-rotation-scaling matrix

        :return: Matrix44: The translation-rotation-scaling matrix stored in this transform.
        """
        # Scale
        scale_matrix = Matrix44.from_scale(self.scale)

        # Rotate
        rs_matrix = scale_matrix * self._get_rotation_matrix()

        # Translate
        trs_matrix = rs_matrix * Matrix44.from_translation(self.position)

        return trs_matrix

    @staticmethod
    def world_forward():
        """Retrieve the default world forward vector.

        :return: Vector3: The world forward as a Vector3.
        """
        return Vector3([0.0, 0.0, 1.0])

    @staticmethod
    def world_up():
        """Retrieve the default world up vector.

        :return: Vector3: The world up as a Vector3.
        """
        return Vector3([0.0, 1.0, 0.0])

    @staticmethod
    def world_right():
        """Retrieve the default world right vector.

        :return: Vector3: The world right as a Vector3.
        """
        return Vector3([1.0, 0.0, 0.0])
