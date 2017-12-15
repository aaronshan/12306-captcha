# _*_ coding:utf-8 _*_

import os
import scipy.misc
from src.config import cfg


synset_file = cfg.ROOT + 'label/synset'


# 将synset转换为train.txt文件
def load_file(path=synset_file):
    synset = [line.strip() for line in open(path).readlines()]
    print synset
    return synset


def create_file(data_path, file_list, file_name):
    """
    创建训练文件train.txt/test.txt

    :param data_path: 图片文件的上级路径
    :param file_list: synset生成的list
    :param train_file_name: 标签表
    :return:
    """

    try:
        cnt = 0
        if not os.path.isfile(file_name):
            os.mknod(file_name)
        file_txt = open(file_name, mode='wr')
        for file_name in file_list:
            print file_name
            file_path = os.path.join(data_path, file_name)
            print file_path
            if not os.path.isdir(file_path):
                print file_path, '目录不存在'
                continue
            for path in os.listdir(file_path):
                file_txt.write(os.path.join(file_name, path) + " " + str(cnt) + "\n")
            cnt += 1
    except Exception, e:
        print "执行失败", e


def create_train_file(data_path, file_list, train_file_name='train.txt'):
    create_file(data_path, file_list, train_file_name)


def create_test_file(data_path, file_list, test_file_name='test.txt'):
    create_file(data_path, file_list, test_file_name)


if __name__ == '__main__':
    create_train_file(cfg.ROOT + "/data/image/train/", load_file())
    create_test_file(cfg.ROOT + "/data/image/test/", load_file())