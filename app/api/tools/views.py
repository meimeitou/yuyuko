from .jwt import *
from utils.format import ok_msg_with

def views_jwt_decode(args):
  head, body = decode_jwt(args.get('decode'))
  return ok_msg_with({
      "head": head,
      "body": body
  })
