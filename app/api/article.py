from flask import Blueprint, request, jsonify, url_for, g, current_app
from app.utils.core import db
from app.models.model import Haowen
from app.utils.auth import Auth, login_required
from app.utils.util import route, Redis
from app.utils.code import ResponseCode
from app.utils.response import ResMsg
import logging
import json
import upyun
import os

bp = Blueprint("article", __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

@route(bp, '/ad/', methods=['POST'])
def get_ad():
    ad = [
    {
      "id": 11,
      "title": "101",
      "url": "FP8GzAsTWpGrpezKY317SFOUS5gvwexulcjEmKJS.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:30:38"
    },
    {
      "id": 12,
      "title": "102",
      "url": "6d2ptD5Erd1uIEMYXl2nwpEMRdHibon6O6enbF2j.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:31:07"
    },
    {
      "id": 13,
      "title": "103",
      "url": "EOurPnsdL8FMsKvZVRwVEhNsCpLuqLTJLVeeONhw.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:31:23"
    },
    {
      "id": 14,
      "title": "104",
      "url": "gyGhPcNUggbKPHntFWkwli1AvZjvPtGBUGjZizhj.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:31:35"
    },
    {
      "id": 15,
      "title": "105",
      "url": "ZO17jMqTewXJWJAskA3kpP9PuliZXxm1jdB76xH3.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:31:45"
    },
    {
      "id": 16,
      "title": "106",
      "url": "adaII5rhUZfeP2dApEbP0QHYIiPRgI3bCIl8YjCO.jpeg",
      "type": "banner",
      "created_at": "2019-08-09 20:32:01"
    }
  ]
    return ResMsg(data=ad).data

@route(bp, '/article/classify', methods=['GET'])
def get_article_classify():
    classify = [
    {
      "name": "前端",
      "tags": {
        "0": "javascript",
        "1": "HTML5",
        "3": "vue",
        "7": "react",
        "12": "sapper",
        "13": "svelte",
        "16": "axios",
        "18": "vuex",
        "21": "vue-cli",
        "22": "小程序",
        "26": "面试",
        "27": "算法题",
        "29": "回流",
        "30": "重绘",
        "31": "虚拟dom",
        "32": "数独游戏"
      }
    },
    {
      "name": "后端",
      "tags": {
        "0": "python",
        "6": "laravel",
        "15": "go",
        "16": "C++",
        "21": "php",
        "25": "node",
        "28": "redis",
        "31": "echo",
        "37": "gin",
        "40": "qt"
      }
    },
    {
      "name": "工具",
      "tags": {
        "0": "git",
        "2": "Grunt",
        "3": "Gulp",
        "5": "webpack",
        "6": "markdown",
        "7": "OpenCV",
        "8": "ffmpeg",
        "11": "vs2017",
        "12": "Travis CI",
        "13": "mac",
        "14": "pdf",
        "15": "docker",
        "16": "rollup",
        "17": "C++",
        "18": "外挂",
        "22": "postman"
      }
    },
    {
      "name": "比特币",
      "tags": [
        "比特币"
      ]
    },
    {
      "name": "脚本",
      "tags": [
        "pdf",
        "python"
      ]
    }
  ]
    return ResMsg(data=classify).data

@route(bp, '/article/', methods=['POST'])
# @token_auth.login_required
# @permission_required(Permission.WRITE)
def get_article():
    '''获取一篇新文章'''
    data = request.get_json()
    if not data.get('id'):
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data
    id = data.get('id')
    if id:
        haowen = Haowen.query.get_or_404(id)
        data = haowen.to_dict(False, False, True, True)
    return ResMsg(data=data).data

@route(bp, '/article/add', methods=['POST'])
def add_article():
    '''添加一篇新文章'''
    data = request.get_json()
    if not data:
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data

    haowen = Haowen()
    haowen.houtai_create_from_dict(data)
    
    db.session.add(haowen)
    db.session.commit()
    return ResMsg(message='文章添加成功！').data

@route(bp, '/article/edit', methods=['POST'])
def edit_article():
    '''修改一篇新文章'''
    data = request.get_json()
    if not data:
        code = ResponseCode.InvalidParameter
        data = 'You must post JSON data.'
        return ResMsg(code=code, data=data).data

    id = data["id"]
    haowen = Haowen.query.get_or_404(id)
    
    haowen.houtai_create_from_dict(data)
    db.session.commit()
    return ResMsg(message='文章修改成功！').data

@route(bp, '/article/list/', methods=['POST'])
def get_articles():
    '''返回文章集合，分页'''
    data = request.get_json()
    # page = request.args.get('page', 1, type=int)
    page = data['page']
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    # Haowen.query.order_by(Haowen.timestamp.desc()).filter(Haowen.down==True)
    haowen = Haowen.query.order_by(Haowen.top.desc(),Haowen.timestamp.desc())
    if not data.get('all'):
        data = Haowen.to_web_dict(haowen.filter(Haowen.down==False), \
            page, per_page,'article.get_articles')
    else:
        data = Haowen.to_web_dict(haowen, page, per_page,'article.get_articles')
    
    ret = {
            "current_page": data["_meta"]["page"],
            "first_page_url": "http://api.golang365.com/api/v2/article/list?page=1",
            "from": 1,
            "last_page": data["_meta"]["total_pages"],
            "last_page_url": "http://api.golang365.com/api/v2/article/list?page=9",
            "next_page_url": "http://api.golang365.com/api/v2/article/list?page=2",
            "path": "http://api.golang365.com/api/v2/article/list",
            "per_page": 6,
            "prev_page_url": None,
            "to": 6,
            "total": data["_meta"]["total_items"]}
    ret["data"] = data["items"]

    return ResMsg(data=ret).data

@route(bp, '/article/delete', methods=['POST'])
# @token_auth.login_required
def delete_article():
    '''下架一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    # db.session.delete(haowen)
    haowen.make_down()
    db.session.commit()
    return ResMsg(message='文章下架成功！').data

@route(bp,'/article/remove', methods=['POST'])
# @token_auth.login_required
def remove_article():
    '''删除一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    db.session.delete(haowen)
    db.session.commit()
    return {'code':200,'status':'success','message':'彻底删除成功'}

@route(bp, '/article/restored', methods=['POST'])
# @token_auth.login_required
def restored_article():
    '''恢复一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    haowen.make_restored()
    db.session.commit()
    return ResMsg(message='文章恢复成功！').data

@route(bp, '/article/top', methods=['POST'])
# @token_auth.login_required
def top_article():
    '''置顶一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    # db.session.delete(haowen)
    haowen.make_top()
    db.session.commit()
    return ResMsg(message='文章置顶成功！').data

@route(bp, '/article/untop', methods=['POST'])
# @token_auth.login_required
def untop_article():
    '''取消置顶一篇文章'''
    id = request.get_json()["id"]
    haowen = Haowen.query.get_or_404(id)
    # db.session.delete(haowen)
    haowen.make_untop()
    db.session.commit()
    return ResMsg(message='文章取消置顶成功！').data




