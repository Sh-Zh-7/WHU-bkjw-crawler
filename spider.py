__author__ = "Sh-Zh-7"
__copyright__ = "Copyright (C) 2019 Sh-Zh-7"
__license__ = "MIT"
__email__ = "2431297348@qq.com"

import os
import json
import time
import getpass
import requests
import argparse
import warnings
from bs4 import BeautifulSoup as bs

# 禁止任何报错
warnings.filterwarnings("ignore")
# 禁止TF打印任何日志信息
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from dao.query import Query
from connect import login
from connect.grade import GetGradePageContent
from captcha import other
from captcha.recognize import RecognizeCAPTCHA
from connect.helper import HTML2CSV, CaptchaException, OtherException
from dao.lesson import LessonArray

max_try_time = 2


def Core(args):
    """
    根据不同的命令行参数作出不同的动作
    大部分情况下都在选择符合条件的课程
    """
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


def ShowLessonInfo(lessons, args):
    """
    根据课程和目标信息打印最后的结果
    :param lessons: 用户选择的课程集合
    :param args: 需要查询哪些信息（GPA，平均分，加权平均分，总学分）
    """
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


def GetUsernameAndPwd():
    """
    根据用户的输入或者本地的存储返回学号和密码
    """
    # 不使用mysql那种通过命令行传递用户名和密码的方式登录
    # 使用Linux的方法，在进程中要求用户给定用户名和密码
    if not os.path.exists("user_info.json"):
        username = input("请输入您的学号: ")
        password = getpass.getpass("请输入您的密码: ")
        print()
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
    """
    获取验证码
    :param session: 全局唯一的回话对象
    :return: 验证码结果的字符串形式，第一次访问教务系统得到的cookie
    """
    target_captcha, cookie = other.GetCAPTCHA(session)
    captcha = RecognizeCAPTCHA(target_captcha)
    return captcha, cookie


def GetArgs():
    """
    解析用户输入的命令行参数
    """
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

            # 循环登录
            success = False
            try_time = 0
            while not success and try_time <= max_try_time:
                try:
                    try_time += 1
                    captcha, cookie = GetCAPTCHA(session)
                    login_cookie, csrf_token = login.Login(session, username, password, captcha, cookie)
                    success = True
                except CaptchaException:
                    print("验证码错误")
                    print("重试中.....")
                    time.sleep(5)
                except OtherException as e:
                    print(e.msg)
                    # 方便用户进行重新登录
                    if e.msg == "用户名/密码错误":
                        os.remove("./user_info.json")
                    exit(0)
            if try_time > max_try_time:
                print("\n您就是非洲人? 请重试")
                exit(0)

            content = GetGradePageContent(session, login_cookie, csrf_token)
            with open("grades_table.html", "w", encoding="GBK") as f:
                f.write(content)
            HTML2CSV(content)
        Core(args)


if __name__ == "__main__":
    Main(GetArgs())

