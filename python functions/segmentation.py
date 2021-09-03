import sys


# initialize an image with a certain color (shade of grey)
def initialize_color(im_original, im_new, color):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][0] = color
            im_new[i][j][1] = color
            im_new[i][j][2] = color



# create an image with minus 1
def initialize_minus_1(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][0] = -1
            im_new[i][j][1] = -1
            im_new[i][j][2] = -1


# create a black image
def initialize_0(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][0] = 0
            im_new[i][j][1] = 0
            im_new[i][j][2] = 0


# create a white image
def initialize_255(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][0] = 255
            im_new[i][j][1] = 255
            im_new[i][j][2] = 255


# erosion
def erosion(im_original, im_new, flag, l_min, l_max, h_min, h_max, window, distance):
    if flag < 127:
        initialize_255(im_original, im_new)
        background = 255
    else:
        initialize_0(im_original, im_new)
        background = 0

    for i in range(l_min, l_max):
        for j in range(h_min, h_max):
            if im_original[i][j][0] == flag:
                neighbour = 0
                for row in range(i - distance, i + distance + 1):
                    for column in range(j - distance, j + distance + 1):
                        if h_min <= column <= h_max and l_min <= row <= l_max:
                            # if one element of the shape has at least one neighbour which is from the background,
                            # the element is eroded
                            if window == 8:
                                if im_original[row][column][0] != flag:
                                    neighbour = neighbour + 1
                            else:
                                if im_original[row][column][0] != flag:
                                    neighbour = neighbour + 1
                if neighbour > 0:
                    im_new[i][j][0] = background
                    im_new[i][j][1] = background
                    im_new[i][j][2] = background
                else:
                    im_new[i][j][0] = flag
                    im_new[i][j][1] = flag
                    im_new[i][j][2] = flag


# dilatation
def dilatation(im_original, im_new, flag, l_min, l_max, h_min, h_max, window, distance):
    if flag < 127:
        initialize_255(im_original, im_new)
    else:
        initialize_0(im_original, im_new)

    for i in range(l_min, l_max):
        for j in range(h_min, h_max):
            if im_original[i][j][0] == flag:
                for row in range(i - distance, i + distance + 1):
                    for column in range(j - distance, j + distance + 1):
                        # all the neighbours around takes the color of the element that is from the shape
                        if h_min <= column <= h_max and l_min <= row <= l_max:
                            if window == 8:
                                im_new[row][column][0] = flag
                                im_new[row][column][1] = flag
                                im_new[row][column][2] = flag
                            else:
                                if row == i or column == j:
                                    im_new[row][column][0] = flag
                                    im_new[row][column][1] = flag
                                    im_new[row][column][2] = flag


# function that test the distance between a pixel and a flag
def is_compatible(region, candidate, threshold):
    compatible = 0
    if abs(candidate - region) <= threshold:
        compatible = 1
    return compatible


# do a region growing using conditional dilation from a seed - iterative
def region_growing_seed(im_original, im_new, color, seed_i, seed_j, flag, l_min, l_max, h_min, h_max, threshold,
                        window):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])
    image_size = length * height

    # initialize the background of the new image
    if flag < 127:
        initialize_255(im_original, im_new)
    else:
        initialize_0(im_original, im_new)

    # we mark the initial seed on the picture
    im_new[seed_i][seed_j][0] = flag
    im_new[seed_i][seed_j][1] = flag
    im_new[seed_i][seed_j][2] = flag

    # two lists : one with the pixels to be inspected, the other one with the points of the region
    seeds_to_be_inspected = [[seed_i, seed_j]]
    region_points = [[seed_i, seed_j]]
    region_size = 1

    # the retrieve the max, min of i and j at the end
    j_max = seed_j
    j_min = seed_j
    i_max = seed_i
    i_min = seed_i

    # Region growing until there are no seed anymore to be inspected
    while len(seeds_to_be_inspected) > 0 and region_size < image_size:
        # loop to check the neighbours
        for i in range(seed_i - 1, seed_i + 2):
            for j in range(seed_j - 1, seed_j + 2):
                # we give to the neighbours that have the same color of the centered pixel
                if h_min <= j <= h_max and l_min <= i <= l_max and i != seed_i and j != seed_j:
                    if im_new[i][j][0] != flag and is_compatible(color, im_original[i][j][0], threshold) == 1:
                        if window == 8:
                            # we give a flag to the point
                            im_new[i][j][0] = flag
                            im_new[i][j][1] = flag
                            im_new[i][j][2] = flag

                            # we add the new point to the region
                            region_points.append([i, j])

                            # we add the new point that has potential neighbours
                            # from the shape to the list to be inspected
                            seeds_to_be_inspected.append([i, j])

                            # the size of the region is higher
                            region_size += 1

                            # min, max check
                            if j_min > j:
                                j_min = j
                            if j_max < j:
                                j_max = j
                            if i_min > i:
                                i_min = i
                            if i_max < i:
                                i_max = i
                        else:
                            if i == seed_i or j == seed_j:
                                # we give a flag to the point
                                im_new[i][j][0] = flag
                                im_new[i][j][1] = flag
                                im_new[i][j][2] = flag

                                # we add the new point to the region
                                region_points.append([i, j])

                                # we add the new point that has potential neighbours
                                # from the shape to the list to be inspected
                                seeds_to_be_inspected.append([i, j])

                                # the size of the region is higher
                                region_size += 1

                                # min, max check
                                if j_min > j:
                                    j_min = j
                                if j_max < j:
                                    j_max = j
                                if i_min > i:
                                    i_min = i
                                if i_max < i:
                                    i_max = i

        # we remove the seed
        seeds_to_be_inspected.remove([seed_i, seed_j])

        # we change the need seed_i and seed_j
        if len(seeds_to_be_inspected) > 0:
            seed_i = seeds_to_be_inspected[-1][0]
            seed_j = seeds_to_be_inspected[-1][1]
    return region_points, region_size, i_min, i_max, j_min, j_max


# do conditional dilatation - recursive so since python has a recursion limit, we have a counter and a limit to deal it
def conditional_dilatation(im_original, im_new, color, i, j, flag, l_min, l_max, h_min, h_max, distance, threshold,
                           window, limit, counter):
    new_i = -1
    new_j = -1
    for row in range(i - distance, i + distance + 1):
        for column in range(j - distance, j + distance + 1):
            # we give to the neighbours that have the same color of the centered pixel
            if h_min <= column <= h_max and l_min <= row <= l_max and row != i and column != j:
                if im_new[row][column][0] != flag and is_compatible(color, im_original[row][column][0],
                                                                    threshold) == 1:
                    if window == 8:
                        im_new[row][column][0] = flag
                        im_new[row][column][1] = flag
                        im_new[row][column][2] = flag
                        counter = counter + 1

                        if counter < limit:
                            conditional_dilatation(im_original, im_new, color, row, column, flag, l_min, l_max, h_min,
                                                   h_max, distance, threshold, window, limit, counter)
                            new_i = -1
                            new_j = -1
                        else:
                            new_i = row
                            new_j = column
                    else:
                        if row == i or column == j:
                            im_new[row][column][0] = flag
                            im_new[row][column][1] = flag
                            im_new[row][column][2] = flag
                            counter = counter + 1
                            if counter < limit:
                                conditional_dilatation(im_original, im_new, color, row, column, flag, l_min, l_max,
                                                       h_min, h_max, distance, threshold, window, limit, counter)
                                new_i = -1
                                new_j = -1
                            else:
                                new_i = row
                                new_j = column
    return new_i, new_j


# region growing - give a flag to the different regions and return the number of flags
def region_growing(im_original, im_new, color, l_min, l_max, h_min, h_max, threshold, window, mod):
    flag = 0
    flag_max = 0
    mini = 255
    counter = 0

    # initialize the background of the new image
    if color < 127:
        initialize_255(im_original, im_new)
        background = 255
    else:
        initialize_0(im_original, im_new)
        background = 0

    for i in range(l_min, l_max):
        for j in range(h_min, h_max):
            # we find an element of the region that is not tagged yet
            if is_compatible(color, im_original[i][j][0], threshold) and im_new[i][j][0] == background:
                if flag > flag_max:
                    flag_max = flag

                # we check if a neighbour already has a flag
                for row in range(i - 1, i + 2):
                    for column in range(j - 1, j + 2):
                        # limit of image
                        if h_min <= column <= h_max and l_min <= row <= l_max:
                            if window == 8:
                                if mini >= im_new[row][column][0] and is_compatible(color, im_original[row][column][0],
                                                                                    threshold):
                                    mini = im_new[row][column][0]
                            else:
                                if (row == i or column == j) and mini >= im_new[row][column][0] \
                                        and is_compatible(color, im_original[i][j][0], threshold):
                                    mini = im_new[row][column][0]

                # incrementation of flags
                if mod == 0:
                    if mini != 255 and flag < 255:
                        flag = mini
                        # we check give the same flag for all the neighbour
                        for row in range(i - 1, i + 2):
                            for column in range(j - 1, j + 2):
                                # limit of image
                                if h_min <= column <= h_max and l_min <= row <= l_max:
                                    if window == 8:
                                        if im_new[row][column][0] > mini and \
                                                is_compatible(color, im_original[row][column][0], threshold):
                                            im_new[row][column][0] = mini
                                            im_new[row][column][1] = mini
                                            im_new[row][column][2] = mini
                                    else:
                                        if (row == i or column == j) and im_new[row][column][0] > mini \
                                                and is_compatible(color, im_original[i][j][0], threshold):
                                            im_new[row][column][0] = mini
                                            im_new[row][column][1] = mini
                                            im_new[row][column][2] = mini
                    else:
                        flag = flag + 1
                    mini = 255
                # we give a different flags for each region
                else:
                    flag = (flag + 20) % 256

                im_new[i][j][0] = flag
                im_new[i][j][1] = flag
                im_new[i][j][2] = flag

                # we do a conditional dilatation
                again = -1
                new_i = i
                new_j = j
                while again == -1:
                    new_i, new_j = conditional_dilatation(im_original, im_new, color, new_i, new_j, flag,
                                                          l_min, l_max, h_min, h_max, 1, threshold, window, counter,
                                                          sys.getrecursionlimit())
                    if new_i == -1 and new_j == -1:
                        again = 0
                    else:
                        again = -1
                counter = 0

    # we return the number of the flag
    return flag_max


# region growing : we find all the elements with the same color
def region_growing_process(im_original, im_new, color, flag, l_min, l_max, h_min, h_max, threshold, window):
    # initialize the background of the new image
    if flag < 127:
        initialize_255(im_original, im_new)
    else:
        initialize_0(im_original, im_new)

    for i in range(l_min, l_max):
        for j in range(h_min, h_max):
            if is_compatible(color, im_original[i][j][0], threshold) == 1:
                for row in range(i - 1, i + 2):
                    for column in range(j - 1, j + 2):
                        if h_min <= column <= h_max and l_min <= row <= l_max:
                            if window == 8:
                                if is_compatible(color, im_original[row][column][0], threshold) == 1:
                                    im_new[row][column][0] = flag
                                    im_new[row][column][1] = flag
                                    im_new[row][column][2] = flag
                            else:
                                if row == i or column == j:
                                    if is_compatible(color, im_original[row][column][0], threshold) == 1:
                                        im_new[row][column][0] = flag
                                        im_new[row][column][1] = flag
                                        im_new[row][column][2] = flag


# watershed algorithm
def watershed(im_original, im_new, window, distance):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    mini = 256
    mini_i = 0
    mini_j = 0

    initialize_minus_1(im_original, im_new)

    # find pool
    for k in range(0, 256):
        for i in range(0, length):
            for j in range(0, height):
                if im_original[i][j][0] == k:
                    for row in range(i - 1, i + 2):
                        for column in range(j - 1, j + 2):
                            if 0 <= row < length and 0 <= column < height:
                                # we check if there is a pool around and we keep the range of i and j
                                if window == 8:
                                    if mini >= im_original[row][column][0]:
                                        mini = im_original[row][column][0]
                                        mini_i = row
                                        mini_j = column
                                else:
                                    if row == i or column == j:
                                        if mini >= im_original[row][column][0]:
                                            mini = im_original[row][column][0]
                                            mini_i = row
                                            mini_j = column
                    im_new[i][j][0] = im_original[mini_i][mini_j][0]
                    im_new[i][j][1] = im_original[mini_i][mini_j][0]
                    im_new[i][j][2] = im_original[mini_i][mini_j][0]
                    mini = 256

        # dilatation
        for i in range(0, length):
            for j in range(0, height):
                if im_new[i][j][0] == k:
                    for row in range(i - distance, i + distance):
                        for column in range(j - distance, j + distance):
                            if 0 <= row < length and 0 <= column < height:
                                # for each pool, we do a dilatation around
                                if im_original[row][column][0] >= k:
                                    if window == 8:
                                        im_new[i][j][0] = k
                                        im_new[i][j][1] = k
                                        im_new[i][j][2] = k
                                    else:
                                        if row == i or column == j:
                                            im_new[i][j][0] = k
                                            im_new[i][j][1] = k
                                            im_new[i][j][2] = k
