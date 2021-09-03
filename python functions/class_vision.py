import measure


class Point:
    def __init__(self, i, j):
        # coordinates on the image
        self.__i = i
        self.__j = j

        # polar angle
        self.__polar_angle = 0

        # distance
        self.__distance = 0

    def get_i(self):
        return self.__i

    def set_i(self, i):
        self.__i = i

    def get_j(self):
        return self.__j

    def set_j(self, j):
        self.__j = j

    def get_polar_angle(self):
        return self.__polar_angle

    def set_polar_angle(self, polar_angle):
        self.__polar_angle = polar_angle

    def get_distance(self):
        return self.__distance

    def set_distance(self, distance):
        self.__distance = distance


class Shape:
    def __init__(self):
        # flag of the region
        self.__flag = -1

        # mean color of the region
        self.__mean_color = -1

        # number of point of the shape
        self.__points = []

        # edges
        self.__edges = []

        # area
        self.__area = -1

        # perimeter
        self.__perimeter = -1
        self.__perimeter_crofton = -1

        # bounding box
        self.__bb = []
        self.__vertical = -1
        self.__horizontal = -1
        self.__elongation = -1

        # better bounding box
        self.__bbb = []
        self.__b_vertical = -1
        self.__b_horizontal = -1
        self.__b_elongation = -1

        # Férêt
        self.__max_feret_diameter = -1
        self.__min_feret_diameter = -1

        # Convex Hull
        self.__most_bottom_left = Point(0, 0)
        self.__hull = []

        # Circularity
        self.__geometrical = -1
        self.__radial = -1

        # Symmetry
        self.__minkowski = -1
        self.__blaschke = -1

        # Connectivity
        self.__connect = -1
        self.__nb_connected_component = -1
        self.__nb_holes = -1

    # getter
    def get_flag(self):
        return self.__flag

    def get_mean_color(self):
        return self.__mean_color

    def get_points(self):
        return self.__points

    def get_edges(self):
        return self.__edges

    def get_area(self):
        return self.__area

    def get_perimeter(self):
        return self.__perimeter

    def get_perimeter_crofton(self):
        return self.__perimeter_crofton

    def get_bb(self):
        return self.__bb

    def get_bb_points(self):
        return self.__bb[0], self.__bb[1], self.__bb[2], self.__bb[3]

    def get_vertical(self):
        return self.__vertical

    def get_horizontal(self):
        return self.__horizontal

    def get_elongation(self):
        return self.__elongation

    def get_bbb(self):
        return self.__bbb

    def get_b_vertical(self):
        return self.__b_vertical

    def get_b_horizontal(self):
        return self.__b_horizontal

    def get_b_elongation(self):
        return self.__b_elongation

    def get_max_feret_diameter(self):
        return self.__max_feret_diameter

    def get_min_feret_diameter(self):
        return self.__min_feret_diameter

    def get_most_bottom_left(self):
        return self.__most_bottom_left

    def get_hull(self):
        return self.__hull

    def get_geometrical(self):
        return self.__geometrical

    def get_radial(self):
        return self.__radial

    def get_radial(self):
        return self.__radial

    def get_minkowski(self):
        return self.__minkowski

    def get_blaschke(self):
        return self.__blaschke

    def get_connect(self):
        return self.__connect

    def get_nb_connected_component(self):
        return self.__nb_connected_component

    def get_nb_holes(self):
        return self.__nb_holes

    # setter
    def set_flag(self, flag):
        self.__flag = flag

    def set_mean_color(self, mean_color):
        self.__mean_color = mean_color

    def set_points(self, points):
        self.__points = points

    def set_edges(self, edges):
        self.__edges = edges

    def set_area(self, area):
        self.__area = area

    def set_perimeter(self, perimeter):
        self.__perimeter = perimeter

    def set_perimeter_crofton(self, perimeter_crofton):
        self.__perimeter_crofton = perimeter_crofton

    def set_bb(self, bb):
        self.__bb = bb
        self.__vertical = bb[1].get_i() - bb[0].get_i()
        self.__horizontal = bb[3].get_j() - bb[0].get_j()
        if self.__vertical != 0:
            self.__elongation = self.__horizontal / self.__vertical
        else:
            self.__elongation = 0

    def set_vertical(self, vertical):
        self.__vertical = vertical

    def set_horizontal(self, horizontal):
        self.__horizontal = horizontal

    def set_elongation(self, elongation):
        self.__elongation = elongation

    def set_bbb(self, bbb):
        self.__bbb = bbb
        self.__b_vertical = measure.distance(self.__bbb[3].get_i(), self.__bbb[3].get_j(),
                                             self.__bbb[0].get_i(), self.__bbb[0].get_j())
        self.__b_horizontal = measure.distance(self.__bbb[1].get_i(), self.__bbb[1].get_j(),
                                               self.__bbb[0].get_i(), self.__bbb[0].get_j())
        if self.__b_vertical != 0:
            self.__b_elongation = self.__b_horizontal / self.__b_vertical
        else:
            self.__b_elongation = 0

    def set_b_vertical(self, b_vertical):
        self.__b_vertical = b_vertical

    def set_b_horizontal(self, b_horizontal):
        self.__b_horizontal = b_horizontal

    def set_b_elongation(self, b_elongation):
        self.__b_elongation = b_elongation

    def set_max_feret_diameter(self, m_diameter):
        self.__max_feret_diameter = m_diameter

    def set_min_feret_diameter(self, m_diameter):
        self.__min_feret_diameter = m_diameter

    def set_most_bottom_left(self, mbl):
        self.__most_bottom_left = mbl

    def set_hull(self, hull):
        self.__hull = hull

    def set_radial(self, radial):
        self.__radial = radial

    def set_geometrical(self, geometrical):
        self.__geometrical = geometrical

    def set_minkowski(self, minkowski):
        self.__minkowski = minkowski

    def set_blaschke(self, blaschke):
        self.__blaschke = blaschke

    def set_connect(self, connect):
        self.__connect = connect

    def set_nb_connected_component(self, nb_cc):
        self.__nb_connected_component = nb_cc

    def set_nb_holes(self, nb_h):
        self.__nb_holes = nb_h
