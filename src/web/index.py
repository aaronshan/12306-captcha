# _*_ coding: utf-8 _*_

from flask import Flask
from flask import render_template
from flask import redirect, url_for
from flask import request
import urllib2
import ssl
import numpy as np
import random
import hashlib
import datetime
import cookielib
import sys

import utils.Img12306 as Img12306
from src.config import cfg

caffe_root = cfg.CAFFE_ROOT
sys.path.insert(0, caffe_root + 'python')

import caffe

### config_file_path
pj_dir= cfg.ROOT + "/src/web"


app = Flask(__name__)

### caffe config
net_file = cfg.ROOT + '/src/image/model/image_deploy.prototxt'
caffe_model = cfg.ROOT + 'model/image/f14_snapshot_iter_99000.caffemodel'
labels_filename =  cfg.ROOT + 'label/synset'

net = caffe.Net(net_file, caffe_model, caffe.TEST)
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
"读取的图片文件格式为H×W×K，需转化为K×H×W"
transformer.set_transpose('data', (2, 0, 1))
# transformer.set_mean('data', mean=np.float32([103.939, 116.779, 123.68]))
"将图片存储为[0, 1]，而caffe中将图片存储为[0, 255"
transformer.set_raw_scale('data', 255)
"caffe中图片是BGR格式，而原始格式是RGB，所以要转化"
transformer.set_channel_swap('data', (2, 1, 0))

### agent config
ssl._create_default_https_context = ssl._create_unverified_context
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
login = 'https://kyfw.12306.cn/otn/login/init'
domain = 'kyfw.12306.cn'
cookieJ = cookielib.CookieJar()
op = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJ))
op.add_handler = [('User-agent', agent)]
op.add_handler = [('Host', domain)]
op.open(login)
# '获取cookie'
cookies = ''
for Cookie in enumerate(cookieJ):
    ck = Cookie[1]
    cookies += ck.name + '=' + ck.value + ";"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh - CN, zh;q = 0.8',
        'Cache-Control': 'no - cache',
        'Connection': 'keep-alive',
        'Referer': login,
        'Cookie': cookies,
        'Host': domain,
        'User-aget': agent
    }


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/12306submit', methods=['POST'])
def submit12306():
    img_url = request.form['img_url']
    error_idx = request.form['error_idx']
    if error_idx != "":
        error_idx_arr = request.form['error_idx'].split("-")
        error_idx_arr.remove("")
        results=[request.form['result0'], request.form['result1'], request.form['result2'], request.form['result3'], request.form['result4'], request.form['result5'], request.form['result6'], request.form['result7']]
        file_path = "%s%s" % (pj_dir, img_url)
        img_file_name = file_path.split("/")[-1];
        img = Img12306.get_img_file(file_path)
        img_split = Img12306.get_img(img)
        for idx in error_idx_arr:
            i = int(idx)
            if results[i] == "":
                continue
            out_path = "%s/error/%s/%s_%s" % (pj_dir, results[i], i, img_file_name)
            Img12306.save_as_img_file(img_split[i], out_path)

    return redirect(url_for('img'))

@app.route('/12306')
def img():
    total = np.random.randint(1, 2)
    const_url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&'
    random_token = random.uniform(0, 1)
    img_url = const_url + urllib2.quote(str(random_token))
    while total > 0:
        resq = urllib2.Request(img_url)
        response = urllib2.urlopen(resq)
        total = total - 1

    raw = response.read()
    fn = hashlib.md5(raw).hexdigest()
    dt=datetime.datetime.now()
    dt=dt.strftime('%Y%m%d')
    output_file_name = "%s/static/tmp/%s_%s.jpg" % (pj_dir, dt, fn);
    with open(output_file_name, 'wb') as fp:
       fp.write(raw)

    no_noise_file_name = "%s/static/tmp/%s_%s_no_noise.jpg" % (pj_dir, dt, fn);
    Img12306.remove_file_noise(output_file_name, no_noise_file_name)

    # arr = np.asarray(bytearray(raw), dtype=np.uint8)
    # img = cv2.imdecode(arr,cv2.IMREAD_UNCHANGED)
    # img = img / 255.
    # img = img[:,:,(2,1,0)]
    img = caffe.io.load_image(no_noise_file_name)

    img_split = Img12306.get_img(img)
    results = []
    for i in range(img_split.__len__()):
        im = img_split[i]
        results.append(judge(im).decode("utf8"))

    img_src = "/static/tmp/%s_%s.jpg" % (dt, fn);
    return render_template('12306.html', img_url=img_src, results=results)

def judge(im):
    net.blobs['data'].data[...] = transformer.preprocess('data', im)
    out = net.forward()

    labels = np.loadtxt(labels_filename, str, delimiter='\t')
    # prob = out['softmax'][0]
    top_k = net.blobs['softmax'].data[0].flatten().argsort()[-1:-6:-1]

    return labels[top_k[0]]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5111, debug=False)
