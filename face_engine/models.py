#! /usr/bin/env python
# coding=utf-8
from deepface.basemodels import VGGFace, OpenFace, Facenet, FbDeepFace, ArcFace, Facenet512, DeepID, DlibResNet, SFaceWrapper, DlibWrapper
from deepface.commons import functions, distance
from keras.preprocessing.image import img_to_array
import numpy as np
import cv2


class Recognizer:
    def __init__(self, Model='VGGFace', Distance='Euclidean'):
        face_models = [
            "VGGFace",
            "OpenFace",
            "Facenet",
            "FbDeepFace",
            "ArcFace",
            "Facenet512",
            "DeepID",
            "DlibResNet",
            "DlibWrapper",
            "SFaceWrapper"
        ]
        distances = ['Cosine', 'Euclidean']
        if f'{Distance}' not in distances:
            raise ValueError(f'[ERROR] {Distance} is not valid. please use either one of these: {distances}')
        else:
            self.distance = Distance

        if f'{Model}' not in face_models:
            raise ValueError(f'[ERROR] {Model} is not valid. please use either one of these: {face_models}')
        else:
            try:
                self.model = globals()[f'{Model}'].loadModel()
            except:
                self.model = globals()[f'{Model}'].load_model()

    def encode(self, img):
        target_size_0, target_size_1 = functions.find_input_shape(self.model)
        # factor0 = target_size_0 / img.shape[0]
        # factor1 = target_size_1 / img.shape[1]
        # factor = min(factor0, factor1)
        # dsize = (int(img.shape[1] * factor), int(img.shape[0] * factor))
        img = cv2.resize(img, (target_size_0, target_size_1))
        # normalize in [0, 1]
        # img = cv2.resize(img, dsize)
        # diff0 = target_size_0 - img.shape[0]
        # diff1 = target_size_1 - img.shape[1]
        # img_pixels = np.pad(img, ((diff0 // 2, diff0 - diff0 // 2), (diff1 // 2, diff1 - diff1 // 2), (0, 0)),
        #                     'constant')
        img_pixels = img_to_array(img)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels /= 255
        encoding = self.model.predict(img_pixels)[0]
        return encoding

    def compare(self, face1, face2):
        if self.distance == 'Cosine':
            dst = distance.findCosineDistance(face1, face2)
        else:
            dst = distance.findEuclideanDistance(face1, face2)
        return dst



