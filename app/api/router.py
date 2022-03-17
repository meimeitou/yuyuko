from flask import Blueprint, jsonify
from .qrmaster.views import *
from .tools.views import *
from webargs.flaskparser import use_args
from .args import *
import requests

api = Blueprint(
    'api',
    __name__,
    template_folder='templates',
    url_prefix="/api",
    static_folder='static')


@api.route('/wx/code')
def api_wxcode():
    code = request.args.get("code")
    payload = {
        "appid": "id",
        "secret": "sec",
        "js_code": code,
        "grant_type": "authorization_code"
    }
    res = requests.get(
        "https://api.weixin.qq.com/sns/jscode2session", params=payload)
    try:
        data = res.json()
        print(data)
    except Exception as e:
        print(e)
    return jsonify({"errcode": 0, "errmsg": "", "data": "token@1234"})


@api.route('/wx/userinfo')
def api_wx_user():
    if 'token' not in request.headers:
        return jsonify({"errcode": 401, "errmsg": "token not exist", "data": ""})
    token = request.headers['token']
    if token != "token@1234":
        return jsonify({"errcode": 401, "errmsg": "token error", "data": ""})
    return jsonify({"errcode": 0, "errmsg": "", "data": "xxx@xxx.cn"})


@api.route('/ping', methods=['POST', 'GET'])
def ping():
    return "Pong"


@api.route('/qrdecode', methods=['POST', 'GET'])
def api_qrdecode():
    return views_api_qrdecode()


@api.route('/qrencode', methods=['GET'])
@use_args(QrEncodeArgs, location="query")
def api_qrencode(args):
    return views_api_qrencode(args)


@api.route('/jwtdecode', methods=['GET'])
@use_args(JwtDecodeArgs, location="query")
def api_jwt_decode(args):
    return views_jwt_decode(args)

@api.route('/aes', methods=['GET', 'POST'])
@use_args(HashSaltArgs, location="json")
def api_hash_salt(args:HashSaltArgs):
    '''
    aes加密/解密
    '''
    return views_aes(args)

@api.route('/curl', methods=['POST'])
@use_args(CurlArgs, location="json")
def api_curl(args):
    logging.info(f'''
    {args.get("url")}
    {args.get("methods")}
    {args.get("params")}
    {args.get("cookies")}
    {args.get("headers")}
    {args.get("bodyType")}
    {args.get('textBody')}
    ''')
    if 'body' not in request.files:
        return 'no file'
    return 'ok'
