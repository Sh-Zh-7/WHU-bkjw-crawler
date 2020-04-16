import requests
import cv2 as cv
from bs4 import BeautifulSoup as bs

import utils

# 各种资源的url
url_home = "http://bkjw.whu.edu.cn/"
url_image = url_home + "servlet/_89ab36cec99d8d?v=2"
url_login = url_home + "servlet/_90e916fe3"
url_index = url_home + "stu/stu_index.jsp"
url_success = url_home + "servlet/../stu/stu_index.jsp"


def GetCAPTCHA(session, url=url_image):
    # 设置一个User-Agent, 伪装成浏览器
    # 这是第一次访问, 所以要记录cookies
    print(url)
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
    captcha_content = input("请输入验证码: ")
    # 将密码加密后登录
    encrypted_pwd = utils.EncryptPassword(pwd)
    login = SendPost(user, encrypted_pwd, captcha_content, cookie, session=session)
    if login.url == url_success:
        # 获取csrf_token和的登录后的cookie并返回
        login_cookie = login.cookies
        return session, login_cookie, GetToken(login_cookie, session=session)
    else:
        print("登录失败!")
        failed_content = login.text
        soup = bs(failed_content, "html.parser")
        reason = soup.select("#loginInputBox > tr:nth-child(4) > td > font")[0].get_text()
        print(reason)
        exit(0)


if __name__ == "__main__":
    user = "2018302080182"
    password = "20000721"
    Login(user, password)
