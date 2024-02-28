#! /usr/bin/env python
# coding=utf-8
from deepface.commons import distance
from deepface import DeepFace


class Encoder:
    def __init__(self, Model='VGG-Face', Distance='Euclidean'):
        face_models = [
            "VGG-Face",
            "Facenet",
            "Facenet512",
            "OpenFace",
            "DeepFace",
            "DeepID",
            "ArcFace",
            "Dlib",
            "SFace",
        ]
        distances = ['Cosine', 'Euclidean']
        if f'{Distance}' not in distances:
            raise ValueError(f'[ERROR] {Distance} is not valid. please use either one of these: {distances}')
        else:
            self.distance = Distance

        if f'{Model}' not in face_models:
            raise ValueError(f'[ERROR] {Model} is not valid. please use either one of these: {face_models}')
        else:
            self.model = Model

    def encode(self, img):
        embedding_objs = DeepFace.represent(img_path=img,
                                            model_name=self.model, enforce_detection=False)
        return embedding_objs

    def compare(self, face1, face2):
        if self.distance == 'Cosine':
            dst = distance.findCosineDistance(face1, face2)
        else:
            dst = distance.findEuclideanDistance(face1, face2)
        return dst



