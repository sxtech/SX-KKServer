# -*- coding: utf-8 -*-
import os
import socket
import struct
import base64

import requests

# ip地址转整数
def ip2int(ip):
    return struct.unpack('!I', socket.inet_aton(ip))[0]

def write_info(url, data):
    return requests.post(url, data=data)

# 保存图片
def save_img(path, name, data):
    if not os.path.isdir(path):
        os.makedirs(path)
    imgname = '{0}/{1}.jpg'.format(path, name)
    file = open(imgname, 'wb')
    file.write(base64.b64decode(data))
    file.close()
    return imgname
