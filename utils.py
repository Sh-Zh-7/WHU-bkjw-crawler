import json
import hashlib
import time
import cv2 as cv
import pytesseract as tess

from PIL import Image
from io import BytesIO
from matplotlib.pyplot import imread

def Json2Dict(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def Bin2Img(bin_obj):
    return imread(BytesIO(bin_obj), "jpeg")

def GetTimeStamp():
    return str(int(time.time() * 1000))

def GetWHUEncode():
    return "%E6%AD%A6%E5%A4%A7%E6%9C%AC%E7%A7%91%E6%95%99%E5%8A%A1%E7%B3%BB%E7%BB%9F"

def EncryptPassword(pwd):
    encrypt = hashlib.md5()
    encrypt.update(pwd.encode("ASCII"))
    return encrypt.hexdigest()

def RecognizeCAPTCHA(img):
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    bin1 = cv. morphologyEx(binary, cv.MORPH_OPEN, kernel)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    out = cv.morphologyEx(bin1, cv.MORPH_OPEN, kernel)

    cv.bitwise_not(out, out)
    text_image = Image.fromarray(out)
    text = tess.image_to_string(text_image)
    return text.replace(" ", "")

if __name__ == "__main__":
    print(GetTimeStamp())

