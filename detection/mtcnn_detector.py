import cv2
import mtcnn
from detection.recognize import recognize

face_detector = mtcnn.MTCNN()
conf_t = 0.99

def detect_faces(cv2_img):
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    results = face_detector.detect_faces(img_rgb)
    faces = []
    for res in results:
        x1, y1, width, height = res['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        confidence = res['confidence']
        if confidence < conf_t:
            continue
        faces.append(cv2_img[y1:y2,x1:x2])
    return faces

def detect_face(cv2_img):
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    results = face_detector.detect_faces(img_rgb)
    x1, y1, width, height = results[0]['box']
    cv2.waitKey(1)
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height

    confidence = results[0]['confidence']
    if confidence < conf_t:
        return None
    return cv2_img[y1:y2,x1:x2]

def detect_and_draw_boxes(cv2_img):
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    people = recognize(cv2_img)
    results = face_detector.detect_faces(img_rgb)
    if not results or people is None:
        return cv2_img
    for i, res in enumerate(results):
        x1, y1, width, height = res['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        confidence = res['confidence']
        if confidence < conf_t:
            continue
        if people[i] == 'UNKNOWN':
            cv2.rectangle(cv2_img, (x1,y1),(x2,y2),(0,255,0),2)
        else:
            cv2.rectangle(cv2_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(cv2_img, people[i], (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
    return cv2_img