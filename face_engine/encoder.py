#! /usr/bin/env python
# coding=utf-8
from deepface.commons import distance
from deepface import DeepFace


class Encoder:
    """
    An encoder class for generating facial embeddings and comparing faces using the DeepFace library.
    Attributes:
        model (str): The name of the facial recognition model to use.
        distance (str): The type of distance metric to use for face comparison.
    Methods:
        __init__(Model, Distance): Initializes the Encoder with the specified model and distance metric.
        encode(img): Generates an embedding for the given image using the specified model.
        compare(face1, face2): Compares two facial embeddings using the specified distance metric.
    """
    def __init__(self, Model='VGG-Face', Distance='Euclidean'):
        """
        Initializes the Encoder instance with a specified model and distance metric.
        Args:
            Model (str): The name of the facial recognition model to use (default is 'VGG-Face').
            Distance (str): The type of distance metric to use for face comparison (default is 'Euclidean').
        Raises:
            ValueError: If the specified model or distance metric is not valid.
        """
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
        """
        Generates an embedding for the given image using the specified model.
        Args:
            img (str): The path to the image file to encode.
        Returns:
            list: A list of embedding objects generated by the model.
        """
        embedding_objs = DeepFace.represent(img_path=img,
                                            model_name=self.model, enforce_detection=False)
        return embedding_objs

    def compare(self, face1, face2):
        """
        Compares two facial embeddings using the specified distance metric.
        Args:
            face1 (numpy.ndarray): The first facial embedding.
            face2 (numpy.ndarray): The second facial embedding.
        Returns:
            float: The distance between the two embeddings based on the specified metric.
        """
        if self.distance == 'Cosine':
            dst = distance.findCosineDistance(face1, face2)
        else:
            dst = distance.findEuclideanDistance(face1, face2)
        return dst



