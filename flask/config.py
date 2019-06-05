#coding=utf-8

#配置
class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False




class TestingConfig(Config):
    DEBUG = True
    TESTING = True