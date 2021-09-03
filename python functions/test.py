import os
import cv2
import numpy as np
from tkinter import *

from matplotlib import pyplot

import animal_detection
import car_detection
import histogram
import filter
import hsv
import human_detection
import segmentation
import measure
import video_vision
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def menu():
    print("Menu : Image, video or object detection ?")
    print("1. Analyze an image")
    print("2. Track a ball in a video")
    print("3. Object detection")
    print("0. Quit")


# enter choice for general menu
def enter_choice(mini, maxi):
    while True:
        try:
            choice = int(input("Enter your choice : "))
            break
        except ValueError:
            print("Your choice is not a number.")

    while choice < mini or choice > maxi:
        print("Your choice is not available.")
        menu()
        while True:
            try:
                choice = int(input("Please enter a new one : "))
                break
            except ValueError:
                print("Your choice is not a number.")
    return choice


# treat choice for general menu
def treat_choice_menu(choice):
    # quit
    if choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    # choice 1 : analyze an image
    elif choice == 1:
        choice2 = -2
        while choice2 != -1:
            menu_image()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_image(choice2, "")
    # choice 2 : track a ball
    elif choice == 2:
        choice2 = -2
        while choice2 != -1:
            menu_video()
            choice2 = enter_choice(-1, 1)
            treat_choice_menu_video(choice2)
    elif choice == 3:
        choice2 = -2
        while choice2 != -1:
            menu_object_detection()
            choice2 = enter_choice(-1, 3)
            treat_choice_menu_object_detection(choice2)
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# menu for image
def menu_image():
    print("Menu : Image processing")
    print("1. Filters (Grey image)")
    print("2. Filters (Colored image)")
    print("3. Threshold (Grey image)")
    print("4. Histogram (Grey image)")
    print("5. Segmentation (Binary image)")
    print("0. Quit")
    print("-1. Previous")


# treat choice for image processing menu
def treat_choice_menu_image(choice, path=""):
    if choice > 0 and path == "":
        path = input("Please, enter the absolute path of the image : ")
        is_exist = os.path.exists(path)
        while not is_exist:
            print("Your path is not reachable")
            path = input("Please, enter an available absolute path : ")
            is_exist = os.path.exists(path)

    # return to the general menu
    if choice == -1:
        menu()
        choice2 = enter_choice(0, 3)
        treat_choice_menu(choice2)
    # quit
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        im_original = cv2.imread(path)
        im_grey = np.copy(im_original)
        filter.greyscale(im_original, im_grey)
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_grey()
            choice2 = enter_choice(-1, 12)
            treat_choice_menu_filter_grey(choice2, im_grey, path)
    elif choice == 2:
        im_original = cv2.imread(path)
        im_grey = np.copy(im_original)
        filter.greyscale(im_original, im_grey)
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_colored()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_filter_colored(choice2, im_original, path)
    elif choice == 3:
        im_original = cv2.imread(path)
        im_grey = np.copy(im_original)
        filter.greyscale(im_original, im_grey)
        choice2 = -2
        h, mini, maxi, nb = histogram.compute_histogram(im_grey, 0)
        ch = histogram.cumulative_histogram(h)
        while choice2 != -1:
            menu_image_threshold()
            choice2 = enter_choice(-1, 7)
            if choice2 > 0:
                treat_choice_menu_threshold(choice2, im_grey, h, ch, nb)
            else:
                treat_choice_menu_threshold(choice2, im_grey)
    elif choice == 4:
        im_original = cv2.imread(path)
        im_grey = np.copy(im_original)
        filter.greyscale(im_original, im_grey)
        choice2 = -2
        h, mini, maxi, nb = histogram.compute_histogram(im_grey, 0)
        ch = histogram.cumulative_histogram(h)
        while choice2 != -1:
            menu_image_histogram()
            choice2 = enter_choice(-1, 5)
            if choice2 > 0:
                treat_choice_menu_histogram(choice2, im_grey, h, ch, nb, mini, maxi)
            else:
                treat_choice_menu_histogram(choice2, im_grey)
    elif choice == 5:
        im_original = cv2.imread(path)
        im_grey = np.copy(im_original)
        filter.greyscale(im_original, im_grey)
        choice2 = -2
        shape, im_object, flag, window = compute_shape(im_grey)
        while choice2 != -1:
            menu_image_segmentation()
            choice2 = enter_choice(-1, 10)
            if choice2 > 0:
                treat_choice_menu_segmentation(choice2, im_grey, im_object, shape, flag, window)
            else:
                treat_choice_menu_segmentation(choice2, im_grey)
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# Menu for filter on grey image
def menu_image_filter_grey():
    print("Menu : Filter on grey image")
    print("1. Negative filter")
    print("2. Average filter")
    print("3. Median filter")
    print("4. Gaussian filter")
    print("5. Erosion filter")
    print("6. Dilatation filter")
    print("7. Closing filter")
    print("8. Opening filter")
    print("9. Roberts gradient filter")
    print("10. Prewitt filter")
    print("11. Sobel filter")
    print("12. Laplacian filter")
    print("0. Quit")
    print("-1. Previous")


# treat choice for filter grey
def treat_choice_menu_filter_grey(choice, im_grey, path):
    im_new = np.copy(im_grey)

    if choice == -1:
        choice2 = -2
        while choice2 != -1:
            menu_image()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_image(choice2, "")
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        filter.negative(im_grey, im_new)
        filter.show_image(im_new, register_path_image + "/negative_grey.bmp")
        filter.save_image(im_new, register_path_image + "/negative_grey.bmp")
    elif choice == 2:
        while True:
            try:
                p = int(input("Please enter a dimension for the filter : "))
                if p != abs(p):
                    p = -p
                break
            except ValueError:
                print("Your dimension is not a number.")
        filter.mean(im_grey, im_new, p)
        filter.show_image(im_new, register_path_image + "/average_grey_" + str(2 * p + 1) + ".bmp")
        filter.save_image(im_new, register_path_image + "/average_grey_" + str(2 * p + 1) + ".bmp")
    elif choice == 3:
        while True:
            try:
                p = int(input("Please enter a dimension for the filter : "))
                if p != abs(p):
                    p = -p
                break
            except ValueError:
                print("Your dimension is not a number.")
        filter.median(im_grey, im_new, p)
        filter.show_image(im_new, register_path_image + "/median_grey_" + str(2 * p + 1) + ".bmp")
        filter.save_image(im_new, register_path_image + "/median_grey_" + str(2 * p + 1) + ".bmp")
    elif choice == 4:
        while True:
            try:
                p = int(input("Please enter a dimension for the filter : "))
                if p != abs(p):
                    p = -p
                break
            except ValueError:
                print("Your dimension is not a number.")
        filter.gaussian(im_grey, im_new, p, 0.6)
        filter.show_image(im_new, register_path_image + "/gaussian_grey_" + str(2 * p + 1) + ".bmp")
        filter.save_image(im_new, register_path_image + "/gaussian_grey_" + str(2 * p + 1) + ".bmp")
    elif choice == 5:
        while True:
            try:
                p = int(input("Please enter a dimension for the filter : "))
                if p != abs(p):
                    p = -p
                break
            except ValueError:
                print("Your dimension is not a number.")
        filter.erosion(im_grey, im_new, p)
        filter.show_image(im_new, register_path_image + "/erosion_grey_" + str(2 * p + 1) + ".bmp")
        filter.save_image(im_new, register_path_image + "/erosion_grey_" + str(2 * p + 1) + ".bmp")
    elif choice == 6:
        while True:
            try:
                p = int(input("Please enter a dimension for the filter : "))
                if p != abs(p):
                    p = -p
                break
            except ValueError:
                print("Your dimension is not a number.")
        filter.dilatation(im_grey, im_new, p)
        filter.show_image(im_new, register_path_image + "/dilatation_grey_" + str(2 * p + 1) + ".bmp")
        filter.save_image(im_new, register_path_image + "/dilatation_grey_" + str(2 * p + 1) + ".bmp")
    elif choice == 7:
        while True:
            try:
                p = int(input("Please enter a dimension for the filter : "))
                if p != abs(p):
                    p = -p
                break
            except ValueError:
                print("Your dimension is not a number.")
        filter.closing(im_grey, im_new, p)
        filter.show_image(im_new, register_path_image + "/closing_grey_" + str(2 * p + 1) + ".bmp")
        filter.save_image(im_new, register_path_image + "/closing_grey_" + str(2 * p + 1) + ".bmp")
    elif choice == 8:
        while True:
            try:
                p = int(input("Please enter a dimension for the filter : "))
                if p != abs(p):
                    p = -p
                break
            except ValueError:
                print("Your dimension is not a number.")
        filter.opening(im_grey, im_new, p)
        filter.show_image(im_new, register_path_image + "/opening_grey_" + str(2 * p + 1) + ".bmp")
        filter.save_image(im_new, register_path_image + "/opening_grey_" + str(2 * p + 1) + ".bmp")
    elif choice == 9:
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_grey_sobel_prewitt_roberts("Menu : Roberts filters")
            choice2 = enter_choice(-1, 4)
            treat_choice_menu_filter_grey_roberts(choice2, im_grey, path)
    elif choice == 10:
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_grey_sobel_prewitt_roberts("Menu : Prewitt filters")
            choice2 = enter_choice(-1, 4)
            treat_choice_menu_filter_grey_prewitt(choice2, im_grey, path)
    elif choice == 11:
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_grey_sobel_prewitt_roberts("Menu : Sobel filters")
            choice2 = enter_choice(-1, 4)
            treat_choice_menu_filter_grey_sobel(choice2, im_grey, path)
    elif choice == 12:
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_grey_laplacian()
            choice2 = enter_choice(-1, 2)
            treat_choice_menu_filter_grey_laplacian(choice2, im_grey, path)
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# Menu for sobel, prewitt, roberts
def menu_image_filter_grey_sobel_prewitt_roberts(title):
    print(title)
    print("1. Norm L1")
    print("2. Norm L2")
    print("3. Norm Lsup")
    print("4. Direction")
    print("0. Quit")
    print("-1. Previous")


# treat choice for roberts
def treat_choice_menu_filter_grey_roberts(choice, im_grey, path):
    im_new = np.copy(im_grey)

    if choice == -1:
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_grey()
            choice2 = enter_choice(-1, 12)
            treat_choice_menu_filter_grey(choice2, im_grey, path)
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        filter.roberts_gradient(im_grey, im_new, 1)
        filter.show_image(im_new, register_path_image + "/roberts_L1_grey.bmp")
        filter.save_image(im_new, register_path_image + "/roberts_L1_grey.bmp")
    elif choice == 2:
        filter.roberts_gradient(im_grey, im_new, 2)
        filter.show_image(im_new, register_path_image + "/roberts_L2_grey.bmp")
        filter.save_image(im_new, register_path_image + "/roberts_L2_grey.bmp")
    elif choice == 3:
        filter.roberts_gradient(im_grey, im_new, 3)
        filter.show_image(im_new, register_path_image + "/roberts_Lsup_grey.bmp")
        filter.save_image(im_new, register_path_image + "/roberts_Lsup_grey.bmp")
    elif choice == 4:
        filter.roberts_gradient(im_grey, im_new, 4)
        filter.show_image(im_new, register_path_image + "/roberts_direction_grey.bmp")
        filter.save_image(im_new, register_path_image + "/roberts_direction_grey.bmp")
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# treat choice for prewitt
def treat_choice_menu_filter_grey_prewitt(choice, im_grey, path):
    im_new = np.copy(im_grey)

    if choice == -1:
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_grey()
            choice2 = enter_choice(-1, 12)
            treat_choice_menu_filter_grey(choice2, im_grey, path)
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        filter.prewitt(im_grey, im_new, 1)
        filter.show_image(im_new, register_path_image + "/prewitt_L1_grey.bmp")
        filter.save_image(im_new, register_path_image + "/prewitt_L1_grey.bmp")
    elif choice == 2:
        filter.prewitt(im_grey, im_new, 2)
        filter.show_image(im_new, register_path_image + "/prewitt_L2_grey.bmp")
        filter.save_image(im_new, register_path_image + "/prewitt_L2_grey.bmp")
    elif choice == 3:
        filter.prewitt(im_grey, im_new, 3)
        filter.show_image(im_new, register_path_image + "/prewitt_Lsup_grey.bmp")
        filter.save_image(im_new, register_path_image + "/prewitt_Lsup_grey.bmp")
    elif choice == 4:
        filter.prewitt(im_grey, im_new, 4)
        filter.show_image(im_new, register_path_image + "/prewitt_direction_grey.bmp")
        filter.save_image(im_new, register_path_image + "/prewitt_direction_grey.bmp")
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# treat choice for sobel
def treat_choice_menu_filter_grey_sobel(choice, im_grey, path):
    im_new = np.copy(im_grey)

    if choice == -1:
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_grey()
            choice2 = enter_choice(-1, 12)
            treat_choice_menu_filter_grey(choice2, im_grey, path)
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        filter.sobel(im_grey, im_new, 1)
        filter.show_image(im_new, register_path_image + "/sobel_L1_grey.bmp")
        filter.save_image(im_new, register_path_image + "/sobel_L1_grey.bmp")
    elif choice == 2:
        filter.sobel(im_grey, im_new, 2)
        filter.show_image(im_new, register_path_image + "/sobel_L2_grey.bmp")
        filter.save_image(im_new, register_path_image + "/sobel_L2_grey.bmp")
    elif choice == 3:
        filter.sobel(im_grey, im_new, 3)
        filter.show_image(im_new, register_path_image + "/sobel_Lsup_grey.bmp")
        filter.save_image(im_new, register_path_image + "/sobel_Lsup_grey.bmp")
    elif choice == 4:
        filter.sobel(im_grey, im_new, 4)
        filter.show_image(im_new, register_path_image + "/sobel_direction_grey.bmp")
        filter.save_image(im_new, register_path_image + "/sobel_direction_grey.bmp")
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# Menu for laplacian
def menu_image_filter_grey_laplacian():
    print("Menu : Laplacian filter")
    print("1. First matrix")
    print("   | 0 -1  0 |")
    print("   |-1  4 -1 |")
    print("   | 0 -1  0 |")
    print("2. Second matrix")
    print("   |-1 -1 -1 |")
    print("   |-1  8 -1 |")
    print("   |-1 -1 -1 |")
    print("0. Quit")
    print("-1. Previous")


# treat choice for laplacian
def treat_choice_menu_filter_grey_laplacian(choice, im_grey, path):
    im_new = np.copy(im_grey)

    if choice == -1:
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_grey()
            choice2 = enter_choice(-1, 12)
            treat_choice_menu_filter_grey(choice2, im_grey, path)
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        filter.laplacian(im_grey, im_new, 4)
        filter.show_image(im_new, register_path_image + "/laplacian_4_grey.bmp")
        filter.save_image(im_new, register_path_image + "/laplacian_4_grey.bmp")
    elif choice == 2:
        filter.laplacian(im_grey, im_new, 8)
        filter.show_image(im_new, register_path_image + "/laplacian_8_grey.bmp")
        filter.save_image(im_new, register_path_image + "/laplacian_8_grey.bmp")
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# Menu on filter with colored image
def menu_image_filter_colored():
    print("Menu : Filter on colored image")
    print("1. Negative filter")
    print("2. Grey filter")
    print("3. Median filter")
    print("4. Convert into HSV")
    print("5. Colored filter")
    print("0. Quit")
    print("-1. Previous")


# treat choice for colored filter
def treat_choice_menu_filter_colored(choice, im_colored, path):
    im_new = np.copy(im_colored)

    if choice == -1:
        choice2 = -2
        while choice2 != -1:
            menu_image()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_image(choice2, "")
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        filter.negative(im_colored, im_new)
        filter.show_image(im_new, register_path_image + "/negative_colored.bmp")
        filter.save_image(im_new, register_path_image + "/negative_colored.bmp")
    elif choice == 2:
        filter.greyscale(im_colored, im_new)
        filter.show_image(im_new, register_path_image + "/grey_colored.bmp")
        filter.save_image(im_new, register_path_image + "/grey_colored.bmp")
    elif choice == 3:
        while True:
            try:
                p = int(input("Please enter a dimension for the filter : "))
                if p != abs(p):
                    p = -p
                break
            except ValueError:
                print("Your dimension is not a number.")
        filter.median_rgb(im_colored, im_new, p)
        filter.show_image(im_new, register_path_image + "/median_colored_" + str(2 * p + 1) + ".bmp")
        filter.save_image(im_new, register_path_image + "/median_colored_" + str(2 * p + 1) + ".bmp")
    elif choice == 4:
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_colored_hsv()
            choice2 = enter_choice(-1, 3)
            if choice2 > 0:
                im_hue = np.copy(im_colored)
                im_saturation = np.copy(im_colored)
                im_value = np.copy(im_colored)
                hsv.compute_hsv(im_colored, im_hue, im_saturation, im_value)
                treat_choice_menu_filter_colored_hsv(choice2, im_colored, path, im_hue, im_saturation, im_value)
            else:
                treat_choice_menu_filter_colored_hsv(choice2, im_colored, path)
    elif choice == 5:
        while True:
            try:
                color = int(input("Choose a color between : red (0), green (1), blue (2), yellow (3), cyan (4), "
                                  "magenta (5)"))
                break
            except ValueError:
                print("Your color is not a number.")

        while 5 < color < 0:
            print("The color is not available.")
            while True:
                try:
                    color = int(input(
                        "Choose a color between : red (0), green (1), blue (2), yellow (3), cyan (4), magenta (5)"))
                    break
                except ValueError:
                    print("Your color is not a number.")

        if color == 0:
            filter.red_filter(im_colored, im_new)
            filter.show_image(im_new, register_path_image + "/red_colored.bmp")
            filter.save_image(im_new, register_path_image + "/red_colored.bmp")
        elif color == 1:
            filter.green_filter(im_colored, im_new)
            filter.show_image(im_new, register_path_image + "/green_colored.bmp")
            filter.save_image(im_new, register_path_image + "/green_colored.bmp")
        elif color == 2:
            filter.blue_filter(im_colored, im_new)
            filter.show_image(im_new, register_path_image + "/blue_colored.bmp")
            filter.save_image(im_new, register_path_image + "/blue_colored.bmp")
        elif color == 3:
            filter.yellow_filter(im_colored, im_new)
            filter.show_image(im_new, register_path_image + "/yellow_colored.bmp")
            filter.save_image(im_new, register_path_image + "/yellow_colored.bmp")
        elif color == 4:
            filter.cyan_filter(im_colored, im_new)
            filter.show_image(im_new, register_path_image + "/cyan_colored.bmp")
            filter.save_image(im_new, register_path_image + "/cyan_colored.bmp")
        elif color == 5:
            filter.magenta_filter(im_colored, im_new)
            filter.show_image(im_new, register_path_image + "/magenta_colored.bmp")
            filter.save_image(im_new, register_path_image + "/magenta_colored.bmp")
        else:
            print("You're not suppose to be here !")
            sys.exit(1)
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# Menu for hsv
def menu_image_filter_colored_hsv():
    print("Menu : HSV conversion")
    print("1. Hue")
    print("2. Saturation")
    print("3. Value")
    print("0. Quit")
    print("-1. Previous")


# treat choice for colored filter hsv
def treat_choice_menu_filter_colored_hsv(choice, im_colored, path, im_hue=None, im_saturation=None, im_value=None):
    if choice > 0 and (im_hue is None or im_saturation is None or im_value is None):
        print("An issue has occurred, there is no matrices")
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_colored()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_filter_colored(choice2, im_colored, path)

    if choice == -1:
        choice2 = -2
        while choice2 != -1:
            menu_image_filter_colored()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_filter_colored(choice2, im_colored, path)
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        filter.show_image(im_hue, register_path_image + "/hue_colored.bmp")
        filter.save_image(im_hue, register_path_image + "/hue_colored.bmp")
    elif choice == 2:
        filter.show_image(im_saturation, register_path_image + "/saturation_colored.bmp")
        filter.save_image(im_saturation, register_path_image + "/saturation_colored.bmp")
    elif choice == 3:
        filter.show_image(im_value, register_path_image + "/value_colored.bmp")
        filter.save_image(im_value, register_path_image + "/value_colored.bmp")
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# Menu for threshold on grey image
def menu_image_threshold():
    print("Menu : Threshold on grey image")
    print("1. Manual")
    print("2. Entropy maximization")
    print("3. Variance inter-class maximization")
    print("4. Multi entropy maximization")
    print("5. Multi variance inter-class maximization")
    print("6. Manual multi threshold")
    print("7. Watershed")
    print("0. Quit")
    print("-1. Previous")


# treat choice for threshold menu
def treat_choice_menu_threshold(choice, im_grey, h=None, ch=None, nb=0):
    im_new = np.copy(im_grey)

    if (choice == 2 or choice == 3 or choice == 4 or choice == 5) and (h is None or ch is None or nb == 0):
        print("An issue has occurred, there is no histogram")
        choice2 = -2
        while choice2 != -1:
            menu_image()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_image(choice2, "")

    if choice == -1:
        choice2 = -2
        while choice2 != -1:
            menu_image()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_image(choice2, "")
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        while True:
            try:
                threshold = int(input("Please enter a threshold between 0 and 255 included : "))
                break
            except ValueError:
                print("Your threshold is not a number.")

        while threshold < 0 or threshold > 255:
            print("The threshold is not available.")
            while True:
                try:
                    threshold = int(input("Please enter a threshold between 0 and 255 included : "))
                    break
                except ValueError:
                    print("Your threshold is not a number.")

        filter.manual_threshold(im_grey, im_new, threshold)
        filter.show_image(im_new, register_path_image + "/manual_threshold_grey_" + str(threshold) + ".bmp")
        filter.save_image(im_new, register_path_image + "/manual_threshold_grey_" + str(threshold) + ".bmp")
    elif choice == 2:
        threshold = histogram.entropy_maximization(h, ch, nb)
        print("The best threshold is then : ", threshold)
        filter.manual_threshold(im_grey, im_new, threshold)
        filter.show_image(im_new, register_path_image + "/entropy_threshold_grey_" + str(threshold) + ".bmp")
        filter.save_image(im_new, register_path_image + "/entropy_threshold_grey_" + str(threshold) + ".bmp")
    elif choice == 3:
        threshold = histogram.inter_class_variance_maximization(h, nb)
        print("The best threshold is then : ", threshold)
        filter.manual_threshold(im_grey, im_new, threshold)
        filter.show_image(im_new, register_path_image + "/variance_threshold_grey_" + str(threshold) + ".bmp")
        filter.save_image(im_new, register_path_image + "/variance_threshold_grey_" + str(threshold) + ".bmp")
    elif choice == 4:
        while True:
            try:
                k = int(input("Please enter a number of thresholds between 1 and 255 included : "))
                break
            except ValueError:
                print("Your number of threshold is not a number.")
        while 255 < k or k < 1:
            print("The number of thresholds is not available.")
            while True:
                try:
                    k = int(input("Please enter a number of thresholds between 1 and 255 included : "))
                    break
                except ValueError:
                    print("Your number of threshold is not a number.")

        list_threshold = histogram.entropy_maximization_multi(h, ch, nb)
        histogram.multi_k_thresholding(im_grey, im_new, list_threshold, k)
        filter.show_image(im_new, register_path_image + "/entropy_" + str(k) + "_threshold_grey.bmp")
        filter.save_image(im_new, register_path_image + "/entropy_" + str(k) + "_threshold_grey.bmp")
    elif choice == 5:
        while True:
            try:
                k = int(input("Please enter a number of thresholds between 1 and 255 included : "))
                break
            except ValueError:
                print("Your number of threshold is not a number.")

        while 255 < k or k < 1:
            print("The number of thresholds is not available.")
            while True:
                try:
                    k = int(input("Please enter a number of thresholds between 1 and 255 included : "))
                    break
                except ValueError:
                    print("Your number of threshold is not a number.")

        list_threshold = histogram.inter_class_variance_maximization_multi(h, nb)
        histogram.multi_k_thresholding(im_grey, im_new, list_threshold, k)
        filter.show_image(im_new, register_path_image + "/variance_" + str(k) + "_threshold_grey.bmp")
        filter.save_image(im_new, register_path_image + "/variance_" + str(k) + "_threshold_grey.bmp")
    elif choice == 6:
        while True:
            try:
                k = int(input("Please enter a number of thresholds between 1 and 255 included : "))
                break
            except ValueError:
                print("Your number of threshold is not a number.")
        while 255 < k or k < 1:
            print("The number of thresholds is not available.")
            while True:
                try:
                    k = int(input("Please enter a number of thresholds between 1 and 255 included : "))
                    break
                except ValueError:
                    print("Your number of threshold is not a number.")

        list_threshold = np.zeros((k, 2), dtype=np.float64)
        for i in range(0, k):
            while True:
                try:
                    threshold = int(input("Please enter a thresholds between 1 and 255 included : "))
                    break
                except ValueError:
                    print("Your threshold is not a number.")

            while 255 < k or k < 1:
                print("The thresholds is not available.")
                while True:
                    try:
                        threshold = int(input("Please enter a thresholds between 1 and 255 included : "))
                        break
                    except ValueError:
                        print("Your threshold is not a number.")

            list_threshold[i][0] = threshold
        histogram.multi_k_thresholding(im_grey, im_new, list_threshold, k)
        filter.show_image(im_new, register_path_image + "/manual_" + str(k) + "_threshold_grey.bmp")
        filter.save_image(im_new, register_path_image + "/manual_" + str(k) + "_threshold_grey.bmp")
    elif choice == 7:
        while True:
            try:
                window = int(input("Please enter the window that you want to use (V4 : 4 or V8 : 8) : "))
                break
            except ValueError:
                print("Your window is not a number.")

        while window != 4 and window != 8:
            print("The window is not available.")
            while True:
                try:
                    window = int(input("Please enter the window that you want to use (V4 : 4 or V8 : 8) : "))
                    break
                except ValueError:
                    print("Your window is not a number.")

        while True:
            try:
                distance_color = int(input("Please enter the color distance between two pixels of the same region : "))
                break
            except ValueError:
                print("Your distance is not a number.")

        while 20 < distance_color or distance_color < 0:
            print("The window is not available.")
            while True:
                try:
                    distance_color = int(
                        input("Please enter the color distance between two pixel of the same region : "))
                    break
                except ValueError:
                    print("Your distance is not a number.")

        segmentation.watershed(im_grey, im_new, window, distance_color)
        filter.show_image(im_new, register_path_image + "/watershed_grey.bmp")
        filter.save_image(im_new, register_path_image + "/watershed_grey.bmp")
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# Menu for histogram
def menu_image_histogram():
    print("Menu : Histogram and Entropy")
    print("1. Histogram")
    print("2. Cumulative histogram")
    print("3. Dynamical expansion")
    print("4. Histogram equalization")
    print("5. Entropy")
    print("0. Quit")
    print("-1. Previous")


# treat choice for histogram menu
def treat_choice_menu_histogram(choice, im_grey, h=None, ch=None, nb=0, mini=0, maxi=0):
    im_new = np.copy(im_grey)

    if choice > 0 and (h is None or ch is None or nb == 0):
        print("An issue has occurred, there is no histogram")
        choice2 = -2
        while choice2 != -1:
            menu_image()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_image(choice2, "")

    if choice == -1:
        choice2 = -2
        while choice2 != -1:
            menu_image()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_image(choice2, "")
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        pyplot.plot(h)
        pyplot.xlabel("Value")
        pyplot.ylabel("Number")
        pyplot.axis([0, 255, 0, h.max()])
        pyplot.savefig(register_path_image + "/histogram_grey.png")
        pyplot.show()
    elif choice == 2:
        pyplot.plot(ch)
        pyplot.xlabel("Value")
        pyplot.ylabel("Number")
        pyplot.axis([0, 255, 0, ch.max()])
        pyplot.savefig(register_path_image + "/cumulative_histogram_grey.png")
        pyplot.show()
    elif choice == 3:
        print("The actual minimum is ", mini, " and the maximum is ", maxi)
        while True:
            try:
                new_value = int(input("Do you want to choose the new mini and the new maxi ? yes : 1, no : otherwise"))
                break
            except ValueError:
                print("Your choice is not a number.")

        if new_value == 1:
            while True:
                try:
                    v_min = int(input("Please enter the new mini that you want : "))
                    break
                except ValueError:
                    print("Your new mini is not a number.")

            while v_min < 0 or v_min > 255:
                print("The mini is not available.")
                while True:
                    try:
                        v_min = int(input("Please enter the new mini that you want : "))
                        break
                    except ValueError:
                        print("Your new mini is not a number.")

            while True:
                try:
                    v_max = int(input("Please enter the new maxi that you want : "))
                    break
                except ValueError:
                    print("Your new maxi is not a number.")

            while v_max <= v_min or v_max > 255:
                print("The maxi is not available.")
                while True:
                    try:
                        v_max = int(input("Please enter the new maxi that you want : "))
                        break
                    except ValueError:
                        print("Your new maxi is not a number.")

            histogram.contrast_stretching(im_grey, im_new, mini, maxi, v_min, v_max)
        else:
            histogram.contrast_stretching(im_grey, im_new, mini, maxi)
        h2, mini2, maxi2, nb2 = histogram.compute_histogram(im_new, 0)
        pyplot.plot(h2)
        pyplot.xlabel("Value")
        pyplot.ylabel("Number")
        pyplot.axis([0, 255, 0, h2.max()])
        pyplot.savefig(register_path_image + "/histogram_dynamical_expansion_grey.png")
        pyplot.show()
        filter.show_image(im_new, register_path_image + "/dynamical_expansion_grey_" + str(mini2) + "_to_" + str(maxi2)
                          + ".bmp")
        filter.save_image(im_new, register_path_image + "/dynamical_expansion_grey_" + str(mini2) + "_to_" + str(maxi2)
                          + ".bmp")
    elif choice == 4:
        histogram.histogram_equalization(im_grey, im_new, ch, nb)
        h2, mini2, maxi2, nb2 = histogram.compute_histogram(im_new, 0)
        pyplot.plot(h2)
        pyplot.xlabel("Value")
        pyplot.ylabel("Number")
        pyplot.axis([0, 255, 0, h2.max()])
        pyplot.savefig(register_path_image + "/histogram_equalization_grey.png")
        pyplot.show()
        filter.show_image(im_new, register_path_image + "/equalization_grey.bmp")
        filter.save_image(im_new, register_path_image + "/equalization_grey.bmp")
    elif choice == 5:
        print("The entropy of the image is : ", histogram.entropy(h, nb))
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# Menu for segmentation
def menu_image_segmentation():
    print("Menu : Segmentation functions")
    print("1. Region growing")
    print("2. Dilatation")
    print("3. Erosion")
    print("4. Bounding Box")
    print("5. Perimeter")
    print("6. Area")
    print("7. Geometrical circularity")
    print("8. Blaschke coefficient")
    print("9. Connectivity")
    print("10. Elongation")
    print("0. Quit")
    print("-1. Previous")


# we compute the shape with an image for the segmentation
def compute_shape(im_grey):
    im_object = np.copy(im_grey)
    im_new = np.copy(im_grey)

    while True:
        try:
            color = int(input("Please enter the color of the object (0 or 255) : "))
            break
        except ValueError:
            print("Your new color is not a number.")

    while color != 0 and color != 255:
        print("The color is not available.")
        while True:
            try:
                color = int(input("Please enter the color of the object (0 or 255) : "))
                break
            except ValueError:
                print("Your new color is not a number.")

    while True:
        try:
            flag = int(input("Please enter a flag between 0 and 255 included : "))
            break
        except ValueError:
            print("Your flag is not a number.")

    while 255 < flag or flag < 0:
        print("The flag is not available.")
        while True:
            try:
                flag = int(input("Please enter a flag between 0 and 255 included : "))
                break
            except ValueError:
                print("Your flag is not a number.")

    while True:
        try:
            window = int(input("Please enter the window that you want to use (V4 : 4 or V8 : 8) : "))
            break
        except ValueError:
            print("Your window is not a number.")

    while window != 4 and window != 8:
        print("The window is not available.")
        while True:
            try:
                window = int(input("Please enter the window that you want to use (V4 : 4 or V8 : 8) : "))
                break
            except ValueError:
                print("Your window is not a number.")

    while True:
        try:
            distance_color = int(input("Please enter the color distance between two pixel of the same region : "))
            break
        except ValueError:
            print("Your distance is not a number.")

    while 20 < distance_color or distance_color < 0:
        print("The window is not available.")
        while True:
            try:
                distance_color = int(
                    input("Please enter the color distance between two pixel of the same region : "))
                break
            except ValueError:
                print("Your distance is not a number.")

    h, mini, maxi, nb = histogram.compute_histogram(im_grey, 0)
    threshold = histogram.inter_class_variance_maximization(h, nb)
    filter.manual_threshold(im_grey, im_new, threshold)
    segmentation.region_growing_process(im_new, im_object, color, flag, 0, im_grey.shape[0] - 1, 0,
                                        im_grey.shape[1] - 1, distance_color, window)
    shape = measure.shape_points(im_new, im_object, flag, 0, im_grey.shape[0] - 1, 0,
                                 im_grey.shape[1] - 1)
    return shape, im_object, flag, window


# treat choice for segmentation
def treat_choice_menu_segmentation(choice, im_grey, im_object=None, shape=None, flag=0, window=8):
    if choice > 0 and shape is None or im_object is None:
        print("An issue has occurred, there is no shape.")
        choice2 = -2
        while choice2 != -1:
            menu_image()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_image(choice2, "")

    if choice == -1:
        choice2 = -2
        while choice2 != -1:
            menu_image()
            choice2 = enter_choice(-1, 5)
            treat_choice_menu_image(choice2, "")
    elif choice == 0:
        sys.exit(0)
    elif choice == 1:
        filter.show_image(im_object, register_path_image + "/region_growing_grey.bmp")
        filter.save_image(im_object, register_path_image + "/region_growing_grey.bmp")
    elif choice == 2:
        while True:
            try:
                distance_color = int(input("Please enter the distance for the dilatation : "))
                break
            except ValueError:
                print("Your distance is not a number.")

        while 20 < distance_color or distance_color < 0:
            print("The window is not available.")
            while True:
                try:
                    distance_color = int(
                        input("Please enter the distance for the dilatation : "))
                    break
                except ValueError:
                    print("Your distance is not a number.")

        im_new = np.copy(im_object)
        segmentation.dilatation(im_object, im_new, flag, 0, im_grey.shape[0] - 1, 0, im_grey.shape[1] - 1,
                                window, distance_color)
        filter.show_image(im_new, register_path_image + "/dilatation_grey.bmp")
        filter.save_image(im_new, register_path_image + "/dilatation_grey.bmp")
    elif choice == 3:
        while True:
            try:
                distance_color = int(input("Please enter the distance for erosion : "))
                break
            except ValueError:
                print("Your distance is not a number.")

        while 20 < distance_color or distance_color < 0:
            print("The window is not available.")
            while True:
                try:
                    distance_color = int(
                        input("Please enter the color distance between two pixel of the same region : "))
                    break
                except ValueError:
                    print("Your distance is not a number.")

        im_new = np.copy(im_object)
        segmentation.erosion(im_object, im_new, flag, 0, im_grey.shape[0] - 1, 0, im_grey.shape[1] - 1,
                             window, distance_color)
        filter.show_image(im_new, register_path_image + "/erosion_grey.bmp")
        filter.save_image(im_new, register_path_image + "/erosion_grey.bmp")
    elif choice == 4:
        p1, p2, p3, p4 = shape.get_bb_points()
        im_new = np.copy(im_object)
        for i in range(p1.get_i(), p2.get_i() + 1):
            j = p1.get_j()
            im_new[i][j][2] = 255
            im_new[i][j][1] = 0
            im_new[i][j][0] = 0

        for i in range(p4.get_i(), p3.get_i() + 1):
            j = p4.get_j()
            im_new[i][j][2] = 255
            im_new[i][j][1] = 0
            im_new[i][j][0] = 0

        for j in range(p1.get_j(), p4.get_j() + 1):
            i = p1.get_i()
            im_new[i][j][2] = 255
            im_new[i][j][1] = 0
            im_new[i][j][0] = 0

        for j in range(p2.get_j(), p3.get_j() + 1):
            i = p2.get_i()
            im_new[i][j][2] = 255
            im_new[i][j][1] = 0
            im_new[i][j][0] = 0

        print("Coordinates : bottom_left (", p1.get_i(), ",", p1.get_j(), "), bottom_right (", p2.get_i(), ",",
              p2.get_j(), "), top_right (", p3.get_i(), ",", p3.get_j(), "), top_left (", p4.get_i(), ",",
              p4.get_j(), ")")
        filter.show_image(im_new, register_path_image + "/bounding box_grey.bmp")
        filter.save_image(im_new, register_path_image + "/bounding box_grey.bmp")
    elif choice == 5:
        print("The perimeter of the shape is : ", shape.get_perimeter())
    elif choice == 6:
        print("The area of the shape is : ", shape.get_area())
    elif choice == 7:
        measure.geometrical_circularity(shape)
        print("The geometrical circularity of the shape is : ", shape.get_geometrical())
    elif choice == 8:
        measure.symmetry_measure(shape, im_object)
        print("The blaschke coefficient is : ", shape.get_blaschke())
    elif choice == 9:
        measure.connectivity(shape, im_object, 1, window)
        print("The connectivity of the shape is : ", shape.get_connect())
    elif choice == 10:
        print("The elongation of the shape is : ", shape.get_elongation())
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# menu for video
def menu_video():
    print("Menu : Track a ball")
    print("1. Tracking")
    print("0. Quit")
    print("-1. Previous")


def menu_video_data():
    print("Menu : Track a ball - data collected")
    print("1. Position of the ball in function of time")
    print("2. Norm of the speed of the ball in function of time")
    print("3. Direction of the speed of the ball in function of time")
    print("4. Average of the speed of the ball")
    print("0. Quit")
    print("-1. Previous")


def treat_choice_menu_video(choice):
    # return to the general menu
    if choice == -1:
        menu()
        choice2 = enter_choice(0, 3)
        treat_choice_menu(choice2)
    # quit
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        ball_center_i, ball_center_j, ball_time, ball_speed, ball_direction, ball_speed_average = \
            video_vision.launch_video(register_path_video)
        choice2 = -2
        while choice2 != -1:
            menu_video_data()
            choice2 = enter_choice(-1, 4)
            if choice2 > 0:
                treat_choice_menu_video_data(choice2, ball_center_i, ball_center_j, ball_time, ball_speed,
                                             ball_direction, ball_speed_average)
            else:
                treat_choice_menu_video_data(choice)
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


def treat_choice_menu_video_data(choice, ball_center_i=None, ball_center_j=None, ball_time=None,
                                 ball_speed=None, ball_direction=None, ball_speed_average=0):

    if choice > 0 and (ball_center_i is None or ball_center_j is None or ball_time is None or ball_direction is None
                       or ball_speed is None):
        print("An issue has occurred, there is no ball or no video")
        menu()
        choice2 = enter_choice(-1, 1)
        treat_choice_menu_video(choice2)

    # return to the general menu
    if choice == -1:
        menu()
        choice2 = enter_choice(-1, 1)
        treat_choice_menu_video(choice2)
    # quit
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        video_vision.print_ball_center(ball_center_i, ball_center_j, ball_time, register_path_video)
    elif choice == 2:
        video_vision.print_norm_speed(ball_speed, ball_time, register_path_video)
    elif choice == 3:
        video_vision.print_direction_speed(ball_direction, ball_time, register_path_video)
    elif choice == 4:
        print("The speed average of the ball is ", ball_speed_average, " pxl/s")
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# menu for object detection
def menu_object_detection():
    print("Menu : Object detection")
    print("1. Human detection (body and face)")
    print("2. Animal detection (cat's face and birds")
    print("3. Car detection")
    print("0. Quit")
    print("-1. Previous")


def treat_choice_menu_object_detection(choice):
    # return to the general menu
    if choice == -1:
        menu()
        choice2 = enter_choice(0, 3)
        treat_choice_menu(choice2)
    # quit
    elif choice == 0:
        print("Thank you and goodbye !")
        sys.exit(0)
    elif choice == 1:
        human_detection.main_human_detection()
    elif choice == 2:
        while True:
            try:
                cat_birds_choice= int(input("Cat (1) or birds (otherwise) ? "))
                break
            except ValueError:
                print("Your choice is not a number.")
        animal_detection.main_animal_detection(cat_birds_choice)
    elif choice == 3:
        car_detection.main_car_detection()
    else:
        print("You're not suppose to be here !")
        sys.exit(1)


# main

register_path_image = input("Please, enter the absolute path of the repertory where you will register the results "
                            "of image processing : ")
is_exist = os.path.exists(register_path_image)
while not is_exist:
    print("Your path is not reachable")
    register_path_image  = input("Please, enter an available absolute path : ")
    is_exist = os.path.exists(register_path_image )

register_path_video = input("Please, enter the absolute path of the repertory where you will register the results "
                            "of video processing : ")
is_exist = os.path.exists(register_path_video)
while not is_exist:
    print("Your path is not reachable")
    register_path_video = input("Please, enter an available absolute path : ")
    is_exist = os.path.exists(register_path_video )
            
menu()
choice = enter_choice(0, 3)
treat_choice_menu(choice)

