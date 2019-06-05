# coding=utf-8

from flask import Blueprint

# example
example = Blueprint('example', __name__)
from . import user
