__author__ = "Sh-Zh-7"
__copyright__ = "Copyright (C) 2019 Sh-Zh-7"
__license__ = "MIT"
__email__ = "2431297348@qq.com"

import os
import json
import getpass
import argparse


def GetArgs():
    parser = argparse.ArgumentParser()
    # TODO: 加上持久化root和password
    parser.add_argument("-u", "--uid", type=str, default="", help="您的学号")
    parser.add_argument("-p", "--password", type=str, default="", help="您的密码")
    parser.add_argument("-d", "-disable-auto", help="加上这个参数后，手动进行验证码的识别")
    args = parser.parse_args()
    return args

# def Main(args):

if __name__ == "__main__":
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





