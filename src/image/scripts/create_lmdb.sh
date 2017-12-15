#!/usr/bin/env sh

TOOLS_DIR=/home/ruifengshan/caffe/build/tools

dir=`dirname "$0"`
root_path=`cd "$dir/../../..">/dev/null; pwd`
echo "root_path:"$root_path

DATA=$root_path/data/image


rm -rf $DATA/image_train_lmdb
$TOOLS_DIR/convert_imageset \
--shuffle \
--resize_height=68 \
--resize_width=68 \
$DATA/train  $DATA/train.txt  $DATA/image_train_lmdb


rm -rf $DATA/image_test_lmdb
$TOOLS_DIR/convert_imageset \
--shuffle \
--resize_height=68 \
--resize_width=68 \
$DATA/test  $DATA/test.txt  $DATA/image_test_lmdb
