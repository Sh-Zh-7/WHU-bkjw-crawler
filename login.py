__author__ = "Sh-Zh-7"
__copyright__ = "Copyright (C) 2019 Sh-Zh-7"
__license__ = "MIT"
__email__ = "2431297348@qq.com"

import requests
import argparse
import cv2 as cv

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
    # 设置一个User-Agent, 伪装成浏览器了
    captcha = session.get(url=url, headers=header, stream=True)
    img_arr = utils.Bin2Img(captcha.content)
    cv.imshow("title", img_arr)
    cv.waitKey(0)
    # 只要访问了host, 就会给你一个cookies, 不用登录教务系统主页
    return img_arr, captcha.cookies


def Login(user, password, xdvbf, cookie, session=session, url=url_login):
    form_data = {
        "timestamp": utils.GetTimeStamp(),
        "jwb": utils.GetWHUEncode(),
        "id": user,
        "pwd": password,
        "xdvfb": xdvbf
    }
    return session.post(url, form_data, headers=header,
                        cookies=requests.utils.dict_from_cookiejar(cookie))


def GetArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--uid", type=str, default="", help="您的学号")
    parser.add_argument("-p", "--password", type=str, default="", help="您的密码")
    args = parser.parse_args()
    return args

def Main():
    user = "2018302080181"
    pwd = "20000721"
    # 获取验证码
    image, cookie = GetCAPTCHA(session, url_image)
    captcha_content = input("请输入验证码: ")
    # 将密码加密后登录
    encrypted_pwd = utils.EncryptPassword(pwd)
    print(captcha_content)
    login = Login(user, encrypted_pwd, captcha_content, cookie)
    print(login.url)


if __name__ == "__main__":
    Main()
