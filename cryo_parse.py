from bs4 import BeautifulSoup
import re
from datetime import datetime
import lxml
from requests_html import HTMLSession
import sqlite3 as sq

# URLS = ['http://10.1.150.247/accueil.zhtml', 'http://10.1.150.246/accueil.zhtml']
URLS = ['http://10.1.150.247', 'http://10.1.150.246']

def cryo(url):
    session = HTMLSession()
    response = session.get(url)

    try:
        response.html.render(timeout=50)

        bs = BeautifulSoup(response.html.html, 'lxml')
        table = bs.find_all('table')[5]
        row_temper = table.find_next('span', class_='Style4').get_text()
        temper = int(re.findall(r'-\d+', row_temper)[0])
        row_level = table.find_next('span', class_='Style4').find_next('span', class_='Style4').get_text()
        level = float(re.findall(r'\d+.\d+|\d+', row_level)[0])
    except:
        temper = 'Timeout'
        level = 'Timeout'

    return temper, level


if __name__ == '__main__':
    res = []
    i = 1
    for url in URLS:
        temper, level = cryo(url)
        res.append((i, temper, level))
        i += 1
    # temper, level = cryo(URLS[0])
    # res.append((i, temper, level))
    # i += 1
    # temper, level = 'ПЛАНОВАЯ РАЗМОРОЗКА', 'ПЛАНОВАЯ РАЗМОРОЗКА'
    # res.append((i, temper, level))

    try:
        with open(r'C:\Users\operator\PycharmProjects\cryobot\cryodata', 'w', encoding="utf-8") as f:
            for item in res:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Криохран № {item[0]} Температура: {item[1]}°C Уровень: {item[2]} см \n')
    except Exception as e:
        print(f'Error was occured during writing the file cryodata : {e}')

    try:
        with open(r'C:\Users\operator\PycharmProjects\cryobot\cryoweb', 'w', encoding="utf-8") as c:
            for item in res:
                c.write(f'{datetime.now().strftime("%d-%m-%Y %H:%M")} Cryogenic storage # {item[0]} Temp: {item[1]}°C Level: {item[2]} cm \n')
    except Exception as e:
        print(f'Error was occured during writing the file cryoweb : {e}')

    # res = [(1, -166, 4.6), (2, -159, 4.4)] - образец финального списка с данными
    try:
        with sq.connect(r"C:\Users\operator\PycharmProjects\cryobot\cryodata.db") as con:
            cur = con.cursor()
            dt = datetime.now()
            date = dt.strftime('%d-%m-%Y')
            cur.execute(f'INSERT INTO cryo (date, time, temper_1, level_1, temper_2, level_2) VALUES ("{date}",time("now", "localtime"),{res[0][1]},{res[0][2]},{res[1][1]},{res[1][2]})')
    except Exception as e:
        print(f'Database record error was occured : {e}')
