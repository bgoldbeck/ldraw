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
from src.model_conversion.edge import Edge


class UniqueEdgeList:
    """This class is a container for unique edges composed in a list format.
    """

    def __init__(self):
        """Constructor that makes a UniqueEdgeList.
        """
        self.edge_list = []

    def remove(self, edge_to_remove: Edge):
        """Attempt to remove an edge from the list of edges.

        :param edge_to_remove: The edge to search for.
        :return: True, if the edge was removed.
        """
        index_found = -1

        for i in range(len(self.edge_list)):
            if Edge.same_edge(self.edge_list[i], edge_to_remove):
                index_found = i

        if index_found != -1:
            del self.edge_list[index_found]

        return index_found is not -1

    def add(self, new_edge: Edge):
        """Add a new edge to this list, but only if it isn't in there already.

        :param new_edge: The new edge to add to the set.
        :return: True, if the new edge was added.
        """
        found = False
        for e in self.edge_list:
            if Edge.are_overlapping_edges(new_edge, e):
                found = True
                break

        if not found:
            self.edge_list.append(new_edge)

        return not found

    @staticmethod
    def set_difference(a, b):
        """This returns a list of edges in set 'a' that aren't in set 'b'.

        :param a: The first set.
        :param b: The second set.
        :return: A list of edges in set 'a' that aren't in set 'b'.
        """
        result = UniqueEdgeList()
        new_edge_list = []
        for edge_in_a in a.edge_list:
            found = False
            for edge_in_b in b.edge_list:
                if Edge.same_edge(edge_in_a, edge_in_b):
                    found = True
            if not found:
                new_edge_list.append(edge_in_a)
        result.edge_list = new_edge_list
        return result

    def to_vertex_array(self):
        return [[]]

    def display(self):
        for edge in self.edge_list:
            edge.display()

    def get_neighbor_indices_for_edge(self, edge: Edge):
        result = []
        for i in range(len(self.edge_list)):
            if Edge.has_shared_vertex(edge, self.edge_list[i]):
                result.append(i)
        return result


