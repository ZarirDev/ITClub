import sqlite3
from datetime import date

fromDB= sqlite3.connect('students.db')
fromCur=fromDB.cursor()
toDB= sqlite3.connect('users.db')
toCur=toDB.cursor()

fromCur.execute("SELECT * FROM students")
rows = fromCur.fetchall()

uids = []

#251xx00xx

for row in rows:
    uid = str(date.today().year)[-2:]
    # print(row[4])
    if row[4] == "B":
        uid+="0"
    elif row[4] == "E":
        uid+="1"

    if row[3] > 9:
        uid+=str(row[3])
    else:
        uid+=f"0{str(row[3])}"

    uid+=row[5][-4:]

    uids.append(uid)

i=0
for row in rows:
    print(f"{uids[i]} | {row[2]}")
    i+=1