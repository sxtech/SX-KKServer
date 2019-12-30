# -*- coding: utf-8 -*-

class Config(object):
    # 密码 string
    SECRET_KEY = 'thefatboy'
    # 服务器名称 string
    HEADER_SERVER = 'SX-KKServer'
    # 数据库连接 string
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123123@127.0.0.1:54321/site'
    # 数据库连接 dict
    SQLALCHEMY_BINDS = {
        'env': 'mysql+pymysql://root:123123@127.0.0.1:3307/environ',
        'yc': 'mssql+pymssql://sa:123123@127.0.0.1:1433/test'
    }
    # 连接池大小 int
    #SQLALCHEMY_POOL_SIZE = 20
    # 基础路径 string
    BASE_PATH = '/home/images'
    # 基础URL路径 string
    BASE_URL_PATH = 'http://112.91.72.23:8099/images'
    # 时序数据库地址 string
    INFLUXDB_URL = 'http://localhost:8086/write?db=mz'
    # pulsar配置信息 dict
    PULSAR = {
        'url': 'pulsar://localhost:6651',
        'topic': 'persistent://yc/mz/vehicle-pass',
        'client': None,
        'producer': None
    }


class Develop(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False

