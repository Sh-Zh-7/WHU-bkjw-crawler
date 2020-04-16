import requests
from bs4 import BeautifulSoup as bs

from connect.captcha import *

def SendPost(user, password, xdvbf, cookie, session, url=URL.form):
    form_data = {
        "timestamp": helper.GetTimeStamp(),
        "jwb": helper.GetWHUEncode(),
        "id": user,
        "pwd": password,
        "xdvfb": xdvbf
    }
    response = session.post(url, form_data, headers=helper.header,
                            cookies=requests.utils.dict_from_cookiejar(cookie))
    response.encoding = response.apparent_encoding
    return response


def GetCSRF(text):
    soup = bs(text, "html.parser")
    csrf_tokens = {}
    divs = soup.find_all("div")
    for div in divs:
        if div.get("onclick"):
            csrf_tokens[div.get("name")] = div.get("onclick")
    return csrf_tokens


def GetToken(cookie, session, url=URL.index):
    response = session.get(url, headers=helper.header, cookies=cookie)
    response.encoding = response.apparent_encoding
    tokens = GetCSRF(response.text)
    csrf_token = tokens[None].split("'")[1].split('csrftoken=')[-1]
    return csrf_token


def Login(user, pwd):
    session = requests.session()
    try:
        # 获取验证码
        image, cookie = GetCAPTCHA(session, URL.captcha)
        captcha_content = input("请输入验证码: ")
        # 将密码加密后登录
        encrypted_pwd = helper.EncryptPassword(pwd)
        login = SendPost(user, encrypted_pwd, captcha_content, cookie, session=session)
        if login.url == URL.success:
            # 获取csrf_token和的登录后的cookie并返回
            login_cookie = login.cookies
            return session, login_cookie, GetToken(login_cookie, session=session)
        else:
            print("登录失败!")
            failed_content = login.text
            soup = bs(failed_content, "html.parser")
            reason = soup.select("#loginInputBox > tr:nth-child(4) > td > font")[0].get_text()
            print(reason)
            exit(1)
    except:
        print("未知的异常！请联系开发人员!")
        exit(1)


if __name__ == "__main__":
    user = "2018302080181"
    password = "20000721"
    Login(user, password)
    print("登录成功")
