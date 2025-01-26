import pandas as pd
import sqlite3
from datetime import date

db = sqlite3.connect('users.db')
cur = db.cursor()

cur.execute("SELECT COUNT(*) FROM users")
row_count = cur.fetchone()[0]

filepath = "./dataset1.csv"
df = pd.read_csv(filepath)

rows = []
for i in range(len(df)):
    rows.append(df.loc[i].tolist())

uids = []

for row in rows:
    section = row[4]
    grade = row[3]
    regID = str(row_count + 1).zfill(4)
    email = row[1]
    password = row[6]
    name = row[2]

    uid = "ITC" + str(date.today().year)[-2:]
    if section == "B":
        uid += "1"
    elif section == "E":
        uid += "2"

    if grade > 5:
        uid += "1"
    elif grade < 6:
        uid += "2"

    uid += regID

    print(f"{uid} | {name}")
    cur.execute("INSERT OR IGNORE INTO users (uid, email, password, displayname) VALUES (?, ?, ?, ?)", 
                (uid, email, password, name))
    db.commit()

    row_count += 1

db.close()