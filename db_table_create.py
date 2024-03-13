import sqlite3 as sq

def create_table():
    with sq.connect("cryodata.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS cryo (
            date TEXT,
            time TEXT,
            temper_1 REAL,
            level_1 REAL,
            temper_2 REAL,
            level_2 REAL
        )""")
        cur.execute("""CREATE INDEX "date" ON "cryo" ("date")""")


if __name__ == '__main__':
    create_table()



