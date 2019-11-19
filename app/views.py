# -*- coding: utf-8 -*-
import os
import json
import uuid
import base64

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
    header = {'Cache-Control': 'public, max-age=60'}
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

# 根据ip获取设备状态信息
@cache.memoize(60)
def get_device_state_by_ip(ip):
    dev = DeviceState.query.filter_by(ip_addr=ip).first()
    if dev is None:
        return None
    return {'stat_code': dev.stat_code, 'vehicle_point_no': dev.vehicle_point_no, 'direction': dev.direction}

@app.route('/upload', methods=['POST'])
def upload_post():
    if not request.json:
        return jsonify({'message': 'Problems parsing JSON'}), 415
    try:
        uu_id = str(uuid.uuid4())
        plate_no = request.json['AlarmInfoPlate']['result']['PlateResult']['license']
        plate_color = request.json['AlarmInfoPlate']['result']['PlateResult']['colorType']
        pass_time = arrow.get(request.json['AlarmInfoPlate']['result']['PlateResult']['timeStamp']['Timeval']['sec']).to('Asia/Shanghai')
        ip_addr = request.json['AlarmInfoPlate']['ipaddr']
        device_name = request.json['AlarmInfoPlate']['deviceName']
        serialno = request.json['AlarmInfoPlate']['serialno']
        path_seq = (app.config['BASE_PATH'], 'Plate', pass_time.format('YYYYMMDD'), serialno, pass_time.format('HH'))
        img_path = '/'.join(path_seq)
        name = '{0}_{1}_{2}'.format(pass_time.format('YYYYMMDDHHmmss'), serialno, helper.ip2int(ip_addr))
        pic1 = save_img(img_path, name, request.json['AlarmInfoPlate']['result']['PlateResult']['imageFile']).replace(app.config['BASE_PATH'], app.config['BASE_URL_PATH'])
        pic2 = save_img(img_path, name+'_plate', request.json['AlarmInfoPlate']['result']['PlateResult']['imageFragmentFile']).replace(app.config['BASE_PATH'], app.config['BASE_URL_PATH'])
        try:
            vehicle = VehiclePass(plate_no=plate_no, plate_color=plate_color,
                           pass_time=pass_time.datetime, site_id='1',
                           pic1=pic1, pic2=pic2, ip_addr=ip_addr,
                           device_name=device_name, uuid=uu_id,
                           serialno=serialno)
            db.session.add(vehicle)
            db.session.commit()
        except Exception as e:
             logger.error(e)
             db.session.rollback()
        dev = get_device_state_by_ip(ip_addr)
        if dev is None:
            stat_code = 0
            vehicle_point_no = 1
            direction = 1
        else:
            stat_code = dev['stat_code']
            vehicle_point_no = dev['vehicle_point_no']
            direction = dev['direction']
        vehicle2 = VehiclePass2(plate_no=plate_no, plate_color=plate_color,
                        pass_time=pass_time.datetime, stat_code=stat_code,
                        vehicle_point_no=vehicle_point_no, direction=direction,
                        pic1=pic1, pic2=pic2, ip_addr=ip_addr, device_name=device_name,
                        uuid=uu_id, serialno=serialno)
        db.session.add(vehicle2)
        db.session.commit()

    except Exception as e:
        logger.error(e)
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
def set_device_state_by_ip(ip, serialno, white_list='[]'):
    dev = DeviceState.query.filter_by(ip_addr=ip).first()
    if dev is None:
        n = arrow.now('PRC').datetime.replace(tzinfo=None)
        new_dev = DeviceState(ip_addr=ip, serialno=serialno, white_list=white_list,
                    create_time=n, last_modify=n, update_flag=1)
        db.session.add(new_dev)
        db.session.commit()
        return (new_dev.white_list, new_dev.last_modify,  new_dev.update_flag)
    if dev.serialno != serialno:
        dev.serialno = serialno
        dev.last_modify = arrow.now('PRC').datetime.replace(tzinfo=None)
        db.session.commit()
    return (dev.white_list, dev.last_modify,  dev.update_flag)


@app.route('/heart', methods=['POST'])
def heart_post():
    #if not request.json:
    #    return jsonify({'message': 'Problems parsing JSON'}), 415
    try:
        logger.info(request.json)
        data = "{0},host={1},serialno={2} value={3}".format('heart', request.headers.get("X-Real-IP", request.remote_addr), request.json['heartbeat']['serialno'], request.json['heartbeat']['countid'])
        helper.write_info(app.config['INFLUXDB_URL'], data)
        if request.json.get('heartbeat', None) is not None:
            dev = set_device_state_by_ip(request.headers.get("X-Real-IP", request.remote_addr), request.json['heartbeat']['serialno'])
    except Exception as e:
        logger.error(e)
    return jsonify({}), 201, {'Content-Type': 'application/json'}
    #return jsonify(app.config['WHITE_LIST_DEL']), 201