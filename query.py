from lesson import LessonArray

class Query:
    @staticmethod
    def StaticInit(soup):
        table_rows = soup.select("body > table > tr")
        lessons = LessonArray(table_rows)
        return lessons

    @staticmethod
    def SelectAll(soup):
        lessons = Query.StaticInit(soup)
        return lessons

    @staticmethod
    def SelectByCname(soup, cname):
        lessons = Query.StaticInit(soup).GetLessonsList()
        for lesson in lessons:
            if lesson.name == cname:
                return lesson
