from utils import preprocess
from model.facenet_loader import model
import numpy as np
from scipy.spatial.distance import cosine
import os
from detection import mtcnn_detector
import cv2


def encode(img):
    img = np.expand_dims(img, axis=0)
    out = model.predict(img)[0]
    return out


def recognize(img):
    people = mtcnn_detector.detect_faces(img)
    if len(people) == 0:
        return None
    best_people = []
    people = [preprocess(person) for person in people]
    encoded = [encode(person) for person in people]
    database = {}
    for person_path in os.listdir('data/encoded/'):
        for image_path in os.listdir('data/encoded/' + person_path):
            final_path = 'data/encoded/' + person_path + '/' + image_path
            img = np.load(final_path, allow_pickle=True)
            database[final_path] = img
    strengths = []
    for person in encoded:
        best = 1
        best_name = ''
        for k, v in database.items():
            dist = cosine(person, v)
            if dist < best:
                best = dist
                best_name = k.split('/')[-2]
            print(dist)
        if best > 0.00003:
            best_name = 'UNKNOWN'
        best_people.append(best_name)
        strengths.append(best)
    #print(strengths)
    return best_people
