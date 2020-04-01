from flask import Blueprint, request, jsonify, url_for, g, current_app
from app.utils.util import route, Redis
from app.utils.code import ResponseCode
from app.utils.response import ResMsg
from app.models.model import WebInfo
from app.utils.core import db

import logging

bp = Blueprint("webinfo", __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

def init_webinfo():
    data = {
      "title": "Star Here Project Driven博客",
      "keyword": "技术博客",
      "description": None,
      "personinfo": None,
      "github": "htts://github.com/etscript",
      "icp": "粤ICP备19044398号",
      "weixin": "JhHaBjBbrDzDgN22VYXkJTmPnhsJB0mOVrS1eNWa.jpeg",
      "zhifubao": "GruK3LNCt6MdZQ1CZ8MJZqv27wDN7sMNadtzKS7X.jpeg",
      "qq": "407833710",
      "phone": None,
      "email": "etscript@163.com",
      "startTime": "2020-01-01"
    }
    webinfo = WebInfo()
    webinfo.create_from_dict(data)
    db.session.add(webinfo)
    db.session.commit()
    return data

@route(bp, '/webinfo/set', methods=['POST'])
def set_webinfo():
    '''修改网站信息'''
    data = request.get_json()
    if not data:
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data
    
    id = data["id"]
    webinfo = WebInfo.query.get_or_404(id)
    
    webinfo.create_from_dict(data)
    db.session.commit()
    return {
            'code': 200,
            'message': '网站信息修改成功！',
            'status': 'success'
        }

@route(bp, '/webinfo/read', methods=['GET'])
def get_webinfo():
    try:
      webinfo = WebInfo.query.get_or_404(1)
    except:
      data = init_webinfo()
      return {
        "status": "success",
        "code": 200,
        "data":data}
    data = webinfo.to_dict()
    return {
      "status": "success",
      "code": 200,
      "data": data}






