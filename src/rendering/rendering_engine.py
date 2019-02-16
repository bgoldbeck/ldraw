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
from src.rendering.camera import Camera


class RenderingEngine:
    """Contains static rendering context information for OpenGL
    """
    projection = matrix44.create_perspective_projection_matrix(75.0, 4/3, 0.1, 100.0)
    camera = Camera("default")
