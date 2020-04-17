import time
import hashlib
import csv
from bs4 import BeautifulSoup as bs

header = {"User-Agent":
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/78.0.3904.70 '
              'Safari/537.36'}
time_stamp = str(int(time.time() * 1000))
jwb = "%E6%AD%A6%E5%A4%A7%E6%9C%AC%E7%A7%91%E6%95%99%E5%8A%A1%E7%B3%BB%E7%BB%9F"


def EncryptPassword(pwd):
    encrypt = hashlib.md5()
    encrypt.update(pwd.encode("ASCII"))
    return encrypt.hexdigest()

def HTML2CSV(html):
    soup = bs(html, "lxml")
    trs = soup.find_all("tr")
    with open("grades_table.csv", "w") as csv_file:
        field_names = ["课程名称", "课程类型", "通识课类型", "课程属性", "学分", "教师",
                       "授课学院", "学习类型", "学年", "学期", "成绩", "操作"]
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        for i in range(len(trs)):
            if i != 0:
                tds = trs[i].find_all('td')
                writer.writerow({
                    "课程名称": tds[0].get_text().strip() if tds[0].get_text() else "",
                    "课程类型": tds[1].get_text().strip() if tds[1].get_text() else "",
                    "通识课类型": tds[2].get_text().strip() if tds[2].get_text() else "",
                    "课程属性": tds[3].get_text().strip() if tds[3].get_text() else "",
                    "学分": tds[4].get_text().strip() if tds[4].get_text() else "",
                    "教师": tds[5].get_text().strip() if tds[5].get_text() else "",
                    "授课学院": tds[6].get_text().strip() if tds[6].get_text() else "",
                    "学习类型": tds[7].get_text().strip() if tds[7].get_text() else "",
                    "学年": tds[8].get_text().strip() if tds[8].get_text() else "",
                    "学期": tds[9].get_text().strip() if tds[9].get_text() else "",
                    "成绩": tds[10].get_text().strip() if tds[10].get_text() else ""
                })
