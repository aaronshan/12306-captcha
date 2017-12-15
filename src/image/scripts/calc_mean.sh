#!/usr/bin/env bash

TOOLS_DIR=/home/ruifengshan/caffe/build/tools
DATA=/home/ruifengshan/github/12306-captcha/data/image

$TOOLS_DIR/compute_image_mean $DATA/image_train_lmdb $DATA/mean.binaryproto

