import mysql.connector as mydb
import html_parser
import Lecture

FACULTIES = {
    '人文・社会系': '02',
    '法学系': '03',
    '経営学系': '04',
    '理工学系': '05',
    '都市環境学部(2017年以前)': '06',
    'ｼｽﾃﾑﾃﾞｻﾞｲﾝ学部(2017年以前)': '07',
    '健康福祉学部': '08',
    '人間健康科学副専攻': '0B',
    '観光経営副専攻': '0C',
    '基礎ゼミ・情報リテ': '0D01',
    '英語・未修言語': '0D02',
    '理系共通基礎科目': '0D03',
    '保健体育・キャリア': '0D04',
    '教養科目': '0D05',
    '基盤科目': '0D06',
    '国際副専攻': '0E',
    '観光マネジメント副専攻': '0F',
    '分野横断プログラム': '0G',
    '大学院全学共通科目': '0H',
    '数理・データサイエンス副専攻': '0I',
    '人文科学研究科': '11',
    '社会科学研究科': '12',
    '理工学研究科': '13',
    '都市環境科学研究科(2017年以前)': '14',
    'ｼｽﾃﾑﾃﾞｻﾞｲﾝ研究科(2017年以前)': '15',
    '人間健康科学研究科': '16',
    '法学政治学研究科': '18',
    '経営学研究科': '19',
    '理学研究科': '20',
    '助産学専攻科': '50',
    '都市環境科学研究科': '51',
    'ｼｽﾃﾑﾃﾞｻﾞｲﾝ研究科': '52',
    '人文社会学部': 'A1',
    '法学部': 'A2',
    '経済経営学部': 'A3',
    '理学部': 'A4',
    '都市環境学部': 'A5',
    'ｼｽﾃﾑﾃﾞｻﾞｲﾝ学部': 'A6'
}
DAY = {"Mon": '1', "Tue": '2', "Wed": '3',
       "Thu": '4', "Fri": '5', "Other": '9'}
JCODE_PAGES_MAX = 103
YEAR = 2023
BASEINFO_TABLENAME="syllabus_base_info"

def update_lectures(dep, year, db_connection):
    urlList = html_parser.getLectureUrlList(dep, year, JCODE_PAGES_MAX)
    Lecture_list = Lecture.gen_LecturesList(urlList, dep, year)
    for lecture in Lecture_list:
        update_lectureInfo(lecture, db_connection)


def update_lectureInfo(lecture, db_connection):
    id = lecture._id
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM {} WHERE id='{}';".format(BASEINFO_TABLENAME, id))
    result = cursor.fetchall()
    if (result == []):
        cursor.execute(lecture.gen_insertSQL(BASEINFO_TABLENAME))
        print("INSERTED: {}".format(id))
    else:
        cursor.execute(lecture.gen_updateSQL(BASEINFO_TABLENAME))
        print("UPDATED: {}".format(id))
    cursor.close()


# --- main ---#

connection = mydb.connect(host="localhost",
                          user="root",
                          password="PASSWORD",
                          database="DB_NAME",
                          autocommit=True)

for dep in FACULTIES.values():
    update_lectures(dep, YEAR, connection)


connection.close()
