"""
    查询符合条件的课程
"""

from dao.lesson import LessonArray

gb_list = ["公共必修", "公共基础必修"]
gx_list = ["公共选修", "通识教育选修"]
zb_list = ["专业教育必修", "专业必修"]
zx_list = ["专业教育选修"]

class Query:
    # 查询给定成绩的某一科课程(查询期末考试成绩)
    @staticmethod
    def SelectByCname(lessons, cname):
        lessons_list = lessons.GetLessonsList()
        target_lessons = []
        for lesson in lessons_list:
            if cname in lesson.name:
                target_lessons.append(lesson)
        return LessonArray(lesson_list=target_lessons)

    # 根据年份查询课程(奖学金用)
    @staticmethod
    def SelectByYear(lessons, year):
        lessons_list = lessons.GetLessonsList()
        target_lesson = []
        for lesson in lessons_list:
            if lesson.year == year:
                target_lesson.append(lesson)
        return LessonArray(lesson_list=target_lesson)

    @staticmethod
    def SelectByKind(lessons, kind):
        target_lessons = []
        lessons_list = lessons.GetLessonsList()
        kind = kind.upper()
        if kind == "GB":
            for lesson in lessons_list:
                if lesson.kind in gb_list:
                    target_lessons.append(lesson)
        elif kind == "GX":
            for lesson in lessons_list:
                if lesson.kind in gx_list:
                    target_lessons.append(lesson)
        elif kind == "ZB":
            for lesson in lessons_list:
                if lesson.kind in zb_list:
                    target_lessons.append(lesson)
        elif kind == "ZX":
            for lesson in lessons_list:
                if lesson.kind in zx_list:
                    target_lessons.append(lesson)
        elif kind == "B":
            for lesson in lessons_list:
                if lesson.kind in gb_list or lesson.kind in zb_list:
                    target_lessons.append(lesson)
        elif kind == "X":
            for lesson in lessons_list:
                if lesson.kind in gx_list or lesson.kind in zx_list:
                    target_lessons.append(lesson)

        return LessonArray(lesson_list=target_lessons)

