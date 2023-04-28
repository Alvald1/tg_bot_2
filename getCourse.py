import coinbase
import config

from coinbase.wallet.client import Client
client = Client(config.API_COINBASE_2, config.SECRET_API_COINBASE_2)


def get_price(ticket, currency):
    try:
        price = client.get_spot_price(currency_pair=f'{ticket}-{currency}')
    except Exception as e:
        return False
    return round(float(price.amount), 2)
