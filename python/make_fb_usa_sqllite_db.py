import sqlite3
import os
db = sqlite3.connect("fb_usa_dump.db")
db.execute('PRAGMA synchronous = OFF;')
db.execute('PRAGMA journal_mode = MEMORY;')
db.execute('PRAGMA secure_delete = OFF;')
db.execute('PRAGMA locking_mode = EXCLUSIVE;')
db.isolation_level = None
db.execute("""
    CREATE TABLE IF NOT EXISTS
    usa(
        phone_no, user_id, fname, lname,
        gender, city1, city2, relationship,
        company, seen, email
    );
""")
insert_sql = "INSERT INTO usa VALUES (?,?,?,?,?,?,?,?,?,?,?);"
db.commit()
cnt = 0
for cur in os.listdir("."):
    if cur.startswith("USA") and cur.endswith(".txt"):
        todo = []
        with open(cur, encoding="utf-8") as f:
            for row in f:
                row = row.split(":")
                if len(row) == 14:
                    (
                        phone_no, user_id, fname, lname, gender, city1, city2,
                        relationship, company, d1, d2, d3, email, _) = row
                    seen = d1 + ":" + d2 + ":" + d3
                    todo.append((
                        phone_no, user_id, fname, lname, gender,
                        city1, city2, relationship, company, seen, email))
                    if len(todo) % 1000000 == 0 and len(todo) > 0:
                        cnt += len(todo)
                        print("inserted %i records" % cnt)
                        db.executemany(insert_sql, todo)
                        db.commit()
                        todo = []
        if len(todo) > 0:
            cnt += len(todo)
            print("inserting %i records" % cnt)
            db.executemany(insert_sql, todo)
            db.commit()

db.execute("CREATE UNIQUE INDEX pnum ON usa (phone_no);")
db.commit()
