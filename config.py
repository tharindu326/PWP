#! /usr/bin/env python
# coding=utf-8
from easydict import EasyDict as edict

__C = edict()
cfg = __C

__C.db = edict()
__C.db.SQLALCHEMY_DATABASE_URI = 'sqlite:///FacePass.db'
__C.db.SQLALCHEMY_TRACK_MODIFICATIONS = False


__C.detector = edict()
__C.detector.weight_file = "model_data/yolov8n-face.pt"  # model.pt path(s)
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
