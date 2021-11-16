import pandas as pd
import numpy as np
from prettytable import PrettyTable

def fill_nan_with_mean_from_prev_and_next(df):
    for row in df.loc[df['tw_followers'] == 0].values:
        i_sup = 1
        i_inf = 1
        while True:
            if df.iloc[row[0]-i_inf]['tw_followers'] == 0:
                i_inf += 1
            if df.iloc[row[0]+i_sup]['tw_followers'] == 0:
                i_sup += 1
            break
        increment = df.iloc[row[0]+i_sup]['tw_followers'] - df.iloc[row[0]-i_inf]['tw_followers']

        df.at[row[0],'tw_followers'] = int(df.iloc[row[0]-i_inf]['tw_followers'] + increment * i_inf / (i_inf + i_sup))
    return df


def get_table_followers_abs(df):
    df_org = df.copy()
    fill_nan_with_mean_from_prev_and_next(df)

    data = []
    for coin in df.coin.unique():
        if df.loc[df['coin'] == coin].iloc[-1].tw_followers != 0:
            month_followers_increment = (1 - float(df.loc[df['coin'] == coin].iloc[0].tw_followers) / float(df.loc[df['coin'] == coin].iloc[-1].tw_followers)) * 100
            try:
                week_followers_increment = (1 - float(df.loc[df['coin'] == coin].iloc[-7].tw_followers) / float(df.loc[df['coin'] == coin].iloc[-1].tw_followers)) * 100
            except:
                week_followers_increment= 'Null'
        if month_followers_increment > 0 :
            data.append([
                month_followers_increment,
                week_followers_increment,
                coin])

    montly_tw_increment_porcent = sorted(data, reverse=True)

    
    t = PrettyTable(['COIN', 'TW 30d (%)', 'TW 7d (%)'])
    for data in sorted(data, reverse=True):
        t.add_row([data[-1], data[0], data[1]])
    print(t)


def get_table_followers_exp(df, last_n_days=''):
    fill_nan_with_mean_from_prev_and_next(df)
    data = []
    for coin in df.coin.unique():
        followers = df.loc[df['coin'] == coin].tw_followers.values
        days = np.arange(df.loc[df['coin'] == coin].tw_followers.values.size)

        if last_n_days:
            followers = followers[-last_n_days:-1]
            days = days[-last_n_days:-1]
        regresion = np.polyfit(days, np.log(followers), 1)

        regresion_curve = np.exp(regresion[1]) * np.exp(regresion[0]*days)

        mse = np.sqrt((np.square(followers - regresion_curve)).mean(axis=0))
        mse_norm = mse/followers[-1]


        today_increment = 100 * (followers[-1] - followers[-2])/followers[-2]


        data.append(
            [
                regresion[0],
                mse_norm,
                mse,
                today_increment,
                coin
            ]
        )

    t = PrettyTable(['COIN','e', 'mse_norm', 'mse', 'today %'])
    for data in sorted(data, reverse=True):
        t.add_row([data[-1], data[0], data[1], data[2], data[3]])
    print(t)

df = pd.read_csv('database/df.csv')
get_table_followers_exp(df,3)