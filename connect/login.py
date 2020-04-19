"""
    登录您的教务系统账号
"""

import requests
from bs4 import BeautifulSoup as bs

from connect import helper
from connect.url import URL


def GetToken(cookie, session, url=URL.index):
    """
    获取csrf token 后面有用
    :param cookie: 之前访问留下的cookie
    :param session: 全局唯一的session
    :param url: 向哪一个资源发送请求
    :return: 经过解析的csrf token
    """
    response = session.get(url, headers=helper.header, cookies=cookie)
    response.encoding = response.apparent_encoding
    tokens = GetCSRF(response.text)
    csrf_token = tokens[None].split("'")[1].split('csrftoken=')[-1]
    return csrf_token


def GetCSRF(text):
    """
    从response中解析出csrf token
    :param text: response的内容
    :return: csrf token
    """
    soup = bs(text, "html.parser")
    csrf_tokens = {}
    divs = soup.find_all("div")
    for div in divs:
        if div.get("onclick"):
            csrf_tokens[div.get("name")] = div.get("onclick")
    return csrf_tokens


def SendPost(user, password, xdvbf, cookie, session, url=URL.form):
    """
    根据之前获得的信息，发送请求
    :param user: 学号
    :param password: 密码
    :param xdvbf: 验证码内容
    :param cookie: 之前访问获得的cookie
    :param session: 全局唯一的session
    :param url: 向哪个资源发送请求
    :return: response
    """
    form_data = {
        "timestamp": helper.time_stamp,
        "jwb": helper.jwb,
        "id": user,
        "pwd": password,
        "xdvfb": xdvbf
    }
    response = session.post(url, form_data, headers=helper.header,
                            cookies=requests.utils.dict_from_cookiejar(cookie))
    response.encoding = response.apparent_encoding
    return response


def Login(session, user, pwd, captcha, cookie):
    """
    根据之前获得的信息，登录账号
    除此之外还包括登录失败的处理
    :param session: 全局唯一的session
    :param user: 学号
    :param pwd: 密码
    :param captcha: 验证码的字符串形式
    :param cookie: 之前访问获得的cookie
    :return: 登录后的cookie和csrf token
    """
    try:
        # 将密码加密后登录
        encrypted_pwd = helper.EncryptPassword(pwd)
        login = SendPost(user, encrypted_pwd, captcha, cookie, session=session)
        if login.url == URL.success:
            # 获取csrf_token和的登录后的cookie并返回
            login_cookie = login.cookies
            return login_cookie, GetToken(login_cookie, session=session)
        else:
            failed_content = login.text
            soup = bs(failed_content, "html.parser")
            reason = soup.select("#loginInputBox > tr:nth-child(4) > td > font")[0].get_text()
            print(reason)
            # 直接exit会抛出一个异常
            exit(0)
    except SystemExit:
        pass
    except:
        print("未知的异常！请联系开发人员!")
        exit()

"""
Add your login code to test,
e.g.
   if __name__ == "__main__":
    user = "123456"
    password = "654321"
    Login(user, password)
    print("登录成功") 
"""
