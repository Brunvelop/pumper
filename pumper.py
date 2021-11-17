import time
from datetime import datetime
from unicodedata import category


from tqdm import tqdm
import pandas as pd

from extractors.coingeko import Coingeko
from extractors.socialblade import Socialblade

def extract_data_to_df(category, top_n=0):
    print("##### - WELCOME TO PUMPER! - #####")
    start = time.time()

    coingeko = Coingeko()
    print(f'\nDonwloading {category} coins... \n')
    coins = coingeko.get_coins_by_category(category=category)
    if top_n:
        coins = coins[0:top_n]

    print(f'\nDonwloading {category} coins prices... \n')
    prices = coingeko.get_market_info_coins(coins)
    time.sleep(60)
    print(f'\nDonwloading {category} coins twitter names... \n')
    tw_names = coingeko.get_twitter_coins(coins)

    socialblade = Socialblade()
    print('\nDonwloading twitter data... \n')
    twitter_data = socialblade.get_twitter_accounts_data(tw_names)


    print('\nProcesing data extrated... \n')
    df_list = []
    for coin, price in tqdm(prices.items()):
        for p in price.get('market_caps'):
            timestamp=p[0]/1000 #normalice
            value=p[1]

            date_p=datetime.fromtimestamp(timestamp).date()
            tw_followers=0
            if twitter_data.get(coin):
                for data_point in twitter_data.get(coin):
                    if datetime.strptime(data_point.get('date'), '%Y-%m-%d').date() == date_p:
                        tw_followers = data_point.get('followers')
                        break

            df_list.append({
                'coin': coin,
                'market_cap': int(value),
                'tw_followers':tw_followers,
                'date':date_p
            }) 

    df = pd.DataFrame(df_list, columns=
                                        ['coin',
                                        'market_cap',
                                        'tw_followers',
                                        'date'])

    print('\nSaving df.csv \n')
    df.to_csv(f'database/df_{category}.csv')

    print('\nDONE! \n')

    end = time.time()
    print('total time:',end - start)


# category= 'binance-smart-chain'
# category= 'gaming'

for i in range(5):
    try:
        extract_data_to_df(category='binance-smart-chain')
    except:
        continue
    break
