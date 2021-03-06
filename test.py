import cv2
from face_recognition import detect_and_draw_boxes
import time
cam = cv2.VideoCapture(0)

cv2.namedWindow("Your Face!")
cv2.namedWindow("Detected")
while True:
    time.sleep(0.2)
    ret, frame = cam.read()
    if not ret:
        print("[ERROR] failed to grab frame")
        break
    cv2.imshow("Your Face!", frame)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("[INFO] Escape hit, closing...")
        break
    cv2.imshow("Detected",detect_and_draw_boxes(frame))