__author__ = "Sh-Zh-7"
__copyright__ = "Copyright (C) 2019 Sh-Zh-7"
__license__ = "MIT"
__email__ = "2431297348@qq.com"

import argparse

def GetArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--uid", type=str, default="", help="您的学号")
    parser.add_argument("-p", "--password", type=str, default="", help="您的密码")
    parser.add_argument("-d", "-disable-auto", help="加上这个参数后，手动进行验证码的识别")
    args = parser.parse_args()
    return args
