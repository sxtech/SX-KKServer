# -*- coding: utf-8 -*-
import arrow

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
    uuid = db.Column(db.String(32), default='')
    create_time = db.Column(
        db.DateTime, default=arrow.now('PRC').datetime.replace(tzinfo=None))

    def __init__(self, plate_no='-', plate_color='1', pass_time=None,
                 site_id=1, direction='1', status='1', pic1='', pic2='',
                 pic3='', pic4='', ip_addr='', device_name='', uuid='', create_time=None):
        self.plate_no = plate_no
        if pass_time is None:
            self.pass_time = arrow.now('PRC').datetime.replace(tzinfo=None)
        else:
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
        if create_time is None:
            self.create_time = arrow.now('PRC').datetime.replace(tzinfo=None)
        else:
            self.create_time = create_time
        
    def __repr__(self):
        return '<vehicle_pass %r>' % self.id

class DeviceState(db.Model):
    """相机设备状态"""
    __bind_key__ = 'env'
    __tablename__ = 'device_state'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(16), default='')
    serialno = db. Column(db.String(128), default='')
    white_list = db.Column(db.String(256), default='[]')
    last_modify = db.Column(
        db.DateTime, default=arrow.now('PRC').datetime.replace(tzinfo=None))
    update_flag = db.Column(db.Integer, default=0)

    def __init__(self, ip='', serialno='', white_list='[]',
                 last_modify=None, update_flag=0):
        self.ip = ip
        self.serialno = serialno
        self.white_list = white_list
        if last_modify is None:
            self.last_modify = arrow.now('PRC').datetime.replace(tzinfo=None)
        else:
            self.last_modify = last_modify
        self.update_flag = update_flag

    def __repr__(self):
        return '<device_state %r>' % self.id

class VehicleManage(db.Model):
    """白名单管理"""
    __tablename__ = 'vehicle_manage'

    id = db.Column(db.Integer, primary_key=True)
    plate_no = db.Column(db.String(32), default='')
    plate_color = db. Column(db.String(8), default='')
    company = db.Column(db.String(128), default='')
    person = db.Column(db.String(128), default='')
    phone_no = db.Column(db.String(128), default='')
    del_flag = db.Column(db.Integer, default=0)

    def __init__(self, plate_no='', plate_color='', company='',
                 person='', phone_no='', del_flag=0):
        self.plate_no = plate_no
        self.plate_color =  plate_color
        self.company = company
        self.person = person
        self.phone_no = phone_no
        self.del_flag = del_flag

    def __repr__(self):
        return '<vehicle_manage %r>' % self.id
