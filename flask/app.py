# coding=utf-8
# ：程序入口
from flask import Flask, g
import logging
from logging.handlers import TimedRotatingFileHandler
# 处理python版本编码问题
import sys
if int(sys.version[0]) <= 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

# ：创建实例
app = Flask(__name__)

# ：读取配置
#app.config.from_object('config.ProductionConfig')
#app.config.from_object('config.TestingConfig')
app.config.from_object('config.DevelopmentConfig')
from exception import exception

from example import example

import os

#: 注册蓝图，设置url
app.register_blueprint(exception, url_prefix='/error')

app.register_blueprint(example, url_prefix='/example')


# ：关闭数据库连接
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


import io


#:前后端整合后的入口页
@app.route('/')
def index():
    ret = ""
    if os.path.isfile("./index.html"):
        f = io.open('./index.html', encoding='utf-8')
        ret = f.read()
        f.close()
    return ret


# ：启动应用
if __name__ == '__main__':
    logging_format = logging.Formatter(
        '[%(asctime)s][ %(levelname)s ](%(filename)s| %(funcName)s:%(lineno)s): %(message)s')
    handler = TimedRotatingFileHandler(filename="logs/sys.log", when="D", encoding="UTF-8", delay=True)
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=7099)
