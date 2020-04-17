import requests
from bs4 import BeautifulSoup as bs

from connect import helper
from connect.url import URL


def SendPost(user, password, xdvbf, cookie, session, url=URL.form):
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


def Login(session, user, pwd, captcha, cookie):
    try:
        # 将密码加密后登录
        encrypted_pwd = helper.EncryptPassword(pwd)
        login = SendPost(user, encrypted_pwd, captcha, cookie, session=session)
        if login.url == URL.success:
            # 获取csrf_token和的登录后的cookie并返回
            login_cookie = login.cookies
            return login_cookie, GetToken(login_cookie, session=session)
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

"""
Add your login code to test,
e.g.
   if __name__ == "__main__":
    user = "123456"
    password = "654321"
    Login(user, password)
    print("登录成功") 
"""
