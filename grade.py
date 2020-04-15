import requests
import datetime
from bs4 import BeautifulSoup as bs

import login
import utils

# 建立int类型的星期到字符串的映射
week_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
# 全局常量
grade_page_url = 'http://bkjw.whu.edu.cn/servlet/Svlt_QueryStuScore?' \
                 'csrftoken={}&year=0&term=&learnType=&scoreFlag=0&' \
                 't={}%20{}%20{}%20{}%20{}%20GMT+0800%20(%D6%D0%B9%FA%B1%EA%D7%BC%CA%B1%BC%E4)'

# 根据tr转化为Lesson对象
class Lesson:
    def __init__(self, row):
        data = row.select("td")
        self.name = data[0].get_text().strip()
        self.point = data[4].get_text().strip()
        self.grade = data[10].get_text().strip()
        if self.grade:
            self.grade_point = str(GPMap(float(self.grade)))
        else:
            self.grade_point = ""

    def __str__(self):
        return "课程名: " + self.name + "\n" + \
               "学分: " + self.point + "\n" + \
               "成绩: " + self.grade + "\n" + \
               "绩点: " + self.grade_point


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


def SelectByCname(soup, target_name):
    table_rows = soup.select("body > table > tr")
    for row in table_rows:
        lesson_name = row.select(".lessonName")
        if lesson_name:
            lesson_name_text = lesson_name[0].get_text().strip()
            if lesson_name_text == target_name:
                return Lesson(row)


def SelectAll(soup):
    table_rows = soup.select("body > table > tr")
    gps, points = [], []
    for index, row in enumerate(table_rows):
        # 跳过首行
        if index != 0:
            tmp_lesson = Lesson(row)
            print(tmp_lesson)
            if tmp_lesson.grade != "":
                gps.append(float(tmp_lesson.grade_point))
                points.append(float(tmp_lesson.point))
    return GPACalculator(gps, points)


def GPMap(grade):
    if grade >= 90.0:
        gp = 4.0
    elif grade >= 85.0:
        gp = 3.7
    elif grade >= 82.0:
        gp = 3.3
    elif grade >= 78.0:
        gp = 3.0
    elif grade >= 75.0:
        gp = 2.7
    elif grade >= 68.0:
        gp = 2.0
    elif grade >= 64.0:
        gp = 1.5
    elif grade >= 60.0:
        gp = 1.0
    else:
        gp = 0.0
    return gp


def GPACalculator(gps, points):
    tmp = []
    for gp, point in zip(gps, points):
        tmp.append(gp * point)
    return sum(tmp) / sum(points)


if __name__ == "__main__":
    # user = "2018302080181"
    # password = "20000721"
    # session, cookie, csrf_token = login.Login(user, password)
    # content = GetGradePageContent(session, cookie, csrf_token)

    with open("content.html", "r", encoding="GBK") as f:
        content = f.read()

    soup = bs(content, "lxml")
    # lesson = SelectByCname(soup, "NMSL")
    # if lesson:
    #     print(lesson)
    # else:
    #     print("很抱歉！没有找到相应的课程！")

    # print(SelectAll(soup))




