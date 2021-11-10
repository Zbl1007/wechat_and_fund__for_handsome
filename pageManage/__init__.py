from flask import Blueprint

pageManage=Blueprint('pageManage',__name__, url_prefix='/wxTimeMachine')

from . import bind
