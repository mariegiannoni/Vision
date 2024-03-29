import operator
import os
import sys

import cv2

# We use the function detectMultiScale
    # detectMultiScale :
    # we provide it a haar cascade classifier that contains data about the object that we want to detect
    # we also set the scale factor and the min neighbour

    # first, the function will look for the object described in the file on a certain scale
    # then, it will change the scale and look again for objects and so on
    # the scale factor parameter is then the parameter used to the change of scale
    # higher the scale factor is, less we can detect object
    # in general, between 1.1 and 1.5

    # min neighbour is useful in order to avoid false positive
    # it will check that the object is not only detected on a scale but also on other ones
    # if the object is not detected on a number equal to or higher than min neighbour, we don't keep it
    # in general, between 3 and 5

# Use of CascadeClassfier
    # A cascade classifies contains the information about our object and allow its identification
    # The xml file is a haar cascade file. It can be generate with deep learning
    # for this version, the xml file is not generated by myself but taken on internet or on opencv


def car_detection(frame, grey, car):
    car_detected = car.detectMultiScale(grey, scaleFactor=1.4, minNeighbors=3)
    i = 0

    for x, y, w, h in car_detected:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
        # we write the number on the rectangle
        cv2.putText(frame, "car #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (255, 0, 255), 2)
        i += 1

    return frame


# principal function
def main_car_detection():
    # detection of car - xml source : git of krishnaik06
    car = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_car.xml")

    cap = cv2.VideoCapture(0)

    while True:
        try:
            choice = int(input("Do you want to use the webcam (0) or a video (otherwise) ?"))
            break
        except ValueError:
            print("Your choice is not a number.")

    if choice != 0:
        # Upload the video in which we want to find the animals
        path = input("Please, enter the absolute path of a video : ")
        is_exist = os.path.exists(path)
        while not is_exist:
            print("Your video is not reachable")
            path = input("Please, enter an available absolute path : ")
            is_exist = os.path.exists(path)

        cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print("We can't open the video")
        sys.exit(1)

    while True:
        # we recover frame by frame
        ret, frame = cap.read()

        # if frame is read correctly, ret is True
        if not ret:
            print("We cannot receive the frame anymore. It could be because it is the end of the stream or because an "
                  "error has occurred.")
            break

        # it is easier to detect when the image is in greyscale
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = car_detection(frame, grey, car)

        cv2.imshow('video', frame)

        if cv2.waitKey(1) == ord('0'):
            break

    cap.release()
    cv2.destroyAllWindows()