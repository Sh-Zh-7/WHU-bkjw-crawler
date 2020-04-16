__author__ = "Sh-Zh-7"
__copyright__ = "Copyright (C) 2019 Sh-Zh-7"
__license__ = "MIT"
__email__ = "2431297348@qq.com"

import os
import json
import getpass
import argparse
from bs4 import BeautifulSoup as bs
from dao.query import Query

def ShowLessonInfo(lessons, args):
    if args.P:
        print(lessons.GetGPA())
    elif args.S:
        print(lessons.GetAverageScore())


def GetArgs():
    parser = argparse.ArgumentParser(description="您的教务系统助手", epilog="Author: WHU CS 2018级 沈之豪")
    # 登录部分
    parser.add_argument("-u", type=str, default="", help="您的学号")
    parser.add_argument("-p", type=str, default="", help="您的密码")
    # parser.add_argument("-d", "-disable-auto", help="加上这个参数后，自动进行验证码的识别")

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


def Main(args):
    if args.clear:
        if os.path.exists("./grades_table.html"):
            os.remove("./grades_table.html")
        if os.path.exists("./user_info.json"):
            os.remove("./user_info.json")
        exit(0)
    else:
        Core(args)


if __name__ == "__main__":
    Main(GetArgs())





