from pycoingecko import CoinGeckoAPI

class Coingeko():
    def __init__(self) -> None:
        self.cg = CoinGeckoAPI()

    def get_coins_by_category(self, category):
        return self.cg.get_coins_markets(vs_currency='usd', category=category)

    def get_coin_price(self, id, vs_currency='usd', days=15, interval='daily'):
        return self.cg.get_coin_market_chart_by_id(
                id=id,
                vs_currency=vs_currency,
                days=days,
                interval=interval
            )