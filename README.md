# 12306-captcha  [![Author](https://img.shields.io/badge/Author-%E4%B8%AD%E9%BE%84%E7%A8%8B%E5%BA%8F%E5%91%98-blue.svg)](https://www.shanruifeng.win) [![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE) [![Stars](https://img.shields.io/github/stars/aaronshan/12306-captcha.svg?label=Stars&style=social)](https://github.com/aaronshan/12306-captcha)

12306验证码识别

## 1. 训练

### 1.1 准备工作

* 下载caffe并编译, 具体可参考官方文档, 此处不再赘述.
* 修改`src/config.py`中的caffe根目录和项目根目录.
* pip安装easydict, skimage等.

### 1.2 数据

* 通过运行`src/tools/download_image.py`, 会将12306验证码下载至`data/download/all`目录.
* 下载完成后, 通过运行`src/tools/cut_image.py`, 会将其裁剪为图片和文字两部分, 分别放在`data/download/image`目录和`data/download/words`目录.
* 修改`src/image/scripts/words.py`文件main方法中cut方法的参数(其参数为`data/download/words`中子目录的`words_*`中的数字),　它的目的是处理`data/download/words`中的所有子文件, 对多个词语进行分割并调整大小为固定值.
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

#### 图片部分

* 运行`src/image/scripts/create_data.py`, 将会生成图片部分对应的train.txt和test.txt, 里面包含着训练和测试文件及其类别列表.
* 运行`src/image/scripts/create_lmdb.sh`, 将会生成图片部分对应的lmdb文件.

#### 文字部分

* 运行`src/words/scripts/create_data.py`, 将会生成文字部分对应的train.txt和test.txt, 里面包含着训练和测试文件及其类别列表.
* 运行`src/words/scripts/create_lmdb.sh`, 将会生成文字部分对应的lmdb文件.

### 1.3 参数
可以根据实际情况对`src/image/model/image_solver.prototxt`和`src/words/model/words_solver.prototxt`文件进行修改.具体修改方法可参考其他模型.

### 1.4 开始训练
`src/image/scripts/image_train.sh`和`src/image/scripts/image_finetune_train.sh`脚本分别用来进行从头训练/微调训练, 训练方法可参考caffe模型训练方法.

同理：

`src/words/scripts/words_train.sh`和`src/words/scripts/words_finetune_train.sh`脚本分别用来进行从头训练/微调训练, 训练方法可参考caffe模型训练方法.


## 测试
`src/web`提供了一个web测试界面, 运行index.py即可.　运行前, 可以更改对应的模型文件名称.　一个简单示例如下:

![web-demo](https://github.com/aaronshan/12306-captcha/blob/master/web-demo.png)

## 其他

1. 在实际应用中, 会使用从百度/搜狗/谷歌等图片搜索引擎中爬取图片并做处理的方式来完成图片分类收集工作. 比如爬取关键词为档案袋的图片, 再进一步做处理. 以解决从12306下载并裁剪-手工分类效率太低及样本量不足的问题, 提升效率。

2. 此外, 项目里对文字部分的分割也不是很完美. 对图片的分类也是裁剪并逐个进行的, 这样的响应效率不会很高. 可以使用目标检测的方式, 对整个验证码图片做目标检测, 同时检测8个图片及文字部分. 以加快检测速度.
