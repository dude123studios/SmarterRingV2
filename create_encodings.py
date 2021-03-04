import os
from utils import preprocess
import cv2
import numpy as np
from sklearn.preprocessing import Normalizer
import face_recognition
import pickle

encoding_dict = {}
l2_normalizer = Normalizer('l2')

for face_names in os.listdir('data/faces/'):
    person_dir = os.path.join('data/faces/', face_names)
    encodes = []
    for image_name in os.listdir(person_dir):
        image_path = os.path.join(person_dir, image_name)

        face = cv2.imread(image_path)

        face = preprocess(face)
        encoding = face_recognition.encode(face)
        encodes.append(encoding)

    if encodes:
        encoding = np.sum(encodes, axis=0)
        encoding = l2_normalizer.transform(np.expand_dims(encoding, axis=0))[0]
        encoding_dict[face_names] = encoding

path = 'data/encodings/encoding.pkl'
with open(path, 'wb') as file:
    pickle.dump(encoding_dict, file)
