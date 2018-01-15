#!/usr/bin/env bash

TOOLS_DIR=/home/ruifengshan/caffe/build/tools
DATA=/home/ruifengshan/github/12306-captcha/data/words

$TOOLS_DIR/compute_image_mean $DATA/words_train_lmdb $DATA/mean.binaryproto
