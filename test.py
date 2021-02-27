import cv2
from detection.mtcnn_detector import detect_and_draw_boxes
cam = cv2.VideoCapture(0)

cv2.namedWindow("Your Face!")
cv2.namedWindow("Detected")
while True:
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

