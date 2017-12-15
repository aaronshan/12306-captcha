# -*- coding: utf8-*-

# --------------------------------------------------------
# 12306-captcha
# Copyright (c) 2017
# Written by ruifengshan
# --------------------------------------------------------

# 功能: 分割组合图片

import cv2
import os
import time
import skimage.io
import numpy as np
from src.config import cfg

IMG_V_POS = [4, 76, 148, 220]
IMG_H_POS = [40, 108]
IMG_WIDTH = 68  # 每个小图片的宽度
IMG_HEIGHT = 68  # 每个小图片的高度


def read_image(fn):
    """
    得到验证码完整图像
    :param fn:图像文件路径
    :return:图像对象
    """
    im = None
    try:
        im = skimage.io.imread(fn, as_grey=False)
    except Exception:
        pass
    return im


def load_image(im, color=True):
    img = skimage.img_as_float(im).astype(np.float32)
    if img.ndim == 2:
        img = img[:, :, np.newaxis]
        if color:
            img = np.tile(img, (1, 1, 3))

    elif img.shape[2] == 4:
        img = img[:, :, :3]
    return img


def write_image(im, fn):
    skimage.io.imsave(fn, im)


def get_text(im):
    """
    得到图像中的文本部分
    """
    return im[3:24, 116:288]


# 分割图片
def get_image(im):
    img = []
    for v in range(2):  # 图片行
        for h in range(4):  # 图片列
            img.append(im[(40 + (v * 72)):(108 + (v * 72)), (4 + (h * 72)):((h + 1) * 72)])
    return img


# 二值化图像
def binarize(im):
    gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    (retval, dst) = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    return dst


# 获取图像值

def show_image(im):
    print im.ndim, im.dtype
    cv2.imshow("image", im)
    cv2.waitKey(0)


def make_dir(path):
    try:
        if not os.path.exists(path):
            if not os.path.isfile(path):
                os.mkdir(path)
            return True
        else:
            return False
    except Exception, e:
        print str(e)


# 将文件写入到
def cut_image(image_cnt):
    path_dir = cfg.ROOT + '/data/download/'
    img_names = filter(lambda s: not s.startswith("."), os.listdir(path_dir + '/all'))

    while True:
        ocr_path = os.path.join(path_dir, 'words/words_' + str(image_cnt))
        if make_dir(ocr_path):
            break
        image_cnt += 1
    while True:
        img_path = os.path.join(path_dir, 'image/image_' + str(image_cnt))
        if make_dir(img_path):
            break
        image_cnt += 1

    for img_name in img_names:
        f_name = os.path.join(path_dir + '/all', img_name)
        im = read_image(f_name)
        if im is None:
            print "该图片{ %s }处理异常: " % img_name
            continue
        print os.path.join(ocr_path, img_name)
        write_image(get_text(im), os.path.join(ocr_path, img_name))
        num = 1
        sub_name = img_name.split('.')
        for sub_im in get_image(im):
            sub_img_name = sub_name[0] + '_' + str(num) + '.' + sub_name[1]
            num += 1
            write_image(sub_im, os.path.join(img_path, sub_img_name))
        # '删除'
        # os.remove(os.path.join(path_dir + '/all', img_name))
    return image_cnt


def thread_main():
    cnt = 0
    while True:
        cnt = cut_image(cnt)
        time.sleep(60)
        print '第{ %s }次开始切割图片' % cnt
        cnt += 1


if __name__ == '__main__':
    thread_main()
