import cv2
from detection.mtcnn_detector import detect_face
from utils import preprocess
from detection.recognize import encode
from utils import get_specific_frames
from ring.wait_for_video import main
import argparse
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str, help='Name of person who rung doorbell last')

args = parser.parse_args()

main(download_only=True)

times = [3, 6, 9, 12, 15, 18]
img_dir = 'data/faces/' + args.name + '/'
if not os.path.exists(img_dir):
    os.mkdir(img_dir)
dir = 'data/encoded/' + args.name + '/'
if not os.path.exists(dir):
    os.mkdir(dir)
frames = get_specific_frames('last_ding.mp4', times)
for frame in frames:
    img = detect_face(frame)
    if img is None:
        print("[ERROR] An image isn't clear! skipping download!")
        continue
    cv2.imwrite(img_dir + str(len(os.listdir(img_dir))) + '.jpg', img)
    img = preprocess(img)
    encoded = encode(img)
    with open(dir + str(len(os.listdir(dir))) + '.npy', 'wb') as f:
        np.save(f, encoded)
    print('[INFO] {} Saved Successfully'.format(args.name))
