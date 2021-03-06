from utils import preprocess
from model.facenet_loader import model
import numpy as np
from scipy.spatial.distance import cosine
import pickle
from sklearn.preprocessing import Normalizer
import cv2
import mtcnn

l2_normalizer = Normalizer('l2')


def encode(img):
    img = np.expand_dims(img, axis=0)
    out = model.predict(img)[0]
    return out


def load_database():
    with open('data/encodings/encoding.pkl', 'rb') as f:
        database = pickle.load(f)
    return database


recog_t = 0.4


def recognize(img):
    people = detect_faces(img)
    if len(people) == 0:
        return None
    best_people = []
    people = [preprocess(person) for person in people]
    encoded = [encode(person) for person in people]
    encoded = [l2_normalizer.transform(encoding.reshape(1, -1))[0]
               for encoding in encoded]
    database = load_database()
    for person in encoded:
        best = 1
        best_name = ''
        for k, v in database.items():
            dist = cosine(person, v)
            if dist < best:
                best = dist
                best_name = k
        if best > recog_t:
            best_name = 'unknown'
        best_people.append(best_name)
    return best_people


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
        faces.append(cv2_img[y1:y2, x1:x2])
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
    return cv2_img[y1:y2, x1:x2]


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
            cv2.rectangle(cv2_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        else:
            cv2.rectangle(cv2_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(cv2_img, people[i], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
    return cv2_img
