import cv2
from face_recognition import detect_face
from ring import main
from utils import get_specific_frames
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str, help='Name of person to take a picture of')
parser.add_argument('from_door', type=bool, help='If the images will directly come from the ring')

cam = cv2.VideoCapture(0)

cv2.namedWindow("Your Face!")
args = parser.parse_args()
if args.from_door:
    main(download_only=True)

    times = [3, 6, 9, 12, 15, 18]
    img_dir = 'data/faces/' + args.name + '/'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    frames = get_specific_frames('last_ding.mp4', times)
    for frame in frames:
        img = detect_face(frame)
        if img is None:
            print("[ERROR] An image isn't clear! skipping download!")
            continue
        cv2.imwrite(img_dir + str(len(os.listdir(img_dir))) + '.jpg', img)
        print('[INFO] {} Saved Successfully'.format(args.name))
else:
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
