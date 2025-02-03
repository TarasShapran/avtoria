from enum import Enum


class CurrencyCodeEnum(Enum):
    USD = (
        'USD', 840
    )
    UAH = (
        'UAH', 980
    )
    EUR = (
        'EUR', 978
    )

    def __init__(self, currency, code):
        self.currency = currency
        self.code = code
