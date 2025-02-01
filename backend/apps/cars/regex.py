from enum import Enum


class CarRegex(Enum):
    BRAND = (
        r'^[A-Z][a-zA-Z]{1,49}$',
        "Model must consist for first letter uppercase and only letters.",
    )
    MODEL = (
        r'^[A-Z][a-zA-Z0-9 ]{0,49}$',
        "Model must start with an uppercase letter and contain only letters, numbers, and spaces.",
    )



    def __init__(self, pattern: str, msg: str):
        self.pattern = pattern
        self.msg = msg
