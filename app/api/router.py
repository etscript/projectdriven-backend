from app.api.api_test import bp as bp_api_test
from app.api.services import ArticleAPI
from app.api.tianyancha import bp as tianyancha
from app.api.wxusers import bp as wxusers
from app.api.article import bp as article
from app.api.webinfo import bp as webinfo
from app.api.image import bp as image

router = [
    bp_api_test,  # 接口测试
    ArticleAPI,  # 自定义MethodView
    wxusers,
    tianyancha,
    article,
    webinfo,
    image,
]
