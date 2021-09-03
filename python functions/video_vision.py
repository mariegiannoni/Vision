import os
import sys

import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from matplotlib import pyplot

import filter
import measure
import segmentation


#  check ball
def check_ball(im_frame, im_frame_witness, color, flag, background, ball_old_size,
               ball_old_i_min, ball_old_i_max, ball_old_j_min, ball_old_j_max, limit_size):
    ball = False
    points = []
    ball_actual_size = 0
    ball_actual_center_i = 0
    ball_actual_center_j = 0
    ball_actual_i_min = 0
    ball_actual_i_max = 0
    ball_actual_j_min = 0
    ball_actual_j_max = 0
    # we look for the ball
    for i in range(0, im_frame.shape[0]):
        for j in range(0, im_frame.shape[1]):
            if im_frame[i][j][0] == color and im_frame_witness[i][j][0] == background:
                # we find a point that is not in the witness, it is our seed and it could be a ball
                points, ball_actual_size, ball_actual_i_min, ball_actual_i_max, ball_actual_j_min, ball_actual_j_max \
                    = segmentation.region_growing_seed(im_frame, im_frame_witness, color, i, j, flag,
                                                       0, im_frame.shape[0] - 1, 0, im_frame.shape[1] - 1, 25, 8)
                # We don't need to check in the bounding box of the previous candidate
                # so we jump to the maximum i and j find

                # we check the size and the elongation of the ball
                # we conserve the candidate in a tab if it verifies this two conditions
                if ball_actual_i_max - ball_actual_i_min != 0:
                    elongation = (ball_actual_j_max - ball_actual_j_min) / (ball_actual_i_max - ball_actual_i_min)
                    if ball_old_size == -1:
                        if ball_actual_size > limit_size and abs(1 - elongation) < 0.15:
                            ball = True
                            ball_actual_center_i = (ball_actual_i_max - ball_actual_i_min) / 2
                            ball_actual_center_j = (ball_actual_j_max - ball_actual_j_min) / 2
                            return ball, points, ball_actual_size, ball_actual_center_i, ball_actual_center_j, \
                                ball_actual_i_min, ball_actual_i_max, ball_actual_j_min, ball_actual_j_max
                    else:
                        elongation_old = (ball_old_j_max - ball_old_j_min) / (ball_old_i_max - ball_old_i_min)
                        if abs(ball_old_size - ball_actual_size) < 0.2 * limit_size \
                                and abs(elongation_old - elongation) < 0.25:
                            ball = True
                            ball_actual_center_i = (ball_actual_i_max - ball_actual_i_min) / 2
                            ball_actual_center_j = (ball_actual_j_max - ball_actual_j_min) / 2
                            return ball, points, ball_actual_size, ball_actual_center_i, ball_actual_center_j, \
                                ball_actual_i_min, ball_actual_i_max, ball_actual_j_min, ball_actual_j_max

    return ball, points, ball_actual_size, ball_actual_center_i, ball_actual_center_j, \
        ball_actual_i_min, ball_actual_i_max, ball_actual_j_min, ball_actual_j_max


# same center
def same_center(old_i, old_j, new_i, new_j):
    if old_i == new_i and old_j == new_j:
        return True
    else:
        return False


# compute the speed
def speed(old_time, new_time, old_i, old_j, new_i, new_j):
    return measure.distance(old_i, old_j, new_i, new_j) / (new_time - old_time)


# compute the direction
def direction(old_i, old_j, new_i, new_j):
    if old_i == new_i:
        return 0
    else:
        return (old_j - new_j) / (old_i - new_i)


# launch the video
def launch_video(register_path_video):
    path = input("Please, enter the absolute path of a video : ")
    is_exist = os.path.exists(path)
    while not is_exist:
        print("Your video is not reachable")
        path = input("Please, enter an available absolute path : ")
        is_exist = os.path.exists(path)
    video_original = cv2.VideoCapture(path)
    if not video_original.isOpened():
        print("We can't open the video")
        sys.exit(1)
    print("You use the video at the path : ", path)

    while True:
        try:
            color = int(input("Please enter the color of the ball (0 or 255) : "))
            break
        except ValueError:
            print("Your color is not a number.")

    while color != 0 and color != 255:
        print("The color is not available.")
        while True:
            try:
                color = int(input("Please enter the color of the ball (0 or 255) : "))
                break
            except ValueError:
                print("Your color is not a number.")

    while True:
        try:
            flag = int(input("Please enter the flag of the ball (between 0 and 255) : "))
            break
        except ValueError:
            print("Your flag is not a number.")

    while flag < 0 or flag > 255:
        print("The flag is not available.")
        while True:
            try:
                color = int(input("Please enter the flag of the ball (between 0 and 255) : "))
                break
            except ValueError:
                print("Your flag is not a number.")

    # list for keeping the position according to the time-code
    final_video = []
    ball_center_i = []
    ball_center_j = []
    ball_speed = []
    ball_time = []
    ball_speed_average = 0
    nb_ball = 0
    ball_direction = []
    ball_old_size = -1
    ball_old_center_i = -1
    ball_old_center_j = -1
    ball_old_i_max = -1
    ball_old_j_max = -1
    ball_old_i_min = 1
    ball_old_j_min = -1

    limit_size = 300
    fps = video_original.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_original.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    print("Start of processing, please wait.")
    counter = 0

    while True:
        # we recover frame by frame
        ret, frame = video_original.read()

        # if frame is read correctly, ret is True
        if not ret:
            print("We cannot receive the frame anymore. It could be because it is the end of the stream or because an "
                  "error has occurred.")
            break

        im_frame = cv2.resize(frame, dsize=None, fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)
        im_frame_grey = np.copy(im_frame)
        filter.greyscale(im_frame, im_frame_grey)
        im_frame_witness = np.copy(im_frame)
        background = abs(255 - int(flag))
        segmentation.initialize_color(im_frame, im_frame_witness, background)

        if color == 0:
            filter.manual_threshold(im_frame_grey, im_frame, 50)
        else:
            filter.manual_threshold(im_frame_grey, im_frame, 205)

        cv2.imshow("frame_before", im_frame_grey)

        # we check if there is a ball
        ball, ball_actual_points, ball_actual_size, ball_actual_center_i, ball_actual_center_j, ball_actual_i_min, \
            ball_actual_i_max, ball_actual_j_min, ball_actual_j_max = check_ball(im_frame, im_frame_witness, color,
                                                                                 flag, background, ball_old_size,
                                                                                 ball_old_i_min, ball_old_i_max,
                                                                                 ball_old_j_min, ball_old_j_max,
                                                                                 limit_size)

        # if there is a ball, ball is True
        if ball:
            nb_ball += 1
            time = float(video_original.get(cv2.CAP_PROP_POS_MSEC)/1000.0)
            progression = time/duration * 100
            print("Progression : {:.2f}".format(progression), "%")
            # we keep the position of the center in the list
            ball_time.append(time)
            ball_center_i.append(ball_actual_center_i)
            ball_center_j.append(ball_actual_center_j)
            # we print the points on the new image
            measure.print_points_list(ball_actual_points, im_frame, im_frame_grey, flag, flag, flag, background)

            # there was a ball before so we can compute speed and direction
            if ball_old_size != -1:
                # we compute the direction
                d = direction(ball_old_center_i, ball_old_center_j, ball_actual_center_i, ball_actual_center_j)
                ball_direction.append(d)
                # we compute the speed
                s = speed(ball_time[-2], time,
                          ball_old_center_i, ball_old_center_j, ball_actual_center_i, ball_actual_center_j)
                ball_speed.append(s)
                ball_speed_average += s
            else:
                ball_direction.append(0)
                ball_speed.append(0)

            ball_old_size = ball_actual_size
            ball_old_center_i = ball_actual_center_i
            ball_old_center_j = ball_actual_center_j
            ball_old_i_max = ball_actual_i_max
            ball_old_j_max = ball_actual_j_max
            ball_old_i_min = ball_actual_i_min
            ball_old_j_min = ball_actual_j_min

        # There is no ball
        else:
            if ball_old_size == -1:
                print("There is no ball")
                break
            else:
                print("The ball is not present anymore")
                break

        if cv2.waitKey(1) == ord('0'):
            break

        # display the resulting frame
        im_frame = cv2.resize(im_frame_grey, dsize=None, fx=4, fy=4, interpolation=cv2.INTER_LINEAR)
        final_video.append(im_frame)
        cv2.imshow("frame_after", im_frame_grey)

        # We save the image
        filter.save_image(im_frame_grey, register_path_video + "/frame_" + str(counter) + ".bmp")
        counter += 1

    # Release the video
    video_original.release()
    cv2.destroyAllWindows()

    print("The process is finished")
    if nb_ball != 0:
        ball_speed_average = ball_speed_average / nb_ball
    return ball_center_i, ball_center_j, ball_time, ball_speed, ball_direction, ball_speed_average


# print the graphic of the ball center
def print_ball_center(ball_center_i, ball_center_j, ball_time, register_path_video):
    # conversion of the list into array
    ball_center_i_array = np.array(ball_center_i)
    ball_center_j_array = np.array(ball_center_j)
    ball_time_array = np.array(ball_time)

    # x in function of time
    pyplot.plot(ball_time_array, ball_center_i_array)
    pyplot.title("Position of the ball on the axis x in function of time")
    pyplot.ylabel("Position on axis x (pxl)")
    pyplot.xlabel("Time (s)")
    pyplot.savefig(register_path_video + "position_x_ball.png")
    pyplot.show()

    # x in function of time
    pyplot.plot(ball_time_array, ball_center_j_array)
    pyplot.title("Position of the ball on the axis y in function of time")
    pyplot.ylabel("Position on axis y (pxl)")
    pyplot.xlabel("Time (s)")
    pyplot.savefig(register_path_video + "position_y_ball.png")
    pyplot.show()

    # y in function of x
    pyplot.plot(ball_center_i_array, ball_center_j_array)
    pyplot.title("Position of the ball on the axis y in function of x")
    pyplot.xlabel("Position on axis x (pxl)")
    pyplot.ylabel("Position on axis y (pxl)")
    pyplot.savefig(register_path_video + "position_x_y_ball.png")
    pyplot.show()


# print the graphic of the speed norm
def print_norm_speed(ball_speed, ball_time, register_path_video):
    # conversion of the list into array
    ball_speed_array = np.array(ball_speed)
    ball_time_array = np.array(ball_time)

    # y in function of x
    pyplot.plot(ball_time_array, ball_speed_array)
    pyplot.title("Norm of the speed of the ball in function of time")
    pyplot.ylabel("Norm of the speed (pxl/s)")
    pyplot.xlabel("Time (s)")
    pyplot.savefig(register_path_video + "norm_speed_ball.png")
    pyplot.show()


# print the graphic of the speed direction
def print_direction_speed(ball_direction, ball_time, register_path_video):
    # conversion of the list into array
    ball_direction_array = np.array(ball_direction)
    ball_time_array = np.array(ball_time)

    # y in function of x
    pyplot.plot(ball_time_array, ball_direction_array)
    pyplot.title("Direction of the speed of the ball in function of time")
    pyplot.ylabel("Direction of the speed")
    pyplot.xlabel("Time (s)")
    pyplot.savefig(register_path_video + "direction_speed_ball.png")
    pyplot.show()


# create the final video
def display_video(final_video):
    cap = cv2.VideoCapture(final_video)

    while True:
        # we recover frame by frame
        ret, frame = cap.read()

        # if frame is read correctly, red is True
        if not ret:
            print("We cannot receive the frame anymore. It could be because it is the end of the stream or because an "
                  "error occurred.")
            break

        cv2.imshow('video_tracking_ball', frame)