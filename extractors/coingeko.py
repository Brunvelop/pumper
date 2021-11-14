from pycoingecko import CoinGeckoAPI
from tqdm import tqdm
from time import sleep


class Coingeko():
    def __init__(self) -> None:
        self.cg = CoinGeckoAPI()

    def get_coins_by_category(self, category):
        return self.cg.get_coins_markets(vs_currency='usd', category=category)

    def get_coin_price(self, id, vs_currency='usd', days=30, interval='daily'):
        return self.cg.get_coin_market_chart_by_id(
                id=id,
                vs_currency=vs_currency,
                days=days,
                interval=interval
            )

    def get_coin_twitter(self, id):
        return self.cg.get_coin_by_id(id).get('links').get('twitter_screen_name')

    def get_market_info_coins(self, coins):
        prices = {}
        count = 0
        for coin in tqdm(coins):
            count +=1
            if count % 40 == 0:
                print('\nWaiting for CoinGekoAPI')
                sleep(120)
            prices[coin.get('id')] = self.get_coin_price(coin.get('id'))
        return prices

    def get_twitter_coins(self, coins):
        tw_names = {}
        count = 0
        for coin in tqdm(coins):
            count +=1
            if count % 40 == 0:
                print('\nWaiting for CoinGekoAPI request limit...')
                sleep(120)
            tw_names[coin.get('id')]= self.get_coin_twitter(coin.get('id'))
        return tw_names