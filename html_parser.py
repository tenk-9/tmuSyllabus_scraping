from bs4 import BeautifulSoup
import re
import requests

COLUMN_JPEN = {"科目種別": "type",
               "授業番号": "id",
               "学期": "season",
               "曜日": "day",
               "科目": "name",
               "時限": "period",
               "担当教員": "teacher",
               "単位数": "credits",
               "科目ナンバリング※2018年度以降入学生対象": "numbering"}
# コピーしたシラバスのhtmlから授業情報を抜き出す


def soup_local(syllabus_path):
    with open(syllabus_path, 'r', encoding="utf-8")as file:
        text = file.read()
        souped = BeautifulSoup(text, "html.parser")
        # print("soupe: {}".format(syllabus_path))
        return souped


def soup_url(syllabus_url):
    print("Souping:{}".format(syllabus_url))
    text = requests.get(syllabus_url).text
    souped = BeautifulSoup(text, "html.parser")
    return souped


def getLectureUrlList(depCode, year, pages):
    urls = []
    print("Correcting URLs code:{}".format(depCode), end=" ")
    for num in range(1, 1+pages):
        listPageURL = "http://www.kyouikujouhou.eas.tmu.ac.jp/syllabus/{}/JCodeIchiran_{}_{}.html".format(
            year, depCode, num)

        response = requests.get(listPageURL)
        texted = response.text
        if (response.status_code != 200):
            break

        souped = BeautifulSoup(texted, "html.parser")
        lectureCont = souped.find_all(
            onclick=re.compile(".*/{}_.*\.html".format(year)))
        for cont in lectureCont:
            onclickCont = cont.get('onclick')
            urlelem = onclickCont[17:-3]
            lectureURL = "http://www.kyouikujouhou.eas.tmu.ac.jp/syllabus/{}/{}".format(
                year, urlelem)
            urls.append(lectureURL)
    print("Total: {}".format(len(urls)))
    return urls


def getEssence(string):
    buff = ""
    ignore_char = ['\n', ' ', '\t']
    change_char = {'\u3000': ' ', '―': 'None'}
    for c in string:
        if (c not in ignore_char):
            if (c in change_char):
                c = change_char[c]
            buff += c

    return buff


def getBaseInfoDict(soupedSyllabus):
    baseTable = soupedSyllabus.find_all("table")[2]
    heads = baseTable.find_all("td", class_='syllabus-head')
    normals = baseTable.find_all("td", class_='syllabus-normal')
    heads.pop(-1)  # remove blank cell
    normals.pop(-1)  # remove blank cell
    baseInfoDict = {}
    for i in range(len(heads)):
        head_ess = getEssence(heads[i].text)
        normal_ess = getEssence(normals[i].text)
        baseInfoDict[COLUMN_JPEN[head_ess]] = normal_ess
    return baseInfoDict


def getTeacherInfoDict(soupedSyllabus):
    teacherTable = soupedSyllabus.find_all("table")[3]
    cells = teacherTable.find_all("td", class_='syllabus-normal')
    teacherInfoDict = {}

    for i in range(len(cells)//2):
        teacherName_ess = getEssence(cells[i*2].text)
        teacherFaculty_ess = getEssence(cells[i*2+1].text)
        teacherInfoDict[teacherName_ess] = teacherFaculty_ess
    return teacherInfoDict
