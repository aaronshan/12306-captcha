# -*- coding:utf-8 -*-

# --------------------------------------------------------
# 12306-captcha
# Copyright (c) 2017
# Licensed under The Apache License [see LICENSE for details]
# Written by ruifengshan
# --------------------------------------------------------

import cv2
import numpy as np
import cv2
import os
import math as mt
import skimage.transform
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import morphology, color, data
import matplotlib.pyplot as plt
from PIL import Image
from src.config import cfg


def make_dir(path):
    try:
        if not os.path.exists(path):
            if not os.path.isfile(path):
                os.makedirs(path)
        return True
    except Exception, e:
        print str(e)
        return False


def int_max(a, b):
    """求解最大值"""
    return a if a > b else b


def int_min(a, b):
    """求解最小值"""
    return a if a < b else b


def get_mean_value(img):
    """
    求图像分均值
    :param img:
    :return: 平均值
    """
    y, x = img.shape[:2]
    sum_value = 0
    for _x in range(0, x, 1):
        # temp_value = 0
        for _y in range(0, y, 1):
            sum_value += img[_y][_x]

    return sum_value / (x * y)


def pretreatment_image(img, times=3):
    """
    预处理图片
    :param img: 待处理的灰度图图片
    :return: 处理之后的图片
    """

    img = 255 - img
    y, x = img.shape[:2]
    for _ in xrange(times):
        mean_value = get_mean_value(img)
        for _x in range(0, x, 1):
            # temp_value = 0
            for _y in range(0, y, 1):
                if img[_y][_x] >= mean_value:
                    img[_y][_x] -= mean_value
                else:
                    img[_y][_x] = 0
        while (1):
            max_value = -1
            for _x in range(0, x, 1):
                # temp_value = 0
                for _y in range(0, y, 1):
                    if img[_y][_x] + img[_y][_x] * 0.2 >= 255:
                        img[_y][_x] = 255
                    else:
                        img[_y][_x] += img[_y][_x] * 0.2
                    if max_value < img[_y][_x] * 0.2:
                        max_value = img[_y][_x] * 0.2
            if max_value >= mean_value:
                break
            mean_value -= max_value

    return img


def binary_text(im):
    """
     二值化
    :param im: 待处理的原始图片
    :return: 二值化后的图片
    """
    dst = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 0)
    return dst


def rm_noise(img):
    """
    用来去除噪点
    :param img: 原始数据图片
    :return:  去噪点之后的图片
    """
    y, x = img.shape[:2]
    for _x in range(0, x, 1):
        for _y in range(0, y, 1):
            cnt = 0
            if img[_y][_x] > 0:
                if _y > 0 and img[_y - 1][_x] > 0:
                    cnt += 1
                if _y + 1 < y and img[_y + 1][_x] > 0:
                    cnt += 1
                if _x > 0 and img[_y][_x - 1] > 0:
                    cnt += 1
                if _x + 1 < x and img[_y][_x + 1] > 0:
                    cnt += 1
                if _y > 0 and _x > 0 and img[_y - 1][_x - 1] > 0:
                    cnt += 1
                if _y > 0 and _x + 1 < x and img[_y - 1][_x + 1] > 0:
                    cnt += 1
                if _y + 1 < y and _x > 0 and img[_y + 1][_x - 1] > 0:
                    continue
                if _y + 1 < y and _x + 1 < x and img[_y + 1][_x + 1] > 0:
                    cnt += 1
                if cnt > 1:
                    continue
                img[_y][_x] = 0
    return img


def analyse_version(img, threshold=180):
    """
    分析图像类别
    :param threshold: 阈值 默认为180
    :param img:
    :return: 图像类别 1. 表示无背景  2.表示有背景
    """
    "我们认为图像区域的值范围在0~130之间"
    if get_mean_value(img) <= threshold:
        return 2
    return 1


def cut_version2(img, threshold=182):
    """
    对版本二进行图像切割
    :param img:
    :param threshold: 阈值
    :return: 返回图像开始位置链表和结束位置链表
    """
    y, x = img.shape[:2]
    "避免统计到开头的部分"
    img_st_pos = 0
    """图像开始位置"""
    img_rect_st = []
    """图像结束位置"""
    img_rect_en = []
    mean_arr = np.zeros((x, 1))
    for _x in xrange(x):
        tmp_sum = 0
        for _y in xrange(y):
            tmp_sum += img[_y][_x]
        mean_arr[_x] = tmp_sum / y

    for _value in xrange(x):
        if _value > 0 and mean_arr[_value] >= mean_arr[_value - 1] + 30 and mean_arr[_value] >= threshold:
            if _value > img_st_pos + 14:
                img_rect_st.append(img_st_pos)
                img_rect_en.append(_value)
                img_st_pos = _value
                break
            img_st_pos = _value
    if x > img_st_pos + 14:
        img_rect_st.append(img_st_pos)
        img_rect_en.append(x)
    return img_rect_st, img_rect_en


def mesr_text(img, del_text_path, image_cnt, words_name, y_value=10, x_value=30):
    """
    分水岭算法
    :param deep:
    :param x_value:
    :param img:
    :param del_text_path:
    :param image_cnt:
    :param words_name:
    :param a_value:
    :return:
    """
    # B, G, R = cv2.split(img)
    mser = cv2.MSER()
    regions = mser.detect(img)
    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
    """寻找最大区域"""
    for index, hull in enumerate(hulls):
        x_min = 256
        x_max = -1
        y_min = 256
        y_max = -1
        for point in hull:
            x_min = int_min(x_min, point[0][0])
            x_max = int_max(x_max, point[0][0])
            y_min = int_min(y_min, point[0][1])
            y_max = int_max(y_max, point[0][1])
        tmp = img[y_min:y_max, x_min:x_max]
        sub_path = os.path.join(del_text_path, 'words_' + str(image_cnt))
        if make_dir(sub_path):
            final_path = os.path.join(sub_path, words_name.split('.')[0])
            if make_dir(final_path):
                cv2.imwrite(
                    os.path.join(final_path,
                                 words_name.split('.')[0] + '_' + str(index) + '.' +
                                 words_name.split('.')[1]),
                    tmp)


def get_real_image(img, threshold=130):
    """
    截取整体文字区域
    :param img: 灰度图片
    :param threshold： 阈值
    :return: 文字区域图片
    """
    y, x = img.shape[:2]
    real_x_start = 0
    real_x_end = 0
    for _x in xrange(x):
        for _y in xrange(y):
            if img[_y][_x] <= threshold:
                real_x_start = _x
                break
        if real_x_start != 0:
            break
    for _x in range(x - 1, 0, -1):
        for _y in xrange(y):
            if img[_y][_x] <= threshold:
                real_x_end = _x + 1
                break
        if real_x_end != 0:
            break
    return img[0:y, real_x_start:real_x_end]


def get_binary_real_image(img):
    """
    截取整体文字区域
    :param img: 灰度图片
    :return: 文字区域图片
    """
    y, x = img.shape[:2]
    real_x_st = 0
    real_x_en = 0
    for _x in xrange(x):
        for _y in xrange(y):
            if img[_y][_x] != 0:
                real_x_st = _x
                break
        if real_x_st != 0:
            break
    for _x in range(x - 1, 0, -1):
        for _y in xrange(y):
            if img[_y][_x] != 0:
                real_x_en = _x + 1
                break
        if real_x_en != 0:
            break
    return img[0:y, real_x_st:real_x_en]


def get_real_image_rect(img):
    """
    截取整体文字区域
    :param img: 灰度图片
    :return: 文字区域图片
    """
    y, x = img.shape[:2]
    real_x_st = 0
    real_x_en = 0
    """对于水平方向"""
    for _x in xrange(x):
        for _y in xrange(y):
            if img[_y][_x] != 0:
                real_x_st = _x
                break
        if real_x_st != 0:
            break
    for _x in range(x - 1, 0, -1):
        for _y in xrange(y):
            if img[_y][_x] != 0:
                real_x_en = _x
                break
        if real_x_en != 0:
            break
    """对于垂直方向"""
    real_y_st = 0
    real_y_en = 0
    for _x in range(real_x_st, real_x_en + 1, 1):
        for _y in range(0, y, 1):
            if img[_y][_x] != 0:
                real_y_st = _y
                break
        if real_x_st != 0:
            break
    for _x in range(real_x_st, real_x_en + 1, 1):
        for _y in xrange(y - 1, 0, -1):
            if img[_y][_x] != 0:
                real_y_en = _y
                break
        if real_x_en != 0:
            break

    return real_y_en - real_y_st, real_x_en - real_x_st


def judge_the_image_size(img, height=24, width=60):
    """
    设置成固定大小
    :param img:
    :param height: 默认为24
    :param width: 默认为60
    :return:
    """
    y_len, x_len = img.shape[:2]
    new_img = np.zeros((height, width))
    for y_px in xrange(height):
        for i in xrange(width):
            if y_len > y_px and x_len > i:
                new_img[y_px][i] = img[y_px][i]
            else:
                new_img[y_px][i] = 255

    return new_img


# 保存图片
def save_img(img, n_img, del_text_path, image_cnt, words_name, y_value=10, x_value=30):
    """统计能量值"""
    y, x = n_img.shape[:2]
    pol = []

    for _x in range(0, x, 1):
        temp_value = 0
        for _y in range(0, y, 1):
            temp_value += n_img[_y][_x]
        pol.append(temp_value)
    min_value_pre = 0
    min_value_nex = 0
    _len = len(pol)
    equal_size = 0
    line_pre = []
    line_nex = []
    img_cnt = 0
    for index in range(0, _len, 1):
        min_value_nex = index + 1
        if index + 1 < _len and pol[index] > pol[index + 1]:
            equal_size = 1
        elif index + 1 < _len and equal_size > 0 and pol[index] == 0 and pol[index] == pol[index + 1]:
            equal_size += 1

        elif index + 1 < _len and equal_size > 1 and pol[index] < pol[index + 1]:
            while min_value_pre < min_value_nex and pol[min_value_pre] == 0:
                min_value_pre += 1
            while min_value_pre < min_value_nex and pol[min_value_nex] == 0:
                min_value_nex -= 1
            if equal_size > 5:
                line_pre.append(0 if min_value_pre == 0 else min_value_pre - 1)
                line_nex.append(min_value_nex + 1)
                img_cnt += 1
                min_value_pre = min_value_nex
            equal_size = 0
    while min_value_pre < min_value_nex and pol[min_value_pre] == 0:
        min_value_pre += 1
    while min_value_pre < min_value_nex and pol[min_value_nex - 1] == 0:
        min_value_nex -= 1
    if min_value_nex > min_value_pre + 10:
        line_pre.append(0 if min_value_pre == 0 else min_value_pre - 1)
        line_nex.append(min_value_nex + 1)
    write_image(img, del_text_path, image_cnt, words_name, line_pre, line_nex)
    """对于image进行分析"""


def save_img_mat(img, n_img, y_value=10, x_value=30):
    """
    保存图片
    :param n_img:
    :param index:
    :param deep:
    :param x_value:
    :param img:
    :param del_text_path:
    :param image_cnt:
    :param words_name:
    :param a_value:

    :return:
    """
    """统计能量值"""
    y, x = n_img.shape[:2]
    pol = []

    for _x in range(0, x, 1):
        temp_value = 0
        for _y in range(0, y, 1):
            temp_value += n_img[_y][_x]
        pol.append(temp_value)
    min_value_pre = 0
    min_value_nex = 0
    _len = len(pol)
    equal_size = 0
    line_pre = []
    line_nex = []
    img_cnt = 0
    for index in range(0, _len, 1):
        min_value_nex = index + 1
        if index + 1 < _len and pol[index] > pol[index + 1]:
            equal_size = 1
        elif index + 1 < _len and equal_size > 0 and pol[index] == 0 and pol[index] == pol[index + 1]:
            equal_size += 1

        elif index + 1 < _len and equal_size > 1 and pol[index] < pol[index + 1]:
            while min_value_pre < min_value_nex and pol[min_value_pre] == 0:
                min_value_pre += 1
            while min_value_pre < min_value_nex and pol[min_value_nex] == 0:
                min_value_nex -= 1
            if equal_size > 5:
                line_pre.append(0 if min_value_pre == 0 else min_value_pre - 1)
                line_nex.append(min_value_nex + 1)
                img_cnt += 1
                min_value_pre = min_value_nex
            equal_size = 0
            # plt.plot(pol[int(min_value_pre):int(_len)])
            # plt.show()
    while min_value_pre < min_value_nex and pol[min_value_pre] == 0:
        min_value_pre += 1
    while min_value_pre < min_value_nex and pol[min_value_nex - 1] == 0:
        min_value_nex -= 1
    if min_value_nex > min_value_pre + 10:
        line_pre.append(0 if min_value_pre == 0 else min_value_pre - 1)
        line_nex.append(min_value_nex + 1)
    return get_image(img, line_pre, line_nex)
    """对于image进行分析"""


def write_image(img, del_text_path, image_cnt, words_name, line_pre, line_nex, binary_flag=False):
    """
    将图片保存到磁盘中
    :param img: 图片数据
    :param del_text_path:  路径
    :param image_cnt:  words对应编号
    :param words_name:   图片名称
    :param line_pre:   图片开始位置数组
    :param line_nex:   图片结束位置数组
    :param binary_flag: 表示是否对图片进行二值化，默认是不二值化
    :return:
    """
    y, x = img.shape[:2]
    for _indx in xrange(len(line_pre)):

        t_img = img[0:y, int(line_pre[_indx]):int(line_nex[_indx] + 1)]
        if binary_flag:
            t_img = pretreatment_image(t_img, 7)
            t_img = binary_text(t_img)
            t_img = get_binary_real_image(t_img)
        t_img = judge_the_image_size(t_img)
        sub_path = os.path.join(del_text_path, 'words_' + str(image_cnt))
        if make_dir(sub_path):
            cv2.imwrite(
                os.path.join(sub_path,
                             words_name.split('.')[0] + '_' + str(_indx) + '.' +
                             words_name.split('.')[1]),
                t_img)


def get_image(img, line_pre, line_nex, binary_flag=False):
    """
    将图片保存到磁盘中
    :param img: 图片数据
    :param line_pre:   图片开始位置数组
    :param line_nex:   图片结束位置数组
    :param binary_flag: 表示是否对图片进行二值化，默认是不二值化
    :return:
    """
    y, x = img.shape[:2]
    list_img = []
    for _indx in xrange(len(line_pre)):

        t_img = img[0:y, int(line_pre[_indx]):int(line_nex[_indx] + 1)]
        if binary_flag:
            t_img = pretreatment_image(t_img, 7)
            t_img = binary_text(t_img)
            t_img = get_binary_real_image(t_img)
        t_img = judge_the_image_size(t_img)
        list_img.append(t_img)
    return list_img


def cut(image_cnt, path_dir= cfg.ROOT + '/data/download'):
    """
    :param image_cnt: words对应编号
    :param path_dir:
    :return:
    """
    del_text_path = os.path.join(path_dir, 'words_cut_result')
    make_dir(del_text_path)

    words_path = os.path.join(path_dir, 'words/words_' + str(image_cnt))
    if not os.path.exists(words_path):
        return
    for words_name in os.listdir(words_path):
        try:
            print words_name
            img = cv2.imread(os.path.join(words_path, words_name), 0)
            img = get_real_image(img, 160)
            if 2 == analyse_version(img):
                "说明有背景"
                img_rect_st, img_rect_en = cut_version2(img, 182)
                write_image(img, del_text_path, image_cnt, words_name, img_rect_st, img_rect_en, False)
            else:
                # img = rm_noise(img)
                n_img = pretreatment_image(img, 3)
                n_img = binary_text(n_img)
                n_img = get_binary_real_image(n_img)
                save_img(img, n_img, del_text_path, image_cnt, words_name, y_value=10, x_value=28)
                # mesr_text(img, del_text_path, image_cnt, words_name, y_value=10, x_value=28)
        except Exception as e:
            pass


def get_test(img):
    img = get_real_image(img, 160)
    if 2 == analyse_version(img):
        "说明有背景"
        img_rect_st, img_rect_en = cut_version2(img, 182)
        return get_image(img, img_rect_st, img_rect_en, False)
    else:
        # img = rm_noise(img)
        n_img = pretreatment_image(img, 3)
        n_img = binary_text(n_img)
        n_img = get_binary_real_image(n_img)
        return save_img_mat(img, n_img, y_value=10, x_value=28)
        # mesr_text(img, del_text_path, image_cnt, words_name, y_value=10, x_value=28)


# 调整目录中图像大小
def classify_image(path_dir=cfg.ROOT + '/data/download/words',
                   dest_path=cfg.ROOT + '/data/download/words-classify'):
    """
        :param path_dir:
        :param dest_path:
        :return:
    """
    temp = filter(lambda s: not s.startswith("."), os.listdir(path_dir))
    for words_name in temp:
        print words_name
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        sub_root_path = os.path.join(path_dir, words_name)
        if os.path.isdir(sub_root_path):
            classify_image(sub_root_path, os.path.join(dest_path, words_name))
            continue
        img = cv2.imread(sub_root_path, 0)
        new_img = judge_the_image_size(img)
        cv2.imwrite(os.path.join(dest_path, words_name), new_img)
    return 0

if __name__ == '__main__':
    cut(0)
