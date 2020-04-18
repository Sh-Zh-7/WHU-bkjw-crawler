"""
    课程对象和课程集对象
    主要用来获得课程的信息（GPA等）
"""

# 根据tr转化为Lesson对象
class Lesson:
    def __init__(self, row):
        # 为什么这里不用Pandas? 因为效率
        data = row.select("td")
        self.name = data[0].get_text().strip()
        self.kind = data[1].get_text().strip()
        self.college = data[6].get_text().strip()
        self.point = data[4].get_text().strip()
        self.grade = data[10].get_text().strip()
        self.year = data[8].get_text().strip()
        if self.grade:
            self.grade_point = str(GPMap(float(self.grade)))
        else:
            self.grade_point = ""

    def __str__(self):
        return "课程名: " + self.name + "\n" + \
               "学分: " + self.point + "\n" + \
               "成绩: " + (self.grade if self.grade else "None") + "\n" + \
               "绩点: " + (self.grade_point if self.grade_point else "None") + "\n"


class LessonArray:
    def __init__(self, table=None, lesson_list=None):
        if table:
            self.lessons = []
            is_first = True
            for row in table:
                if not is_first:
                    self.lessons.append(Lesson(row))
                else:
                    is_first = False
        elif lesson_list:
            self.lessons = lesson_list

    def __str__(self):
        target_str = ""
        for lesson in self.lessons:
            target_str += (lesson.__str__() + "\n")
        return target_str

    def GetLessonsList(self):
        return self.lessons

    def GetTotalPoint(self):
        total_point = 0
        for lesson in self.lessons:
            total_point += float(lesson.point)
        return total_point

    def GetAverageScore(self):
        score_arr = []
        for lesson in self.lessons:
            if lesson.grade:
                score_arr.append(float(lesson.grade))
        try:
            return sum(score_arr) / len(score_arr)
        except:
            print("未能查询到课程，请检查查询是否正确")
            exit(0)

    def GetGPA(self):
        gp_arr, point_arr = [], []
        for lesson in self.lessons:
            point = lesson.point
            gp = lesson.grade_point
            if gp:
                gp_arr.append(float(point) * float(gp))
                point_arr.append(float(point))
        try:
            return sum(gp_arr) / sum(point_arr)
        except:
            print("查询到的学分为0，请检查查询是否正确")
            exit(0)

    def GetWeightedScore(self):
        total_arr, point_arr = [], []
        for lesson in self.lessons:
            if lesson.grade:
                total_arr.append(float(lesson.grade) * float(lesson.point))
                point_arr.append(float(lesson.point))
        try:
            return sum(total_arr) / sum(point_arr)
        except:
            print("未能查询到相应的课程，请检查查询是否正确")


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
    elif grade >= 72.0:
        gp = 2.3
    elif grade >= 68.0:
        gp = 2.0
    elif grade >= 64.0:
        gp = 1.5
    elif grade >= 60.0:
        gp = 1.0
    else:
        gp = 0.0
    return gp

