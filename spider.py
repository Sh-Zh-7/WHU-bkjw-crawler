from connect.helper import HTML2CSV

__author__ = "Sh-Zh-7"
__copyright__ = "Copyright (C) 2019 Sh-Zh-7"
__license__ = "MIT"
__email__ = "2431297348@qq.com"

import os
import json
import getpass
import requests
import argparse
from bs4 import BeautifulSoup as bs

# 禁止TF打印任何日志信息
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from dao.query import Query
from connect import login
from connect.grade import GetGradePageContent
from captcha import other
from captcha.recognize import RecognizeCAPTCHA


def ShowLessonInfo(lessons, args):
    if args.P:
        print(lessons.GetGPA())
    elif args.S:
        print(lessons.GetAverageScore())


def GetArgs():
    parser = argparse.ArgumentParser(description="您的教务系统助手", epilog="Author: WHU CS 2018级 沈之豪")
    # 登录部分
    parser.add_argument("-d", action="store_true", help="加上这个参数后，禁止验证码的自动识别")

    # 按照不同的需求查找
    parser.add_argument("-Y", type=str, default=0, help="查询某一学年的课程")
    parser.add_argument("-A", action="store_true", help="查询所有的课程")
    parser.add_argument("-C", type=str, default="", help="按照课程名称查找")

    # 查询成绩或者是平均分
    parser.add_argument("-S", action="store_true", help="查询课程的平均分")
    parser.add_argument("-P", action="store_true", help="查询GPA")

    # 其他
    parser.add_argument("--clear", action="store_true", help="删除所有本地存储")

    args = parser.parse_args()
    return args


def GetUsernameAndPwd():
    # 不使用mysql那种通过命令行传递用户名和密码的方式登录
    # 使用Linux的方法，在进程中要求用户给定用户名和密码
    if not os.path.exists("user_info.json"):
        username = input("请输入您的学号: ")
        password = getpass.getpass("请输入您的密码: ")
        # 持久化
        user_info = {"username": username, "password": password}
        with open("user_info.json", "w") as f:
            json.dump(user_info, f, indent=4)
    else:
        with open("user_info.json", "r") as f:
            user_info = json.load(f)
        username = user_info["username"]
        password = user_info["password"]
    return username, password


def GetCAPTCHA(session, disabled):
    target_captcha, cookie = other.GetCAPTCHA(session)
    if disabled:
        print("请根据显示的图片输入对应的验证码(关闭图片后输入)\n")
        other.ShowCAPTCHA(target_captcha)
        captcha = input("请输入验证码")
    else:
        captcha = RecognizeCAPTCHA(target_captcha)
    return captcha, cookie


def Core(args):
    with open("./grades_table.html", "r", encoding="GBK") as f:
        content = f.read()
    soup = bs(content, "lxml")
    if args.C:
        lesson_name = args.C.strip()
        lesson = Query.SelectByCname(soup, lesson_name)
        print(lesson)
    elif args.A:
        lessons = Query.SelectAll(soup)
        ShowLessonInfo(lessons, args)
    elif args.Y:
        year = args.Y.strip()
        lessons = Query.SelectByYear(soup, year)
        ShowLessonInfo(lessons, args)
    else:
        print("不明确的组合！请查阅官方文档！")


def Main(args):
    if args.clear:
        if os.path.exists("./grades_table.html"):
            os.remove("./grades_table.html")
        if os.path.exists("./user_info.json"):
            os.remove("./user_info.json")
        if os.path.exists("./grades_table.csv"):
            os.remove("./grades_table.csv")
    else:
        if not os.path.exists("./grades_table.html"):
            session = requests.session()

            username, password = GetUsernameAndPwd()
            captcha, cookie = GetCAPTCHA(session, args.d)

            login_cookie, csrf_token = login.Login(session, username, password, captcha, cookie)
            content = GetGradePageContent(session, login_cookie, csrf_token)
            with open("grades_table.html", "w", encoding="GBK") as f:
                f.write(content)
            HTML2CSV(content)
        Core(args)


if __name__ == "__main__":
    Main(GetArgs())

