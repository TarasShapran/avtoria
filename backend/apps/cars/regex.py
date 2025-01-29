from enum import Enum


class CarRegex(Enum):
    MODEl = (
        r'^[A-Z][a-zA-Z]{1,49}$',
        "Model must consist fro first letter uppercase and only letters.",
    )



    def __init__(self, pattern: str, msg: str):
        self.pattern = pattern
        self.msg = msg
