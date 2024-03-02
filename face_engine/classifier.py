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
            self.encodings = joblib.load(cfg.recognizer.embedding_file_path)
            print(f'Loaded Embeddings: {np.asarray(self.encodings).shape} and labels: {len(self.names)} belongs to : '
                  f'{np.unique(np.asarray(self.names))} unique peoples')

        if os.path.isfile(cfg.recognizer.model_path):
            self.clf = joblib.load(cfg.recognizer.model_path)

    def get_all_embeddings(self):
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
        data = {"encodings": self.encodings, "labels": self.names}
        with open(cfg.recognizer.embedding_file_path, "wb") as f:
            f.write(pickle.dumps(data))

    def get_user_embeddings(self, user_id):
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
        print('[INFO] training the model ....')
        self.clf.fit(self.encodings, self.names)
        print('[INFO] evaluating the model ....')
        self.clf.score(self.encodings, self.names)
        print('[INFO] saving the model ....')
        joblib.dump(self.clf, cfg.recognizer.model_path)
        self.save_embeddings()
