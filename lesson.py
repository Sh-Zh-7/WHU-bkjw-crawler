# 根据tr转化为Lesson对象
class Lesson:
    def __init__(self, row):
        data = row.select("td")
        self.name = data[0].get_text().strip()
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
               "成绩: " + self.grade + "\n" + \
               "绩点: " + self.grade_point


class LessonArray:
    def __init__(self, rows=None, lesson_list=None):
        if rows:
            self.lessons = []
            is_first = True
            for row in rows:
                if not is_first:
                    self.lessons.append(Lesson(row))
                else:
                    is_first = False
        elif lesson_list:
            self.lessons = lesson_list
        else:
            # TODO: 做点修改
            print("Error")

    def __str__(self):
        length = len(self.lessons)
        for index, lesson in enumerate(self.lessons):
            print(lesson)
            if index != length - 1:
                print()

    def GetLessonsList(self):
        return self.lessons

    def GetGPA(self):
        gp_arr = []
        point_arr = []
        for lesson in self.lessons:
            point = lesson.point
            gp = lesson.grade_point
            if gp:
                gp_arr.append(float(point) * float(gp))
                point_arr.append(float(point))
        # TODO: 增加鲁棒性
        return sum(gp_arr) / sum(point_arr)

    def GetAverageScore(self):
        score_arr = []
        for lesson in self.lessons:
            if lesson.grade:
                score_arr.append(float(lesson.grade))
        # TODO: 增加鲁棒性
        return sum(score_arr) / len(score_arr)


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
