import math


# we retrieve the minimum between two elements
def min_between_two(elt1, elt2):
    if elt1 > elt2:
        elt = elt2
    else:
        elt = elt1
    return elt


# we retrieve the maximum between two elements
def max_between_two(elt1, elt2):
    if elt1 > elt2:
        elt = elt1
    else:
        elt = elt2
    return elt


# we retrieve the minimum between three elements
def min_between_three(elt1, elt2, elt3):
    elt = min_between_two(elt1, elt2)
    elt = min_between_two(elt, elt3)
    return elt


# we retrieve the maximum between three elements
def max_between_three(elt1, elt2, elt3):
    elt = max_between_two(elt1, elt2)
    elt = max_between_two(elt, elt3)
    return elt


# hsv of a color image
def compute_hsv(im_original, im_hue, im_saturation, im_value):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # we apply the threshold
    for i in range(0, length):
        for j in range(0, height):
            r = im_original[i][j][2]
            g = im_original[i][j][1]
            b = im_original[i][j][0]

            # we retrieve the maximum and minimum between the three pixels
            maxi = max_between_three(r, g, b)
            mini = min_between_three(r, g, b)

            # computation of hue
            hue = 2 * float(r) - float(g) - float(b)
            hue = 0.5 * hue

            denominator = (float(r) - float(g)) * (float(r) - float(g)) + (float(r) - float(b)) * (float(g) - float(b))
            denominator = math.sqrt(denominator)

            hue = hue / denominator
            hue = (180 / math.pi) * math.acos(hue)

            if b > g:
                hue = 360 - hue

            im_hue[i][j][0] = hue
            im_hue[i][j][1] = hue
            im_hue[i][j][2] = hue

            # computation of saturation
            if maxi == 0:
                saturation = 0
            else:
                saturation = maxi - mini
                saturation = 100 * (saturation + 0.5) / maxi

            im_saturation[i][j][0] = saturation
            im_saturation[i][j][1] = saturation
            im_saturation[i][j][2] = saturation

            # computation of value
            value = 100 * (maxi + 0.5) / 255

            im_value[i][j][0] = value
            im_value[i][j][1] = value
            im_value[i][j][2] = value


# hue of an image
def compute_h(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # we apply the threshold
    for i in range(0, length):
        for j in range(0, height):
            r = im_original[i][j][2]
            g = im_original[i][j][1]
            b = im_original[i][j][0]
            # # we retrieve the maximum and minimum between the three pixels
            # maxi = max_between_three(r, g, b)
            # mini = min_between_three(r, g, b)
            #
            # # difference between maximum and minimum
            # m = maxi - mini

            intermediate = 2 * float(r) - float(g) - float(b)
            intermediate = 0.5 * intermediate

            denominator = (float(r) - float(g)) * (float(r) - float(g)) + (float(r) - float(b)) * (float(g) - float(b))
            denominator = math.sqrt(denominator)

            intermediate = intermediate / denominator
            intermediate = (180 / math.pi) * math.acos(intermediate)

            if b > g:
                intermediate = 360 - intermediate

            # if m >= 0:
            #     # there is no maximum and minimum
            #     if m == 0:
            #         intermediate = 0
            #     # the maximum is red
            #     elif maxi == r:
            #         intermediate = 60 * ((g - b) / m + 360)
            #         intermediate = intermediate % 360
            #     # the maximum is green
            #     elif maxi == g:
            #         intermediate = 60 * ((b - r) / m + 120)
            #     # the maximum is blue
            #     elif maxi == b:
            #         intermediate = 60 * ((r - g) / m + 240)

            im_new[i][j][0] = intermediate
            im_new[i][j][1] = intermediate
            im_new[i][j][2] = intermediate


# saturation of an image
def compute_s(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # we apply the threshold
    for i in range(0, length):
        for j in range(0, height):
            # we retrieve the maximum and minimum between the three pixels
            maxi = max_between_three(im_original[i][j][0], im_original[i][j][1], im_original[i][j][2])
            mini = min_between_three(im_original[i][j][0], im_original[i][j][1], im_original[i][j][2])

            if maxi == 0:
                intermediate = 0
            else:
                intermediate = maxi - mini
                intermediate = 100 * (intermediate + 0.5) / maxi

            if intermediate < 0:
                intermediate = 0
            if intermediate > 255:
                intermediate = 255

            im_new[i][j][0] = intermediate
            im_new[i][j][1] = intermediate
            im_new[i][j][2] = intermediate


# value of an image
def compute_v(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # we apply the threshold
    for i in range(0, length):
        for j in range(0, height):
            maxi = max_between_three(im_original[i][j][0], im_original[i][j][1], im_original[i][j][2])
            intermediate = 100 * (maxi + 0.5) / 255

            if intermediate < 0:
                intermediate = 0
            if intermediate > 255:
                intermediate = 255

            im_new[i][j][0] = intermediate
            im_new[i][j][1] = intermediate
            im_new[i][j][2] = intermediate
