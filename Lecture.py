import html_parser


class Lecture:
    def __init__(self):
        self._year = -1
        self._season = ""
        self._day = ""
        self._period = ""
        self._teacher = ""
        self._name = ""
        self._id = ""
        self._creadits = -1
        self._url = ""
        self._numbering = ""
        self._type = ""
        self._faculty = ""

    def insert(self, infoDict):
        self._year = infoDict["year"]
        self._season = infoDict["season"]
        self._day = infoDict["day"]
        self._period = infoDict["period"]
        self._teacher = infoDict["teacher"]
        self._name = infoDict["name"]
        self._id = infoDict["id"]
        self._creadits = infoDict["credits"]
        self._url = infoDict["url"]
        self._numbering = infoDict["numbering"]
        self._type = infoDict["type"]
        self._faculty = infoDict["faculty"]

    def gen_insertSQL(self, targetTableName):
        columns = "year,season,day,period,teacher,name,id,credits,url,type,faculty"
        values = "{},'{}','{}','{}','{}','{}','{}',{},'{}','{}','{}'".format(
            str(self._year),
            self._season,
            self._day,
            str(self._period),
            self._teacher,
            self._name,
            self._id,
            str(self._creadits),
            self._url,
            self._type,
            self._faculty)

        return "INSERT INTO {} ({}) VALUES({});".format(
            targetTableName, columns, values)

    def gen_updateSQL(self, targetTableName):
        set_str = '''
        year={},season='{}',day='{}',period='{}',teacher='{}',name='{}',id='{}',credits={},url='{}',type='{}',faculty='{}'
        '''.format(str(self._year),
                   self._season,
                   self._day,
                   str(self._period),
                   self._teacher,
                   self._name,
                   self._id,
                   str(self._creadits),
                   self._url,
                   self._type,
                   self._faculty)
        return "UPDATE {} SET {} WHERE id='{}';".format(targetTableName, set_str, self._id)


def gen_LecturesList(syllabusURLlist, depCode, year):
    lectures = []
    for lecURL in syllabusURLlist:
        souped = html_parser.soup_url(lecURL)
        try:
            infoDict = html_parser.getBaseInfoDict(souped)
            infoDict["url"] = lecURL
            infoDict["year"] = year
            infoDict["faculty"] = depCode
            lec = Lecture()
            lec.insert(infoDict)
            lectures.append(lec)
        except IndexError:
            print("ERROR:{} was not found.".format(lecURL))

    return lectures
