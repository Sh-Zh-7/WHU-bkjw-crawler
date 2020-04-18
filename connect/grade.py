"""
    爬取成绩页面
"""


import datetime

import requests
from connect import helper

# 建立int类型的星期到字符串的映射
week_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
# 全局常量
grade_page_url = 'http://bkjw.whu.edu.cn/servlet/Svlt_QueryStuScore?' \
                 'csrftoken={}&year=0&term=&learnType=&scoreFlag=0&' \
                 't={}%20{}%20{}%20{}%20{}%20GMT+0800%20(%D6%D0%B9%FA%B1%EA%D7%BC%CA%B1%BC%E4)'


def GetGradePageUrl(csrf_token):
    """
    获取成绩也是需要URL的
    :param csrf_token
    :return: 被赋值过的URL
    """
    now = datetime.datetime.now()
    # 获取当前时间
    weekday = week_map[now.weekday()]
    month = month_map[now.month]
    day = now.day
    year = now.year
    time = now.strftime("%H:%M:%S")
    url = grade_page_url.format(csrf_token, weekday, month, day, year, time)
    return url


def GetGradePageContent(session, cookie, csrf_token):
    """
    下载成绩页面的HTML
    :param session: 全局唯一的session
    :param cookie: 之前访问得到的cookie
    :param csrf_token
    :return: HTML
    """
    target_url = GetGradePageUrl(csrf_token)
    response = session.get(target_url, headers=helper.header, cookies=requests.utils.dict_from_cookiejar(cookie))
    response.encoding = response.apparent_encoding  # 推断出编码方式
    return response.text

