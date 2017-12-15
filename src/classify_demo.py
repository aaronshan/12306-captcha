# -*-coding:utf-8-*-

# --------------------------------------------------------
# 12306-captcha
# Copyright (c) 2017
# Licensed under The Apache License [see LICENSE for details]
# Written by ruifengshan
# --------------------------------------------------------

"""验证码识别"""

import os
import sys

import cv2
import numpy as np
from tools import words
from tools import remove_noisy
import skimage
import skimage.io
import skimage.transform

from tools import cut_image
from src.config import cfg

# =================================== common start ============================================
caffe_root = cfg.CAFFE_ROOT
sys.path.insert(0, caffe_root + 'python')

import caffe

imagenet_labels_filename = cfg.ROOT + 'label/synset'
labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
# ===================================  common end  =============================================

# ====================================image start=================================================
image_net_file = cfg.ROOT + '/src/image/model/image_deploy.prototxt'
image_caffe_model = cfg.ROOT + 'model/image/f18_snapshot_iter_84600.caffemodel'
image_net = caffe.Net(image_net_file, image_caffe_model, caffe.TEST)
image_transformer = caffe.io.Transformer({'data': image_net.blobs['data'].data.shape})
"读取的图片文件格式为H×W×K，需转化为K×H×W"
image_transformer.set_transpose('data', (2, 0, 1))
# transformer.set_mean('data', mean=np.float32([103.939, 116.779, 123.68]))
"将图片存储为[0, 1]，而caffe中将图片存储为[0, 255"
image_transformer.set_raw_scale('data', 255)
"caffe中图片是BGR格式，而原始格式是RGB，所以要转化"
image_transformer.set_channel_swap('data', (2, 1, 0))
# ====================================image end=================================================


# ====================================words start=================================================
words_net_file = cfg.ROOT + '/src/words/model/words_deploy.prototxt'
words_caffe_model = cfg.ROOT + 'model/words/words_4_snapshot_iter_160000.caffemodel'
words_net = caffe.Net(words_net_file, words_caffe_model, caffe.TEST)
words_transformer = caffe.io.Transformer({'data': words_net.blobs['data'].data.shape})
"读取的图片文件格式为H×W×K，需转化为K×H×W"
words_transformer.set_transpose('data', (2, 0, 1))
# transformer.set_mean('data', mean=np.float32([103.939, 116.779, 123.68]))
"将图片存储为[0, 1]，而caffe中将图片存储为[0, 255"
words_transformer.set_raw_scale('data', 255)
"caffe中图片是BGR格式，而原始格式是RGB，所以要转化"
words_transformer.set_channel_swap('data', (2, 1, 0))


# ====================================words end=================================================
def judge_words(img):
    """返回文件坐标"""
    list_img = words.get_test(img)
    _text = []
    if list_img is None:
        return None
    for im in list_img:
        # 灰度图转化为多通道RGB
        im = cv2.merge([im, im, im])  # 前面分离出来的三个通道
        words_net.blobs['data'].data[...] = words_transformer.preprocess('data', im.astype(np.int))
        out = words_net.forward()
        prob = out['softmax'][0]
        top_k = words_net.blobs['softmax'].data[0].flatten().argsort()[-1:-6:-1]
        _text.append(labels[top_k[0]])
    return _text


def judge_image(list_img, list_label):
    """判断是不是文件夹"""
    if list_img is None:
        return None
    _index = 1
    for im in list_img:

        img = remove_noisy.rm_blackNoisy(im)
        img = cut_image.load_image(img)

        image_net.blobs['data'].data[...] = image_transformer.preprocess('data', img)
        out = image_net.forward()
        prob = out['softmax'][0]
        top_k = image_net.blobs['softmax'].data[0].flatten().argsort()[-1:-6:-1]
        print "第", _index, " 图预测是：", labels[top_k[0]]
        for label in list_label:
            if labels[top_k[0]] == label:
                print "++++++++++++++++++图片位置：", _index, label, "+++++++++++++++++"
        _index += 1


def train_main():
    path_dir = '/home/ruifengshan/github/12306-captcha/data/download/'
    img_names = filter(lambda s: not s.startswith("."), os.listdir(path_dir + '/all'))

    for img_name in img_names:
        im = cut_image.read_image(os.path.join(path_dir + '/all', img_name))
        if im is None:
            print "该图片{ %s }处理异常: " % img_name
            continue
        # 转为灰度图
        list_text = judge_words(cut_image.get_text(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)))
        print "文字部分的内容："
        for text in list_text:
            print text
        judge_image(cut_image.get_image(im), list_text)
        skimage.io.imshow(im)


if __name__ == '__main__':
    train_main()
