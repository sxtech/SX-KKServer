# -*- coding: utf-8 -*-
import json

import arrow

from app import db, logger, access_logger
from app.models import *


def get_white_list():
    white_list = VehicleManage.query.all()
    #print(white_list)
    #return 0
    w = {
        'addWhiteList': {
            'add_data': []
        }
    }
    n = arrow.now('PRC')
    st = n.format('YYYYMMDDHHmmss')
    et = n.shift(months=3).format('YYYYMMDDHHmmss')
    print(st, et)
    for i in white_list:
        info = {
            'carnum': i.plate_no,
            'startime': st,
            'endtime': et
        }
        w['addWhiteList']['add_data'].append(info)
    return w

if __name__ == '__main__':
    r = get_white_list()
    logger.info(json.dumps(r, ensure_ascii=False).encode("gbk"))

