# -*- coding: utf-8 -*-
import os
import json
import base64 
import socket
import struct
import uuid

import arrow
from flask import g, request, make_response, jsonify, abort

from . import db, app, cache, logger, access_logger
from .models import *
from . import helper


@app.route('/')
def index_get():
    result = {
        'upload': '%supload' % (request.url_root),
        'heart': '%sheart' % (request.url_root)
    }
    header = {'Cache-Control': 'public, max-age=60, s-maxage=60'}
    return jsonify(result), 200, header

# 保存图片
def save_img(path, name, data):
    if not os.path.isdir(path):
        os.makedirs(path)
    imgname = '{0}/{1}.jpg'.format(path, name)
    file = open(imgname, 'wb')
    file.write(base64.b64decode(data))
    file.close()
    return imgname

@app.route('/upload', methods=['POST'])
def upload_post():
    if not request.json:
        return jsonify({'message': 'Problems parsing JSON'}), 415
    try:
        uu_id = str(uuid.uuid4())
        plate_no = request.json['AlarmInfoPlate']['result']['PlateResult']['license']
        plate_color = request.json['AlarmInfoPlate']['result']['PlateResult']['colorType']
        #t = request.json['AlarmInfoPlate']['result']['PlateResult']['timeStamp']['Timeval']['sec']
        ms = request.json['AlarmInfoPlate']['result']['PlateResult']['timeStamp']['Timeval']['usec']
        pass_time = arrow.get(request.json['AlarmInfoPlate']['result']['PlateResult']['timeStamp']['Timeval']['sec']).to('Asia/Shanghai')
        ip_addr = request.json['AlarmInfoPlate']['ipaddr']
        device_name = request.json['AlarmInfoPlate']['deviceName']
        serialno = request.json['AlarmInfoPlate']['serialno']
        path_seq = (app.config['BASE_PATH'], 'Plate', pass_time.format('YYYYMMDD'), serialno, pass_time.format('HH'))
        img_path = '/'.join(path_seq)
        name = '{0}_{1}_{2}'.format(pass_time.format('YYYYMMDDHHmmss'), ms, helper.ip2int(ip_addr))
        pic1 = save_img(img_path, name, request.json['AlarmInfoPlate']['result']['PlateResult']['imageFile']).replace(app.config['BASE_PATH'], app.config['BASE_URL_PATH'])
        pic2 = save_img(img_path, name+'_plate', request.json['AlarmInfoPlate']['result']['PlateResult']['imageFragmentFile']).replace(app.config['BASE_PATH'], app.config['BASE_URL_PATH'])
        vehicle = VehiclePass(plate_no=plate_no, plate_color=plate_color,
                       pass_time=pass_time.datetime, site_id='1',
                       pic1=pic1, pic2=pic2, ip_addr=ip_addr,
                       device_name=device_name, uuid=uu_id,
                       serialno=serialno)
        db.session.add(vehicle)
        db.session.commit()

    except Exception as e:
        logger.exception(e)
        return jsonify({}), 201
    result = {
        "Response_AlarmInfoPlate": {
            "info": "ok",
            "content": "retransfer_stop",
            "is_pay": "true"
        }
    }
    return jsonify(result), 201

#@cache.memoize(60)
def get_device_state_by_ip(ip, serialno, white_list='[]'):
    dev = DeviceState.query.filter_by(ip=ip).first()
    if dev is None:
        n = arrow.now('PRC').datetime.replace(tzinfo=None)
        dev2 = DeviceState(ip=ip, serialno=serialno, white_list=white_list,
                    create_time=n, last_modify=n)
        db.session.add(dev2)
        db.session.commit()
        return (dev2.white_list, dev2.last_modify,  dev2.update_flag)
    return (dev.white_list, dev.last_modify,  dev.update_flag)

@cache.memoize(60)
def get_white_list():
    white_list = VehicleManage.query.filter_by(del_flag=0).all()
    w = {
        'addWhiteList': {
            'add_data': []
        }
    }
    n = arrow.now('PRC')
    st = n.format('YYYYMMDDHHmmss')
    et = n.shift(months=3).format('YYYYMMDDHHmmss')
    for i in white_list:
        info = {
            'carnum': i.plate_no,
            'startime': st,
            'endtime': et
        }
        w['addWhiteList']['add_data'].append(info)
    return w

# 更新标记设置为1
def update_device_state_flag_by_ip(ip, update_flag=-1, white_list='[]'):
    dev = DeviceState.query.filter_by(ip=ip).first()
    if update_flag != -1:
        dev.update_flag = update_flag
    if white_list != '[]':
        dev.white_list = json.dumps(white_list)
        dev.last_modify = arrow.now('PRC').datetime.replace(tzinfo=None)
    db.session.commit()

@app.route('/heart', methods=['POST'])
def heart_post():
    #if not request.json:
    #    return jsonify({'message': 'Problems parsing JSON'}), 415
    # 接收的json格式错误 设置为false
    r_j_error = False
    try:
        if not request.json:
            return jsonify({'message': 'Problems parsing JSON'}), 415
    except Exception as e:
        logger.error(e)
        r_j_error = True

    # 如果收到的json格式错误则直接获取POST请求的数据
    try:
        if r_j_error:
            logger.info(request.get_data())
            logger.info(request.get_data().decode("gbk"))
            r = json.loads(request.get_data().decode("gbk"))
            if r.get('Response_whiteList', None) is not None:
                update_device_state_flag_by_ip(request.headers.get("X-Real-IP", request.remote_addr), -1, r['Response_whiteList']['data'])
            return jsonify({}), 201, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(e)

    try:
        result = '{}'
        logger.info(request.json)
        if request.json.get('heartbeat', None) is not None:
            dev = get_device_state_by_ip(request.headers.get("X-Real-IP", request.remote_addr), request.json['heartbeat']['serialno'])
            if dev[2] == 0:
                # 更新前先删除旧白名单数据
                result = json.dumps(app.config['WHITE_LIST_DEL'])
        # 添加白名单后更新状态
        if request.json.get('Response_AddWhiteList', None) is not None:
            update_device_state_flag_by_ip(request.headers.get("X-Real-IP", request.remote_addr), 1)
            result = json.dumps(app.config['WHITE_LIST_QUE'])
        # 更新白名单数据
        if request.json.get('Response_DeleteWhiteList', None) is not None:
            result = json.dumps(get_white_list(), ensure_ascii=False).encode("gbk")
            logger.info(result)
    except Exception as e:
        logger.error(e)
    return result, 201, {'Content-Type': 'application/json'}
    #return jsonify(app.config['WHITE_LIST_DEL']), 201