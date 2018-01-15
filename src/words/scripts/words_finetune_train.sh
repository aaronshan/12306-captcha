#!/usr/bin/env sh
#该指令是用来在已有的模型上，进行微调，需要注意的是模型的图片大小以及layer需要保持一致. 
# 如果要开启GPU模式，只需要在该指令的末尾加上 -gpu 0 即可. ps 默认情况下run as cpu-only

dir=`dirname "$0"`
root_path=`cd "$dir/../../..">/dev/null; pwd`
echo "root_path:"$root_path

TOOLS_DIR=/home/ruifengshan/caffe/build/tools

MODEL_CONFIG_DIR=$root_path/src/image/model
MODEL_DIR=$root_path/model/image

$TOOLS_DIR/caffe train \
-solver $MODEL_CONFIG_DIR/words_solver.prototxt  \
-gpu 0 \
-weights $MODEL_DIR/words_4_snapshot_iter_160000.caffemodel  1> $MODEL_DIR/words_train.log 2>&1 &
