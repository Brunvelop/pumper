import pandas as pd

df = pd.read_csv('database/df.csv')

data = []
for coin in df.coin.unique():
    if df.loc[df['coin'] == coin].iloc[-1].tw_followers != 0:
        month_followers_increment = (1 - float(df.loc[df['coin'] == coin].iloc[0].tw_followers) / float(df.loc[df['coin'] == coin].iloc[-1].tw_followers)) * 100
        week_followers_increment = (1 - float(df.loc[df['coin'] == coin].iloc[-7].tw_followers) / float(df.loc[df['coin'] == coin].iloc[-1].tw_followers)) * 100
    if month_followers_increment > 0 :
        data.append([
            month_followers_increment,
            week_followers_increment,
            coin])

montly_tw_increment_porcent = sorted(data, reverse=True)

from prettytable import PrettyTable
t = PrettyTable(['COIN', 'TW 30d (%)', 'TW 7d (%)'])
for data in sorted(data, reverse=True):
    t.add_row([data[-1], data[0], data[1]])
print(t)