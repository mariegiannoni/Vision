# STEPS :
# 1. negative or background images
# we need a description file
# bg.txt file that contains the path to each image by line
# example line : neg/1.jpg
# 2. positives images
# we need a description file
# pos.txt that contains path to each image, by line along with how many objects and where they are located
# example line : pos/1.jpg 1 0 0 50 50 (image, num objects, start point, end point
# 3. create a positive vector file by stitching together all positives (with OpenCV)
# 4. Train cascade (with OpenCV)
