#coding=utf-8
#统一异常处理
from . import exception
from flask import request, make_response
import traceback

@exception.app_errorhandler(500)
def exception_500(err):
    resp = make_response()
    resp.status_code = 200
    resp.data = '{"status":500,"data":"","msg":"服务器无法响应"}'
    return resp

