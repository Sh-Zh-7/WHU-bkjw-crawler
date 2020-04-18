"""
    根据教务系统首页的内容获取各种资源的URI
    这样就不用担心servlet变来变去的情况
"""

import requests
from bs4 import BeautifulSoup as bs

from connect import helper

class URL:
    # 静态代码块
    home = "http://bkjw.whu.edu.cn/"
    # 获得首页的内容
    __session = requests.session()
    __request = __session.get(home, headers=helper.header)
    __home_page_content = __request.text
    # 爬取验证码和表单验证的uri
    __soup = bs(__home_page_content, "html.parser")
    __form_servlet = __soup.select("#loginBox > form")[0].get("action")
    __img_list__ = __soup.select("#loginInputBox > tr:nth-child(3) > td:nth-child(2) > div:nth-child(2)")[0]
    __target_img__ = __img_list__.find("img", attrs={"name": "sleep"})
    __captcha_servlet = __target_img__.get("src")

    prefix = home[:-1]
    # 具体的各个url
    captcha = prefix + __captcha_servlet
    form = prefix + __form_servlet
    index = home + "stu/stu_index.jsp"
    success = home + "servlet/../stu/stu_index.jsp"

