import cv2
import numpy as np
import math


# save the image on the device
import histogram


def save_image(image, filename):
    cv2.imwrite(filename, image)


# show the image on the screen
def show_image(image, filename):
    cv2.imshow(filename, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# copy image
def copy_image(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # conversion of rgb color into grey color
    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][0] = im_original[i][j][0]
            im_new[i][j][1] = im_original[i][j][1]
            im_new[i][j][2] = im_original[i][j][2]


# greyscale
def greyscale(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # conversion of rgb color into grey color
    for i in range(0, length):
        for j in range(0, height):
            grey = 0.2125 * im_original[i][j][2] + 0.7154 * im_original[i][j][1] + 0.0721 * im_original[i][j][0]
            im_new[i][j][0] = grey
            im_new[i][j][1] = grey
            im_new[i][j][2] = grey


# negative image
def negative(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # reversing of color
    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][0] = 255 - im_original[i][j][0]
            im_new[i][j][1] = 255 - im_original[i][j][1]
            im_new[i][j][2] = 255 - im_original[i][j][2]


# manual threshold
def manual_threshold(im_original, im_new, threshold):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # we apply the threshold
    for i in range(0, length):
        for j in range(0, height):
            if im_original[i][j][0] > threshold:
                im_new[i][j][0] = 255
                im_new[i][j][1] = 255
                im_new[i][j][2] = 255
            else:
                im_new[i][j][0] = 0
                im_new[i][j][1] = 0
                im_new[i][j][2] = 0


# kernel convolution matrix
def convolution(x, y, im_original, p):
    # initialization of the convolution matrix
    matrix = np.zeros((2 * p + 1, 2 * p + 1, 2 * p + 1))
    for i in range(-p, p + 1):
        for j in range(-p, p + 1):
            matrix[i + p][j + p][0] = im_original[x + i][y + j][0]
            matrix[i + p][j + p][1] = im_original[x + i][y + j][1]
            matrix[i + p][j + p][2] = im_original[x + i][y + j][2]
    return matrix


# mean filter
def mean(im_original, im_new, p):
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # compute mean
    for i in range(p, length - p):
        for j in range(p, height - p):
            matrix = convolution(i, j, im_original, p)

            red = 0
            green = 0
            blue = 0

            for k in range(2 * p + 1):
                for l in range(2 * p + 1):
                    red += matrix[k][l][0]
                    green += matrix[k][l][1]
                    blue += matrix[k][l][2]

            im_new[i][j][0] = red / ((2 * p + 1) * (2 * p + 1))
            im_new[i][j][1] = green / ((2 * p + 1) * (2 * p + 1))
            im_new[i][j][2] = blue / ((2 * p + 1) * (2 * p + 1))


# gaussian filter
def gaussian(im_original, im_new, p, sigma):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # sum and gaussian coefficient
    gaussian_sum = np.zeros(3)
    gauss = np.zeros((2 * p + 1, 2 * p + 1, 2 * p + 1))

    # compute the gaussian coefficient
    for i in range(-p, p + 1):
        for j in range(-p, p + 1):
            x1 = 2 * np.pi * (sigma ** 2)
            x2 = np.exp(-(i ** 2 + j ** 2) / (2 * sigma ** 2))
            gauss[i + p][j + p][i + p] = (1 / x1) * x2
            gaussian_sum[0] += gauss[i + p][j + p][0]
            gaussian_sum[1] += gauss[i + p][j + p][1]
            gaussian_sum[2] += gauss[i + p][j + p][2]

    # compute gaussian filter
    for i in range(p, length - p):
        for j in range(p, height - p):
            matrix = convolution(i, j, im_original, p)
            matrix = gauss * matrix

            red = 0
            green = 0
            blue = 0

            for k in range(2 * p + 1):
                for l in range(2 * p + 1):
                    red += matrix[k][l][0]
                    green += matrix[k][l][1]
                    blue += matrix[k][l][2]

            im_new[i][j][0] = red / gaussian_sum[0]
            im_new[i][j][1] = green / gaussian_sum[1]
            im_new[i][j][2] = blue / gaussian_sum[2]


# median filter
def median(im_original, im_new, p):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # compute gaussian filter
    for i in range(p, length - p):
        for j in range(p, height - p):
            matrix = convolution(i, j, im_original, p)
            median_list = []

            # I put all the element in a list and sort it
            for k in range(2 * p + 1):
                for l in range(2 * p + 1):
                    median_list.append(matrix[k][l][0])
            median_list.sort()
            size_list = len(median_list)

            # I retrieve the median element
            if size_list % 2:
                weight = (median_list[(size_list - 1) // 2] + median_list[size_list // 2]) / 2.0
            else:
                weight = median_list[size_list // 2]

            im_new[i][j][0] = weight
            im_new[i][j][1] = weight
            im_new[i][j][2] = weight


# we retrieve the maximum in a list that comes from a matrix
def maximum(list_matrix):
    maxi = list_matrix[0]
    for i in list_matrix:
        if i >= maxi:
            maxi = i
    return maxi


# dilatation filter
def dilatation(im_original, im_new, p):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # compute dilatation filter
    for i in range(p, length - p):
        for j in range(p, height - p):
            matrix = convolution(i, j, im_original, p)
            dilatation_list = []

            # we retrieve the local maximum
            for k in range(2 * p + 1):
                for n in range(2 * p + 1):
                    dilatation_list.append(matrix[k][n][0])
            maxi = maximum(dilatation_list)

            im_new[i][j][0] = maxi
            im_new[i][j][1] = maxi
            im_new[i][j][2] = maxi


# we retrieve the minimum of a list
def minimum(list_matrix):
    mini = list_matrix[0]
    for i in list_matrix:
        if i <= mini:
            mini = i
    return mini


# erosion filter
def erosion(im_original, im_new, p):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # compute erosion filter
    for i in range(p, length - p):
        for j in range(p, height - p):
            matrix = convolution(i, j, im_original, p)
            erosion_list = []

            # we retrieve the local maximum
            for k in range(2 * p + 1):
                for n in range(2 * p + 1):
                    erosion_list.append(matrix[k][n][0])
            mini = minimum(erosion_list)

            im_new[i][j][0] = mini
            im_new[i][j][1] = mini
            im_new[i][j][2] = mini


# opening filter
def opening(im_original, im_new, p):
    erosion(im_original, im_new, p)
    im_new2 = np.copy(im_new)
    dilatation(im_new2, im_new, p)


# closing filter
def closing(im_original, im_new, p):
    dilatation(im_original, im_new, p)
    im_new2 = np.copy(im_new)
    erosion(im_new2, im_new, p)


# Roberts filter
def roberts_gradient(im_original, im_new, norm):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # roberts gradient - horizontal and vertical
    gx = np.copy(im_original)
    gy = np.copy(im_original)

    # compute roberts filter
    for i in range(1, length - 1):
        for j in range(1, height - 1):
            gx = abs(int(im_original[i][j + 1][0]) - int(im_original[i][j][0]))
            gy = abs(int(im_original[i + 1][j][0]) - int(im_original[i][j][0]))

            # norm l1
            if norm == 1:
                roberts = abs(gx) + abs(gy)
            # norm l2
            elif norm == 2:
                roberts = math.sqrt(abs(gx) ** 2 + abs(gy) ** 2)
            # norm sup
            elif norm == 3:
                if gx > gy:
                    roberts = gx
                else:
                    roberts = gy
            # direction
            else:
                roberts = (255 / 2) * (1 + math.atan2(gy, gx) / math.pi)

            if roberts > 255:
                roberts = 255
            elif roberts < 0:
                roberts = 0

            im_new[i][j][0] = roberts
            im_new[i][j][1] = roberts
            im_new[i][j][2] = roberts
    return gx, gy


# prewitt filter
def prewitt(im_original, im_new, norm):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # prewitt matrix
    prew_x = np.zeros((3, 3))
    prew_x[0][0] = -1
    prew_x[1][0] = -1
    prew_x[2][0] = -1
    prew_x[0][1] = 0
    prew_x[1][1] = 0
    prew_x[2][1] = 0
    prew_x[0][2] = 1
    prew_x[1][2] = 1
    prew_x[2][2] = 1

    prew_y = np.zeros((3, 3))
    prew_y[0][0] = -1
    prew_y[1][0] = 0
    prew_y[2][0] = 1
    prew_y[0][1] = -1
    prew_y[1][1] = 0
    prew_y[2][1] = 1
    prew_y[0][2] = -1
    prew_y[1][2] = 0
    prew_y[2][2] = 1

    # compute prewitt filter
    for i in range(1, length - 1):
        for j in range(1, height - 1):
            gx = prew_x[0][0] * im_original[i - 1][j - 1][0] + prew_x[0][1] * im_original[i][j - 1][0] \
                 + prew_x[0][2] * im_original[i + 1][j - 1][0] + prew_x[1][0] * im_original[i - 1][j][0] \
                 + prew_x[1][1] * im_original[i][j][0] + prew_x[1][2] * im_original[i + 1][j][0] \
                 + prew_x[2][0] * im_original[i - 1][j + 1][0] + prew_x[2][1] * im_original[i][j + 1][0] \
                 + prew_x[2][2] * im_original[i + 1][j + 1][0]

            gy = prew_y[0][0] * im_original[i - 1][j - 1][0] + prew_y[0][1] * im_original[i][j - 1][0] \
                 + prew_y[0][2] * im_original[i + 1][j - 1][0] + prew_y[1][0] * im_original[i - 1][j][0] \
                 + prew_y[1][1] * im_original[i][j][0] + prew_y[1][2] * im_original[i + 1][j][0] \
                 + prew_y[2][0] * im_original[i - 1][j + 1][0] + prew_y[2][1] * im_original[i][j + 1][0] \
                 + prew_y[2][2] * im_original[i + 1][j + 1][0]

            # norm l1
            if norm == 1:
                prew = abs(gx) + abs(gx)
            # norm l2
            elif norm == 2:
                prew = math.sqrt(abs(gx) ** 2 + abs(gx) ** 2)
            # norm sup
            elif norm == 3:
                if gx > gy:
                    prew = gx
                else:
                    prew = gy
            # direction
            else:
                prew = (255 / 2) * (1 + math.atan2(gx, gx) / math.pi)

            if prew > 255:
                prew = 255
            elif prew < 0:
                prew = 0

            im_new[i][j][0] = prew
            im_new[i][j][1] = prew
            im_new[i][j][2] = prew


# sobel filter
def sobel(im_original, im_new, norm):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # sobel matrix
    sob_x = np.array([[1, 0, -1],
                      [2, 0, -2],
                      [1, 0, -1]])
    sob_y = np.array([[1, 2, 1],
                      [0, 0, 0],
                      [-1, -2, -1]])

    for i in range(1, length - 1):
        for j in range(1, height - 1):
            gx = sob_x[0][0] * im_original[i - 1][j - 1][0] + sob_x[0][1] * im_original[i][j - 1][0] \
                    + sob_x[0][2] * im_original[i + 1][j - 1][0] + sob_x[1][0] * im_original[i - 1][j][0] \
                    + sob_x[1][1] * im_original[i][j][0] + sob_x[1][2] * im_original[i + 1][j][0] \
                    + sob_x[2][0] * im_original[i - 1][j + 1][0] + sob_x[2][1] * im_original[i][j + 1][0] \
                    + sob_x[2][2] * im_original[i + 1][j + 1][0]

            gy = sob_y[0][0] * im_original[i - 1][j - 1][0] + sob_y[0][1] * im_original[i][j - 1][0] \
                  + sob_y[0][2] * im_original[i + 1][j - 1][0] + sob_y[1][0] * im_original[i - 1][j][0] \
                  + sob_y[1][1] * im_original[i][j][0] + sob_y[1][2] * im_original[i + 1][j][0] \
                  + sob_y[2][0] * im_original[i - 1][j + 1][0] + sob_y[2][1] * im_original[i][j + 1][0] \
                  + sob_y[2][2] * im_original[i + 1][j + 1][0]

            # norm l1
            if norm == 1:
                sob = abs(gx) + abs(gy)
            # norm l2
            elif norm == 2:
                sob = math.sqrt(abs(gx) ** 2 + abs(gy) ** 2)
            # norm sup
            elif norm == 3:
                if gx > gy:
                    sob = gx
                else:
                    sob = gy
            # direction
            else:
                sob = (255 / 2) * (1 + math.atan2(gx, gx) / math.pi)

            if sob < 0:
                sob = 0
            if sob > 255:
                sob = 255

            im_new[i][j][0] = sob
            im_new[i][j][1] = sob
            im_new[i][j][2] = sob


# laplacian filter
def laplacian(im_original, im_new, size):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # laplacian matrix
    if size == 4:
        lapla_x = np.array([[0, -1, 0],
                            [-1, 4, -1],
                            [0, -1, 0]])
    else:
        lapla_x = np.array([[-1, -1, -1],
                            [-1, 8, -1],
                            [-1, -1, -1]])

    for i in range(1, length - 1):
        for j in range(1, height - 1):
            lapla = lapla_x[0][0] * im_original[i - 1][j - 1][0] + lapla_x[0][1] * im_original[i][j - 1][0] \
                    + lapla_x[0][2] * im_original[i + 1][j - 1][0] + lapla_x[1][0] * im_original[i - 1][j][0] \
                    + lapla_x[1][1] * im_original[i][j][0] + lapla_x[1][2] * im_original[i + 1][j][0] \
                    + lapla_x[2][0] * im_original[i - 1][j + 1][0] + lapla_x[2][1] * im_original[i][j + 1][0] \
                    + lapla_x[2][2] * im_original[i + 1][j + 1][0]

            if lapla < 0:
                lapla = 0
            if lapla > 255:
                lapla = 255

            im_new[i][j][0] = lapla
            im_new[i][j][1] = lapla
            im_new[i][j][2] = lapla


# choice = 1 (closing - opening), choice = 2 (dilation - erosion)
def morphological_gradient(im_original, im_new, choice, p):
    # dimension
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    if choice == 1:
        # closing - opening
        im_closing = np.copy(im_original)
        im_opening = np.copy(im_original)

        closing(im_original, im_closing, p)
        opening(im_original, im_opening, p)

        for i in range(0, length - 1):
            for j in range(0, height - 1):
                im_new[i][j][0] = im_closing[i][j][0] - im_opening[i][j][0]
                im_new[i][j][1] = im_closing[i][j][1] - im_opening[i][j][1]
                im_new[i][j][2] = im_closing[i][j][2] - im_opening[i][j][2]
    else:
        # dilatation - erosion
        im_dilatation = np.copy(im_original)
        im_erosion = np.copy(im_original)

        dilatation(im_original, im_dilatation, p)
        erosion(im_original, im_erosion, p)

        for i in range(0, length - 1):
            for j in range(0, height - 1):
                im_new[i][j][0] = im_dilatation[i][j][0] - im_erosion[i][j][0]
                im_new[i][j][1] = im_dilatation[i][j][1] - im_erosion[i][j][1]
                im_new[i][j][2] = im_dilatation[i][j][2] - im_erosion[i][j][2]


# median filter rgb
def median_rgb(im_original, im_new, p):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(p, length - p):
        for j in range(p, height - p):
            min_dist_tot = 99999999999999
            min_dist_k1 = 0
            min_dist_n1 = 0
            for k1 in range(i - p, i + p + 1):
                for n1 in range(j - p, j + p + 1):
                    dist_tot = 0
                    for k2 in range(i - p, i + p + 1):
                        for n2 in range(j - p, j + p + 1):
                            dist_tot = dist_tot \
                                       + (int(im_original[k2][n2][0]) - int(im_original[k1][n1][0])) * (
                                               int(im_original[k2][n2][0]) - int(im_original[k1][n1][0])) \
                                       + (int(im_original[k2][n2][1]) - int(im_original[k1][n1][1])) * (
                                               int(im_original[k2][n2][1]) - int(im_original[k1][n1][1])) \
                                       + (int(im_original[k2][n2][2]) - int(im_original[k1][n1][2])) * (
                                               int(im_original[k2][n2][2]) - int(im_original[k1][n1][2]))

                    if min_dist_tot > dist_tot:
                        min_dist_tot = dist_tot
                        min_dist_k1 = k1
                        min_dist_n1 = n1

            im_new[i][j][0] = im_original[min_dist_k1][min_dist_n1][0]
            im_new[i][j][1] = im_original[min_dist_k1][min_dist_n1][1]
            im_new[i][j][2] = im_original[min_dist_k1][min_dist_n1][2]


# red filter
def red_filter(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][2] = im_original[i][j][2]
            im_new[i][j][1] = 0
            im_new[i][j][0] = 0


# green filter
def green_filter(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][1] = im_original[i][j][1]
            im_new[i][j][2] = 0
            im_new[i][j][0] = 0


# blue filter
def blue_filter(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][0] = im_original[i][j][0]
            im_new[i][j][1] = 0
            im_new[i][j][2] = 0


# yellow filter
def yellow_filter(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][2] = im_original[i][j][2]
            im_new[i][j][1] = im_original[i][j][1]
            im_new[i][j][0] = 0


# green filter
def cyan_filter(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][1] = im_original[i][j][1]
            im_new[i][j][2] = 0
            im_new[i][j][0] = im_original[i][j][0]


# magenta filter
def magenta_filter(im_original, im_new):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][0] = im_original[i][j][0]
            im_new[i][j][1] = 0
            im_new[i][j][2] = im_original[i][j][2]
