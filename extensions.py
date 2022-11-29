import requests
import json

keys = {
    "биткоин": "BTC",
    "эфириум": "ETH",
    "доллар": "USD",
    "евро": "EUR",
    "йена": "JPY",
    "рубль": "RUB",
    "фунт": "GBP",
    "франк": "CHF",
    "юань": "CNY",
    "крона": "SEK",
    "песо": "MXN",
    "лира": "TRY",
    "рупия": "INR",

}

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f"Невозможно перевести одинаковые валюты   '{base}'-'{base}'")

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту    "{quote}"')

        try:
            base_tiker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту    "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество    "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount