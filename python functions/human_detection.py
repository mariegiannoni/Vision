import operator
import os
import sys

import cv2


# Tools :
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

# Histogram of Oriented Gradients descriptor and SVM detector
    # we have two samples : one of positive images and one of negative image
    # positive are the one we want to detect
    # negative are elements that we don't want to detect (background for example)
    # we might have more elements in negative sample than in positive one
    # we train on positive and negative samples
    # HOG compute local histogram of oriented gradients to detect the edges of an object
    # It will then combine all the histograms together : that will be the detector
    #SVM is linear classificator

    # OpenCV provide a HOG detector for detecting people in images


# detection of the person
def person_detection(frame, grey, hog):
    # we detect people in the image
    # image : frame
    # hitThreshold : threshold for the distance between features and SVM classifying plane
    #                maximum euclidean distance between the input HOG features and the classifying plane
    # winStide : 2-tuple parameter, x and y location of the sliding window
    #            the smaller it is, the more we need to evaluate the window to do detection
    #            (high complexity if too small)
    #            the larger it is, less we need window but more we risk to miss the object
    # padding : indicate the number of pixel in x and y in which the sliding window is padded
    # scale : coefficient of the detection window
    #         small : increase the number of layers in the image and then the complexity
    #         large : decrease number of layers but increase the risk to miss human
    # useMeanshiftGrouping : grouping algorithm
    #                        boolean indicating if mean-shift grouping should be performed, to avoid overlapping

    (people, weights) = hog.detectMultiScale(grey, hitThreshold=0, winStride=(8, 8), padding=(16, 16), scale=1.05,
                                             useMeanshiftGrouping=True, finalThreshold=2)

    i = 0
    for (x, y, w, h) in people:
        # we draw a rectangle around the person
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        # we write the number on the rectangle
        cv2.putText(frame, "people #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (255, 255, 0), 2)
        i += 1

    return frame


# detection of the face
def face_detection(frame, grey, face_cascade, face_profile_cascade, width, limit):
    # now we detect the faces
    face_array = []
    face = face_cascade.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=4)

    for x, y, w, h in face:
        face_array.append([x, y, x + w, y + h])

    profile_left = face_profile_cascade.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=4)
    for x, y, w, h in profile_left:
        face_array.append([x, y, x + w, y + h])

    # we flip the frame to check the other side of the profile
    gray_flip = cv2.flip(grey, 1)
    profile_left = face_profile_cascade.detectMultiScale(gray_flip, scaleFactor=1.2, minNeighbors=4)
    for x, y, w, h in profile_left:
        face_array.append([width - x, y, width - x - w, y + h])

    face_array = sorted(face_array, key=operator.itemgetter(0, 1))
    i = 0
    for x, y, x2, y2 in face_array:
        if not i or (x - face_array[i - 1][0] > limit or y - face_array[i - 1][1] > limit
                     or abs(x2 / 2 - face_array[i - 1][2]/2) > limit + 10
                     or (abs(y2 / 2 - face_array[i - 1][3]/2) > limit + 10)):
            # we draw a rectangle around the cat face
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
            # we write the number on the rectangle
            cv2.putText(frame, "face #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                        (0, 0, 255), 2)
            i += 1

    return frame


# principal function
def main_human_detection():
    # We initialize the HOG descriptor which is our human detector - xml source : opencv
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Detection of the face - xml source : opencv
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    face_profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

    cap = cv2.VideoCapture(0)
    limit = 100

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

    width = int(cap.get(3))

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

        # people detection
        frame = person_detection(frame, grey, hog)

        # face detection
        frame = face_detection(frame, grey, face_cascade, face_profile_cascade, width, limit)

        cv2.imshow('video', frame)

        if cv2.waitKey(1) == ord('0'):
            break

    cap.release()
    cv2.destroyAllWindows()