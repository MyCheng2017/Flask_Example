# coding=utf-8
from . import example
from flask import abort, current_app
import traceback
from common import fun
from dao.Model import Model
import common.status as status
import json

table = "example"


@example.route('/list', methods=['POST', 'GET'])
def list_user():
    try:
        res = '{"status": %s, "data": "%s","msg":"获取用户列表失败！"}' % (status.FAIL, '')
        row = Model(table).select()
        if row:
            res = '{"status": %s, "data": %s}' % (status.SUCCESS, json.dumps(row))
        return fun.funResponse(res)
    except Exception:
        current_app.logger.error(traceback.format_exc())
        abort(500)


@example.route('/add', methods=['POST', 'GET'])
def add_user():
    try:
        res = '{"status": %s, "data": "%s","msg":"增加用户失败！"}' % (status.FAIL, '')
        form = fun.funRequest()
        row = Model(table).addData(form).add()
        if row:
            res = '{"status": %s, "data": %s,"msg":"增加成功！"}' % (status.SUCCESS, json.dumps(row))
        return fun.funResponse(res)
    except Exception:
        current_app.logger.error(traceback.format_exc())
        current_app.logger.error(form)
        abort(500)
