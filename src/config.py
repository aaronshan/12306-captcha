#! _*_ coding:utf-8 _*_

# --------------------------------------------------------
# 12306-captcha
# Copyright (c) 2017 
# Written by ruifengshan
# --------------------------------------------------------

# `pip install easydict` if you don't have it
from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by:
#   from src.config import cfg
cfg = __C

# caffe根目录
__C.CAFFE_ROOT = '/home/ruifengshan/caffe-ssd/'

# 项目根目录
__C.ROOT = '/home/ruifengshan/github/12306-captcha/'