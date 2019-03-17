# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import math
import numpy as np


class Edge:
    """In geometry, an edge is a particular type of line segment joining two vertices in a polygon.
    We define an edge as having a start and an end point (Start 1) *----------->* (End 2)
    """

    def __init__(self, x1, y1, z1, x2, y2, z2):
        """Construct and edge from a set of points.

        :param x1: Start x component.
        :param y1: Start y component.
        :param z1: Start z component.
        :param x2: End x component.
        :param y2: End y component.
        :param z2: End z component.
        """
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

    def length(self):
        """Get the length or 'Magnitude' of the edge.

        :return: A floating point value of the length of the edge.
        """
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        dz = self.z2 - self.z1
        return np.power(
            np.power(dx, 2.0) +
            np.power(dy, 2.0) +
            np.power(dz, 2.0), .5)

    def get_vertices(self):
        """
        Give a list of vertices
        :return: 2 vertices of the edge.
        """
        list_vertices = []
        list_vertices.append([self.x1, self.y1, self.z1])
        list_vertices.append([self.x2, self.y2, self.z2])
        return list_vertices

    @staticmethod
    def shortest_distance(edge_1, edge_2):
        """

        :param edge_1:
        :param edge_2:
        :return: the distance between two edges
        """
        shortest_distance = 0
        # TODO: find the distant
        return shortest_distance

    @staticmethod
    def co_linear(edge_1, edge_2, tolerance_angel, tolerance_distance):
        """
        Check if 2 edges is co-linear.
        Instead of checking if 4 point is in same line, if both edges are parallel
        and the distance between them is 0 (has some tolerance), they are co-linear.
        :param edge_1:
        :param edge_2:
        :param tolerance_angel:
        :param tolerance_distance:
        :return:
        """
        if Edge.are_parallel(edge_1, edge_2, tolerance_angel):
            if Edge.shortest_distance(edge_1, edge_2) <= tolerance_distance:
                return True
        return False

    @staticmethod
    def dot(a, b):
        """Compute the dot product between two edges.

        :param a: First edge.
        :param b: Second edge.
        :return: A floating value that represents the dot product of two edges.
        """
        return (a.x2 - a.x1) * (b.x2 - b.x1) + \
               (a.y2 - a.y1) * (b.y2 - b.y1) + \
               (a.z2 - a.z1) * (b.z2 - b.z1)

    @staticmethod
    def same_edge(a, b):
        """Determine if two edges are the same.

        :param a: The first edge.
        :param b: The second edge.
        :return: True, if the edges are the same.
        """
        return ((a.x1 == b.x1) and
                (a.y1 == b.y1) and
                (a.z1 == b.z1) and
                (a.x2 == b.x2) and
                (a.y2 == b.y2) and
                (a.z2 == b.z2))

    @staticmethod
    def are_overlapping_edges(a, b):
        """Determine if two edges are overlapping.

        :param a: The first edge.
        :param b: The second edge.
        :return: True, if the edges are overlapping.
        """
        # Case 1. Exactly the same edges.
        if Edge.same_edge(a, b):
            return True

        # Case 2. Edges in opposite directions.
        if (  # 'a' start vs 'b' end
           (a.x1 == b.x2) and (a.y1 == b.y2) and (a.z1 == b.z2) and
            # 'b' start vs 'a' end
           (b.x1 == a.x2) and (b.y1 == a.y2) and (b.z1 == a.z2)):
            return True
        return False

    @staticmethod
    def has_shared_vertex(a, b):
        """Determine if two edges have a shared vertice.

        :param a: The first edge.
        :param b: The second edge.
        :return: True, if the edges share a vertex.
        """
        result = None

        # Case 1. End of a == Start of b
        if (a.x2 == b.x1) and (a.y2 == b.y1) and (a.z2 == b.z1):
            result = [a.x2, a.y2, a.z2]

        # Case 2. Start of a == Start of b
        elif (a.x1 == b.x1) and (a.y1 == b.y1) and (a.z1 == b.z1):
            result = [a.x1, a.y1, a.z1]

        # Case 3. Start of a == End of b
        elif (a.x1 == b.x2) and (a.y1 == b.y2) and (a.z1 == b.z2):
            result = [a.x1, a.y1, a.z1]

        # Case 4. End of a == End of b
        elif (a.x2 == b.x2) and (a.y2 == b.y2) and (a.z2 == b.z2):
            result = [a.x2, a.y2, a.z2]

        return result

    @staticmethod
    def are_parallel(a, b, tolerance):
        """Determine if two edges are parallel with tolerance angle
        Two edges are parallel if, Angle in in the range [-tolerance, +tolerance]

        :param a: The first edge.
        :param b: The second edge.
        :param tolerance: Tolerance angle to be close enough to parallel.
        :return: True, if two edges are either parallel.
        """
        dot = Edge.dot(a, b)
        ratio = np.round(dot / (a.length() * b.length()), 5)
        radians = np.arccos(ratio)
        angle = math.degrees(radians)

        return -tolerance <= angle <= tolerance

    @staticmethod
    def are_parallel_or_anti_parallel(a, b, tolerance=0.1):
        """Determine if two edges are parallel or anti-parallel.

        :param a: The first edge.
        :param b: The second edge.
        :param tolerance: Tolerance angle to be close enough to parallel.
        :return: True, if two edges are either parallel or anti-parallel.
        """
        dot = Edge.dot(a, b)
        ratio = np.round(dot / (a.length() * b.length()), 5)
        radians = np.arccos(ratio)
        angle = math.degrees(radians)

        return (-tolerance <= angle <= tolerance or
                (180-tolerance) <= angle <= (tolerance+180))

    def display(self):
        print("x1: " + str(self.x1) + ", y1: " + str(self.y1) + ", z1: " + str(self.z1) +
              " || , x2: " + str(self.x2) + ", y2: " + str(self.y2) + ", z2: " + str(self.z2) +
              " Length: " + str(self.length()))
