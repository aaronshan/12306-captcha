# _*_ coding: utf-8 _*_

import cv2
import os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

"""
    该函数用来去除图像的中黑色斑点,同时采用插值法进行该点像素的补充
    ,param threshold, 设定黑色斑点的最大值
    ,param img, RGB图像的数据
    ,return, 返回RGB图像数据
"""
def rm_blackNoisy(im, threshold=20):
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
                average = _sum / num
                if img[_y, _x] + 100 <= average:
                    img[_y, _x] = average

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

def remove_file_noise(input_path, output_path):
    im_in = cv2.imread(input_path, 1);
    im_out = rm_blackNoisy(im_in);
    cv2.imwrite(output_path, im_out)


# 分割图片12306图片
def get_img(im):
    img = []
    for v in range(2):  # 图片行
        for h in range(4):  # 图片列
            img.append(im[(40 + (v * 72)):(108 + (v * 72)), (4 + (h * 72)):((h + 1) * 72)])
    return img

# 得到图像中的文本部分
def get_text(im):
    return im[3:24, 116:288]

def get_img_file(input_path):
    return cv2.imread(input_path, 1);

def save_as_img_file(im, output_path):
    if output_path.endswith(".jpg"):
        dir_path = "/".join(output_path.split("/")[0:-1])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    # output_path= output_path.decode("utf8")
    cv2.imwrite(output_path, im)