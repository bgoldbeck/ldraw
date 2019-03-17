# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
from src.model_conversion.triangle import Triangle
from src.model_conversion.unique_edge_list import UniqueEdgeList


class Face:
    """
    A face is a group of triangles that share same normal and are connected to each other.
    """

    def __init__(self, triangles=None):
        """

        :param triangles: list of Triangles
        """
        if triangles:
            self.triangles = triangles
            self.normal = triangles[0].get_normal()
        else:
            self.triangles = []
            self.normal = None

    def match_normal(self, normal):
        """Checks if the given normal matches the Face's normal

        :param normal: [x, y, z]
        :return:
        """
        return self.normal == normal

    def count(self):
        """
        Counts the numbers of triangles in a face
        :return: Int value
        """
        return len(self.triangles)

    def add_triangle(self, triangle: Triangle):
        """
        Assuming the input triangle is the correct triangle (that is satisfying the face's condition)
        :param triangle:
        :return:
        """
        self.triangles.append(triangle)

    def remove_triangle(self, triangle_to_remove: Triangle):
        """

        :param triangle_to_remove: The triangle to attempt to remove.
        :return:
        """
        index_to_remove = -1

        for i in range(len(self.triangles)):
            if Triangle.are_equal(self.triangles[i], triangle_to_remove):
                index_to_remove = i
                break
        if index_to_remove != -1:
            self.triangles.pop(i)

        return index_to_remove != -1

    def has_neighbor(self, test_triangle: Triangle):
        """
        Checks if given triangle has a neighbor in the triangle group
        :param test_triangle: Triangle
        :return: True or False
        """
        for triangle in self.triangles:
            if Triangle.are_neighbors(triangle, test_triangle):
                return True
        return False

    def has_neighbor_improved(self, test_triangle: Triangle):
        """
        Checks if given triangle has a neighbor in the triangle group
        :param test_triangle: Triangle
        :return: True or False
        """
        for triangle in self.triangles:
            if Triangle.are_neighbors_improved(triangle, test_triangle):
                return True
        return False

    def get_normal(self):
        """
        Returns the normal value
        :return:
        """
        return self.normal

    def get_edges(self):
        """Gets all the edges of all the triangles in a Face

        :return:
        """
        result = UniqueEdgeList()
        for triangle in self.triangles:
            result.add(triangle.edges[0])
            result.add(triangle.edges[1])
            result.add(triangle.edges[2])
        return result

    def display_face(self):
        """
        Display all triangle of this face.
        """
        print("This face contain these triangle(s): \n")
        for triangle in self.triangles:
            triangle.display_triangle()

    def get_triangles(self):
        """

        :return: A list of triangle that this face hold.
        """
        return self.triangles

    @staticmethod
    def set_difference(group_1, group_2):
        """
        Returns groups from group_1 that are not in group_2 (group_1 - group_2)
        :param group_1: List of triangles
        :param group_2: List of triangles
        :return: list of triangles
        """

        triangles = []
        for triangle_a in group_1:
            found = False
            for triangle_b in group_2:
                if Triangle.are_equal(triangle_a, triangle_b):
                    found = True
                    break
            if not found:
                triangles.append(triangle_a)

        return triangles
