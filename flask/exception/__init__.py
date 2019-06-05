#coding=utf-8

from flask import Blueprint
#创建exception对象
exception = Blueprint('exception',__name__)
from exception import exception