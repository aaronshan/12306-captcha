#!/usr/bin/env sh

TOOLS_DIR=/home/ruifengshan/caffe/build/tools

dir=`dirname "$0"`
root_path=`cd "$dir/../../..">/dev/null; pwd`
echo "root_path:"$root_path

DATA=$root_path/data/words

rm -rf $DATA/words_train_lmdb
$TOOLS_DIR/convert_imageset \
--shuffle \
--resize_height=24 \
--resize_width=60 \
$DATA/train  $DATA/train.txt  $DATA/words_train_lmdb


rm -rf $DATA/words_test_lmdb
$TOOLS_DIR/convert_imageset \
--shuffle \
--resize_height=24 \
--resize_width=60 \
$DATA/test  $DATA/test.txt  $DATA/words_test_lmdb
