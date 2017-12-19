# 12306-captcha [![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)

12306验证码识别

## 1. 训练

### 1.1 准备工作

* 下载caffe并编译, 具体可参考官方文档, 此处不再赘述.
* 修改`src/config.py`中的caffe根目录和项目根目录.
* pip安装easydict, skimage等.

### 1.2 数据

* 通过运行`src/tools/download_image.py`, 会将12306验证码下载至`data/download/all`目录.
* 下载完成后, 通过运行`src/tools/cut_image.py`, 会将其裁剪为图片和文字两部分, 分别放在`data/download/image`目录和`data/download/words`目录.
* 然后手工对其进行分类, 分别放至`data/image`和`data/words`目录. 可以将其分为两部分，分别放在对应的train和test目录.比如,一个示例目录如下:
  ```
  -image
  --test
  ---蜡烛
  ----1-1.jpg
  ---沙漠
  ----2-1.jpg
  --train
  ---蜡烛
  ----1-2.jpg
  ---沙漠
  ----2-2.jpg
  ```
* 运行`src/image/scripts/create_data.py`, 将会生成对应的train.txt和test.txt, 里面包含着训练和测试文件及其类别列表.
* 运行`src/image/scripts/create_lmdb.sh`, 将会生成对应的lmdb文件.

### 1.3 参数
可以根据实际情况对`src/image/model/image_solver.prototxt`文件进行修改.具体修改方法可参考其他模型.

### 1.4 开始训练
`src/image/scripts/image_train.sh`和`src/image/scripts/image_finetune_train.sh`脚本分别用来进行从头训练/微调训练, 训练方法可参考caffe模型训练方法.


## 测试
`src/web`提供了一个web测试界面, 运行index.py即可.　运行前, 可以更改对应的模型文件名称.　一个简单示例如下:

![web-demo](https://github.com/aaronshan/12306-captcha/blob/master/web-demo.png)
