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
from src.rendering.scene_object import SceneObject
from src.rendering.tranform import Transform
from math import sin, cos, radians
import math


# Code is attributed to totex/PyOpenGL_season_02
# -Attila Toth from GitHub.
class Camera(SceneObject):
    def __init__(self, tag):
        """The class that contains information about a camera object for the OpenGL Rendering Scene.
        """
        SceneObject.__init__(self, tag)
        self.transform.position = Vector3([0.0, 0.0, 3.0])
        self.target = Vector3([0.0, 0.0, 0.0])
        self.mouse_sensitivity = 0.25
        self.transform.eulerAngles = Vector3([0.0, 0.0, 0.0])
        self.transform.forward = Vector3([0.0, 0.0, 1.0])
        self.pitch = 89.9999
        self.yaw = -89.9999
        self.follow_distance = 4.0

    def get_view_matrix(self):
        """Get the cameras view matrix.

        :return: The Matrix44 representaiton for the view matrix.
        """
        return matrix44.create_look_at(self.transform.position, self.target, self.transform.up)

    def draw(self):
        """Camera doesn't need to draw anything.

        :return: None
        """
        pass

    def update(self):
        """Update the camera's transform based on the current pitch and yaw rotation.

        :return: None
        """
        front = Vector3([0.0, 0.0, 0.0])
        front[0] = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front[1] = sin(radians(self.pitch))
        front[2] = sin(radians(self.yaw)) * cos(radians(self.pitch))

        self.transform.forward = vector.normalise(front)
        self.transform.right = vector.normalise(vector3.cross(self.transform.forward, Vector3([0.0, 1.0, 0.0])))
        self.transform.up = vector.normalise(vector3.cross(self.transform.right, self.transform.forward))
        self.transform.position = self.transform.forward * -self.follow_distance
