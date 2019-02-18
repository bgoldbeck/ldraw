# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
from src.rendering.tranform import Transform


class SceneObject:
    """A scene object that is part of the scene.
    """
    def __init__(self, tag):
        """Constructor for a scene object.

        :param tag: The tag is used to easily find the object in the dictionary.
        """
        self.transform = Transform()
        self.tag = tag
        self.enabled = False

    def enable(self):
        """Enable this scene object.

        :return: None
        """
        self.enabled = True

    def disable(self):
        """Disable this scene object.

        :return: None
        """
        self.enabled = False
