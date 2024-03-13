import sqlite3 as sq

DB_NAME = "cryodata.db"

def db_create(db_name):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""
        """)

if __name__ == '__main__':
    try:
        db_create(DB_NAME)
    except Exception as e:
        print(f'Database creation error {e}')
