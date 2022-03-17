from .jwt import *
from utils.format import ok_msg_with, err_msg
from config import Config
from .aes import AESCipher
from  app.api.args import  *
import logging

def views_jwt_decode(args):
  head, body = decode_jwt(args.get('decode'))
  return ok_msg_with({
      "head": head,
      "body": body
  })

def views_aes(args: HashSaltArgs):
  aes = None
  if args.get("salt"):
    aes = AESCipher(args.get("salt"))
  else:
    aes = AESCipher(Config.SECRET_KEY)
  
  ret = []
  try:
    if args.get("encrypt"): # 加码
      for item in args.get("data"):
        inData = {}
        for key,value in item.items():
          if key in args.get("skips"):
            inData[key] = value
            continue
          inData[key] = aes.encrypt(value)
        ret.append(inData)
    else: # 解码
      for item in args.get("data"):
        inData = {}
        for key,value in item.items():
          if key in args.get("skips"):
            inData[key] = value
            continue
          inData[key] = aes.decrypt(value)
        ret.append(inData)
    return ok_msg_with(ret)
  except ValueError as e:
    logging.error(e)
    return err_msg(1000, "加密解密格式错误，检查是否有中文等非法字符.")
