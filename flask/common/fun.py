# coding=utf-8
# 公共函数
from flask import request, make_response
import random
import hashlib

import uuid

import time



def md5(src):
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()


def randInt(start, end):
    return random.randint(start, end)


def create_id():
    return str(uuid.uuid1().hex)


def time2int(format="%Y-%m-%d %H:%M:%S", strTime=''):
    timeArray = time.strptime(strTime, format)
    return int(time.mktime(timeArray))


def int2time(format="%Y-%m-%d %H:%M:%S", intTime=0):
    timeArray = time.localtime(intTime)
    otherStyleTime = time.strftime(format, timeArray)
    return otherStyleTime


def intTime():
    return int(time.time())


def funRequest():
    '''
    \获取前端上传的数据
    :return:
    '''
    jsonData = request.json
    cookies = request.cookies
    headers = request.headers

    if jsonData != None or (
            "Content-Type" in request.headers and request.headers["Content-Type"] == "application/json"):
        return jsonData

    form = request.form.to_dict()
    if "Content-Type" in request.headers and request.headers["Content-Type"] == "application/x-www-form-urlencoded":
        return form

    args = request.args.to_dict()
    formLen = 0
    if form != None:
        formLen = len(form)
    argsLen = 0
    if args != None:
        argsLen = len(args)
    if argsLen >= formLen:
        return args
    else:
        return form


#:响应处理
def funResponse(data=None, headers=None, cookies=None, redirect=None):
    '''
    响应
    :param data:  响应数据
    :param headers: 响应头
    :param cookies: 响应cookies
    :param redirect: 重定向
    :return:
    '''
    # 重定向
    if redirect:
        return redirect(redirect)
    # 获取响应
    resp = make_response()
    # 填充数据
    if data:
        resp.data = data

        # 设置请求头
    if headers:
        for key in headers:
            resp.headers[str(key)] = str(headers[key])
    # 设置cookies
    if cookies:
        for key in cookies:
            resp.set_cookie(str(key), str(cookies[key]))
    # 返回响应
    return resp
