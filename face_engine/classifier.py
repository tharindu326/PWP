#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from config import cfg
from face_engine.encoder import Encoder
from sklearn.svm import SVC
import joblib
import pickle
import numpy as np


class Classifier:
    """
    A classifier for encoding facial images and training a Support Vector Machine (SVM) model to recognize faces.
    Attributes:
        reco (Encoder): An encoder to generate facial embeddings.
        names (list): A list of labels (user IDs) corresponding to the facial embeddings.
        encodings (list): A list of facial embeddings.
        clf (SVC): An SVM classifier with probability support.

    Methods:
        __init__(): Initializes the classifier, loads existing embeddings and model if available.
        get_all_embeddings(): Generates embeddings for all faces in the database.
        save_embeddings(): Saves the current embeddings and labels to a file.
        get_user_embeddings(user_id): Generates embeddings for a specific user.
        train(): Trains the SVM model using the current embeddings and labels.
    """
    
    def __init__(self):
        self.reco = Encoder(Model=cfg.recognizer.model, Distance=cfg.recognizer.distance_type)
        self.names = []
        self.encodings = []
        self.clf = SVC(probability=True)
        if not os.path.isfile(cfg.recognizer.embedding_file_path):
            if len(os.listdir(cfg.db.database)) != 0:
                print(f'Not found: {cfg.recognizer.embedding_file_path} and {len(os.listdir(cfg.db.database))} records existing in Database,'
                      f' start generating embeddings for existing faces')
                self.get_all_embeddings()
        else:
            data = joblib.load(cfg.recognizer.embedding_file_path)
            self.encodings = data['encodings']
            self.names = data['labels']
            print(f'Loaded Embeddings: {np.asarray(self.encodings).shape} and labels: {len(self.names)} belongs to : '
                  f'{np.unique(np.asarray(self.names))} unique peoples')

        if os.path.isfile(cfg.recognizer.model_path):
            self.clf = joblib.load(cfg.recognizer.model_path)

    def get_all_embeddings(self):
        """
        Generates facial embeddings for all faces in the database.
        Iterates through all user directories in the database, encodes each image, and stores the resulting embeddings
        and labels. Saves the embeddings to a file.
        """
        print('[INFO] extracting encodings ....')
        for ID in os.listdir(f'{cfg.db.database}'):
            if os.path.isdir(f'{cfg.db.database}{ID}'):
                print(f'[INFO] encoding {ID}')
                for image in os.listdir(f'{cfg.db.database}{ID}'):
                    try:
                        face_encode = self.reco.encode(f'{cfg.db.database}{ID}/{image}')
                        self.names.append(ID)
                        self.encodings.append(face_encode)
                    except Exception as e:
                        print(f'[ERROR] {cfg.db.database}{ID}/{image} : {e}')
        print(f'Generated Embeddings: {np.asarray(self.encodings).shape} and labels: {len(self.names)} belongs to : '
              f'{np.unique(np.asarray(self.names))} unique peoples')
        self.save_embeddings()

    def save_embeddings(self):
        """
        Saves the current facial embeddings and labels to a file.
        Stores the encodings and labels as a dictionary in a pickle file specified by the configuration.
        """
        data = {"encodings": self.encodings, "labels": self.names}
        with open(cfg.recognizer.embedding_file_path, "wb") as f:
            f.write(pickle.dumps(data))

    def get_user_embeddings(self, user_id):
        """
        Generates facial embeddings for a specific user.
        Encodes each image in the user's directory and updates the embeddings and labels. Saves the updated embeddings to a file.
        Args:
            user_id (int): The ID of the user to generate embeddings for.
        """
        user_path = f'{cfg.db.database}{user_id}'
        if os.path.isdir(user_path):
            print(f'[INFO] encoding {user_id}')
            for image in os.listdir(f'{cfg.db.database}{user_id}'):
                try:
                    face_encode = self.reco.encode(f'{cfg.db.database}{user_id}/{image}')
                    self.names.append(user_id)
                    self.encodings.append(face_encode)
                except Exception as e:
                    print(f'[ERROR] {cfg.db.database}{user_id}/{image} : {e}')
            self.save_embeddings()
        else:
            print(f'Error: no user found {user_id} in {user_path}')

    def train(self):
        """
        Trains the SVM model using the current facial embeddings and labels.
        Fits the SVM model to the embeddings, evaluates its performance, and saves the trained model to a file.
        Also saves the embeddings to ensure they are up to date.
        """
        print('[INFO] training the model ....')
        self.clf.fit(self.encodings, self.names)
        print('[INFO] evaluating the model ....')
        self.clf.score(self.encodings, self.names)
        print('[INFO] saving the model ....')
        joblib.dump(self.clf, cfg.recognizer.model_path)
        self.save_embeddings()
