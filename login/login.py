__author__ = "Sh-Zh-7"
__copyright__ = "Copyright (C) 2019 Sh-Zh-7"
__license__ = "MIT"
__email__ = "2431297348@qq.com"

import requests
import argparse

from login import utils

# 各种资源的url
url_prefix = "http://bkjw.whu.edu.cn/"
url_image = url_prefix + "servlet/GenImg"
url_login = url_prefix + "servlet/Login"

# 配置文件路径
captcha_path = "../config/captcha.json"
login_path = "../config/login.json"

# 全局变量
session = requests.session()

def GetCAPTCHA(session=session, url=url_image):
    http_request_header = utils.Json2Dict(captcha_path)
    captcha = session.get(url=url, headers=http_request_header).content
    img_arr = utils.Bin2Img(captcha)
    return img_arr

def Login(user, password, xdvbf, session=session, url=url_login):
    http_request_header = utils.Json2Dict(login_path)
    form_data = {
        "id": user,
        "pwd": password,
        "xdvfb": xdvbf
    }
    return session.post(url, form_data, http_request_header)

def GetArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--uid", type=str, default="", help="您的学号")
    parser.add_argument("-p", "--password", type=str, default="", help="您的密码")
    args = parser.parse_args()
    return args

def Main(args):
    image = GetCAPTCHA(session, url_image)

if __name__ == "__main__":
    # Main(GetArgs())

    # 获取验证码图片
    image = GetCAPTCHA(session, url_image)
