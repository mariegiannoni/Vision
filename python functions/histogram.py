import numpy as np
import matplotlib.pyplot as plt
import math


# compute the histogram of an image
def compute_histogram(image, dim):
    # dimensions
    length = int(image.shape[0])
    height = int(image.shape[1])

    # minimum and maximum
    mini = 9999999999999
    maxi = 0
    h = np.zeros(256, dtype=np.float32)

    if dim >= 0 & dim <= 2:
        for i in range(0, length):
            for j in range(0, height):
                # count number of pixel with this intensity
                k = image[i][j][dim]
                h[k] = h[k] + 1
                # find the minimum value of the image
                if mini > image[i][j][dim]:
                    mini = image[i][j][dim]
                # find the maximum value of the image
                if maxi < image[i][j][dim]:
                    maxi = image[i][j][dim]

    counter = height*length
    return h, mini, maxi, counter


# compute the cumulative histogram of an image
def cumulative_histogram(h):
    cumulative = 0
    ch = np.zeros(256, dtype=np.float32)
    for k in range(0, 256):
        cumulative = cumulative + h[k]
        ch[k] = cumulative
    return ch


# do histogram equalization on an image
def histogram_equalization(im_original, im_new, ch, nb):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    for i in range(0, height - 1):
        for j in range(0, length - 1):
            im_new[i][j][0] = 255 * ch[int(im_original[i][j][0])] / nb
            im_new[i][j][1] = 255 * ch[int(im_original[i][j][1])] / nb
            im_new[i][j][2] = 255 * ch[int(im_original[i][j][2])] / nb


# dynamical expansion
def contrast_stretching(im_original, im_new, mini, maxi, v_min = 0, v_max = 255):
    # dimensions
    length = int(im_original.shape[0])
    height = int(im_original.shape[1])

    # new_px = (px - mini) * (v_max - v_min)/(maxi - mini) + v_min
    # v_min = 0
    # v_max = 255

    delta_sup = v_max - v_min
    delta_inf = maxi - mini
    delta = delta_sup / delta_inf

    for i in range(0, length):
        for j in range(0, height):
            im_new[i][j][0] = (int(im_original[i][j][0]) - mini) * delta + v_min
            im_new[i][j][1] = (int(im_original[i][j][1]) - mini) * delta + v_min
            im_new[i][j][2] = (int(im_original[i][j][2]) - mini) * delta + v_min


# compute the entropy of an image
def entropy(h, nb):
    e = 0
    for k in range(0, 256):
        pi = h[k] / nb
        if pi != 0:
            pi = pi * math.log(pi)
        else:
            pi = 0
        e = e - pi
    return e


# do a multi thresholding with a list of threshold
def multi_k_thresholding(im_original, im_new, threshold, k):
    if k > 1:
        # tab of threshold
        threshold_k = np.zeros(k, dtype=np.float64)
        for i in range(0, k):
            threshold_k[i] = threshold[i][0]

        # dimensions
        length = int(im_original.shape[0])
        height = int(im_original.shape[1])

        # we apply the threshold
        for i in range(0, length):
            for j in range(0, height):
                for n in range(1, k):
                    if threshold_k[n-1] < im_original[i][j][0] <= threshold_k[n]:
                        im_new[i][j][0] = threshold_k[n]
                        im_new[i][j][1] = threshold_k[n]
                        im_new[i][j][2] = threshold_k[n]

                if im_original[i][j][0] < threshold_k[0]:
                    im_new[i][j][0] = 0
                    im_new[i][j][1] = 0
                    im_new[i][j][2] = 0

                if im_original[i][j][0] > threshold_k[k-1]:
                    im_new[i][j][0] = threshold_k[k-1]
                    im_new[i][j][1] = threshold_k[k-1]
                    im_new[i][j][2] = threshold_k[k-1]


# return a list of threshold sorted by entropy
def entropy_maximization_multi(h, ch, nb):
    threshold_sorted = np.zeros((256, 2), dtype=np.float64)

    sum_min = 0
    sum_max = 0

    for threshold in range(0, 256):
        for k in range(0, 256):
            pi = h[k] / nb
            if pi != 0:
                pi = pi * math.log(pi)
            else:
                pi = 0
            if k <= threshold:
                sum_min = sum_min + pi
            else:
                sum_max = sum_max + pi

        if ch[threshold] != 0:
            sum_min = sum_min / ch[threshold]

        if nb - ch[threshold] != 0:
            sum_max = sum_max / (nb - ch[threshold])

        e = math.log1p(ch[threshold] * (nb - ch[threshold]))
        e = e - sum_min - sum_max

        threshold_sorted[int(threshold)][0] = threshold
        threshold_sorted[int(threshold)][1] = e

        sum_max = 0
        sum_min = 0

    new_threshold_sorted = sorted(threshold_sorted, key=lambda x: x[1], reverse=True)
    return new_threshold_sorted


# retrieve the value of grey level for which we have the highest entropy
def entropy_maximization(h, ch, nb):
    threshold_max = 0
    e_max = 0

    sum_min = 0
    sum_max = 0

    for threshold in range(0, 256):
        for k in range(0, 256):
            pi = h[k] / nb
            if pi != 0:
                pi = pi * math.log(pi)
            else:
                pi = 0
            if k <= threshold:
                sum_min = sum_min + pi
            else:
                sum_max = sum_max + pi

        if ch[threshold] != 0:
            sum_min = sum_min / ch[threshold]

        if nb - ch[threshold] != 0:
            sum_max = sum_max / (nb - ch[threshold])

        e = math.log1p(ch[threshold] * (nb - ch[threshold]))
        e = e - sum_min - sum_max

        # we keep the threshold for the maximal entropy
        if e_max < e:
            e_max = e
            threshold_max = threshold
        sum_max = 0
        sum_min = 0

    return threshold_max


# return the list of all threshold sorted by variance
def inter_class_variance_maximization_multi(h, nb):
    threshold_sorted = np.zeros((256, 2), dtype=np.float64)

    sum_min = 0
    sum_max = 0

    nb_min = 0
    nb_max = 0

    mean_max = 0
    mean_min = 0

    for threshold in range(0, 256):
        for k in range(0, 256):
            if k <= threshold:
                nb_min = nb_min + h[k]
                sum_min = sum_min + k*h[k]
            else:
                nb_max = nb_max + h[k]
                sum_max = sum_max + k*h[k]

        if nb_max != 0:
            mean_max = sum_max / nb_max

        if nb_min != 0:
            mean_min = sum_min / nb_min

        sum_total = sum_min + sum_max
        mean = sum_total / nb

        mean_min = mean - mean_min
        mean_max = mean - mean_max

        p_min = nb_min / nb
        p_max = nb_max / nb

        var = p_min * mean_min * mean_min + p_max * mean_max * mean_max

        threshold_sorted[int(threshold)][0] = threshold
        threshold_sorted[int(threshold)][1] = var

        nb_max = 0
        nb_min = 0
        sum_max = 0
        sum_min = 0

    new_threshold_sorted = sorted(threshold_sorted, key=lambda x: x[1], reverse=True)

    return new_threshold_sorted


# retrieve the value of grey level for which we have the highest inter-class variance
def inter_class_variance_maximization(h, nb):
    threshold_max = 0
    var_max = 0

    sum_min = 0
    sum_max = 0

    nb_min = 0
    nb_max = 0

    mean_max = 0
    mean_min = 0

    for threshold in range(0, 256):
        for k in range(0, 256):
            if k <= threshold:
                nb_min = nb_min + h[k]
                sum_min = sum_min + k*h[k]
            else:
                nb_max = nb_max + h[k]
                sum_max = sum_max + k*h[k]

        if nb_max != 0:
            mean_max = sum_max / nb_max

        if nb_min != 0:
            mean_min = sum_min / nb_min

        sum_total = sum_min + sum_max
        mean = sum_total / nb

        mean_min = mean - mean_min
        mean_max = mean - mean_max

        p_min = nb_min / nb
        p_max = nb_max / nb

        var = p_min * mean_min * mean_min + p_max * mean_max * mean_max

        # we keep the threshold that maximize the inter-class variance
        if var_max < var:
            var_max = var
            threshold_max = threshold

        nb_max = 0
        nb_min = 0
        sum_max = 0
        sum_min = 0

    return threshold_max


# show the histogram of an image
def show_histogram(h):
    plt.figure(figsize=(8, 6))
    plt.plot(h)
    plt.axis([0, 255, 0, h.max()])
    plt.xlabel("Value")
    plt.ylabel("Number")
    plt.show()
