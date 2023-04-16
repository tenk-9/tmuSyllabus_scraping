import mysql.connector as mydb
connection = mydb.connect(host="localhost",
                          user="root",
                          password="~~PASSWORD~~",
                          database="tmuSyllabus_test",
                          autocommit=True)

cur = connection.cursor()
cur.execute("SELECT * FROM base_info;")
result = cur.fetchall()
with open("_out.tsv", 'w', encoding="utf-8") as f:
    f.write("開講年度\t開講学期\t曜日\t時限\t教員\t科目名\t授業番号\t単位数\tシラバスURL\t科目区分\t学部コード\n")
    for col in result:
        for i in range(len(list(col))):
            if (i == 0):
                f.write("{}".format(list(col)[i]))
            else:
                f.write("\t{}".format(list(col)[i]))
        f.write('\n')
