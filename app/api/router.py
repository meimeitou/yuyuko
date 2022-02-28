from flask import Blueprint
from .qrmaster.views import *
from .tools.views import  *
from webargs.flaskparser import use_args
from .args import *

api = Blueprint(
    'api',
    __name__,
    template_folder='templates',
    url_prefix="/api",
    static_folder='static')

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

@api.route('/curl', methods=['POST'])
@use_args(CurlArgs, location="form")
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
