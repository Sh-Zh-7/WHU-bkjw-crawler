import requests
import cv2 as cv
from bs4 import BeautifulSoup as bs

import utils

# 各种资源的url
url_home = "http://bkjw.whu.edu.cn/"
url_image = url_home + "servlet/_33cb6c3?v=2"
url_login = url_home + "servlet/_9b11715648"
url_index = url_home + "stu/stu_index.jsp"

def GetCAPTCHA(session, url=url_image):
    # 设置一个User-Agent, 伪装成浏览器
    # 这是第一次访问, 所以要记录cookies
    response = session.get(url=url, headers=utils.header, stream=True)
    captcha = response.content
    cookie = response.cookies
    # 转化成图片并展示
    image = utils.Bin2Img(captcha)
    cv.imshow("title", image)
    cv.waitKey(0)
    return image, cookie


def SendPost(user, password, xdvbf, cookie, session, url=url_login):
    form_data = {
        "timestamp": utils.GetTimeStamp(),
        "jwb": utils.GetWHUEncode(),
        "id": user,
        "pwd": password,
        "xdvfb": xdvbf
    }
    response = session.post(url, form_data, headers=utils.header,
                            cookies=requests.utils.dict_from_cookiejar(cookie))
    response.encoding = response.apparent_encoding
    return response


def GetCSRF(text):
    soup = bs(text, 'html.parser')
    c = {}
    for r in soup.find_all('div'):
        if r.get('onclick') is not None:
            c[r.get('name')] = r.get('onclick')
    return c


def GetToken(cookie, session, url=url_index):
    response = session.get(url, headers=utils.header, cookies=cookie)
    response.encoding = response.apparent_encoding
    tokens = GetCSRF(response.text)
    csrf_token = tokens[None].split("'")[1].split('csrftoken=')[-1]
    return csrf_token


def Login(user, pwd):
    session = requests.session()
    # 获取验证码
    image, cookie = GetCAPTCHA(session, url_image)
    # TODO: 给用户更多的选择
    captcha_content = input("请输入验证码: ")

    # 将密码加密后登录
    encrypted_pwd = utils.EncryptPassword(pwd)
    login = SendPost(user, encrypted_pwd, captcha_content, cookie, session=session)
    print(login.url)

    # 获取csrf_token和的登录后的cookie并返回
    login_cookie = login.cookies
    return session, login_cookie, GetToken(login_cookie, session=session)


if __name__ == "__main__":
    user = "2018302080181"
    password = "20000721"
    Login(user, password)
