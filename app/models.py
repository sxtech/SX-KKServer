﻿# -*- coding: utf-8 -*-
import arrow
from sqlalchemy import MetaData

from . import db


class VehiclePass(db.Model):
    """过车记录"""
    __tablename__ = 'vehicle_pass'

    id = db.Column(db.Integer, primary_key=True)
    plate_no = db.Column(db.String(32), default='-')
    plate_color = db. Column(db.String(8), default='1')
    pass_time = db.Column(
        db.DateTime, default=arrow.now('PRC').datetime.replace(tzinfo=None))
    site_id = db.Column(db.Integer, default=1)
    direction = db.Column(db.String(8), default='1')
    status = db.Column(db.String(8), default='1')
    pic1 = db.Column(db.String(128), default='')
    pic2 = db.Column(db.String(128), default='')
    pic3 = db.Column(db.String(128), default='')
    pic4 = db.Column(db.String(128), default='')
    ip_addr = db.Column(db.String(16), default='127.0.0.1')
    device_name = db.Column(db.String(32), default='')
    uuid = db.Column(db.String(36), default='')
    create_time = db.Column(
        db.DateTime, default=arrow.now('PRC').datetime.replace(tzinfo=None))
    serialno = db.Column(db.String(128), default='')

    def __init__(self, plate_no='-', plate_color='1', pass_time=None,
                 site_id=1, direction='1', status='1', pic1='', pic2='',
                 pic3='', pic4='', ip_addr='', device_name='', uuid='', 
                 create_time=None, serialno=''):
        self.plate_no = plate_no
        self.plate_color = plate_color
        self.pass_time = pass_time
        self.site_id = site_id
        self.direction = direction
        self.status = status
        self.pic1 = pic1
        self.pic2 = pic2
        self.pic3 = pic3
        self.pic4 = pic4
        self.ip_addr = ip_addr
        self.device_name = device_name
        self.uuid = uuid
        self.create_time = create_time
        self.serialno = serialno
        
    def __repr__(self):
        return '<vehicle_pass %r>' % self.id


class VehiclePass2(db.Model):
    """过车记录"""
    __bind_key__ = 'env'
    __tablename__ = 'vehicle_pass'
    metadata = MetaData()

    id = db.Column(db.Integer, primary_key=True)
    plate_no = db.Column(db.String(32), default='-')
    plate_color = db. Column(db.Integer, default=0)
    pass_time = db.Column(
        db.DateTime, default=arrow.now('PRC').datetime.replace(tzinfo=None))
    stat_code = db.Column(db.Integer, default=0)
    vehicle_point_no = db.Column(db.Integer, default=1)
    direction = db.Column(db.String(8), default='1')
    status = db.Column(db.String(8), default='1')
    pic1 = db.Column(db.String(128), default='')
    pic2 = db.Column(db.String(128), default='')
    pic3 = db.Column(db.String(128), default='')
    pic4 = db.Column(db.String(128), default='')
    ip_addr = db.Column(db.String(16), default='127.0.0.1')
    device_name = db.Column(db.String(32), default='')
    uuid = db.Column(db.String(36), default='')
    create_time = db.Column(
        db.DateTime, default=arrow.now('PRC').datetime.replace(tzinfo=None))
    serialno = db.Column(db.String(128), default='')

    def __init__(self, plate_no='-', plate_color=0, pass_time=None,
                 stat_code=0, vehicle_point_no=1, direction='1', status='1',
                 pic1='', pic2='', pic3='', pic4='', ip_addr='127.0.0.1',
                 device_name='', uuid='', create_time=None, serialno=''):
        self.plate_no = plate_no
        self.plate_color = plate_color
        self.pass_time = pass_time
        self.stat_code = stat_code
        self.vehicle_point_no = vehicle_point_no
        self.direction = direction
        self.status = status
        self.pic1 = pic1
        self.pic2 = pic2
        self.pic3 = pic3
        self.pic4 = pic4
        self.ip_addr = ip_addr
        self.device_name = device_name
        self.uuid = uuid
        self.create_time = create_time
        self.serialno = serialno
        
    def __repr__(self):
        return '<vehicle_pass2 %r>' % self.id


class DeviceState(db.Model):
    """相机设备状态"""
    __bind_key__ = 'env'
    __tablename__ = 'device_state'

    id = db.Column(db.Integer, primary_key=True)
    ip_addr = db.Column(db.String(16), default='')
    serialno = db. Column(db.String(128), default='')
    device_name = db.Column(db.String(128), default='')
    white_list = db.Column(db.String(256), default='[]')
    stat_code = db.Column(db.Integer, default=0)
    vehicle_point_no = db.Column(db.Integer, default=1)
    direction = db.Column(db.Integer, default=1)
    long = db.Column(db.Numeric(9, 6), default=0.0)
    lat = db.Column(db.Numeric(9, 6), default=0.0)
    ps = db.Column(db.String(256), default='')
    create_time = db.Column(db.DateTime, default='')
    last_modify = db.Column(db.DateTime, default='')
    update_flag = db.Column(db.Integer, default=0)
    del_flag = db.Column(db.Integer, default=0)

    def __init__(self, ip_addr='', serialno='', device_name='', white_list='[]',
                 stat_code=0, vehicle_point_no=1, direction=1, long=0.0,
                 lat=0.0, ps='', create_time='', last_modify='',
                 update_flag=0, del_flag=0):
        self.ip_addr = ip_addr
        self.serialno = serialno
        self.device_name = device_name
        self.white_list = white_list
        self.stat_code = stat_code
        self.vehicle_point_no = vehicle_point_no
        self.direction = direction
        self.long = long
        self.lat = lat
        self.ps = ps
        self.create_time = create_time
        self.last_modify = last_modify
        self.update_flag = update_flag
        self.del_flag = del_flag

    def __repr__(self):
        return '<device_state %r>' % self.id

