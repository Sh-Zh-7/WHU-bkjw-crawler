from lesson import LessonArray

class Query:
    @staticmethod
    def StaticInit(soup):
        table_rows = soup.select("body > table > tr")
        lessons = LessonArray(table_rows)
        return lessons

    # 查询本科阶段所有课程(查询GPA)
    @staticmethod
    def SelectAll(soup):
        lessons = Query.StaticInit(soup)
        return lessons

    # 查询给定成绩的某一科课程(查询期末考试成绩)
    @staticmethod
    def SelectByCname(soup, cname):
        lessons = Query.StaticInit(soup).GetLessonsList()
        for lesson in lessons:
            if lesson.name == cname:
                return lesson

    # 根据年份查询课程(奖学金用)
    @staticmethod
    def SelectByYear(soup, year):
        lessons = Query.StaticInit(soup).GetLessonsList()
        target_lesson = []
        for lesson in lessons:
            if lesson.year == year:
                target_lesson.append(lesson)
        return LessonArray(lesson_list=target_lesson)

