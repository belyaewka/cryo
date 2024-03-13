from flask import Flask
from flask import render_template
from db_export import get_data
import datetime

app = Flask(__name__)

@app.route("/")
def base():
    res = []
    try:
        with open('cryoweb', 'r', encoding="utf-8") as f:
            for x in f:
                res.append(x)

    except Exception as e:
        res = ["There was an error occured, ", 'please contact Cryopal service']
    return render_template('base.html', title = 'CRYOPAL WEB SERVER', menu = res)

@app.route('/temperature')
def temp():
    return render_template('temperature.html',
                           current_date=datetime.datetime.now().strftime('%d-%m-%Y'),
                           time=get_data('time'),
                           temper_1=get_data('temper_1'),
                           temper_2=get_data('temper_2'))

@app.route('/level')
def level():
    return render_template('level.html',
                           current_date=datetime.datetime.now().strftime('%d-%m-%Y'),
                           time=get_data('time'),
                           level_1=get_data('level_1'),
                           level_2=get_data('level_2'))

if __name__ == '__main__':
    app.run(debug=True, host="10.1.97.147", port="5000")
