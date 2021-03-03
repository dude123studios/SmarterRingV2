import cv2
from detection.mtcnn_detector import detect_face
from utils import preprocess
from detection.recognize import encode
import argparse
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str, help='Name of person to take a picture of')

cam = cv2.VideoCapture(0)

cv2.namedWindow("Your Face!")
args = parser.parse_args()

while True:
    ret, frame = cam.read()
    if not ret:
        print("[ERROR] failed to grab frame")
        break
    cv2.imshow("Your Face!", frame)
    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("[INFO] Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        img = detect_face(frame)
        if img is None:
            print("[ERROR] Image isn't clear! Try again!")
            continue
        img_dir = 'data/faces/' + args.name + '/'
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)
        cv2.imwrite(img_dir + str(len(os.listdir(img_dir))) + '.jpg', img)
        print('[INFO] {} Saved Successfully'.format(args.name))
