# -*- coding:utf-8 -*-

# --------------------------------------------------------
# 12306-captcha
# Copyright (c) 2017
# Licensed under The Apache License [see LICENSE for details]
# Written by ruifengshan
# --------------------------------------------------------

"""设置去除图像中的黑色斑点"""
import cv2
import numpy as np


def rm_blackNoisy(im, threshold=20):
    """
    该函数用来去除图像的中黑色斑点,同时采用插值法进行该点像素的补充
    ,param threshold, 设定黑色斑点的最大值
    ,param img, RGB图像的数据
    ,return, 返回RGB图像数据
    """

    def min(c_val, t_val):
        return c_val if c_val < t_val else t_val

    def sum(_val, _sum, _num):
        return _val + _sum, _num + 1

    def rm_blackNoisy_component(img, threshold):
        y, x = img.shape[:2]  # x,y表示坐标
        for _x in range(0, x, 1):
            for _y in range(0, y, 1):
                cnt = 0
                _sum = num = 0
                if _y > 0:
                    _sum, num = sum(img[_y - 1, _x], _sum, num)
                if _y + 1 < y:
                    _sum, num = sum(img[_y + 1, _x], _sum, num)
                if _x > 0:
                    _sum, num = sum(img[_y, _x - 1], _sum, num)
                if _x + 1 < x:
                    _sum, num = sum(img[_y, _x + 1], _sum, num)
                if _y > 0 and _x > 0:
                    _sum, num = sum(img[_y - 1, _x - 1], _sum, num)
                if _y > 0 and _x + 1 < x:
                    _sum, num = sum(img[_y - 1, _x + 1], _sum, num)
                if _y + 1 < y and _x > 0:
                    _sum, num = sum(img[_y + 1, _x - 1], _sum, num)

                if _y + 1 < y and _x + 1 < x:
                    _sum, num = sum(img[_y + 1, _x + 1], _sum, num)
                if cnt > 0 or num < 1:  # 说明不是单个点
                    continue
                # 如果是孤点,则可以依据权重进行插值
                arvage = _sum / num
                if img[_y, _x] + 100 <= arvage:
                    img[_y, _x] = arvage

        return img

    if im.ndim == 3:
        b, g, r = cv2.split(im)
        _b = rm_blackNoisy_component(b, threshold)
        _g = rm_blackNoisy_component(g, threshold)
        _r = rm_blackNoisy_component(r, threshold)
        img = cv2.merge([_b, _g, _r])  # 前面分离出来的三个通道

    else:
        return rm_blackNoisy_component(im, threshold)

    return img
