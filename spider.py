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
from connect.helper import HTML2CSV
from dao.lesson import LessonArray


def ShowLessonInfo(lessons, args):
    try:
        if args.G:
            print(lessons.GetGPA())
        elif args.S:
            print(lessons.GetAverageScore())
        elif args.W:
            print(lessons.GetWeightedScore())
        elif args.T:
            print(lessons.GetTotalPoint())
        elif args.print:
            print(lessons)
        else:
            print("请输入您想查询的信息：GPA？平均分？加权平均分？总学分？")
    except:
        print("未能查询到课程，请检查您的查询条件")


def GetArgs():
    parser = argparse.ArgumentParser(description="您的教务系统助手", epilog="Author: WHU CS 2018级 沈之豪")
    # 查询条件
    parser.add_argument("-A", action="store_true", help="查询所有的课程")
    parser.add_argument("-Y", type=str, default=0, help="查询某一学年的课程")
    parser.add_argument("-C", type=str, default="", help="按照课程名称查找")
    parser.add_argument("-K", type=str, default="",
                        choices=["GB", "GX", "ZB", "ZX", "B", "X"], help="按照课程的种类查找")

    # 查询需求
    requirement = parser.add_mutually_exclusive_group()
    requirement.add_argument("-S", action="store_true", help="查询课程的平均分")
    requirement.add_argument("-G", action="store_true", help="查询GPA")
    requirement.add_argument("-W", action="store_true", help="查询以学分为权的平均分")
    requirement.add_argument("-T", action="store_true", help="查询总学分")
    requirement.add_argument("--print", action="store_true", help="打印所有课程信息")

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


def GetCAPTCHA(session):
    target_captcha, cookie = other.GetCAPTCHA(session)
    captcha = RecognizeCAPTCHA(target_captcha)
    return captcha, cookie


def Core(args):
    with open("./grades_table.html", "r", encoding="GBK") as f:
        content = f.read()
    soup = bs(content, "html.parser")
    table_rows = soup.select("body > table > tr")
    lessons = LessonArray(table_rows)

    if args.C:
        try:
            lesson_name = args.C.strip()
            lesson = Query.SelectByCname(lessons, lesson_name)
            print(lesson)
        except:
            print("未能查询到课程，请检查您的查询条件")
            exit(0)
    elif args.K or args.Y or args.A:
        if args.K:
            kind = args.K.strip()
            lessons = Query.SelectByKind(lessons, kind)
        if args.Y:
            year = args.Y.strip()
            lessons = Query.SelectByYear(lessons, year)
        ShowLessonInfo(lessons, args)
    else:
        print("不明确的组合！请查阅官方文档！https://github.com/Sh-Zh-7/WHU-bkjw-crawler")


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
            captcha, cookie = GetCAPTCHA(session)

            login_cookie, csrf_token = login.Login(session, username, password, captcha, cookie)
            content = GetGradePageContent(session, login_cookie, csrf_token)
            with open("grades_table.html", "w", encoding="GBK") as f:
                f.write(content)
            HTML2CSV(content)
        Core(args)


if __name__ == "__main__":
    Main(GetArgs())
