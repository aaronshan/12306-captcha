# -*-coding:utf-8-*-

# --------------------------------------------------------
# 12306-captcha
# Copyright (c) 2017
# Licensed under The Apache License [see LICENSE for details]
# Written by ruifengshan
# --------------------------------------------------------

import os
import sys

import numpy as np
from src.tools import remove_noisy
from src.tools import cut_image as cimg
import logging
from src.config import cfg

caffe_root = cfg.CAFFE_ROOT
sys.path.insert(0, caffe_root + 'python')

import caffe

net_file = cfg.ROOT + '/src/image/model/image_deploy.prototxt'
caffe_model = cfg.ROOT + 'model/image/f16_snapshot_iter_208000.caffemodel'
synset_file = cfg.ROOT + 'label/synset'

logger = logging.getLogger(__name__)


def judge(path, file_path=synset_file):
    """判断是不是文件夹"""
    img_names = os.listdir(path)
    for img_name in img_names:
        logger.info("文件名：　%s", img_name)
        tmp_img_name = os.path.join(path, img_name)
        if os.path.isdir(tmp_img_name):
            judge(tmp_img_name)
            os.removedirs(tmp_img_name)
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$文件夹已经被删除', tmp_img_name
        elif tmp_img_name.split('.')[1] != "DS_Store":
            im1 = cimg.read_image(tmp_img_name)
            img = remove_noisy.rm_blackNoisy(im1)
            im = cimg.load_image(img)
            net.blobs['data'].data[...] = transformer.preprocess('data', im)
            out = net.forward()

            imagenet_labels_filename = synset_file
            labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
            prob = out['softmax'][0]
            top_k = net.blobs['softmax'].data[0].flatten().argsort()[-1:-6:-1]
            for i in np.arange(top_k.size):
                print '照片名: %s , 对应的类：%s , 概率 %%%3f' % (img_name, labels[top_k[i]], prob[top_k[i]] * 100)
                print top_k[i], labels[top_k[i]]
            new_path = os.path.join("/home/ruifengshan/github/12306-captcha/judge-image-result/", labels[top_k[0]])
            cimg.makeDir(new_path)
            cimg.write_image(im1, os.path.join(new_path, img_name))
            # '删除'
            os.remove(tmp_img_name)
            print '++++++++++++++++++++++++++++++++++++文件已经被删除', tmp_img_name
            # time.sleep(1)


if __name__ == '__main__':
    net = caffe.Net(net_file, caffe_model, caffe.TEST)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    "读取的图片文件格式为H×W×K，需转化为K×H×W"
    transformer.set_transpose('data', (2, 0, 1))
    # transformer.set_mean('data', mean=np.float32([103.939, 116.779, 123.68]))
    "将图片存储为[0, 1]，而caffe中将图片存储为[0, 255"
    transformer.set_raw_scale('data', 255)
    "caffe中图片是BGR格式，而原始格式是RGB，所以要转化"
    transformer.set_channel_swap('data', (2, 1, 0))
    image_dir='/home/ruifengshan/github/12306-captcha/judge-image'
    judge(image_dir)
