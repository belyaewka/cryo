import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from db_export import db_export, DATABASE
import datetime
import io
from config import BOT_TOKEN

logging.basicConfig(filename='bot.log',
                    format='%(asctime)s '
                           'LOGGER=%(name)s '
                           'MODULE=%(module)s.py '
                           'FUNC=%(funcName)s'
                           ' %(levelname)s '
                           '%(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level='INFO',
                    encoding='utf8')

logger = logging.getLogger('bot')

# ALLOWED_USERS = []


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

button1 = KeyboardButton('Получить данные c криохранов')
button2 = KeyboardButton('/start')
markup4 = ReplyKeyboardMarkup().row(button1, button2)
TEMPER_1 = ['t1', 'T1', 'т1', 'Т1']
LEVEL_1 = ['l1', 'L1', 'л1', 'Л1', 'у1', 'У1']
TEMPER_2 = ['t2', 'T2', 'т2', 'Т2']
LEVEL_2 = ['l2', 'L2', 'л2', 'Л2', 'у2', 'У2']

def cryo():
    res = []
    try:
        with open('cryodata', 'r', encoding="utf-8") as f:
            for x in f:
                res.append(x)

    except Exception as e:
        res = 'Ошибка получения данных cryodata'
        logger.error(f'error occured during getting cryodata {e}')
    return f'{res[0]}\n{res[1]}'


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg):
    await msg.reply(
        text=f'Я криобот для получения показаний с криохранилищ ОПУ ОРРБП. Привет, {msg.from_user.first_name}!',
        reply_markup=markup4)
    logger.debug(f'message START or HELP was received from user {msg.from_user.first_name}')


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    data = None
    param = None

    if msg.text == 'Получить данные c криохранов':
        try:
            data = cryo()
            logger.info('getting data via call function cryo()')
            await msg.answer(data)
        except Exception as e:
            data = 1  # делаем data is not None
            logger.error(f'error occured during getting the data {e}')
            await msg.answer('Ошибка получения данных')

    # recognize command from user
    if msg.text in TEMPER_1:
        param = 'temper_1'
    if msg.text in TEMPER_2:
        param = 'temper_2'
    if msg.text in LEVEL_1:
        param = 'level_1'
    if msg.text in LEVEL_2:
        param = 'level_2'
    if param:
        await msg.answer(f'График {param} по вашему запросу подготавливается...')
        try:
            # sq_pd_to_png(f'{param}')
            dt = datetime.datetime.now()
            date = dt.strftime('%d-%m-%Y')
            query = f'SELECT time, {param} from cryo WHERE date="{date}"'
            logger.info(f'{query}')

            try:
                df = db_export(DATABASE, query)
            except Exception as e:
                logger.error(f'Database export error {e}')
                df = None

            if df is not None:

                # making a plot
                fig = plt.figure()
                sns.set(font_scale=0.5)
                my_plot = sns.lineplot(x='time', y=f'{param}', data=df, marker='o', legend='auto', label=f'{param}')
                my_plot.set_xticklabels(my_plot.get_xticklabels(), rotation=90)

                # saving a plot as png image to buffer i/o
                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=200)
                buf.seek(0)
                try:
                    await bot.send_photo(chat_id=msg.chat.id, photo=buf)
                except Exception as e:
                    logger.error(f'Send plot error {e}')
                    await msg.answer('Ошибка генерации графика')

                # closing and removing all plot objects
                plt.clf()
                del df
                plt.close(fig)
                del fig
        except:
            await msg.answer('Ошибка генерации графика на бэкенде')

        data = 1  # делаем data is not None

    if data is None:
        data = 'Вы ввели неверную команду, попробуйте еще раз'
        await msg.answer(data)


if __name__ == '__main__':
    executor.start_polling(dp)
