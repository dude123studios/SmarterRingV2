import tensorflow as tf
from utils import preprocess
import numpy as np
import cv2
import os
import random

path = 'data/faces/'
faces = []
for actor in os.listdir(path):
    faces.append([np.expand_dims(preprocess(cv2.imread(path + actor + '/' + actor_name)),axis=0) for actor_name in
                  os.listdir(os.path.join(path, actor))])

# generate all of the congruent pairs
pairs1 = []
pairs2 = []
labels = []
congruent = np.zeros((1))
for person in faces:
    for i, imgA in enumerate(person[:-2]):
        for imgB in person[i + 1:]:
            pairs1.append(imgA)
            pairs2.append(imgB)
            labels.append(congruent)
# generate the same number of non congruent pairs
non_congruent_label = np.ones((1))
for i in range(len(pairs1)):
    j = random.randint(0, len(faces) - 2)
    k = random.randint(j + 1, len(faces) - 1)
    l = random.randint(0, len(faces[j]) - 1)
    m = random.randint(0, len(faces[k]) - 1)
    pairs1.append(faces[j][l])
    pairs2.append(faces[k][m])
    labels.append(non_congruent_label)

del faces


def shuffle_in_unison(a, b, c):
    shuffled_a = np.empty((len(a),1, 160, 160, 3), dtype=np.float32)
    shuffled_b = np.empty((len(a),1, 160, 160, 3), dtype=np.float32)
    shuffled_c = np.empty((len(c),1, 1), dtype=np.float32)
    permutation = np.random.permutation(len(a))
    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]
        shuffled_c[new_index] = c[old_index]
    return shuffled_a, shuffled_b, shuffled_c


pairs1, pairs2, labels = shuffle_in_unison(pairs1, pairs2, labels)
print(pairs1.shape)
