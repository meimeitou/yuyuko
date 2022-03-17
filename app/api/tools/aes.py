import base64
import hashlib
# from Crypto import Rndom
from Crypto.Cipher import AES

class AESCipher(object):
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
    def encrypt(self, data):
        '''
        AES的ECB模式加密方法
        :param data:被加密字符串（明文）
        :return:密文
        '''
        # 字符串补位
        data = self._pad(data)
        cipher = AES.new(self.key, AES.MODE_ECB)
        # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
        result = cipher.encrypt(data.encode())
        encodestrs = base64.b64encode(result)
        enctext = encodestrs.decode('utf8')
        return enctext
    def decrypt(self, data):
        '''
        :param data: 加密后的数据（密文）
        :return:明文
        '''
        data = base64.b64decode(data)
        cipher = AES.new(self.key, AES.MODE_ECB)

        # 去补位
        text_decrypted = self._unpad(cipher.decrypt(data))
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted