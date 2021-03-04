from utils import preprocess
from model.facenet_loader import model
import numpy as np
from scipy.spatial.distance import cosine
import os
from detection import mtcnn_detector
import pickle
from sklearn.preprocessing import Normalizer
import cv2

l2_normalizer = Normalizer('l2')


def encode(img):
    img = np.expand_dims(img, axis=0)
    out = model.predict(img)[0]
    return out


def load_database():
    with open('data/encodings/encoding.pkl', 'rb') as f:
        database = pickle.load(f)
    return database


recog_t = 0.35


def recognize(img):
    people = mtcnn_detector.detect_faces(img)
    if len(people) == 0:
        return None
    best_people = []
    people = [preprocess(person) for person in people]
    encoded = [encode(person) for person in people]
    encoded = [l2_normalizer.transform(encoding.reshape(1, -1))[0]
               for encoding in encoded]
    strengths = []
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
            best_name = 'UNKNOWN'
        best_people.append(best_name)
        strengths.append(best)
    print(strengths)
    return best_people
