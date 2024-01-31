#! /usr/bin/env python
# coding=utf-8
from easydict import EasyDict as edict

__C = edict()
cfg = __C

__C.mysql = edict()
__C.mysql.host = 'test-db.ccj8723txgvr.eu-north-1.rds.amazonaws.com'
__C.mysql.user = 'admin'
__C.mysql.password = ''
__C.mysql.database = 'FaceDB'
