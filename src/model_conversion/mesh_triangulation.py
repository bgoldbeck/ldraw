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
import triangle as tr
from stl import Mesh
from src.model_conversion.edge import Edge
from src.model_conversion.unique_edge_list import UniqueEdgeList
from src.model_conversion.triangle import Triangle
from src.model_conversion.face import Face


def get_mesh_triangles(mesh: Mesh):
    """
    Converts the mesh to Triangle objects
    :return: List of Triangles
    """
    mesh_triangles = []  # array of Triangles
    for data in mesh.data:
        normal = get_unit_normal(data[0])  # data[0] contains normal value eg: [0, 0, 4]
        vertex_1 = data[1][0]
        vertex_2 = data[1][1]
        vertex_3 = data[1][2]
        edge_1 = Edge(vertex_1[0], vertex_1[1], vertex_1[2], vertex_2[0], vertex_2[1], vertex_2[2])
        edge_2 = Edge(vertex_2[0], vertex_2[1], vertex_2[2], vertex_3[0], vertex_3[1], vertex_3[2])
        edge_3 = Edge(vertex_3[0], vertex_3[1], vertex_3[2], vertex_1[0], vertex_1[1], vertex_1[2])
        mesh_triangles.append(Triangle(edge_1, edge_2, edge_3, normal=normal))
    return mesh_triangles


def get_unit_normal(normal):
    """
    Calculate the unit normal of a normal.
    Eg: Unit normal of [0, 0, 4] is [0, 0, 1]
    :param normal:
    :return: List of normal vertices
    """
    squared_length = 0
    for vertex in normal:
        squared_length += vertex ** 2
    length = math.sqrt(squared_length)
    unit_normal = list(map(lambda x: x / length, normal))
    return unit_normal


def make_normal_groups(triangles: []):
    """
    Group triangles by normal
    :param triangles: List of Triangles
    :return: List of List of Triangles
    """
    triangles_groups = []
    origin = (0.0, 0.0, 0.0)
    group_match = False
    for triangle in triangles:
        for group in triangles_groups:
            group_normal = group[0].normal  # Normal of first triangle in the group
            triangle_normal = triangle.normal
            origin_group_normal_edge = Edge(origin[0], origin[1], origin[2], group_normal[0], group_normal[1], group_normal[2])
            origin_triangle_normal_edge = Edge(origin[0], origin[1], origin[2], triangle_normal[0], triangle_normal[1], triangle_normal[2])
            if Edge.are_parallel(origin_group_normal_edge, origin_triangle_normal_edge, tolerance=0.01):
                group_match = True
                group.append(triangle)
                break
        if not group_match:
            triangles_groups.append([triangle])
        group_match = False
    return triangles_groups


def make_face_groups_loop(normal_groups):
    """
    Take the list of normal groups as input. Return a list of faces.
    :param normal_groups:
    :return: a list of faces
    """
    list_faces = []
    while normal_groups:
        n_g = normal_groups.pop()
        while n_g:
            triangle = n_g.pop()
            f = Face([triangle])
            # Get all neighbor:
            flag = True
            while flag:
                flag = False
                for e_triangle in n_g:
                    if f.has_neighbor_improved(e_triangle):
                        f.add_triangle(e_triangle)
                        n_g.remove(e_triangle)
                        flag = True
            """
            triangle_list = f.get_triangles()
            for e_triangle in triangle_list:
                if e_triangle in n_g:
                    n_g.remove(e_triangle)
            """
            list_faces.append(f)
    return list_faces


def make_face_boundaries(faces: []):
    """Step 2. Remove shared edges.
    :param faces: List of faces.
    :return: List of a list of edges where each list of edges is the edges that
    were not shared in that face.
    """
    # Faces is a list of faces, where faces are composed of triangles on the same plane and
    # have some edge connecting them.
    # faces.count() should return the number of planes on an object IE: A cube has 6 faces.
    output = []
    normals = []
    k = -1
    for face in faces:
        shared_edges = UniqueEdgeList()
        all_edges_in_face = face.get_edges()

        # len(face.triangles) should return the # of triangles in the face.
        while len(face.triangles) > 0:
            for m in range(len(face.triangles)):
                for n in range(len(face.triangles)):
                    if m is not n:
                        for i in range(3):
                            for j in range(3):
                                # Compare an edge in triangle "m" vs the 3 other edges in
                                # triangle "n"
                                if Edge.are_overlapping_edges(face.triangles[m].edges[i],
                                                              face.triangles[n].edges[j]):
                                    shared_edges.add(face.triangles[m].edges[i])

                face.triangles.pop(m)
                break

        k += 1
        normals.append(face.get_normal())
        output.append(UniqueEdgeList())
        output[k] = UniqueEdgeList.set_difference(all_edges_in_face, shared_edges)

    return output, normals


def make_simple_boundaries(grouped_edges):
    """
    #Step 3
    :param grouped_edges: A list of list of edges, grouped by connectivity between edges.
    :return: List of a list of edges where each list of edges have been simplified. Connecting
    edges that were parallel are joined together.
    """
    output = []
    for outline_edge_group in grouped_edges:
        edge_list = UniqueEdgeList()
        output.append(make_simple_boundary(edge_list, outline_edge_group))

    return output


def make_simple_boundary(outline_edge_group: UniqueEdgeList, all_edges: UniqueEdgeList):
    """
    Step 3 recursive
    :param outline_edge_group: A list of edges, grouped by connectivity between edges.
    :param all_edges:
    :return: ???
    """
    while len(all_edges.edge_list) > 0:
        current_edge = all_edges.edge_list[0]

        work = False
        neighbors = all_edges.get_neighbor_indices_for_edge(current_edge)

        # Loop against all neighboring edges, gobble up the neighbors.
        for neighbor in neighbors:
            neighbor_edge = all_edges.edge_list[neighbor]

            if not Edge.same_edge(current_edge, neighbor_edge):
                shared_vertex = Edge.has_shared_vertex(current_edge, neighbor_edge)
                parallel = Edge.are_parallel_or_anti_parallel(current_edge, neighbor_edge)

                if shared_vertex is not None and parallel:

                    # Case 1.
                    start_vertex = [neighbor_edge.x1, neighbor_edge.y1, neighbor_edge.z1]

                    # Case 2.
                    if (neighbor_edge.x1 == shared_vertex[0] and
                            neighbor_edge.y1 == shared_vertex[1] and
                            neighbor_edge.z1 == shared_vertex[2]):
                        start_vertex = [neighbor_edge.x2, neighbor_edge.y2, neighbor_edge.z2]

                    # Case 3.
                    end_vertex = [current_edge.x1, current_edge.y1, current_edge.z1]

                    # Case 4.
                    if (current_edge.x1 == shared_vertex[0] and
                            current_edge.y1 == shared_vertex[1] and
                            current_edge.z1 == shared_vertex[2]):
                        end_vertex = [current_edge.x2, current_edge.y2, current_edge.z2]

                    new_edge = Edge(start_vertex[0], start_vertex[1], start_vertex[2],  # Edge Start
                                    end_vertex[0], end_vertex[1], end_vertex[2])  # Edge end

                    all_edges.remove(current_edge)
                    all_edges.remove(neighbor_edge)
                    all_edges.add(new_edge)

                    work = True
                    break

        if not work and len(all_edges.edge_list) > 0:
            outline_edge_group.add(current_edge)
            all_edges.remove(current_edge)

    return outline_edge_group


def split_boundaries(grouped_edges):
    """
    Step 3 part 2
    Splits each outline into groups by connectivity. If a face has holes, its
    outline would be split into multiple groups
    :param grouped_edges: A list of UniqueEdgeLists that compose the edges of a face.
    :return:
    """
    buckets = []

    for group in grouped_edges:
        if len(group.edge_list) > 0:
            current_edge_list = UniqueEdgeList()
            current_edge_list.add(group.edge_list[0])

            unique_edge_lists = split_boundary([current_edge_list], group, 0)

            buckets.append(unique_edge_lists)

    return find_outside_boundary(buckets)


def split_boundary(unique_edge_lists: [], all_edges: UniqueEdgeList, i: int):
    """
    Step 3 part 2 recursive
    :param unique_edge_lists:
    :param all_edges:
    :param i:
    :return:
    """
    i = 0
    j = 0

    while len(all_edges.edge_list) > 0:
        current_edge_in_bucket = unique_edge_lists[i].edge_list[j]
        work = False

        for e in all_edges.edge_list:
            if (not Edge.same_edge(e, current_edge_in_bucket)) and \
                    (Edge.has_shared_vertex(e, current_edge_in_bucket) is not None):
                if unique_edge_lists[i].add(e):
                    work = True

        # Remove all_edges from list that exist in bucket.
        for e in unique_edge_lists[i].edge_list:
            all_edges.remove(e)

        if work is False:
            if len(all_edges.edge_list) > 0:
                new_edge_list = UniqueEdgeList()
                new_edge_list.add(all_edges.edge_list[0])
                all_edges.edge_list.pop(0)
                unique_edge_lists.append(new_edge_list)
                i += 1
                j = 0
        else:

            j += 1

    return unique_edge_lists


def find_outside_boundary(buckets):
    """
    find_outside_boundary (put outside outline at index 0)
    :param buckets:
    :return:
    """
    # output_step_3_part_3: Contains a list of "buckets", where each bucket contains a list of

    for bucket in buckets:
        outer_boundary_index = 0
        max_dist_to_origin = -1.0
        for i in range(len(bucket)):
            boundary = bucket[i]
            for edge in boundary.edge_list:
                origin_to_start = Edge(0, 0, 0, edge.x1, edge.y1, edge.z1)
                origin_to_end = Edge(0, 0, 0, edge.x2, edge.y2, edge.z2)

                if origin_to_start.length() > max_dist_to_origin:
                    max_dist_to_origin = origin_to_start.length()
                    outer_boundary_index = i

                if origin_to_end.length() > max_dist_to_origin:
                    max_dist_to_origin = origin_to_end.length()
                    outer_boundary_index = i

        if outer_boundary_index > 0:
            # Swap list[outer_boundary_index] and list[0]
            bucket[outer_boundary_index], bucket[0] = bucket[0], bucket[outer_boundary_index]

    return buckets


def buckets_to_dicts(buckets):
    """
    Convert the output from previous steps into a form that can be used by
    triangulation library.

    :param buckets: List of lists of lists.... of edges
    :return:List of face dictionaries. Each dict has 'segments' (edges),
    'vertices', and 'holes' keys.
    """

    # Need to transform current edges into list of indices referencing vertex list
    faces = []

    for face in buckets:
        # Dictionary where keys are unique vertices, values = index of vert list
        vert_dict = {}

        new_face = {}  # dict with edge, vert, and hole lists
        vert_list = []  # all unique verts in this face
        edge_list = []  # all edges in this face.
        # Each edge is of form [a,b] where a and b are index of vert_list
        hole_list = []  # 1 interior point for every hole on this face

        for b in range(len(face)):  # each boundary
            boundary_edges = []  # edges for current boundary

            for edge in face[b].edge_list:
                v1 = (edge.x1, edge.y1, edge.z1)
                v2 = (edge.x2, edge.y2, edge.z2)
                # if verts aren't in dictionary, add them to both vert list and dict
                # key value will be index of that vert in the vert list
                if v1 not in vert_dict:
                    vert_dict[v1] = len(vert_list)
                    vert_list.append(v1)
                if v2 not in vert_dict:
                    vert_dict[v2] = len(vert_list)
                    vert_list.append(v2)

                boundary_edges.append([vert_dict[v1], vert_dict[v2]])

            if b > 0:  # This boundary is a hole
                # Get an interior point by triangulating and finding centroid
                hole = {"vertices": np.asarray(vert_list),
                        "segments": np.asarray(boundary_edges)}

                tri_hole = triangulate(hole)
                hole_coord = find_inner_point(tri_hole)
                hole_list.append(hole_coord)

            edge_list += boundary_edges  # add boundary edges to all face edges

        new_face["segments"] = np.asarray(edge_list)
        new_face["holes"] = np.asarray(hole_list)
        new_face["vertices"] = np.asarray(vert_list)
        faces.append(new_face)

    return faces


def triangulate(face):
    """
    Does triangulation of face in 3D. Does 2D projection, triangulates, and
    returns points to 3D

    :param face: Dictionary representing face outline. Each dict has
    'segments' (edges), 'vertices', and 'holes' keys.
    :return: Dictionary representing triangulated face. Has keys 'vertices'
    with xyz coordinates, and 'triangles', a list of 3 tuples referencing vertex
    indices
    """
    has_holes = False
    if "holes" in face and len(face['holes']) > 0:
        has_holes = True

    # Take 3 points from vertex list
    # Since all points should lie on a plane, triangle v1,v2,v3 lies on same plane
    v1 = face['vertices'][0]
    v2 = face['vertices'][1]
    v3 = face['vertices'][2]

    face_normal = np.cross(v2 - v1, v3 - v1)
    new_normal = face_normal / np.sqrt(face_normal.dot(face_normal))

    # Identity matrices
    rot_matrix = np.identity(3)
    rev_matrix = np.identity(3)

    # If plane is straight up/down, need to rotate it for projection
    if abs(face_normal[2]) < .1:
        if abs(face_normal[0]) < abs(face_normal[1]):
            # Checks which normal component (x/y) is lesser, and rotates 90 deg on that axis
            # This causes least distortion for projection
            # rotating 90 degrees x
            rot_matrix = np.array([[1.0, 0.0, 0.0],
                                   [0.0, 0.0, -1.0],
                                   [0.0, 1.0, 0.0]])

            rev_matrix = np.array([[1.0, 0.0, 0.0],
                                   [0.0, 0.0, 1.0],
                                   [0.0, -1.0, 0.0]])
        else:
            # rotating 90 degrees y
            rot_matrix = np.array([[0.0, 0.0, 1.0],
                                   [0.0, 1.0, 0.0],
                                   [-1.0, 0.0, 0.0]])

            rev_matrix = np.array([[0.0, 0.0, -1.0],
                                   [0.0, 1.0, 0.0],
                                   [1.0, 0.0, 0.0]])

    # Do rotation (this is none, if plane is not upright)
    face_verts_xyz = face['vertices']
    face_verts_xyz = np.dot(face_verts_xyz, rot_matrix)
    if has_holes:
        hole_verts_xyz = face['holes']
        hole_verts_xyz = np.dot(hole_verts_xyz, rot_matrix)

    # Make planar straight line graph, only take xy coords of vertices
    pslg = {'vertices': face_verts_xyz[:,:2],
            'segments': face['segments']}

    if has_holes:
        pslg['holes'] = hole_verts_xyz[:, :2] #WOW

    triangulation = tr.triangulate(pslg, opts='p')

    # Reverse rotation if any
    face_verts_xyz = np.dot(face_verts_xyz, rev_matrix)

    return {'vertices': face_verts_xyz,
            'triangles': triangulation['triangles']}


def find_inner_point(triangulation):
    """
    Finds a point inside a mesh surface (not on a boundary)
    :param triangulation: Dictionary containing list of vertices, and triangles
    referencing those vertices
    :return: [x,y,z] coordinate representing a hole
    """

    tri_coords = []

    for i in range(len(triangulation['triangles'][0])):
        index = triangulation['triangles'][0][i]
        tri_coords.append(triangulation['vertices'][index])

    tri_coords = np.asarray(tri_coords)
    centroid = tri_coords.mean(axis=0)
    return centroid


def triangulation_to_mesh(triangulations, normals):
    """

    :param triangulations:
    :param normals:
    :return:
    """
    meshes = []
    for i in range(len(triangulations)):
        tri_count = len(triangulations[i]['triangles'])  # Number of triangles

        # load triangulation data into a mesh format (list of triangles)
        out_data = np.zeros(tri_count, dtype=Mesh.dtype)
        for tri_num in range(tri_count):

            # Make new tri and load in the 3 vertices
            new_tri = []
            for vert in triangulations[i]['triangles'][tri_num]:
                new_tri.append(triangulations[i]['vertices'][vert])

            # Calculate normal of new tri
            new_normal = np.cross(new_tri[1] - new_tri[0], new_tri[2] - new_tri[0])
            new_normal = new_normal / np.sqrt(new_normal.dot(new_normal))
            flipped_normal = -1*new_normal

            # Check if the normal is different than original face normal
            new_dif = np.sum(abs(normals[i] - new_normal))
            flipped_dif = np.sum(abs(normals[i] - flipped_normal))

            new_tri = np.asarray(new_tri)

            if flipped_dif < new_dif:
                # Reverse order of vertices to flip tri normal
                new_tri = np.flip(new_tri, axis=0)

            out_data['vectors'][tri_num] = new_tri

        meshes.append(out_data)

    meshes = np.concatenate(meshes)  # combine all mesh vertices to one object
    new_mesh = Mesh(meshes.copy())   # create mesh object from triangle data
    return new_mesh
