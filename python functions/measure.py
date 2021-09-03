import math
import sys

import numpy as np
import filter
import class_vision
import segmentation


# compute the shape with : area, perimeter, points, edges, bounding box,
def shape_points(im_original, im_object, flag, l_min, l_max, h_min, h_max):
    shape = class_vision.Shape()

    # flag of the region
    shape.set_flag(flag)

    # declaration of useful variables
    max_i = -1
    max_j = -1
    min_i = 999999
    min_j = 999999
    mean = 0

    points = []
    edges = []

    counter2 = 0

    for i in range(l_min, l_max):
        for j in range(h_min, h_max):
            # if we find an element from the shape
            if im_object[i][j][0] == flag:
                # we add the point to the attribute points of the shape
                points.append(class_vision.Point(i, j))
                if i < min_i:
                    min_i = i
                if j < min_j:
                    min_j = j
                if i > max_i:
                    max_i = i
                if j > max_j:
                    max_j = j

                # we sum the color
                mean = mean + im_original[i][j][0]

                # we count the number of neighbours, the border of the image are counted as neighbours
                neighbour = 0
                for n in range(i - 1, i + 2):
                    for m in range(j - 1, j + 2):
                        if l_min <= n <= l_max and h_min <= m <= h_max:
                            if im_object[n][m][0] != flag:
                                neighbour = neighbour + 1
                        else:
                            neighbour = neighbour + 1

                if neighbour > 0:
                    # we add the point to the attribute edges of the shape
                    edges.append(class_vision.Point(i, j))
                if neighbour > 1:
                    counter2 += 1

    if len(points) != 0 and len(edges) != 0 and max_i != -1 and max_j != -1 and min_i != 999999 and min_j != 999999:
        mean = mean / len(points)
        shape.set_mean_color(mean)
        shape.set_area(len(points))
        counter2 = (len(edges) + counter2) / 2
        shape.set_perimeter(counter2)

        # bounding box
        bb = []

        # lower on the left
        p1 = class_vision.Point(min_i, min_j)
        # lower on the right
        p2 = class_vision.Point(max_i, min_j)
        # upper on the right
        p3 = class_vision.Point(max_i, max_j)
        # upper on the left
        p4 = class_vision.Point(min_i, max_j)

        # we add the points to the bounding box
        bb.append(p1)
        bb.append(p2)
        bb.append(p3)
        bb.append(p4)

        # we sort the points and the edges
        edges = sorted(edges[0:], key=lambda p: p.get_j())
        points = sorted(points[0:], key=lambda p: p.get_j())

        shape.set_bb(bb)
        shape.set_points(points)
        shape.set_edges(edges)
    else:
        print("There is no shape")
    return shape


# vector
def vector(i1, j1, i2, j2):
    i = i2 - i1
    j = j2 - j1
    return i, j


# norm
def norm(i, j):
    return math.sqrt(i * i + j * j)


# scalar product
def scalar_product(i1, j1, i2, j2):
    return i1 * i2 + j1 * j2


# angle
def angle(i1, j1, i2, j2, rad):
    if rad == 1:
        return math.acos(scalar_product(i1, j1, i2, j2) / (norm(i1, j1) * norm(i2, j2)))
    else:
        return 180 / math.pi * math.acos(scalar_product(i1, j1, i2, j2) / (norm(i1, j1) * norm(i2, j2)))


# distance
def distance(i1, j1, i2, j2):
    return math.sqrt((i2 - i1) * (i2 - i1) + (j2 - j1) * (j2 - j1))


# orientation
def orientation(i1, j1, i2, j2, i3, j3):
    o = (j2 - j1) * (i3 - i1) - (i2 - i1) * (j3 - j1)
    if o < 0:
        # turn to the left
        return -1
    elif o > 0:
        # turn to the right
        return 1
    else:
        # collinear
        return 0


# find the bottom-most point
def find_min_j(points):
    min_j = -1
    rank_min = 0

    for i, point in enumerate(points):
        if point.get_j() > min_j:
            min_j = point.get_j()
            rank_min = i
        if point.get_j() == min_j:
            if point.get_i() > points[rank_min].get_i():
                rank_min = i

    return points[rank_min], rank_min


# angle decision
def polar_decision(i1, j1, i2, j2, i3, j3):
    o = orientation(i1, j1, i2, j2, i3, j3)
    if o < 0:
        return -1
    elif o > 0:
        return 1
    else:
        if distance(i1, j1, i2, j2) < distance(i1, j1, i3, j3):
            return -1
        else:
            return 1


def side_of_line(p1, p2, p3):
    li = p2.get_i() - p1.get_i()
    lj = p2.get_j() - p1.get_j()
    pi = p3.get_i() - p1.get_i()
    pj = p3.get_j() - p1.get_j()
    return li*pi-lj*pj


def distance_points(a, b):
    return (a.get_i()-b.get_i())**2+(a.get_j()-b.get_j())**2


def convex_hull_jarvis(shape):
    edges = list(set(shape.get_edges()))
    p0 = min(edges, key=lambda x: x.get_i())
    hull = [p0]
    for point in hull:
        end = edges[0]
        for third_point in edges:
            side_var = side_of_line(point, end, third_point)
            if side_var < 0 and end != point and third_point != point:
                # change max to min, if you want all boundary points
                end = max(end, third_point, key=lambda x: distance_points(x, point))
            if (end == point) or side_var < 0:
                end = third_point
        if end == p0:
            break
        hull.append(end)
        edges.remove(end)
    shape.set_hull(hull)


# convex hull _ graham
def convex_hull_graham(shape, im_new, l_max):
    # we need the bottom-most point
    # it is the point with minimal j
    # in case of tie, we choose the point with minimal k
    edges = shape.get_edges()
    p0, rank = find_min_j(edges)

    # we put p0 on the first position
    if rank != 0:
        edges[0], edges[rank] = edges[rank], edges[0]

    # we compute the polar angle and the distance for each point
    for k in range(1, len(edges) - 1):
        vector_1_i, vector_1_j = vector(l_max, p0.get_j(), p0.get_i(), p0.get_j())
        vector_2_i, vector_2_j = vector(edges[k].get_i(), edges[k].get_j(), p0.get_i(), p0.get_j())
        polar_angle = angle(vector_1_i, vector_1_j, vector_2_i, vector_2_j, 0)
        dist = distance(p0.get_i(), p0.get_j(), edges[k].get_i(), edges[k].get_j())
        edges[k].set_polar_angle(polar_angle)
        edges[k].set_distance(dist)

    # we sort the element according to the polar angle
    sorted_polar_edges = sorted(edges[1:], key=lambda x: [x.get_polar_angle(), -x.get_distance()], reverse=True)

    # if there is more than one point that form the same angle with p0, we remove the super-numeric ones
    removed = []
    for k in range(len(sorted_polar_edges) - 1):
        o = orientation(sorted_polar_edges[k].get_i(), sorted_polar_edges[k].get_j(),
                        sorted_polar_edges[k + 1].get_i(), sorted_polar_edges[k + 1].get_j(),
                        p0.get_i(), p0.get_j())
        if o == 0:
            removed.append(k)
    print(len(edges), len(removed))

    sorted_polar_edges = [k for m, k in enumerate(sorted_polar_edges) if m not in removed]

    hull = []
    # if we have at least three points
    if len(sorted_polar_edges) > 1:
        # we keep the three first points
        hull.append(p0)
        p1 = sorted_polar_edges.pop()
        hull.append(p1)
        p2 = sorted_polar_edges.pop()
        hull.append(p2)

        hull_size = 3
        for k in range(2, len(sorted_polar_edges)):
            while True:
                o = polar_decision(hull[hull_size - 2].get_i(), hull[hull_size - 2].get_j(),
                                   hull[hull_size - 1].get_i(), hull[hull_size - 1].get_j(),
                                   sorted_polar_edges[k].get_i(), sorted_polar_edges[k].get_j())
                if o < 0:
                    hull.append(sorted_polar_edges[k])
                    hull_size = hull_size + 1
                    break
                else:
                    hull.pop()
                    hull_size = hull_size - 1
                hull.append(sorted_polar_edges[k])
                hull_size = hull_size + 1

        print(len(hull))
        for point in hull:
            print(point.get_i(), point.get_j())

    shape.set_hull(hull)


# print points on a picture
def print_points_list(points, im_original, im_new, red, green, blue, background):
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])
    segmentation.initialize_color(im_original, im_new, background)

    # compute mean
    if len(points) > 0:
        for point in points:
            im_new[point[0]][point[1]][0] = blue
            im_new[point[0]][point[1]][1] = green
            im_new[point[0]][point[1]][2] = red


# print points on a picture
def print_points(points, im_original, im_new, red, green, blue, background):
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])
    segmentation.initialize_color(im_original, im_new, background)

    # compute mean
    if len(points) > 0:
        for point in points:
            for n in range(point.get_i() - 1, point.get_i() + 2):
                for m in range(point.get_j() - 1, point.get_j() + 2):
                    if 0 <= n < length and 0 <= m < height:
                        im_new[n][m][0] = blue
                        im_new[n][m][1] = green
                        im_new[n][m][2] = red


# geometrical circularity
def geometrical_circularity(shape):
    geometrical = math.sqrt(4 * math.pi * shape.get_area() / (shape.get_perimeter() ** 2))
    shape.set_geometrical(geometrical)


# symmetry measure - Blaschke
def symmetry_measure(shape, im_original):
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    im_x = np.copy(im_original)
    im_x_minus = np.copy(im_original)

    if shape.get_flag() < 127:
        segmentation.initialize_255(im_original, im_x)
        segmentation.initialize_255(im_original, im_x_minus)
    else:
        segmentation.initialize_0(im_original, im_x)
        segmentation.initialize_0(im_original, im_x_minus)

    # we divide the area to work in order to stay beyond the borders
    div = length * height / (shape.get_horizontal() * shape.get_vertical())

    # we resize x
    length_div = int(length / div)
    height_div = int(height / div)
    length_offset = int((length - length / div) / 2)
    height_offset = int((height - height / div) / 2)
    for i in range(0, length_div):
        for j in range(0, height_div):
            i_div = int(i * div)
            j_div = int(j * div)
            new_i = int(i + length_offset)
            new_j = int(j + height_offset)
            im_x[new_i][new_j][0] = im_original[i_div][j_div][0]
            im_x[new_i][new_j][1] = im_original[i_div][j_div][1]
            im_x[new_i][new_j][2] = im_original[i_div][j_div][2]

    # we create the shape of x
    im_new_x = np.copy(im_x)
    shape_x = shape_points(im_new_x, im_x, shape.get_flag(), 0, length - 1, 0, height - 1)
    edges_x = shape_x.get_edges()
    p0_x, p1_x, p2_x, p3_x = shape_x.get_bb_points()

    # we draw minus x
    for i in range(p0_x.get_i(), p2_x.get_i()):
        for j in range(p0_x.get_j(), p2_x.get_j()):
            new_i = int(p2_x.get_i() + p0_x.get_i() - i)
            new_j = int(p2_x.get_j() + p0_x.get_j() - j)
            im_x_minus[i][j][0] = im_x[new_i][new_j][0]
            im_x_minus[i][j][1] = im_x[new_i][new_j][1]
            im_x_minus[i][j][2] = im_x[new_i][new_j][2]

    # we create the shape of x minus
    im_x_minus_2 = np.copy(im_x_minus)
    shape_x_minus = shape_points(im_x_minus_2, im_x_minus, shape.get_flag(), 0, length - 1, 0, height - 1)
    points_x_minus = shape_x_minus.get_points()

    # for all the point of the edge of the shape x
    for k in edges_x:
        for i in range(0, shape_x_minus.get_horizontal()):
            for j in range(0, shape_x_minus.get_vertical()):
                new_i = int(points_x_minus[0].get_i() + i)
                new_j = int(points_x_minus[0].get_j() + j)
                if im_x_minus[new_i][new_j][0] == shape_x_minus.get_flag():
                    new_i_2 = int(k.get_i() + i)
                    new_j_2 = int(k.get_j() + j)
                    im_x[new_i_2][new_j_2][0] = im_x_minus[new_i][new_j][0]
                    im_x[new_i_2][new_j_2][1] = im_x_minus[new_i][new_j][1]
                    im_x[new_i_2][new_j_2][2] = im_x_minus[new_i][new_j][2]

    # we count the sum of x and x minus
    counter = 0
    for i in range(0, length):
        for j in range(0, height):
            if im_x[i][j][0] == shape_x.get_flag():
                counter += 1

    # we multiply with 2 / div
    counter = counter * div**2 /2
    shape.set_minkowski(counter)
    if shape.get_minkowski() != 0:
        blaschke = shape.get_area() / shape.get_minkowski()
        shape.set_blaschke(blaschke)
    else:
        shape.set_blaschke(0)

    filter.save_image(im_x, "D:/ISEN/Vbox/partage/filtre/symmetrical.bmp")


# connectivity measure
def connectivity(shape, im_original, threshold, window):
    im_new = np.copy(im_original)
    im_new_2 = np.copy(im_original)

    # first: we label the connected components and retrieve the last label, which is the number of labels
    p0, p1, p2, p3 = shape.get_bb_points()
    nb_cc = segmentation.region_growing(im_original, im_new, shape.get_flag(), p0.get_i(), p2.get_i(),
                                        p0.get_j(), p2.get_j(), threshold, window, 0)
    shape.set_nb_connected_component(nb_cc)

    # second: we threshold the image for safety
    filter.manual_threshold(im_original, im_new, nb_cc + 1)

    # third: we reverse the color
    filter.negative(im_new, im_new_2)

    # fourth: we label the holes and the background
    nb_h = segmentation.region_growing(im_new_2, im_new, shape.get_flag(), p0.get_i() - 10, p2.get_i() + 10,
                                       p0.get_j() - 10, p2.get_j() + 10, threshold, window, 0)
    nb_h -= 1
    shape.set_nb_holes(nb_h)
    nb_cc = nb_cc - nb_h
    shape.set_connect(nb_cc)
