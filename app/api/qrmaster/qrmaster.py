import cv2
import numpy as np
from .amzqr import run
import os

def qrdecode(filedata: bytes) -> str:
    img = np.asarray(bytearray(filedata), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    qrCodeDetector = cv2.QRCodeDetector()
    decodedText, points, _ = qrCodeDetector.detectAndDecode(img)
    if points is None:
        return "二维码识别失败"
    return decodedText

# 生成二维码
def qrencode(text: str):
    return  run(
        text,
        version=1,
        level='H',
        picture=None,
        colorized=False,
        contrast=1.0,
        brightness=1.0,
        save_name=None,
        save_dir=os.getcwd()
    )
