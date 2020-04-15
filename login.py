import requests
import cv2 as cv
from bs4 import BeautifulSoup as bs

import utils

# 各种资源的url
url_home = "http://bkjw.whu.edu.cn/"
url_image = url_home + "servlet/_33cb6c3?v=2"
url_login = url_home + "servlet/_9b11715648"
url_index = url_home + "stu/stu_index.jsp"

# 全局变量
session = requests.session()
header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}


def GetCAPTCHA(session=session, url=url_image):
    # 设置一个User-Agent, 伪装成浏览器
    # 这是第一次访问, 所以要记录cookies
    response = session.get(url=url, headers=header, stream=True)
    captcha = response.content
    cookie = response.cookies
    # 转化成图片并展示
    image = utils.Bin2Img(captcha)
    cv.imshow("title", image)
    cv.waitKey(0)
    return image, cookie


def SendPost(user, password, xdvbf, cookie, session=session, url=url_login):
    form_data = {
        "timestamp": utils.GetTimeStamp(),
        "jwb": utils.GetWHUEncode(),
        "id": user,
        "pwd": password,
        "xdvfb": xdvbf
    }
    return session.post(url, form_data, headers=header,
                        cookies=requests.utils.dict_from_cookiejar(cookie))

def GetTokenAndCookie(cookie, session=session, url=url_index):
    result = session.get(url, headers=header, cookie=cookie)
    csrf_token =


def Login(user, pwd):
    # 获取验证码
    image, cookie = GetCAPTCHA(session, url_image)
    # TODO: 给用户更多的选择
    captcha_content = input("请输入验证码: ")

    # 将密码加密后登录
    encrypted_pwd = utils.EncryptPassword(pwd)
    login = SendPost(user, encrypted_pwd, captcha_content, cookie)
    print(login.url)

    # 获取csrf_token和的登录后的cookie并返回
    login_cookie = login.cookies
    return GetTokenAndCookie(cookie=login_cookie)


if __name__ == "__main__":
    user = "2018302080181"
    password = "20000721"
    Login(user, password)
