#! /usr/bin/env python
# coding=utf-8
from easydict import EasyDict as edict

__C = edict()
cfg = __C

__C.db = edict()
__C.db.SQLALCHEMY_DATABASE_URI = 'sqlite:///FacePass.db'
__C.db.SQLALCHEMY_TRACK_MODIFICATIONS = False
__C.db.database = 'database/'

__C.app = edict()
__C.app.allowed_extensions = ['jpeg', 'png', 'jpg']
__C.app.port = 8080
__C.app.host = '0.0.0.0'

__C.detector = edict()
__C.detector.weight_file = "face_engine/model_data/yolov8n-face.pt"  # model.pt path(s)
__C.detector.classes = [0]  # filter by class: --class 0, or --class 0 2 3
__C.detector.OBJECTNESS_CONFIDANCE = 0.2
__C.detector.NMS_THRESHOLD = 0.45
__C.detector.device = 'cpu'  # if GPU give the device ID; EX: , else 'cpu'
__C.detector.rotate_frame = False
__C.detector.frame_resize = (640, 640)


# overlay Flags
__C.flags = edict()
__C.flags.image_show = False
__C.flags.render_detections = True
__C.flags.render_labels = True

__C.permission = edict()
__C.permission.user_permission_levels = [
                                            'superadmin',
                                            'admin',
                                            'manager',
                                            'employee',
                                            'intern',
                                            'contractor',
                                            'guest',
                                            'supervisor',
                                            'security'
                                        ]

# recognizer options
__C.recognizer = edict()
__C.recognizer.distance_type = 'Euclidean'  # ['Cosine', 'Euclidean']  # available options for calculate the distance between images for get matches
__C.recognizer.model = "Facenet512"  # ["VGGFace", "OpenFace", "Facenet", "FbDeepFace", "ArcFace", "Facenet512", "DeepID", "DlibResNet", "DlibWrapper", "SFaceWrapper"]  # face recognition algorithm options.
__C.recognizer.threshold = 30
__C.recognizer.model_path = 'face_engine/model_data/model_svc.pkl'
__C.recognizer.embedding_file_path = 'face_engine/model_data/embeddings.pkl'
