#!/usr/bin/env bash

dir=`dirname "$0"`
root_path=`cd "$dir/../../..">/dev/null; pwd`
echo "root_path:"$root_path

TOOLS_DIR=/home/ruifengshan/caffe/build/tools

MODEL_CONFIG_DIR=$root_path/src/image/model
MODEL_DIR=$root_path/model/image

$TOOLS_DIR/caffe train \
-solver $MODEL_CONFIG_DIR/words_solver.prototxt  $@ 1>$MODEL_DIR/words_train.log 2>&1 &
