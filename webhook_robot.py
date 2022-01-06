import base64
import hashlib
import hmac
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
import hashlib
import base64
from Crypto.Cipher import AES


from configs import *

timestamp = int(datetime.now().timestamp())


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def decrypt_string(self, enc):
        enc = base64.b64decode(enc)
        return self.decrypt(enc).decode('utf8')


class BaseBot:

    def __init__(self):
        self.session = requests.Session()
        # 设置重试
        self.session.mount('https://', HTTPAdapter(
            max_retries=Retry(total=5, method_whitelist=frozenset(['GET', 'POST']))))

    def gen_sign(self, secret):
        # 拼接时间戳以及签名校验
        string_to_sign = '{}\n{}'.format(timestamp, secret)

        # 使用 HMAC-SHA256 进行加密
        hmac_code = hmac.new(
            string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
        ).digest()

        # 对结果进行 base64 编码
        sign = base64.b64encode(hmac_code).decode('utf-8')

        return sign


class BaseMsgBot(BaseBot):
    def __init__(self):
        super(BaseMsgBot, self).__init__()

    def send_base_msg(self, msg):
        """
        发送基本的信息
        :return:
        """
        sign = self.gen_sign(WEBHOOK_SECRET)
        params = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "text",
            "content": {"text": msg}
        }

        resp = requests.post(WEBHOOK_URL, json=params)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") and result.get("code") != 0:
            print(f"发送失败：{result['msg']}")
            return
        print("消息发送成功")


if __name__ == '__main__':
    BaseMsgBot().send_base_msg('懒编程YYDS!')
