# -*- coding: utf-8 -*-
import requests

# ip地址转整数
def ip2int(ip):
    return struct.unpack('!I', socket.inet_aton(ip))[0]

def write_info(url, data):
    return requests.post(url, data=data)
