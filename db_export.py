from pandas import read_sql
import sqlite3 as sq
import datetime

DATABASE = 'cryodata.db'
QUERY = 'SELECT * from cryo'
OUTPUT_FILE = 'history_data.xlsx'


def db_export(database: str, query: str):
    """export data from SQlite database to Pandas dataframe"""
    with sq.connect(database) as con:
        df = read_sql(query, con)
    return df


def pd_to_excel(df, file: str) -> None:
    """this function create xlsx file from Pandas dataframe"""
    df.to_excel(file)



def get_data(column):
    """get data from database for temperature and level trends on the Flask/Chart.js"""
    with sq.connect('cryodata.db') as con:
        cur = con.cursor()
        dt = datetime.datetime.now()
        date = dt.strftime('%d-%m-%Y')

        obj_cur = cur.execute(f'SELECT {column} FROM cryo WHERE date="{date}"')
        return [x[0] for x in obj_cur]


if __name__ == '__main__':
    try:
        df = db_export(DATABASE, QUERY)
    except Exception as e:
        print(f'Database export error {e}')
        df = None
    if df is not None:
        pd_to_excel(df, OUTPUT_FILE)
    else:
        print('WARNING! Nothing was written to the file')

