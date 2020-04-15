import requests
import datetime
from bs4 import BeautifulSoup as bs

import login
from query import Query
import utils

# 建立int类型的星期到字符串的映射
week_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
# 全局常量
grade_page_url = 'http://bkjw.whu.edu.cn/servlet/Svlt_QueryStuScore?' \
                 'csrftoken={}&year=0&term=&learnType=&scoreFlag=0&' \
                 't={}%20{}%20{}%20{}%20{}%20GMT+0800%20(%D6%D0%B9%FA%B1%EA%D7%BC%CA%B1%BC%E4)'


def GetGradePageUrl(csrf_token):
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
    target_url = GetGradePageUrl(csrf_token)
    response = session.get(target_url, headers=utils.header, cookies=requests.utils.dict_from_cookiejar(cookie))
    response.encoding = response.apparent_encoding  # 推断出编码方式
    return response.text


if __name__ == "__main__":
    # user = "2018302080181"
    # password = "20000721"
    # session, cookie, csrf_token = login.Login(user, password)
    # content = GetGradePageContent(session, cookie, csrf_token)

    with open("content.html", "r", encoding="GBK") as f:
        content = f.read()

    soup = bs(content, "lxml")

    # lesson = Query.SelectByCname(soup, "数据结构")
    # print(lesson)

    # lessons = Query.SelectAll(soup)
    # print(lessons.GetAverageScore())

    lessons = Query.SelectByYear(soup, "2019")
    print(lessons.GetAverageScore())
