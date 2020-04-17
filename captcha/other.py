from PIL import Image
import cv2 as cv
from io import BytesIO

from connect import helper
from connect.url import URL
from matplotlib.pyplot import imread


def ShowCAPTCHA(img):
    cv.imshow("CAPTCHA", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def GetCAPTCHA(session, url=URL.captcha):
    # 设置一个User-Agent, 伪装成浏览器
    # 这是第一次访问, 所以要记录cookies
    response = session.get(url=url, headers=helper.header, stream=True)
    captcha = response.content
    cookie = response.cookies
    image_numpy = imread(BytesIO(captcha), "jpeg")
    image = Image.fromarray(image_numpy)
    return image, cookie
