import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from db_export import db_export, DATABASE
import datetime
from time import sleep
import os
import io



def sq_pd_to_png(param: str): # params - temper_1, temper_2, level_1, level_2
    """this function create png image file from SQLite through Pandas dataframe"""
    dt = datetime.datetime.now()
    date = dt.strftime('%d-%m-%Y')
    query = f'SELECT time, {param} from cryo WHERE date="{date}"'

    try:
        df = db_export(DATABASE, query)
        # print(query)
    except Exception as e:
        print(f'Database export error {e}')
        df = None

    if df is not None:
        #remove old file
        file = f"{param}.png"
        if os.path.isfile(file):
            os.remove(file)
        # making a plot
        fig = plt.figure()
        # sns.set(rc={'figure.figsize': (100, 80)})
        sns.set(font_scale=0.5)
        my_plot = sns.lineplot(x='time', y=f'{param}', data=df,  marker='o', legend='auto', label=f'{param}')
        my_plot.set_xticklabels(my_plot.get_xticklabels(), rotation=90)
        # saving a plot as png image
        # buf = io.BytesIO()
        # plt.savefig(buf, format='png')
        # buf.seek(0)
        plt.savefig(f"{param}.png", format="png", dpi=150)
        plt.clf()
        # closing and removing all plot objects
        del df
        plt.close(fig)
        del fig

    else:
        print('Nothing was written to the file')




if __name__ == '__main__':

    sq_pd_to_png('level_2')
    # sq_pd_to_png('level_1')
    # sq_pd_to_png('temper_1')
    # sq_pd_to_png('temper_2')
    # os.remove('level_2.png')
    # sleep(3)
